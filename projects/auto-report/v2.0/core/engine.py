from config.config import PI_COLS

import pandas as pd
from typing import cast


class ReportEngine:
    def __init__(self, cfg, calc_func=None):
        """
        :param cfg: 报表配置
        :param calc_func: 对应 CALC_CONFIG 中的 lambda 函数
        """
        self.cfg = cfg
        self.calc_func = calc_func

    def run(self, streamer, observers):
        has_multiple_cursors = self.cfg.get('multi_cursor', 0)

        # 0. 统一包装为带索引的迭代器，输出格式为 (cursor_idx, chunk)
        indexed_streamer = streamer if has_multiple_cursors else ((0, chunk) for chunk in streamer)

        for cursor_idx, chunk in indexed_streamer:
            # 1. 一站式处理：清洗 + 基础算 + 特有算 + 精度控制
            _, data = 0, chunk
            if isinstance(chunk, tuple) and len(chunk) == 2:
                _, data = chunk

            processed_chunk = self._prepare_data(data)

            # 2. 分发给观察者（此时列名仍为英文，方便 Observer 计算合计行）
            for obs in observers:
                obs.on_next(cursor_idx, processed_chunk)

        # 3. 统一结束通知
        for obs in observers:
            obs.on_completed()

    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        统一预处理流水线：
        1. 格式清洗 (大写列名)
        2. 基础计算 (FEE_TOTAL 自动汇总)
        3. 特有逻辑 (执行配置中的 calc_func)
        4. 精度控制 (四舍五入)
        """
        if df.empty:
            return df

        # --- 阶段 1：基础清洗 ---
        # 统一大写列名，防止 Oracle 字段大小写不一致导致的 KeyError
        df.columns = [c.upper().strip() for c in df.columns]

        # --- 阶段 2：通用业务逻辑 (FEE_TOTAL) ---
        # 自动识别并计算应收费用 (针对水务基础 6 费项目)
        existing_pi_cols = [c for c in PI_COLS if c in df.columns]
        if len(existing_pi_cols) == 6:
            # 识别数值行（排除掉如‘收回率’等可能混入的非数值描述行）
            is_numeric_row = pd.to_numeric(df[existing_pi_cols[0]], errors='coerce').notnull()
            # 仅对数值行执行横向求和
            df.loc[is_numeric_row, 'FEE_TOTAL'] = df.loc[is_numeric_row, existing_pi_cols].fillna(0).sum(axis=1)

        # --- 阶段 3：报表特有计算 (calc_func) ---
        # 执行类似 3-23 报表的 EXTRA_MONEY 或 SEVEN_TOTAL 计算
        if self.calc_func and callable(self.calc_func):
            # 此时执行的是 df.assign(...) 逻辑
            # 强制转换类型，消除 "object is not assignable to DataFrame" 报错
            result = self.calc_func(df)
            df = cast(pd.DataFrame, result)

        # --- 阶段 4：精度处理 ---
        # 只对数值型列（整数、浮点数）进行四舍五入，避免时间戳或字符串被误伤
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            float_keywords = ['PRICE', 'MONEY', 'FEE', 'LATEFEE', 'TRANSFER', 'RATE', 'SEVEN']
            if any(kw in col.upper() for kw in float_keywords):
                df[col] = df[col].round(2)  # 金额类保留两位小数
            else:
                df[col] = df[col].fillna(0).astype('Int64')  # 其他数值保留整数，使用 Pandas 的 Nullable Integer 类型

        return df
