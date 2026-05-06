import pandas as pd
from abc import ABC, abstractmethod

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
    def __init__(self, indices):
        """
        indices: 游标索引列表
        """
        self.indices = indices
        self.results = {idx: 0 for idx in indices}

    def on_next(self, idx, chunk):
        # 只有在 indices 中的 idx 才会处理
        if idx in self.indices:
            # 假设所有报表都要核对 ACC_MONEY
            self.results[idx] += chunk['ACC_MONEY'].sum()

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
