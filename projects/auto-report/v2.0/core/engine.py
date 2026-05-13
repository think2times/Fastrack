from config.config import PI_COLS

import pandas as pd


class ReportEngine:
    def __init__(self, calc_func=None):
        """
        :param calc_func: 对应你 CALC_CONFIG 中的 lambda 函数
        """
        self.calc_func = calc_func

    def run(self, streamer, observers):
        for cursor_idx, chunk in streamer:
            # --- 预处理数据块 ---
            # 1. 执行通用处理
            chunk = self.standard_preprocess(chunk)
            
            # 2. 执行报表特有的计算
            if self.calc_func:
                chunk = self.calc_func(chunk)
            
            # --- 预处理结束，再交给观察者 ---
            for obs in observers:
                obs.on_next(cursor_idx, chunk)

        for obs in observers:
            obs.on_completed()

    def standard_preprocess(self, df):
        """
        通用预处理：大写列名、计算应收费用、四舍五入
        """
        if df.empty:
            return df
    
        # 1. 统一大写列名，防止 SQL 字段大小写不一致
        df.columns = [c.upper() for c in df.columns]

        # 2. 自动识别 PI_COLS 并计算 FEE_TOTAL
        # 只有当 DataFrame 中包含这些列时才计算，避免报错
        existing_pi_cols = [c for c in PI_COLS if c in df.columns]
        if len(existing_pi_cols) == 6:
            # 识别哪些行是纯数值行（排除掉收回率这种带 % 的字符串行）
            # 我们只对 PI1_MONEY 这一列是数值类型的行进行计算
            is_numeric_row = pd.to_numeric(df[existing_pi_cols[0]], errors='coerce').notnull()

            # 只有数值行才计算 FEE_TOTAL，其他行（如收回率行）保持原样或设为 0
            df.loc[is_numeric_row, 'FEE_TOTAL'] = df.loc[is_numeric_row, existing_pi_cols].fillna(0).sum(axis=1)

        # 3. 只对数值型列（整数、浮点数）进行四舍五入
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].round(2)

        return df
