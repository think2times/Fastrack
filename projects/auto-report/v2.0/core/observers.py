import pandas as pd
from abc import ABC, abstractmethod

from config.config import REPORTS


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
        self.cfg = cfg
        self.results = {}

    def on_next(self, chunk):
        # 确定数据源（如果有多个游标，这里可以根据 idx 来区分）
        if self.cfg.get('multi_cursors', 1) > 1:
            cursor_indices = [i for i in range(self.cfg['multi_cursors'])]
        else:
            # 获取需要汇总的列，进行累加
            if self.cfg.get('sum_cols'):
                for col in self.cfg['sum_cols']:
                    self.results[col] = self.results.get(col, 0) + chunk[col].sum()

    def on_completed(self):
        return self.results

# 导出观察者：负责写Excel
class ExportObserver(DataObserver):
    def __init__(self, file_path, index_to_sheet):
        """
        index_to_sheet: {0: '汇总表', 1: '明细表'}
        """
        self.writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        self.index_to_sheet = index_to_sheet
        self.curr_rows = {idx: 0 for idx in index_to_sheet.keys()}

    def on_next(self, idx, chunk):
        if idx in self.index_to_sheet:
            sheet_name = self.index_to_sheet[idx]
            is_first = (self.curr_rows[idx] == 0)
            
            chunk.to_excel(self.writer, sheet_name=sheet_name, 
                           startrow=self.curr_rows[idx], 
                           index=False, header=is_first)
            
            self.curr_rows[idx] += len(chunk)

    def on_completed(self):
        self.writer.close()
        return f"文件已保存至 {self.writer}"
