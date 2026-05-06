import os
import oracledb

from config.config import DB_CONFIG, REPORTS

from core.engine import ReportEngine
from core.streamer import DataStreamer
from core.observers import AuditObserver, ExportObserver


def connect2db(lib_dir, db_config):
    """连接数据库，设置环境变量，确保中文字符正确显示"""
    # 设置环境变量，确保中文字符正确显示
    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.ZHS16GBK'
    # 设置数据库客户端库路径
    oracledb.init_oracle_client(lib_dir=lib_dir)

    return oracledb.connect(**db_config)

if __name__ == "__main__":
    # 连接数据库，使用本地驱动而不是内置的 Thin 驱动
    lib_dir = r'F:\app\pluto\product\instantclient_11_2'
    # 连接数据库，设置环境变量，确保中文字符正确显示
    conn = connect2db(lib_dir, DB_CONFIG)

    # 创建统一的结果集
    report_pool = {}

    # 迭代报表配置，生成报表
    for r_id, cfg in REPORTS.items():
        # 创建数据流对象
        streamer = DataStreamer(conn, cfg['proc_name'], cfg['params'])
        # 创建观察者对象
        cursor_indices = [0]  # 默认只有一个游标索引为 0
        if cfg.get('multi_cursors', 1) > 1:
            cursor_indices = [i for i in range(cfg['multi_cursors'])]
        observers = [AuditObserver(cursor_indices), ExportObserver(cfg['export_path'], cfg['sheet_name'])]

        # 运行报表引擎
        engine = ReportEngine(streamer)
        results = engine.run(streamer, observers)
        print(f"Report {r_id} completed. Audit results: {results['AuditObserver']}")

        # 将结果存入统一的结果池
        report_pool[r_id] = results
    
    # 所有的 for 循环结束后，进行跨表逻辑核对
