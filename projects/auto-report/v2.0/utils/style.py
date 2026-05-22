import pandas as pd
from datetime import datetime

from dateutil.relativedelta import relativedelta


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
        is_money = any(key in col_name for key in ['金', '费', '税', '价', '率', '账户', '转账', '划账'])
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
    time = datetime.now()
    create_time = time.strftime('%Y-%m-%d')
    # 根据日期确定账期，如果是1-25号，则账期为上个月；如果是26号以后，则账期为当前月
    today = datetime.now().strftime('%d')
    if int(today) <= 25:
        stat_period = (time - relativedelta(months=1)).strftime('%Y%m')
    else:
        stat_period = time.strftime('%Y%m')

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

def merge_hierarchical_cells(worksheet, df, merge_cols, start_row, cell_fmt):
    """
    处理多级合并的情况，例如先按第一列合并，再在每个大组内按第二列合并
    :param worksheet: xlsxwriter 的 worksheet 对象
    :param df: 当前写入的 DataFrame
    :param merge_cols: 需要依次合并的列索引列表，例如 [0, 1]
    :param start_row: 数据开始写入的行索引（0-based）
    :param cell_fmt: 合并单元格的格式对象
    """
    if not merge_cols or df.empty:
        return

    # 1. 确保 merge_cols 全是数字索引。如果是列名，转换它
    col_indices = []
    for col in merge_cols:
        if isinstance(col, str):
            col_indices.append(df.columns.get_loc(col))
        else:
            col_indices.append(col)

    # 2. 定义内部递归函数
    def recursive_merge(col_depth_idx, s_row, e_row):
        # col_depth_idx: 当前处理 col_indices 中的第几个
        if col_depth_idx >= len(col_indices):
            return

        current_col = col_indices[col_depth_idx]
        
        # 在 [s_row, e_row] 范围内寻找相同的值块
        i = s_row
        while i <= e_row:
            # 计算在 DataFrame 中的实际行索引
            df_idx = i - start_row
            current_val = df.iloc[df_idx, current_col]
            
            run_end = i
            # 探测相同块的边界
            while run_end + 1 <= e_row:
                next_val = df.iloc[run_end + 1 - start_row, current_col]
                # 逻辑：值相同，且不包含“计”字（避开合计/小计行）
                if next_val == current_val and pd.notnull(current_val) and "计" not in str(current_val):
                    run_end += 1
                else:
                    break
            
            # 执行合并
            if run_end > i:
                worksheet.merge_range(i, current_col, run_end, current_col, current_val, cell_fmt)
                # 递归处理子列：仅在当前合并的 [i, run_end] 范围内
                recursive_merge(col_depth_idx + 1, i, run_end)
            else:
                worksheet.write(i, current_col, current_val, cell_fmt)
                # 即便单行，也可能需要递归处理子列
                recursive_merge(col_depth_idx + 1, i, i)
                
            i = run_end + 1

    # 3. 启动递归：覆盖整个数据范围
    max_row = len(df) + start_row - 1
    recursive_merge(0, start_row, max_row)

def set_excel_style(workbook, worksheet, df, config, sum_row_index=None):
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

    # 5. 根据配置进行列合并
    merge_cols = config.get('merge_cols', [])
    if merge_cols:
        # 获取在格式池中定义的带边框居中格式
        center_fmt = fmts['data']
        
        # 假设我们只处理第一列的合并
        # 注意：data_start_row 是 4，意味着数据从 Excel 第 5 行开始
        merge_hierarchical_cells(worksheet, df, merge_cols, start_row=4, cell_fmt=center_fmt)
