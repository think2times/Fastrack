from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from exporters import export_excel_package
from db_helper import init_client, call_procedure
from config import REPORTS, DB_CONFIG
from processors import generate_report_package, process_report_logic, prepare_report_data, reconcile_metrics


def fetch_data_from_db(report_id, subcoms=None, bill_month=None):
    """获取指定 report_id 的报表数据，返回 DataFrame 列表"""
    if subcoms is None:
        subcoms = ''

    if bill_month is None:
        # 获取上个月的年月，格式为 YYYY-MM
        last_month = datetime.now() - relativedelta(months=2)
        bill_month = last_month.strftime('%Y-%m')

        # 获取当前年月，格式为 YYYY-MM
        # bill_month = datetime.now().strftime('%Y-%m')

    # 连接数据库，使用本地驱动而不是内置的 Thin 驱动
    lib_dir = r'F:\app\pluto\product\instantclient_11_2'
    init_client(lib_dir)

    # 取数
    cfg = REPORTS[report_id]
    proc_params = cfg['params'](subcoms, bill_month)

    # 调用新的支持多数据源的函数，返回的是一个 list
    return call_procedure(cfg['proc'], proc_params, DB_CONFIG)

def reconcile_ys_reports(report_package):
    """
    核对报表间的数值一致性
    report_package: 存储了各报表原始 DataFrame 的字典 (Key 为 '3-10', '2-8' 等)
    """
    results = []
    
    # 获取各个报表的 DataFrame
    df_310 = report_package.get('3-10')
    df_28 = report_package.get('2-8')
    df_37 = report_package.get('3-7')
    #df_323 = report_package.get('3-23')
    df_323 = None

    # --- 1. 3-10 vs 2-8 水量核对 ---
    print("正在核对 3-10 和 2-8 的水量是否一致。。。")
    if df_310 is not None and df_28 is not None:
        # 3-10 排除 IC卡购水后的售水量总和
        water_310 = df_310[df_310['FEE_TYPE'] != 'IC卡购水']['ACC_WATER'].sum()
        # 2-8 实际水量 (开账 - 减免)
        df_28 = process_report_logic([df_28], '2-8')  # 先处理 2-8 的计算逻辑，确保有 ACTUAL_WATER 列
        water_28 = df_28['ACTUAL_WATER'].sum()

        diff = round(abs(water_310 - water_28), 2)
        status = "✅" if diff == 0 else "❌"
        print(f"{status} [水量核对] 3-10(非IC卡水量): {water_310:.2f} vs 2-8(实际水量): {water_28:.2f} (差异: {diff})")
        results.append(f"{status} [水量核对] 3-10(非IC卡水量): {water_310:.2f} vs 2-8(实际水量): {water_28:.2f} (差异: {diff})")

    # --- 2. 3-10 vs 3-7 合计核对 ---
    print("正在核对 3-10 和 3-7 的合计金额是否一致。。。")
    if df_310 is not None and df_37 is not None:
        # 注意：如果 df_310 包含合计行，需排除或只取合计行
        sum_310 = df_310['ACC_MONEY'].sum()
        sum_37 = df_37['FEE_TOTAL'].sum()

        diff = round(abs(sum_310 - sum_37), 2)
        status = "✅" if diff < 0.1 else "❌"
        print(f"{status} [合计核对] 3-10总额: {sum_310:.2f} vs 3-7总额: {sum_37:.2f} (差异: {diff})")
        results.append(f"{status} [合计核对] 3-10总额: {sum_310:.2f} vs 3-7总额: {sum_37:.2f} (差异: {diff})")

    return results

def reconcile_ss_reports(report_package):
    """
    核对实收相关报表间的数值一致性
    report_package: 存储了各报表原始 DataFrame 的字典 (Key 为 '3-4', '3-6', '3-13', '3-14' 等)
    """
    results = []
    
    # 获取各个报表的 DataFrame
    df_34 = report_package.get('3-4')
    df_36 = report_package.get('3-6')
    df_313 = report_package.get('3-13')
    df_314 = report_package.get('3-14')

    # --- 1. 3-4 vs 3-14 金额核对 ---
    # 检查3-4中账单金额、需划账费用、集团划账、账户支出、账户存入、纯账户存入
    # 与 3-14 中应收费用、集团划账、应收费用加违约金、账户支出、账户存入、纯账户预存/支出是否一致；
    if df_34 is not None and df_314 is not None:
        # 3-4 账单金额、需划账费用、集团划账、账户支出、账户存入和纯账户存入
        # 3-14 应收费用、集团划账、应收费用加违约金、账户支出、账户存入、纯账户预存/支出
        # 营业网点列只需要第三方代收机构所在行
        include_sites = ['微信', '支付宝', '银联', '利安', '农行', '建行', '光大银行', '广发', '乌鲁木齐银行']
        df_314_filtered = df_314[df_314['SUBCOM_NAME2'].isin(include_sites)]
        # 准备对比数据集 (封装成字典，Key 是描述，Value 是 (3-4值, 3-14值))
        map_34_314 = {
            "应收费用 vs 账单金额": (df_34['ACC_MONEY'].sum(), df_314_filtered['FEE_TOTAL'].sum()),
            "需划账费用 vs 集团划账": (df_34['PST_ACTUAL_MONEY'].sum(), df_314_filtered['TOTAL_TRANSFER'].sum()),
            "集团划账 vs 应收+违约金": (df_34['TOTAL_TRANSFER'].sum(), df_314_filtered['FEE_TOTAL'].sum() + df_314_filtered['ACTUAL_LATEFEE'].sum()),
            "账户支出": (df_34['PST_PRESTORE_OUT_MONEY'].sum(), df_314_filtered['PT_PRESTORE_OUT_MONEY'].sum()),
            "账户存入": (df_34['TURN_PRESTORE_IN_MONEY'].sum(), df_314_filtered['PT_PRESTORE_IN_MONEY'].sum()),
            "纯账户存入/预存支出": (df_34['PST_PRESTORE_IN_MONEY'].sum(), df_314_filtered['RATE'].sum())
        }

        reconcile_metrics('3-4', '3-14', map_34_314)

    # --- 2. 3-6 vs 3-14 金额核对 ---
    if df_36 is not None and df_314 is not None:
        # 检查3-14中应收费用、违约金合计与3-6中实际收回小计、违约金是否一致
        map_36_314 = {
            "实际收回小计 vs 应收费用+违约金": (df_36[df_36['FEE_TYPE'] == '本月实收小计']['FEE_TOTAL'].sum(), df_314['FEE_TOTAL'].sum()),
            "违约金": (df_36[df_36['FEE_TYPE'] == '当月违约金']['ACTUAL_LATEFEE'].sum(), df_314['ACTUAL_LATEFEE'].sum())
        }

        reconcile_metrics('3-6', '3-14', map_36_314)

    # --- 3. 3-6 vs 3-13 金额核对 ---
    if df_36 is not None and df_313 is not None:
        # 检查3-13中数据（各项当月、当年未报、以前年度）与3-6中对应数据是否一致
        not_sum = df_313['收费方式'] != '汇总'
        map_36_313 = {
            "本月收回当月各项费用": (df_36[df_36['FEE_TYPE'] == '本月收回当月各项费用']['FEE_TOTAL'].sum(), df_313[(df_313['费用项目'] == '本月收回当月各项费用') & not_sum]['FEE_TOTAL'].sum()),
            "本月收回当年各项费用": (df_36[df_36['FEE_TYPE'] == '本月收回当年各项费用']['FEE_TOTAL'].sum(), df_313[(df_313['费用项目'] == '本月收回当年各项费用') & not_sum]['FEE_TOTAL'].sum()),
            "本月收回往年各项费用": (df_36[df_36['FEE_TYPE'] == '本月收回往年各项费用']['FEE_TOTAL'].sum(), df_313[(df_313['费用项目'] == '本月收回往年各项费用') & not_sum]['FEE_TOTAL'].sum()),
            "本月实收小计": (df_36[df_36['FEE_TYPE'] == '本月实收小计']['FEE_TOTAL'].sum(), df_313[(df_313['费用项目'] == '小计') & not_sum]['FEE_TOTAL'].sum()),
            "违约金": (df_36[df_36['FEE_TYPE'] == '当月违约金']['ACTUAL_LATEFEE'].sum(), df_313[(df_313['费用项目'] == '违约金') & not_sum]['FEE_TOTAL'].sum())
        }

        reconcile_metrics('3-6', '3-13', map_36_313)

def export_report(report_id):
    """导出指定 report_id 的报表，支持动态参数和多游标处理"""
    # 调用新的支持多数据源的函数，返回的是一个 list
    dfs = fetch_data_from_db(report_id)

    # 处理各个报表的特殊逻辑，得到最终用于导出的 DataFrame
    report_df = prepare_report_data(dfs, report_id)

    # 添加合计和组内小计等数据，将英文列名翻译成中文，并按照 config 中的 order 进行排序
    cfg = REPORTS[report_id]
    report_df = generate_report_package(report_df, cfg)

    # 保存
    full_path = os.path.join(base_dir, cfg['folder'], cfg['file_name'])
    export_excel_package(report_df, cfg, full_path)
    print(f"{report_id}报表已生成！")

if __name__ == '__main__':
    # 定义基础目录
    base_dir = r'F:\NewSystem\Reports'

    # 如果文件夹不存在，则自动创建（避免报错）
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # 先核对应收汇总报表的数值一致性，确保数据质量
    print("\n正在核对应收汇总报表的一致性...")
    ys_report_ids = ['3-10', '2-8', '3-7']
    report_package = {}

    for report_id in ys_report_ids:
        report_package[report_id] = fetch_data_from_db(report_id)
        report_package[report_id] = prepare_report_data(report_package[report_id], report_id)  # 预处理数据，确保核对时的计算逻辑正确

    # 调用核对函数
    results = reconcile_ys_reports(report_package)

    # 然后核对实收汇总报表的一致性
    print("\n正在核对实收汇总报表的一致性...")
    ss_report_ids = ['3-4', '3-6', '3-13', '3-14']

    # 清空数据包，重新加载实收相关报表的数据
    report_package = {}
    for report_id in ss_report_ids:
        report_package[report_id] = fetch_data_from_db(report_id)
        report_package[report_id] = prepare_report_data(report_package[report_id], report_id)  # 预处理数据，确保核对时的计算逻辑正确

    # 调用核对函数
    results = reconcile_ss_reports(report_package)

    # 最后核对汇总与明细报表的一致性
    

    exit()

    # 导出所有报表
    for report_id in REPORTS.keys():
        if report_id == '3-13':
            export_report(report_id)
            break
        #export_report(report_id)
