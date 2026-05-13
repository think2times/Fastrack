from datetime import datetime
from dateutil.relativedelta import relativedelta


def apply_xlsxwriter_style(workbook, worksheet, df, config):
    """
    专门负责第二版 (xlsxwriter) 的样式美化
    """
    # 0. 准备格式 (Format)
    title_fmt = workbook.add_format({
        'bold': True, 'font_size': 20, 'align': 'center', 'valign': 'vcenter'
    })
    
    header_fmt = workbook.add_format({
        'bold': True, 'bg_color': '#DDEBF7', 'border': 1, 
        'align': 'center', 'valign': 'vcenter'
    })
    
    data_fmt = workbook.add_format({
        'border': 1, 'align': 'center', 'valign': 'vcenter'
    })
    datetime_fmt = workbook.add_format({
        'num_format': 'yyyy-mm-dd hh:mm:ss', # 强制显示为时间格式
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })
    
    left_fmt = workbook.add_format({'font_size': 11, 'align': 'left', 'valign': 'vcenter'})
    right_fmt = workbook.add_format({'font_size': 11, 'align': 'right', 'valign': 'vcenter'})

    # 1. 基础设置
    max_col = df.shape[1]
    display_subcoms = '全部分公司'
    
    # 动态获取配置中的信息
    report_title = f"{display_subcoms}{config.get('title', '自动生成报表')}"
    stat_period = datetime.now().strftime('%Y%m')
    create_time = datetime.now().strftime('%Y-%m-%d')

    # 获取上个月的年月，格式为 YYYY-MM
        # 根据日期确定账期，如果是1-25号，则账期为上个月；如果是26号以后，则账期为当前月
        # today = datetime.now().strftime('%d')
        # if int(today) <= 25:
        #      bill_month = (datetime.now() - relativedelta(months=1)).strftime('%Y-%m')
        # else:
        #      bill_month = datetime.now().strftime('%Y-%m')

    # 2. 标题美化 (第 1 行, 索引 0)
    worksheet.set_row(0, 35) # 行高
    worksheet.merge_range(0, 0, 0, max_col - 1, report_title, title_fmt)

    # 3. 副标题 (第 2 行, 索引 1)
    worksheet.set_row(1, 25)
    # 计算中间分界点
    mid_point = max_col // 2
    # 左侧制表时间：合并前半段列来靠左
    worksheet.merge_range(1, 0, 1, mid_point - 1, f"统计账期：{stat_period}", left_fmt)
    # 右侧制表时间：合并后半段列来靠右
    worksheet.merge_range(1, mid_point, 1, max_col - 1, f"制表时间：{create_time}", right_fmt)

    # 4. 统计站点 (第 3 行, 索引 2)
    worksheet.set_row(2, 25)
    worksheet.merge_range(2, 0, 2, max_col - 1, f"统计站点：{display_subcoms}", left_fmt)

    # 5. 写入表头 (第 4 行, 索引 3)
    # xlsxwriter 建议手动写入表头以便应用格式
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(3, col_num, value, header_fmt)

    # 6. 写入数据与列宽计算
    is_large_data = len(df) > 10000
    col_widths = [len(str(c)) for c in df.columns] # 初始宽度设为列名长度

    for row_num, row_data in enumerate(df.values):
        actual_row = row_num + 4 # 数据从第 5 行开始写入
        for col_num, cell_value in enumerate(row_data):
            col_name = df.columns[col_num]
            
            # 判断是否是时间列（根据你的 columns_map 里的中文名判断）
            if "时间" in col_name:
                worksheet.write(actual_row, col_num, cell_value, datetime_fmt)
            else:
                worksheet.write(actual_row, col_num, cell_value, data_fmt)
        
        # 如果不是大数据模式，动态计算列宽
        if not is_large_data:
            for i, val in enumerate(row_data):
                str_val = str(val or "")
                # 简单计算长度：中文2，英文1
                length = sum(2 if ord(c) > 127 else 1 for c in str_val)
                if length > col_widths[i]:
                    col_widths[i] = length

    # 7. 统一设置列宽
    if is_large_data:
        worksheet.set_column(0, max_col - 1, 18) # 大数据给统一宽度
    else:
        for i, width in enumerate(col_widths):
            final_width = min(max(width + 4, 10), 50)
            worksheet.set_column(i, i, final_width)