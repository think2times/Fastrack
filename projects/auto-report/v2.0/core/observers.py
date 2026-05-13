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
        # 用一个列表把所有的 chunk 攒起来
        self.all_chunks = []

    def on_next(self, idx, chunk):
        if not chunk.empty:
            # 翻译列名
            chunk.columns = [c.upper().strip() for c in chunk.columns]
            if self.columns_map:
                up_map = {k.upper().strip(): v for k, v in self.columns_map.items()}
                chunk = chunk.rename(columns=up_map)
            
            # 先不写磁盘，存进列表
            self.all_chunks.append(chunk)

    def on_completed(self):
        if not self.all_chunks:
            return
        
        # 合并所有数据
        final_df = pd.concat(self.all_chunks, ignore_index=True)

        # 处理空值，将 NaN 替换为空字符串
        final_df = final_df.fillna("")

        # 写入 Excel
        t0 = time()
        with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Sheet1')
            
            # 统一应用样式函数，传入最终的 DataFrame 和配置
            apply_xlsxwriter_style(workbook, worksheet, final_df, self.cfg)
            
        print(f"Excel 导出成功，总行数: {len(final_df)}, 耗时: {time() - t0:.2f} 秒")