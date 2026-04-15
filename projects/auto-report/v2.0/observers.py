import pandas as pd
from abc import ABC, abstractmethod

class DataObserver(ABC):
    @abstractmethod
    def on_next(self, chunk):
        """每当新的一块数据(DataFrame)到来时执行"""
        pass

    @abstractmethod
    def on_completed(self):
        """流处理结束时的收尾工作（如关闭文件、返回统计值）"""
        pass

# 核对观察者：负责算总数
class AuditObserver(DataObserver):
    def __init__(self, sum_columns):
        self.sum_columns = sum_columns
        self.totals = {col: 0 for col in sum_columns}

    def on_next(self, chunk):
        for col in self.sum_columns:
            self.totals[col] += chunk[col].sum()

    def on_completed(self):
        return self.totals

# 导出观察者：负责写Excel
class ExportObserver(DataObserver):
    def __init__(self, file_path, sheet_name):
        self.writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        self.sheet_name = sheet_name
        self.curr_row = 0

    def on_next(self, chunk):
        chunk.to_excel(self.writer, sheet_name=self.sheet_name, 
                       startrow=self.curr_row, index=False, header=(self.curr_row == 0))
        self.curr_row += len(chunk)

    def on_completed(self):
        self.writer.close()
