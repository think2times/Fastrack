from datetime import datetime
from dateutil.relativedelta import relativedelta


def apply_xlsxwriter_style(workbook, worksheet, df, config, sum_row_index=None):
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

    # 合计行基础格式
    sum_base_cfg = {
        'bold': True,
        'bg_color': '#F2F2F2', # 浅灰色背景区别于普通行
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '#,##0' # 保证金额格式正确
    }

    # 合计行文字格式（用于第一列“合计”字样）
    sum_text_fmt = workbook.add_format(sum_base_cfg)

    # 金额：千分位+2位小数
    money_cfg = {'num_format': '#,##0.00', 'border': 1, 'align': 'center', 'valign': 'vcenter'}
    money_fmt = workbook.add_format({**money_cfg, 'border': 1})
    sum_money_fmt = workbook.add_format({**sum_base_cfg, **money_cfg})

    # 数量格式 (户数、水量)
    count_cfg = {'num_format': '#,##0', 'border': 1, 'align': 'center', 'valign': 'vcenter'}
    count_fmt = workbook.add_format({**count_cfg, 'border': 1})
    sum_count_fmt = workbook.add_format({**sum_base_cfg, **count_cfg})

    # 日期格式
    date_cfg = {'num_format': 'yyyy/mm/dd'}
    date_fmt = workbook.add_format({
        **date_cfg,
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
        worksheet.set_row(3, 25) # 设置表头行高

    # 6. 写入数据与列宽计算
    is_large_data = len(df) > 10000
    col_widths = [len(str(c)) for c in df.columns] # 初始宽度设为列名长度

    # 数据从第 5 行开始写入，索引为 4
    data_start_row = 4
    for row_num, row_data in enumerate(df.values):
        actual_row = row_num + data_start_row
        is_sum_row = (row_num == sum_row_index)

        # 如果是合计行，可以稍微设高一点点，使其更醒目
        if row_num == sum_row_index:
            worksheet.set_row(actual_row, 25)
        else:
            worksheet.set_row(actual_row, 22.5) # 普通数据行高

        for col_num, cell_value in enumerate(row_data):
            col_name = df.columns[col_num]

            # 检查当前值是否是数字
            is_numeric = isinstance(cell_value, (int, float, complex)) and not isinstance(cell_value, bool)

            if is_numeric:
                # 1. 处理日期
                if "日期" in col_name:
                    fmt = date_fmt

                # 2. 处理费用、单价、回收率、转账（两位小数）
                elif any(key in col_name for key in ['金', '费', '税', '价', '率', '账户', '转账']):
                    fmt = sum_money_fmt if is_sum_row else money_fmt

                # 3. 处理户数、水量（整数）
                else:
                    fmt = sum_count_fmt if is_sum_row else count_fmt
            else:
                fmt = sum_text_fmt if is_sum_row else data_fmt

            worksheet.write(actual_row, col_num, cell_value, fmt)

        # 如果数据量不大，动态计算列宽
        if not is_large_data:
            for i, val in enumerate(row_data):
                str_val = str(val or "")
                # 简单计算长度：中文2，英文1
                length = sum(2 if ord(c) > 127 else 1 for c in str_val)
                if length > col_widths[i]:
                    col_widths[i] = length

    # 7. 设置列宽
    if is_large_data:
        worksheet.set_column(0, max_col - 1, 18) # 数据量较大时给统一宽度
    else:
        # 限制最大宽度，防止内容过多导致列太长
        for i, width in enumerate(col_widths):
            final_width = min(max(width + 4, 10), 50)
            worksheet.set_column(i, i, final_width)
