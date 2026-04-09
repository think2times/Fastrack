import os
import oracledb
import pandas as pd


def init_client(lib_dir):
    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.ZHS16GBK'
    try:
        oracledb.init_oracle_client(lib_dir=lib_dir)
    except Exception as e:
        print(f"驱动已初始化: {e}")

def call_procedure(proc_name, in_params, db_config):
    """
    动态检测并调用存储过程，返回所有游标 DataFrame 的列表
    proc_name: 存储过程名
    in_params: list, 输入参数
    db_config: 数据库连接信息
    """
    with oracledb.connect(**db_config) as conn:
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
            
            for i, arg in enumerate(args_info):
                # 如果是 OUT 类型的游标
                if arg[2] == 'OUT' and arg[1] == 'REF CURSOR':
                    out_var = cursor.var(oracledb.CURSOR)
                    full_params.append(out_var)
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
