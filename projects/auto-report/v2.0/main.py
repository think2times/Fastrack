import os
import oracledb
from datetime import datetime
from dateutil.relativedelta import relativedelta

from config.config import DB_CONFIG, REPORTS_CONFIG
from utils.factory import TaskFactory
from utils.reconciler import run_full_reconciliation


def connect2db(lib_dir, db_config):
    """连接数据库，设置环境变量，确保中文字符正确显示"""
    # 设置环境变量，确保中文字符正确显示
    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.ZHS16GBK'
    # 设置数据库客户端库路径
    oracledb.init_oracle_client(lib_dir=lib_dir)

    return oracledb.connect(**db_config)

if __name__ == "__main__":
    # 指定报表查询范围
    subcoms = ''    # 表示获取全部分公司数据，如果需要指定分公司，可以改成 '011,021,...'

    # 获取上个月的年月，格式为 YYYY-MM
    # 根据日期确定账期，如果是1-25号，则账期为上个月；如果是26号以后，则账期为当前月
    today = datetime.now().strftime('%d')
    if int(today) <= 25:
         bill_month = (datetime.now() - relativedelta(months=1)).strftime('%Y-%m')
    else:
         bill_month = datetime.now().strftime('%Y-%m')

    # 连接数据库，使用本地驱动而不是内置的 Thin 驱动
    lib_dir = r'F:\app\pluto\product\instantclient_11_2'
    # 连接数据库，设置环境变量，确保中文字符正确显示
    conn = connect2db(lib_dir, DB_CONFIG)

    # --- 步骤 1: 生成所有报表数据 ---
    all_report_results = {}  # 格式: { r_id: {0: df} }
    task_registry = []

    for r_id, cfg in REPORTS_CONFIG.items():
        # if r_id not in ['3-14', '3-47']:
        #     continue
        factory = TaskFactory(r_id, conn, sub_com=subcoms, month=bill_month)
        engine, streamer, observers = factory.create_task()

        # 仅生成数据，暂不导出
        processed_dict = engine.generate_data(streamer)

        # 为了方便核对逻辑，我们取 0 号位作为该报表的主 DataFrame
        all_report_results[r_id] = processed_dict.get(0)

        # 暂存起来，后面导出用
        task_registry.append({
            'r_id': r_id,
            'engine': engine,
            'observers': observers,
            'data': processed_dict
        })

    # --- 步骤 2: 执行核对 (Reconciler) ---
    if not run_full_reconciliation(all_report_results):
        ans = input("\n⚠️ 对账未通过，是否强制导出？(y/n): ")
        if ans.lower() != 'y':
            print("停止导出。")
            exit()

    # --- 步骤 3: 核对通过后，正式执行导出 ---
    for task in task_registry:
        print(f"正在导出: {task['r_id']}...")
        task['engine'].run_observers(task['data'], task['observers'])

    print("✅ 全部完成！")
