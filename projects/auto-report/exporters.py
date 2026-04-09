import pandas as pd
from styles import apply_sheet_style
from processors import clean_illegal_chars


def export_excel_package(data_package, config, full_path):
    """
    只负责写文件和样式，不负责任何计算
    data_package: { '全部': df1, '分公司A': df2, ... }
    """
    with pd.ExcelWriter(full_path, engine="openpyxl") as writer:
        for sheet_name, final_df in data_package.items():
            # 执行非法字符清洗（这一步也可以提前到准备数据阶段）
            clean_df = final_df.map(clean_illegal_chars)
            
            # 写入 Excel，从第4行开始（留出标题空间）
            clean_df.to_excel(writer, index=False, startrow=3, sheet_name=sheet_name)
            
            # 应用样式（styles.py 里的函数）
            apply_sheet_style(writer.sheets[sheet_name], clean_df, config, sheet_name)
