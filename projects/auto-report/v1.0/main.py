import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from db_helper import connect2db, call_procedure

from config import REPORTS, DB_CONFIG
from processors import generate_report_data, prepare_report_data, reconcile_ys_reports, reconcile_ss_reports, export2excel


def fetch_data_from_db(conn, report_ids, subcoms=None, bill_month=None):
    """获取 report_ids 列表中的报表数据，返回 DataFrame 字典（Key 是 report_id，Value 是对应的 DataFrame）"""
    report_package = {}

    for report_id in report_ids:
        cfg = REPORTS[report_id]
        proc_name = cfg['proc']
        proc_params = cfg['params'](subcoms, bill_month)
        # 调用新的支持多数据源的函数，返回的是一个 list
        report_package[report_id] = call_procedure(conn, proc_name, proc_params)
        report_package[report_id] = prepare_report_data(report_package[report_id], report_id)  # 预处理数据，确保核对时的计算逻辑正确

    return report_package

def process_report_group(conn, report_ids, subcoms, bill_month, reconcile_func):
    """
    封装【取数 -> 核对】的通用逻辑
    """
    print(f"\n正在处理报表组: {report_ids} ...")
    package = fetch_data_from_db(conn, report_ids, subcoms, bill_month)
    
    if reconcile_func(package):
        print(f"✅ {report_ids} 核对通过")
    else:
        print(f"❌ {report_ids} 核对存在差异，请查阅日志")

    return package

def export_report(report_id, report_package):
    """导出指定 report_id 的报表"""
    # 添加合计和组内小计等数据，将英文列名翻译成中文，并按照 config 中的 order 进行排序
    cfg = REPORTS[report_id]
    report_data = generate_report_data(report_package, cfg)

    # 保存
    full_path = os.path.join(base_dir, cfg['folder'], cfg['file_name'])
    export2excel(report_data, cfg, full_path)
    print(f"{report_id}报表已生成！")

if __name__ == '__main__':
    # 定义基础目录
    base_dir = r'F:\NewSystem\Reports'

    # 指定报表查询范围
    subcoms = ''    # 表示获取全部分公司数据，如果需要指定分公司，可以改成 '011,021,...'

    # 获取上个月的年月，格式为 YYYY-MM
    # 根据日期确定账期，如果是1-25号，则账期为上个月；如果是26号以后，则账期为当前月
    now = datetime.now().strftime('%d')
    if int(now) <= 25:
         bill_month = (datetime.now() - relativedelta(months=1)).strftime('%Y-%m')
    else:
         bill_month = datetime.now().strftime('%Y-%m')

    # 连接数据库，使用本地驱动而不是内置的 Thin 驱动
    lib_dir = r'F:\app\pluto\product\instantclient_11_2'
    conn = connect2db(lib_dir, DB_CONFIG)

    # 如果文件夹不存在，则自动创建（避免报错）
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # 处理每个报表组，获取数据并核对
    ys_pkg = process_report_group(conn, ['2-8', '3-7', '3-10', '3-11'], subcoms, bill_month, reconcile_ys_reports)
    ss_pkg = process_report_group(conn, ['3-4', '3-6', '3-13', '3-14'], subcoms, bill_month, reconcile_ss_reports)
    details_pkg = {}
    # details_pkg = process_report_group(conn, ['3-15', '3-20', '3-23', '3-47'], subcoms, bill_month, reconcile_details_reports)

    # 导出已核对报表
    all_packages = {**ys_pkg, **ss_pkg, **details_pkg}
    for r_id, r_data in all_packages.items():
        export_report(r_id, r_data)

    # 导出明细报表
    # for r_id in ['3-15', '3-20', '3-23', '3-47']:
    #     report_package = fetch_data_from_db(conn, [r_id], subcoms, bill_month)[r_id]
    #     export_report(r_id, report_package)
