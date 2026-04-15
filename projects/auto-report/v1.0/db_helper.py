import os
import oracledb
import pandas as pd


def connect2db(lib_dir, db_config):
    """初始化 Oracle 客户端并连接数据库"""
    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.ZHS16GBK'
    try:
        oracledb.init_oracle_client(lib_dir=lib_dir)
        return oracledb.connect(**db_config)
    except Exception as e:
        print(f"驱动已初始化: {e}")

def call_procedure(conn, proc_name, in_params):
    """
    动态检测并调用存储过程，返回所有游标 DataFrame 的列表
    proc_name: 存储过程名
    in_params: list, 输入参数
    conn: 数据库连接对象
    """
    with conn.cursor() as cursor:
        # 1. 动态获取存储过程的参数定义
        # 这能自动识别有多少个 OUT SYS_REFCURSOR，无需手动配置
        cursor.execute("""
            SELECT ARGUMENT_NAME, DATA_TYPE, IN_OUT 
            FROM ALL_ARGUMENTS 
            WHERE OBJECT_NAME = :1 AND PACKAGE_NAME IS NULL
            ORDER BY POSITION
        """, [proc_name.upper()])
        
        args_info = cursor.fetchall()
        
        # 2. 准备参数列表
        full_params = list(in_params)
        out_cursor_positions = [] # 记录游标所在的位置索引
        
        for _, data_type, in_out in args_info:
            if in_out == 'OUT' and data_type == 'REF CURSOR':
                out_var = cursor.var(oracledb.CURSOR)
                full_params.append(out_var)
                # 记录游标在参数列表中的索引位置
                out_cursor_positions.append(len(full_params) - 1)
        
        # 3. 调用存储过程
        cursor.callproc(proc_name, full_params)
        
        # 4. 提取所有游标并转为 DataFrame
        dataframes = []
        for pos in out_cursor_positions:
            rs = full_params[pos].getvalue()
            if rs:
                cols = [col[0] for col in rs.description]
                dataframes.append(pd.DataFrame(rs.fetchall(), columns=cols))
            else:
                dataframes.append(pd.DataFrame()) # 空游标补位
        
        return dataframes
