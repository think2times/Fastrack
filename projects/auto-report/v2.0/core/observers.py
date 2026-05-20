import os
import pandas as pd
from time import time
from abc import ABC, abstractmethod
from utils.style import apply_xlsxwriter_style


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
        self.total_results = {col: 0 for col in self.sum_cols}

    def on_next(self, idx, chunk):
        # 确定数据源（如果有多个游标，这里可以根据 idx 来区分）
        # 获取需要汇总的列，进行累加
        
        for col in self.sum_cols:
            self.total_results[col] += chunk[col].sum()

    def on_completed(self):
        return self.total_results

# 导出观察者：负责写Excel
class ExportObserver:
    def __init__(self, cfg):
        self.cfg = cfg

        # 定义基础目录
        base_dir = r'F:\NewSystem\Reports'
        self.file_path = os.path.join(base_dir, self.cfg['folder'], self.cfg['file_name'])
        self.columns_map = cfg.get('columns_map')
        self.sum_row_index = None # 记录合计行索引，样式函数会用到
        # 用一个列表把所有的 chunk 攒起来
        self.all_chunks = []

    def on_next(self, idx, chunk):
        if not chunk.empty:
            # 把列名统一转换为大写，并去掉前后空格，确保和配置中的列名一致
            chunk.columns = [c.upper().strip() for c in chunk.columns]

            # 先不写磁盘，存进列表
            self.all_chunks.append(chunk)

    def on_completed(self):
        if not self.all_chunks:
            return

        # 合并所有数据
        final_df = pd.concat(self.all_chunks, ignore_index=True)

        # 处理空值
        # 识别数值型列和非数值型列
        numeric_cols = final_df.select_dtypes(include=['number']).columns
        non_numeric_cols = final_df.select_dtypes(exclude=['number']).columns

        # 差异化填充
        final_df[numeric_cols] = final_df[numeric_cols].fillna(0)
        final_df[non_numeric_cols] = final_df[non_numeric_cols].fillna("")

        # 获取配置中定义的英文列名列表，过滤掉原始数据中多余的列，并严格按照配置的顺序排列
        mapping = self.cfg.get('columns_map', {})
        ordered_cols = [col for col in mapping.keys() if col in final_df.columns]
        final_df = final_df[ordered_cols]

        # 获取配置：哪些列需要合计，合计放哪里
        sum_cols = self.cfg.get('sum_cols', [])
        sum_pos = self.cfg.get('sum_position', 'none') # top, bottom, 或 none
        if sum_pos != 'none' and sum_cols:
            # 构造合计行
            sum_row = {col: '' for col in final_df.columns} # 先创建一个空行
            sum_row[final_df.columns[0]] = '合计' # 第一列写上“合计”字样

            for col in sum_cols:
                if col in final_df.columns:
                    # 确保只对数值列求和，避免因为非数值列（如字符串列）导致求和出错
                    sum_row[col] = pd.to_numeric(final_df[col], errors='coerce').sum()

            # 创建一个 DataFrame 来存储合计行，列名要和 final_df 一致
            sum_df = pd.DataFrame([sum_row], columns=final_df.columns)

            # 将合计行插入到第一行或最后一行，根据需求调整
            if sum_pos == 'top':
                final_df = pd.concat([sum_df, final_df], ignore_index=True)
                # 记录合计行所在的索引，方便样式函数加粗
                self.sum_row_index = 0
            else:
                final_df = pd.concat([final_df, sum_df], ignore_index=True)
                self.sum_row_index = len(final_df) - 1
        else:
            self.sum_row_index = None # 没有合计行

        # 所有计算结束后，最后统一重命名为中文列名，确保和样式函数中的列名一致
        final_df = final_df.rename(columns=mapping)

        # 写入 Excel
        t0 = time()
        with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Sheet1')

            # 统一应用样式函数，传入最终的 DataFrame 和配置
            apply_xlsxwriter_style(workbook, worksheet, final_df, self.cfg, self.sum_row_index)

        print(f"Excel 导出成功，总行数: {len(final_df)}, 耗时: {time() - t0:.2f} 秒")
