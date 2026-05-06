import oracledb
import pandas as pd


class DataStreamer:
    """
    统一封装器：无论报表大小，外界只管 for chunk in streamer
    """
    def __init__(self, conn, proc_name, params, chunk_size=50000):
        self.conn = conn
        self.proc_name = proc_name
        self.params = params
        self.chunk_size = chunk_size

    def __iter__(self):
        """让类变得可迭代"""
        cursor = self.conn.cursor()
        # 1. 动态准备参数：识别哪些是游标位
        # 1. 动态获取存储过程的参数定义
        # 这能自动识别有多少个 OUT SYS_REFCURSOR，无需手动配置
        cursor.execute("""
            SELECT ARGUMENT_NAME, DATA_TYPE, IN_OUT 
            FROM ALL_ARGUMENTS 
            WHERE OBJECT_NAME = :1 AND PACKAGE_NAME IS NULL
            ORDER BY POSITION
        """, [self.proc_name.upper()])
        
        args_info = cursor.fetchall()

        full_params = []
        out_cursor_indices = []
        for i, (arg_type, direction) in enumerate(args_info):
            if direction == 'OUT' and arg_type == 'REF CURSOR':
                out_var = cursor.var(oracledb.CURSOR)
                full_params.append(out_var)
                out_cursor_indices.append(len(full_params) - 1)
            else:
                full_params.append(self.params.get(i)) # 假设 params 是按位置组织的

        cursor.callproc(self.proc_name, full_params)
        
        # 2. 依次迭代每个游标
        try:
            for idx in out_cursor_indices:
                rs = full_params[idx].getvalue()
                if not rs: 
                    continue
                
                cols = [col[0] for col in rs.description]
                try: # 针对单个游标的读取
                    while True:
                        rows = rs.fetchmany(self.chunk_size)
                        if not rows: break
                        yield idx, pd.DataFrame(rows, columns=cols)
                finally:
                    # 读完一个游标，立刻释放一个，不需要等整个循环结束
                    rs.close()
        finally:
            cursor.close()