from time import time

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
        for i, (_, arg_type, direction) in enumerate(args_info):
            if direction == 'OUT' and arg_type == 'REF CURSOR':
                out_var = cursor.var(oracledb.CURSOR)
                full_params.append(out_var)
                out_cursor_indices.append(len(full_params) - 1)
            else:
                full_params.append(self.params[i]) # 假设 params 是按位置组织的

        print(f"调用存储过程 '{self.proc_name}'，参数总数: {len(full_params)}, OUT 游标数量: {len(out_cursor_indices)}")
        cursor.callproc(self.proc_name, full_params)
        
        # 2. 依次迭代每个游标
        try:
            # 增加一个游标计数器, 用于标识当前是第几个游标（默认从0开始）
            cursor_count = 0

            for idx in out_cursor_indices:
                rs = full_params[idx].getvalue()
                rs.arraysize = self.chunk_size
                if not rs: continue

                cols = [col[0] for col in rs.description]
                try: # 针对单个游标的读取
                    while True:
                        t0 = time()
                        rows = rs.fetchmany(self.chunk_size)
                        print(f"从第 {cursor_count + 1} 个游标提取 {len(rows)} 行数据，耗时: {time() - t0:.2f} 秒")
                        if not rows: break

                        # 返回 (游标编号, 数据帧)
                        yield cursor_count, pd.DataFrame(rows, columns=cols)
                finally:
                    # 读完一个游标，立刻释放一个，不需要等整个循环结束
                    rs.close()

                # 处理完一个游标，计数器加 1
                cursor_count += 1
        finally:
            cursor.close()