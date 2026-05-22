import pandas as pd
from typing import Any, cast
from config.config import PI_COLS


class ReportEngine:
    def __init__(self, cfg):
        """
        :param cfg: 报表配置
        """
        self.cfg = cfg

    def run(self, streamer, observers):
        has_multiple_cursors = self.cfg.get('multi_cursors', 0)

        for item in streamer:
            # 1. 显式初始化，并标注类型为 Any 避免推导冲突
            cursor_idx: int = 0
            raw_data: Any = None
            
            # 2. 统一包装为带索引的迭代器：单游标转为 (0, df)，多游标保持 (cursor_idx, df)
            if has_multiple_cursors:
                # 针对多游标：item 是 (idx, dataframe)
                cursor_idx, raw_data = item
            else:
                # 针对单游标：item 直接是 dataframe
                cursor_idx, raw_data = 0, item

            # 3. 检查 data 是否被误包成了元组 (由于某些驱动版本差异)
            if isinstance(raw_data, tuple) and len(raw_data) == 2:
                # 如果发现 data 居然还是 (0, df)，二次拆包
                _, raw_data = raw_data
            
            # 4. 将 raw_data 强行转换为 DataFrame 类型
            data = cast(pd.DataFrame, raw_data)

            # 5. 一站式处理：清洗 + 基础计算 + 特有逻辑 + 精度控制
            processed_chunk = self._prepare_data(data)

            # 6. 分发给观察者（此时列名仍为英文，方便 Observer 计算合计行）
            for obs in observers:
                obs.on_next(cursor_idx, processed_chunk)

        # 7. 统一结束通知
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

        # --- 阶段 3：精度处理 ---
        # 只对数值型列（整数、浮点数）进行四舍五入，避免时间戳或字符串被误伤
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            float_keywords = ['PRICE', 'MONEY', 'FEE', 'LATEFEE', 'TRANSFER', 'RATE', 'SEVEN']
            if any(kw in col.upper() for kw in float_keywords):
                df[col] = df[col].round(2)  # 金额类保留两位小数
            else:
                df[col] = df[col].fillna(0).astype('Int64')  # 其他数值保留整数，使用 Pandas 的 Nullable Integer 类型

        return df
