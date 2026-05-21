import pandas as pd
from datetime import datetime

from dateutil.relativedelta import relativedelta




def apply_xlsxwriter_style(workbook, worksheet, df, config, sum_row_index=None):
    """
    样式美化，包括标题、表头、数据行、合计行等的格式设置，以及列宽调整
    :param workbook: xlsxwriter 的 Workbook 对象
    :param worksheet: xlsxwriter 的 worksheet 对象
    :param df: 要写入的 DataFrame
    :param config: 报表配置信息
    :param sum_row_index: 合计行的索引
    """
    # 0. 初始化格式池
    fmts = _get_format_pool(workbook)

    # 1. 写入报表头部 (标题、副标题、站点)
    _write_report_headers(worksheet, df, config, fmts)

    # 2. 写入表头列名
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(3, col_num, value, fmts['header'])
    worksheet.set_row(3, 25)

    # 3. 写入核心数据
    data_start_row = 4
    col_widths = [len(str(c)) for c in df.columns]

    for row_idx, row_data in enumerate(df.values):
        actual_row = row_idx + data_start_row
        is_sum = (row_idx == sum_row_index)
        worksheet.set_row(actual_row, 25 if is_sum else 22.5)

        for col_idx, val in enumerate(row_data):
            # 调用选择器获取正确的格式
            fmt = _get_cell_format(fmts, df.columns[col_idx], val, is_sum)
            worksheet.write(actual_row, col_idx, val, fmt)

            # 更新列宽逻辑 (仅非大数据量)
            if len(df) <= 10000:
                _update_col_widths(col_widths, col_idx, val)

    # 4. 设置列宽
    _set_final_columns(worksheet, df, col_widths)


# --- 内部辅助函数 ---

def _get_format_pool(wb):
    """集中管理所有样式定义"""
    base = {'border': 1, 'align': 'center', 'valign': 'vcenter'}
    sum_base = {**base, 'bold': True, 'bg_color': '#F2F2F2'}
    
    return {
        'title': wb.add_format({'bold': True, 'font_size': 20, 'align': 'center', 'valign': 'vcenter'}),
        'header': wb.add_format({'bold': True, 'bg_color': '#DDEBF7', **base}),
        'date': wb.add_format({'num_format': 'yyyy/mm/dd', **base}),
        'money': wb.add_format({'num_format': '#,##0.00', **base}),
        'count': wb.add_format({'num_format': '###0', **base}),
        'sum_money': wb.add_format({'num_format': '#,##0.00', **sum_base}),
        'sum_count': wb.add_format({'num_format': '###0', **sum_base}),
        'sum_text': wb.add_format(sum_base),
        'data': wb.add_format(base),
        'left': wb.add_format({'align': 'left', 'valign': 'vcenter'}),
        'right': wb.add_format({'align': 'right', 'valign': 'vcenter'})
    }

def _get_cell_format(fmts, col_name, val, is_sum):
    """样式选择器"""
    # 1. 优先判断日期
    if any(kw in col_name for kw in ["日期", "时间"]) or hasattr(val, 'date'):
        return fmts['date']
    
    # 2. 判断数字
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        is_money = any(key in col_name for key in ['金', '费', '税', '价', '率', '账户', '转账'])
        if is_sum:
            return fmts['sum_money'] if is_money else fmts['sum_count']
        return fmts['money'] if is_money else fmts['count']
    
    # 3. 默认文本
    return fmts['sum_text'] if is_sum else fmts['data']

def _write_report_headers(ws, df, cfg, fmts):
    """处理报表顶部的三行"""
    max_col = df.shape[1]
    # 1. 标题美化 (第 1 行, 索引 0)
    display_subcoms = '全部分公司'
    report_title = f"{display_subcoms}{cfg.get('title', '自动生成报表')}"
    ws.merge_range(0, 0, 0, max_col - 1, report_title, fmts['title'])
    ws.set_row(0, 35)

    # 2. 副标题（左账期，右时间）
    # 动态获取配置中的信息
    today = datetime.now()
    stat_period = today.strftime('%Y%m')
    create_time = today.strftime('%Y-%m-%d')

    # 获取上个月的年月，格式为 YYYY-MM
        # 根据日期确定账期，如果是1-25号，则账期为上个月；如果是26号以后，则账期为当前月
        # today = datetime.now().strftime('%d')
        # if int(today) <= 25:
        #      bill_month = (datetime.now() - relativedelta(months=1)).strftime('%Y-%m')
        # else:
        #      bill_month = datetime.now().strftime('%Y-%m')

    mid = max_col // 2
    ws.merge_range(1, 0, 1, mid - 1, f"统计账期：{stat_period}", fmts['left'])
    ws.merge_range(1, mid, 1, max_col - 1, f"制表时间：{create_time}", fmts['right'])
    ws.set_row(1, 25)

    # 3. 统计站点
    ws.merge_range(2, 0, 2, max_col - 1, "统计站点：全部分公司", fmts['left'])
    ws.set_row(2, 25)

def _update_col_widths(widths, idx, val):
    """动态更新单列宽度"""
    str_val = str(val or "")
    length = sum(2 if ord(c) > 127 else 1 for c in str_val) # 中文按2算,英文按1算
    if length > widths[idx]:
        widths[idx] = length

def _set_final_columns(ws, df, widths):
    """应用最终宽度"""
    if len(df) > 10000:
        # 数据量较大时给统一宽度，避免性能问题
        ws.set_column(0, len(df.columns) - 1, 18)
    else:
        for i, w in enumerate(widths):
            # 限制最大宽度，防止内容过多导致列太长
            ws.set_column(i, i, min(max(w + 2, 10), 50))

def _merge_cells_by_col(worksheet, df, col_idx, start_row, fmt):
    """
    根据指定列的值进行合并单元格
    :param worksheet: xlsxwriter 的 worksheet 对象
    :param df: 当前写入的 DataFrame
    :param col_idx: 需要检查合并的列索引
    :param start_row: 数据开始写入的行索引（0-based）
    :param fmt: 合并单元格的格式对象
    """
    if df.empty:
        return

    data_start_idx = 0  # DataFrame 索引从 0 开始
    begin_row = start_row
    max_row = len(df) + start_row - 1
    
    # 遍历 DataFrame 里的数据（比遍历 Excel 单元格快得多）
    for i in range(len(df)):
        current_val = df.iloc[i, col_idx]
        
        # 探测下一行是否相同
        if i + 1 < len(df):
            next_val = df.iloc[i + 1, col_idx]
            # 如果相同且不是合计，继续循环
            if next_val == current_val and pd.notnull(current_val) and "合计" not in str(current_val):
                continue
        
        # 发现不同了，或者到最后一行了，执行合并
        actual_end_row = i + start_row
        if actual_end_row > begin_row:
            worksheet.merge_range(begin_row, col_idx, actual_end_row, col_idx, current_val, fmt)
        else:
            worksheet.write(begin_row, col_idx, current_val, fmt)
            
        # 开启新组
        begin_row = actual_end_row + 1