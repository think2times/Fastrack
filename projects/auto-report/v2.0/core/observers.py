import os
import pandas as pd
from time import time
from abc import ABC, abstractmethod
from config.config import BASE_DIR, REPORTS_CONFIG
from utils.style import set_excel_style
from utils.processor import insert_sum_row


class DataObserver(ABC):
    @abstractmethod
    def on_next(self, idx, chunk):
        """idx: 游标索引，chunk: 数据块（DataFrame）"""
        pass

    @abstractmethod
    def on_completed(self):
        """流处理结束时的收尾工作（如关闭文件、返回统计值）"""
        pass

# 核对观察者：负责算总数
class AuditObserver(DataObserver):
    def __init__(self, cfg):
        """
        cfg: 报表配置
        """
        self.sum_cols = cfg.get('sum_cols') or []
        # 获取该报表定义的“审计游标白名单”，如果不定义则默认只看 idx=0
        self.audit_idx = cfg.get('audit_idx', [0])
        self.total_results = {col: 0 for col in self.sum_cols}

    def on_next(self, idx, chunk):
        # 如果当前游标不是我们要审计的目标（比如只是配置信息游标），直接无视
        if idx not in self.audit_idx:
            return

        # 增加列检查：只有当前 chunk 包含我们要汇总的列时，才进行累加
        for col in self.sum_cols:
            if col in chunk.columns:
                # 转换为数值型再求和，防止因为 NaN 或文字导致报错
                val = pd.to_numeric(chunk[col], errors='coerce').sum()
                self.total_results[col] += val
            else:
                # 如果当前游标不包含此列，静默跳过，等待主数据游标
                continue

    def on_completed(self):
        return self.total_results

    def save_final_result(self, final_df=None):
        """
        补齐方法接口。
        审计观察者可能不需要导出 Excel，所以这里可以只记录日志或执行简单的核查。
        """
        print(f"🔍 AuditObserver: 正在对成品数据进行最后的合规性检查...")
        # 如果审计逻辑也需要基于 final_df 运行，可以在这里写
        pass


# 导出观察者：负责写Excel
class ExportObserver:
    def __init__(self, r_id):
        self.r_id = r_id
        self.cfg = REPORTS_CONFIG.get(r_id, {})
        self.file_path = os.path.join(BASE_DIR, self.cfg['folder'], self.cfg['file_name'])
        self.cursor_buffers = {} # 用于多游标数据的临时存储，key: 游标索引，value: list of chunks

    def on_next(self, cursor_idx, chunk):
        if cursor_idx not in self.cursor_buffers:
            self.cursor_buffers[cursor_idx] = []

        if not chunk.empty:
            # 把列名统一转换为大写，并去掉前后空格，确保和配置中的列名一致
            chunk.columns = [c.upper().strip() for c in chunk.columns]
            # 先不写磁盘，存进字典
            self.cursor_buffers[cursor_idx].append(chunk)

    def on_completed(self):
        if not self.cursor_buffers:
            return
        
        # 1. 汇总每个游标的完整 DataFrame，并按顺序转为列表
        # 这样保证了 buffers[0] 永远是第一个游标，buffers[1] 是第二个
        ordered_buffers = [
            pd.concat(self.cursor_buffers[idx], ignore_index=True) 
            for idx in sorted(self.cursor_buffers.keys())
        ]

        # 2. 执行配置中的特殊逻辑
        processor = self.cfg.get('processor', None)
        if processor:
            # --- 情况 A: 存在多个游标且需要跨游标处理数据 ---
            # 传入所有 buffers，在 processor 内部进行 pd.merge 和 计算
            final_df = processor(ordered_buffers)
        else:
            # --- 情况 B: 只有一个游标或只需要一个游标的数据 ---
            # 默认只取第一个游标，或者按需 concat
            final_df = pd.concat(ordered_buffers, ignore_index=True)

        # 3. 处理空值
        # 确保是一个独立的 DataFrame 副本，避免 SettingWithCopy 风险
        final_df = final_df.copy()

        # 识别数值型列和非数值型列
        numeric_cols = final_df.select_dtypes(include=['number']).columns
        non_numeric_cols = final_df.select_dtypes(exclude=['number']).columns

        # 差异化填充：数值填0，文字填""
        final_df[numeric_cols] = final_df[numeric_cols].fillna(0)
        final_df[non_numeric_cols] = final_df[non_numeric_cols].fillna("")

        # 4. 获取配置中定义的英文列名列表，过滤掉原始数据中多余的列，并严格按照配置的顺序排列
        mapping = self.cfg.get('columns_map', {})
        proc_name = self.cfg.get('proc_name', '')
        if proc_name not in ['RPT_WLMQ_306', 'RPT_WLMQ_313']:
            # 过滤掉不在 mapping 中的列，确保最终输出的 DataFrame 只有配置中定义的列    
            ordered_cols = [col for col in mapping.keys() if col in final_df.columns]
            final_df = final_df[ordered_cols]

        # 5. 根据配置插入小计行、合计行等
        group_by_col = self.cfg.get('group_by', None)
        sum_cols = self.cfg.get('sum_cols', [])
        sum_position = self.cfg.get('sum_position', 'none')
        final_df, sum_row_index = insert_sum_row(final_df, sum_cols, sum_position, proc_name, group_by_col)

        # 所有计算结束后，最后统一重命名为中文列名，确保和样式函数中的列名一致
        final_df = final_df.rename(columns=mapping)

        # 写入 Excel
        t0 = time()
        with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Sheet1')

            # 统一应用样式函数，传入最终的 DataFrame 和配置
            set_excel_style(workbook, worksheet, final_df, self.cfg, sum_row_index)

        print(f"{self.r_id} 报表导出成功，总行数: {len(final_df)}, 耗时: {time() - t0:.2f} 秒")

    def save_final_result(self, final_df):
            """
            新增方法：跳过所有计算逻辑，直接进行样式处理和导出。
            """
            # --- 步骤 1: 处理空值与列名过滤 (复用你原来的逻辑) ---
            final_df = final_df.copy()
            numeric_cols = final_df.select_dtypes(include=['number']).columns
            non_numeric_cols = final_df.select_dtypes(exclude=['number']).columns
            final_df[numeric_cols] = final_df[numeric_cols].fillna(0)
            final_df[non_numeric_cols] = final_df[non_numeric_cols].fillna("")

            mapping = self.cfg.get('columns_map', {})
            proc_name = self.cfg.get('proc_name', '')

            # 306/313 的特殊过滤逻辑
            if proc_name not in ['RPT_WLMQ_306', 'RPT_WLMQ_313']:
                ordered_cols = [col for col in mapping.keys() if col in final_df.columns]
                final_df = final_df[ordered_cols]

            # --- 步骤 2: 插入合计行 ---
            sum_cols = self.cfg.get('sum_cols', [])
            sum_position = self.cfg.get('sum_position', 'none')
            group_by_col = self.cfg.get('group_by', None)
            final_df, sum_row_index = insert_sum_row(final_df, sum_cols, sum_position, proc_name, group_by_col)

            # --- 步骤 3: 写入 Excel ---
            final_df = final_df.rename(columns=mapping)
            with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
                workbook = writer.book
                worksheet = workbook.add_worksheet('Sheet1')
                set_excel_style(workbook, worksheet, final_df, self.cfg, sum_row_index)

            print(f"✅ {self.r_id} 报表已直接导出成品。")
