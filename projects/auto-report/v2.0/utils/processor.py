import numpy as np
import pandas as pd


def insert_subtotal_rows(df, group_col, sum_cols):
    """
    df: 原始数据
    group_col: 指定计算小计的列（如 '站点'）
    sum_cols: 需要累加的数值列
    """
    if group_col not in df.columns:
        return df

    cols = list(df.columns)
    group_idx = cols.index(group_col)
    new_rows = []

    for name, group in df.groupby(group_col, sort=False):
        # 1. 先加入明细数据
        new_rows.append(group)
        
        # 2. 计算小计（仅针对数值列）
        # 使用 Series 构造，方便后续对非数值列进行“清空”处理
        sub_series = pd.Series(index=cols, dtype=object)
        
        # 填充数值列
        for col in sum_cols:
            sub_series[col] = group[col].sum()
        
        # 填充分组列（保持分公司名称，以便后续的“银行”列能正确合并到这里）
        sub_series[group_col] = name
        
        # --- 核心：寻找右侧一列放置“小计” ---
        if group_idx + 1 < len(cols):
            target_col = cols[group_idx + 1]
            sub_series[target_col] = "小计"
            
        # 3. 兜底清洗：将其余列设为空字符串（防止出现 NaN 导致之前的写操作报错）
        sub_series = sub_series.fillna("")
        
        # 转为 DataFrame 并确保列顺序一致
        new_rows.append(pd.DataFrame([sub_series])[cols])
        
    return pd.concat(new_rows, ignore_index=True)

def insert_sum_row(df, sum_cols, sum_pos, proc_name, group_col):
    """根据配置在 DataFrame 中插入合计行"""
    df_with_sum = df
    if sum_pos != 'none' and sum_cols:
        # 先计算真正的总合计，但不放回明细 df 中
        sum_values = df[sum_cols].sum()

        # 构造一个独立的“合计” DataFrame（只有一行）
        sum_row = pd.Series(index=df.columns, dtype=object).fillna("") # 先创建一个空行

        for col in sum_cols:
            sum_row[col] = sum_values[col]
        sum_row[df.columns[0]] = '合计' # 第一列写上“合计”字样

        # 创建一个 DataFrame 来存储合计行，列名要和 df 一致
        sum_df = pd.DataFrame([sum_row], columns=df.columns)

        # 特例处理：对于 3-11 报表，合计行还需要计算单价（总费用 / 累计水量），注意除数不能为0
        if proc_name == 'RPT_WLMQ_311':
            sum_df['UNIT_PRICE'] = sum_df['FEE_TOTAL'] / sum_df['ACC_WATER'] if sum_df['ACC_WATER'].iloc[0] != 0 else 0

        # 只对原始明细数据 df 插入小计
        df_with_subtotals = insert_subtotal_rows(df, group_col, sum_cols)

        # 将合计行插入到第一行或最后一行，根据需求调整
        if sum_pos == 'top':
            df_with_sum = pd.concat([sum_df, df_with_subtotals], ignore_index=True)
            # 记录合计行所在的索引，方便样式函数加粗
            sum_row_index = 0
        else:
            df_with_sum = pd.concat([df_with_subtotals, sum_df], ignore_index=True)
            sum_row_index = len(df_with_sum) - 1
    else:
        sum_row_index = None # 没有合计行

    return df_with_sum, sum_row_index

def process_306_data(buffers, pi_cols):
    """
    3-6 报表的特殊处理逻辑
    buffers: dict of {cursor_idx: DataFrame}
    buffers[0] 是 RESULT_1 (日期范围)
    buffers[1] 是 RESULT_2 (应收数据)
    buffers[2] 是 RESULT_3 (实收数据)
    buffers[3] 是 RESULT_4 (调整数据)
    """
    # 1. 动态获取数据源，防止 engine 的 keys 偏移
    df_sj = buffers[0]
    df_ys = buffers[1].copy() if len(buffers) > 1 else pd.DataFrame()
    df_ss = buffers[2].copy() if len(buffers) > 2 else pd.DataFrame()
    df_tz = buffers[3].copy() if len(buffers) > 3 else pd.DataFrame()
    t = df_sj.iloc[0]

    # 预计算 Data Blocks
    def get_sums(df, cond, cols=pi_cols):
        if df.empty: return pd.Series(0.0, index=cols)
        return df.loc[cond, cols].sum() if cond is not None else df[cols].sum()

    # 实收与调整的过滤条件
    is_stat_curr = df_ss['STATISTIC_BILLING_MONTH'] == t['BILLING_MONTH'] if 'STATISTIC_BILLING_MONTH' in df_ss.columns else False
    is_bill_curr = df_ss['BILLING_MONTH'] == t['BILLING_MONTH'] if 'BILLING_MONTH' in df_ss.columns else False
    is_bill_year = df_ss['BILLING_MONTH'].between(t['START_BILLING_MONTH'], t['BILLING_MONTH']) if 'BILLING_MONTH' in df_ss.columns else False

    # 核心数据映射
    raw_data = {
        '本月应收': get_sums(df_ys, df_ys['BILLING_MONTH'] == t['BILLING_MONTH']),
        '本年应收': get_sums(df_ys, None),
        '本月实收当月': get_sums(df_ss, is_stat_curr & is_bill_curr),
        '本月实收当年': get_sums(df_ss, is_stat_curr & (~is_bill_curr) & is_bill_year),
        '本月实收往年': get_sums(df_ss, is_stat_curr & (df_ss['BILLING_MONTH'] < t['START_BILLING_MONTH'])),
        '本年实收当年': get_sums(df_ss, is_bill_year),
        '本年实收往年': get_sums(df_ss, df_ss['BILLING_MONTH'] < t['START_BILLING_MONTH']),
        '本月调整当年': get_sums(df_tz, (df_tz['FEE_TYPE'] == '本月调整当年各项费用') & (df_tz['STATISTIC_BILLING_MONTH'] == t['BILLING_MONTH'])),
        '本月调整往年': get_sums(df_tz, (df_tz['FEE_TYPE'] == '本月调整往年各项费用') & (df_tz['STATISTIC_BILLING_MONTH'] == t['BILLING_MONTH'])),
        '当月违约金': get_sums(df_ss, is_stat_curr, cols=['ACTUAL_LATEFEE']),
        '本年违约金': get_sums(df_ss, None, cols=['ACTUAL_LATEFEE']),
    }

    # 2. 派生指标计算
    # 统一计算公式，减少 build_row 里的负担
    data_map = {
        '本月应收各项费用': raw_data['本月应收'],
        '本月调整当年各项费用': raw_data['本月调整当年'],
        '本月调整往年各项费用': raw_data['本月调整往年'],
        '本月应收小计': raw_data['本月应收'] + raw_data['本月调整当年'] + raw_data['本月调整往年'],
        '本月收回当月各项费用': raw_data['本月实收当月'],
        '本月收回当年各项费用': raw_data['本月实收当年'],
        '本月收回往年各项费用': raw_data['本月实收往年'],
        '本月实收小计': raw_data['本月实收当月'] + raw_data['本月实收当年'] + raw_data['本月实收往年'],
        '当月违约金': raw_data['当月违约金'],
        '未收回的当月水费': (raw_data['本月应收'] + raw_data['本月调整当年'] + raw_data['本月调整往年']) - raw_data['本月实收当月'],
        '当月收回率 (%)': (raw_data['本月实收当月'] / raw_data['本月应收'].replace(0, np.nan) * 100).fillna(0).round(2),
        '本年应收小计': raw_data['本年应收'],
        '本年收回当年各项费用': raw_data['本年实收当年'],
        '本年收回往年各项费用': raw_data['本年实收往年'],
        '本年实收小计': raw_data['本年实收当年'] + raw_data['本年实收往年'],
        '本年违约金': raw_data['本年违约金'],
        '本年累计欠费': raw_data['本年应收'] - raw_data['本年实收当年'],
        '本年收回率 (%)': (raw_data['本年实收当年'] / raw_data['本年应收'].replace(0, np.nan) * 100).fillna(0).round(2),
    }

    # 3. 定义报表的物理行顺序
    TIME_TYPE = ['本月', '本年']
    FEE_TYPE = ['应收', '实收', '其他']
    report_structure = [
        (TIME_TYPE[0], FEE_TYPE[0], '本月应收各项费用'),
        (TIME_TYPE[0], FEE_TYPE[0], '本月调整当年各项费用'),
        (TIME_TYPE[0], FEE_TYPE[0], '本月调整往年各项费用'),
        (TIME_TYPE[0], FEE_TYPE[0], '本月应收小计'),
        (TIME_TYPE[0], FEE_TYPE[1], '本月收回当月各项费用'),
        (TIME_TYPE[0], FEE_TYPE[1], '本月收回当年各项费用'),
        (TIME_TYPE[0], FEE_TYPE[1], '本月收回往年各项费用'),
        (TIME_TYPE[0], FEE_TYPE[1], '本月实收小计'),
        (TIME_TYPE[0], FEE_TYPE[2], '当月违约金'),
        (TIME_TYPE[0], FEE_TYPE[2], '未收回的当月水费'),
        (TIME_TYPE[0], FEE_TYPE[2], '当月收回率 (%)'),
        (TIME_TYPE[1], FEE_TYPE[0], '本年应收小计'),
        (TIME_TYPE[1], FEE_TYPE[1], '本年收回当年各项费用'),
        (TIME_TYPE[1], FEE_TYPE[1], '本年收回往年各项费用'),
        (TIME_TYPE[1], FEE_TYPE[1], '本年实收小计'),
        (TIME_TYPE[1], FEE_TYPE[2], '本年违约金'),
        (TIME_TYPE[1], FEE_TYPE[2], '本年累计欠费'),
        (TIME_TYPE[1], FEE_TYPE[2], '本年收回率 (%)'),
    ]

    def build_row(c1, c2, item, data_map):
        # 1. 获取预计算好的 Series (PI1_MONEY 到 PI6_MONEY)
        data = data_map.get(item, pd.Series(0.0, index=pi_cols)).copy()

        # 2. 针对不同类型的行进行“内容重塑”
        # --- 情况 A: 违约金行 ---
        current_late_fee = 0
        if "违约金" in item:
            # 提取数值（标量）
            val = data_map.get('当月违约金' if "当月" in item else '本年违约金', 0)
            current_late_fee = float(val.sum() if hasattr(val, 'sum') else val)

            # 违约金行本身：清空六费，只在第一列显示违约金
            data = pd.Series(0.0, index=pi_cols)
            data['PI1_MONEY'] = current_late_fee

            # 对于违约金行，合计就等于它本身，不要再加一遍 data.sum()
            row_total = current_late_fee 
        else:
            # 普通行：合计 = 六费之和 + 该行关联的违约金(如果有)
            row_total = float(data.sum()) + current_late_fee
    
        # --- 情况 B: 收回率行 ---
        if '收回率' in item:
            # 计算该行各费种的收回率，已经在 data_map 里算好了
            # 我们只需要额外算一个“合计收回率”给 SIX_TOTAL 即可
            num = data_map['本月收回当月各项费用'] if '当月' in item else data_map['本年收回当年各项费用']
            den = data_map['本月应收小计'] if '当月' in item else data_map['本年应收小计']
            row_total_val = (num.sum() / den.sum() * 100) if den.sum() != 0 else 0

            return {
                'C1': c1, 'C2': c2, 'FEE_TYPE': item,
                **{k: f"{v:.2f}%" for k, v in data.to_dict().items()},
                'FEE_TOTAL': f"{row_total_val:.2f}%"
            }

        # --- 情况 C: 普通金额行 (如应收、实收、调整、欠费) ---
        return {
            'C1': c1, 'C2': c2, 'FEE_TYPE': item,
            **data.to_dict(),
            'FEE_TOTAL': row_total
        }

    return pd.DataFrame([build_row(*item, data_map) for item in report_structure])

def process_313_data(buffers, pi_cols):
    """
    3-13 报表的特殊处理逻辑
    buffers: dict of {cursor_idx: DataFrame}
    """
    # --- 1. 获取数据源 ---
    df_source = buffers[1].copy()

    if df_source.empty:
        return df_source

    # --- 2. 内部处理函数：重构块状结构 ---
    def reformat_group(group_df, pay_method_label):
        def get_item_sum(names):
            # 使用 isin 匹配列表，或者简单字符串匹配
            mask = group_df['FEE_ITEM'].isin([names] if isinstance(names, str) else names)
            # 返回一个 Series，索引是费用列名
            return group_df.loc[mask, pi_cols].sum()

        # A/B/C: 分别提取不同账期的费用项
        curr_month = get_item_sum('本月收回当月各项费用')
        curr_year = get_item_sum('本月收回当年各项费用')
        prev_years = get_item_sum('本月收回以前年度各项费用')
        
        # D. 违约金 (ACTUAL_LATEFEE)
        # 根据截图，违约金通常独立一行，或放在 PI1 这种位置，这里按你逻辑取总和
        latefee_total = group_df['ACTUAL_LATEFEE'].sum()

        # E. 小计：该收费方式下所有 PI 列的总和
        subtotal_series = group_df[pi_cols].sum()

        # 构建数据行
        res_data = [
            {'收费方式': pay_method_label, '费用项目': '本月收回当月各项费用', **curr_month.to_dict()},
            {'收费方式': pay_method_label, '费用项目': '本月收回当年各项费用', **curr_year.to_dict()},
            {'收费方式': pay_method_label, '费用项目': '本月收回以前年度各项费用', **prev_years.to_dict()},
            {'收费方式': pay_method_label, '费用项目': '小计', **subtotal_series.to_dict()},
            # 违约金行：通常只有一列有值，其他为0
            {'收费方式': pay_method_label, '费用项目': '违约金', 'PI1_MONEY': latefee_total} 
        ]
        
        block_df = pd.DataFrame(res_data)
        # 填充 NaN 为 0，防止拼接后出现空值
        return block_df.fillna(0)

    # --- 3. 循环分组并合并 ---
    all_blocks = []
    
    # A. 顶部的“汇总”块
    all_blocks.append(reformat_group(df_source, '汇总'))
    
    # B. 各明细块
    if 'PAY_METHOD' in df_source.columns:
        unique_methods = df_source['PAY_METHOD'].unique()
        for method in unique_methods:
            if pd.isna(method) or method == '': continue
            sub_df = df_source[df_source['PAY_METHOD'] == method]
            all_blocks.append(reformat_group(sub_df, method))

    # 合并
    final_df = pd.concat(all_blocks, ignore_index=True)
    
    # --- 4. 最后计算横向合计列 (应收费用总计) ---
    # 这一步必须在 concat 之后做，确保所有行都参与计算
    final_df['FEE_TOTAL'] = final_df[pi_cols].sum(axis=1)

    return final_df
