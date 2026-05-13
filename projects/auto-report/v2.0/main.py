import os
import oracledb
from datetime import datetime
from dateutil.relativedelta import relativedelta

from config.config import DB_CONFIG, REPORTS_CONFIG
from utils.factory import TaskFactory


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

    # 创建统一的结果集
    report_pool = {}
    tasks = []

    # 迭代报表配置，生成报表
    for r_id, cfg in REPORTS_CONFIG.items():
        if r_id == '3-47':
            print(f"创建报表任务：{r_id}")
            factory = TaskFactory(conn, sub_com=subcoms, month=bill_month)
            engine, streamer, observers = factory.create_task(r_id)
            tasks.append((engine, streamer, observers))


    # 所有的 for 循环结束后，进行跨表逻辑核对
    for engine, streamer, observers in tasks:
        engine.run(streamer, observers)
