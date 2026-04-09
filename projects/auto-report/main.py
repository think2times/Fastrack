from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from exporters import export_excel_package
from db_helper import init_client, call_procedure
from config import REPORTS, DB_CONFIG
from processors import prepare_multi_cursor_report


def main(report_id, subcoms=None, bill_month=None):
    if subcoms is None:
        subcoms = ''
    
    if bill_month is None:
        # 获取上个月的年月，格式为 YYYY-MM
        last_month = datetime.now() - relativedelta(months=1)
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
    dfs = call_procedure(cfg['proc'], proc_params, DB_CONFIG)
    
    # 如果配置了 multi_source，则把整个列表 dfs 传给 calc_func 处理
    # 否则，默认取第一个游标作为主 df 传给后续逻辑
    report_df = prepare_multi_cursor_report(dfs, cfg)

    # 保存
    full_path = os.path.join(base_dir, cfg['folder'], cfg['file_name'])
    export_excel_package(report_df, cfg, full_path)
    # export_sheet_excel(report_df, cfg, full_path)
    print(f"{report_id}报表已生成！")

if __name__ == '__main__':
    # 定义基础目录
    base_dir = r'F:\NewSystem\Reports'

    # 如果文件夹不存在，则自动创建（避免报错）
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    for report_id in REPORTS.keys():
        if report_id == '3-4':
            main(report_id)
            break
        #main(report_id)
