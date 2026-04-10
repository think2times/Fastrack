import pandas as pd
import numpy as np
import re


PI_COLS = ['PI1_MONEY', 'PI2_MONEY', 'PI3_MONEY', 'PI4_MONEY', 'PI5_MONEY', 'PI6_MONEY']

def clean_illegal_chars(val):
    if isinstance(val, str):
        # 匹配所有 Excel 不支持的控制字符
        # \x00-\x08, \x0b-\x0c, \x0e-\x1f
        ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
        return ILLEGAL_CHARACTERS_RE.sub("", val)
    return val

def standard_preprocess(df):
    """
    通用预处理：大写列名、计算六费合计、四舍五入
    """
    if df.empty:
        return df
        
    # 1. 统一大写列名，防止 SQL 字段大小写不一致
    df.columns = [c.upper() for c in df.columns]
    
    # 2. 自动识别 PI_COLS 并计算 SIX_TOTAL
    # 只有当 DataFrame 中包含这些列时才计算，避免报错
    existing_pi_cols = [c for c in PI_COLS if c in df.columns]
    if len(existing_pi_cols) == 6:
        # 识别哪些行是纯数值行（排除掉收回率这种带 % 的字符串行）
        # 我们只对 PI1_MONEY 这一列是数值类型的行进行计算
        is_numeric_row = pd.to_numeric(df[existing_pi_cols[0]], errors='coerce').notnull()
        
        # 只有数值行才计算 SIX_TOTAL，其他行（如收回率行）保持原样或设为 0
        df.loc[is_numeric_row, 'SIX_TOTAL'] = df.loc[is_numeric_row, existing_pi_cols].fillna(0).sum(axis=1)
    
    # 3. 只对数值型列（整数、浮点数）进行四舍五入
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].round(2)

    return df

def get_structure_weight(row, group_col):
    """计算行的结构权重：明细行=1，小计行=2，合计行=0（绝对置顶）"""
    val_first = str(row.get(group_col, ""))
    # 探测第二列是否有“小计”字样
    val_second = str(row.iloc[1]) if len(row) > 1 else ""
    
    if "合计" in val_first:
        return 0  # 绝对置顶
    if "小计" in val_first or "小计" in val_second:
        return 2  # 组内沉底
    return 1      # 普通明细保持中间

def apply_structural_sort(df, cfg):
    """根据 group_col 进行结构化排序，确保银行分组不散，小计行沉底，合计行置顶"""
    sub_col = cfg.get('group_by')
    if not (sub_col and sub_col in df.columns):
        return df
        
    df = df.copy()
    # 1. 记录当前的原始物理顺序（这是最关键的一步）
    df['_original_order'] = range(len(df))

    # 2. 计算结构权重，明细行=1，小计行=2，合计行=0（绝对置顶）
    df['_sort_weight'] = df.apply(lambda r: get_structure_weight(r, sub_col), axis=1)

    # 3. 核心排序逻辑：
    # 注意：合计行因为 _sort_weight 为 0，会无视银行名排在最前（只要 sub_col 那里也是“合计”）
    # 如果你想确保“合计”二字不参与银行名排序，可以参考之前的 _tmp_group 做法
    df['_tmp_group'] = df[sub_col].apply(lambda x: "" if x == "合计" else x)
    
    # 第一优先级：HEADOFFICE_NAME (保证银行分组不散)
    # 第二优先级：_sort_weight (保证 组内明细 -> 组内小计)
    # 第三优先级：_original_order (关键！确保明细行按原本的物理顺序排列)
    sort_keys = ['_tmp_group', '_sort_weight', '_original_order']
    df = df.sort_values(by=sort_keys, ascending=True, kind='stable')
    
    # 4. 清理所有临时辅助列
    return df.drop(columns=['_original_order', '_sort_weight', '_tmp_group'])

def add_group_subtotals(df, config):
    """
    计算小计值并插入小计行，
    通过传入整个 config 字典，自动处理列名转换
    """
    # 健壮性检查：如果进来的不是 DataFrame 而是 dict，说明调用时机错了
    if isinstance(df, dict):
        # 这种情况下可以报错提示，或者遍历处理
        raise TypeError("add_group_subtotals 接收到了字典，请检查是否在 rename 后调用了它")
    
    col_map = config.get('columns_map', {})
    
    # 获取配置的分组列（可能是英文名也可能是中文名）
    target_group = config.get('group_by')

    # 确定分组列
    group_col = target_group if target_group in df.columns else col_map.get(target_group, target_group)

    # 新逻辑：优先保留在 df 中能找到的列名
    raw_sum_cols = config.get('sum_cols', [])
    sum_cols = []
    for c in raw_sum_cols:
        if c in df.columns:
            sum_cols.append(c) # 英文列名存在，用英文
        else:
            mapped_c = col_map.get(c, c)
            if mapped_c in df.columns:
                sum_cols.append(mapped_c) # 中文列名存在，用中文

    new_rows = []
    for name, group in df.groupby(group_col, sort=False):
        new_rows.append(group)
        
        # 计算小计
        subtotal_series = group[sum_cols].sum()
        subtotal_row = {col: '' for col in df.columns}
        for col in sum_cols:
            subtotal_row[col] = subtotal_series[col]
        
        # 填充标识
        subtotal_row[group_col] = name

        # 寻找放置“小计”二字的位置，默认放在 group_col 的右边一列
        # 找到 group_col 的下一列名
        cols = list(df.columns)
        idx = cols.index(group_col)
        if idx + 1 < len(cols):
            subtotal_row[cols[idx+1]] = "小计"

        # 将小计行转为 DataFrame 并追加，确保它紧跟在明细后面
        new_rows.append(pd.DataFrame([subtotal_row]))

        # --- 针对 3-4 报表的特殊列重算 (使用映射后的中文名) ---
        if config.get('subtotal_hooks'):
            subtotal_row = config['subtotal_hooks'](subtotal_row)
    
    return pd.concat(new_rows, ignore_index=True)

def add_summary(df, cfg, sum_cols=None):
    """
    添加合计
    report_df: 处理完后的 DataFrame
    cfg: 当前报表的字典配置
    sum_cols: 需要求和的列名列表
    """
    # 如果没传 sum_cols，就自动从 cfg 里拿
    sum_cols = sum_cols or cfg.get('sum_cols', [])

    # 如果报表的字典没有配置 sum_cols，也没有传入 sum_cols 参数，就直接返回原 df，不添加合计行
    if not sum_cols:
        return df

    # 3-6、3-13 这两个报表的特殊逻辑：不添加合计行，直接返回
    if cfg.get('proc') in ['RPT_WLMQ_306', 'RPT_WLMQ_313'] or df.empty:
        return df

    # 准备数据
    report_df = df.copy()
    summary_row = {}

    # 排除所有包含“小计”的行
    exclude_pattern = '小计'
    # 动态获取分组列
    group_col = cfg.get('group_by')
    # 检查是否需要进行合计，默认全表都是明细，不做任何排除
    mask = pd.Series(True, index=df.index)

    if group_col and group_col in df.columns:
        # 找到分组列的位置索引
        idx = list(df.columns).index(group_col)
        # 确定需要检查的范围：分组列和它右边那一列
        check_cols = [group_col]
        if idx + 1 < len(df.columns):
            check_cols.append(df.columns[idx + 1])
        # 向量化检查“小计”
        mask = ~df[check_cols].astype(str).stack().str.contains(exclude_pattern).unstack().any(axis=1)

    # 根据过滤后的 mask 来计算 sum_cols 的合计值，确保只对明细行进行求和，排除掉小计行
    real_sum_cols = [col for col in sum_cols if col in report_df.columns]
    summary_series = df.loc[mask, real_sum_cols].sum()
    summary_row = {col: summary_series.get(col, 0) for col in real_sum_cols}

    # 确定合计行的标签列（优先级：group_col -> columns_map 的第一个 Key）
    label_col = group_col if group_col in df.columns else list(cfg.get('columns_map', {}).keys())[0]
    summary_row[label_col] = '合计'

    # 特殊逻辑：合计行单价重算 (针对 3-11)
    # 以后新增 3-12, 3-13 报表只要有“单价”列就能自动处理
    if '单价' in summary_row and '六费合计' in summary_row:
        total_money = summary_row.get('六费合计', 0)
        total_water = summary_row.get('水量', 0)
        # 防止除以 0
        summary_row['单价'] = round(total_money / total_water, 2) if total_water != 0 else 0

    # 使用 report_df 的列名构造，并同步数据类型以消除警告
    summary_df = pd.DataFrame([summary_row], columns=report_df.columns)

    # 准备待合并列表
    # 根据是否配置 sum_first 决定合计行放在最前（sum_first）还是最后
    to_concat = [summary_df, report_df] if cfg.get('sum_first') else [report_df, summary_df]

    # 核心过滤逻辑：只保留非空的 DataFrame
    valid_dfs = [d for d in to_concat if d is not None and not d.empty]

    if valid_dfs:
        report_df = pd.concat(valid_dfs, ignore_index=True)

    return report_df

def prepare_multi_cursor_report(dfs, cfg):
    """
    处理多游标返回的 DataFrame 列表
    dfs: [df_detail, df_summary, ...]
    """
    # --- 第一步：前置清洗 (Pre-cleaning) ---
    # 在合并或组装之前，先把所有原始游标里的数字列该大写的写，该算的算
    # 此时 dfs 里的数据全是刚从数据库出来的数字，计算 SIX_TOTAL 极其安全
    dfs = [standard_preprocess(d) for d in (dfs if isinstance(dfs, list) else [dfs])]

    # --- 第二步：组装与计算 (Assembly & Calculation) ---    
    report_package = {}
    # 标记是否已经在 calc_func 里处理过了
    has_processed = False 
    # 既然是多数据源，就把选择权交给 calc_func，多数据源一定会有特殊逻辑需要处理
    if cfg.get('multi_source') and 'calc_func' in cfg:
        # 已经把游标处理、合并、计算全部做完了
        df = cfg['calc_func'](dfs)
        # 标记一下，防止后面重复跑 calc_func
        has_processed = True
    else:
        # 标准模式：只取第一个游标
        df = dfs[0] if dfs else pd.DataFrame()# 假设第一个游标是核心明细数据

    # --- 第三步：后续处理 (Post-processing) ---
    # 检查是否需要增加组内小计
    if cfg.get('group_by') and cfg.get('proc') != 'RPT_WLMQ_313':  # 3-13 的小计逻辑比较特殊，已经在 calc_func 中处理了
        df = add_group_subtotals(df, cfg)

    # 计算全表合计
    all_df = add_summary(df, cfg)

    # 处理各报表的特殊逻辑
    if cfg.get('calc_func') and not has_processed:
        all_df = cfg['calc_func'](all_df)
    
    # --- 第四步：排序与翻译（Sort & Rename） ---
    # 针对需要分组的报表，进行结构化排序，确保一级分组中顺序不变，小计行沉底，合计行置顶
    all_df = apply_structural_sort(all_df, cfg)

    # 准备展示列名单，首先获取配置中定义的中文列名顺序
    display_cols = list(cfg['columns_map'].values())
    # 重命名列名, rename 会把英文 Key 替换为中文 Value
    report_package["全部"] = all_df.rename(columns=cfg['columns_map'])[display_cols]

    # 处理分公司拆分 (逻辑复用):
    split_col = cfg.get('split_by')
    if split_col and split_col in df.columns:
        groups = df.groupby(split_col)
        for name, group_df in groups:
            sheet_name = str(name)[:12]
            # 计算每个sheet的全表合计
            tmp_df = add_summary(group_df, cfg)
            if 'calc_func' in cfg:
                tmp_df = cfg['calc_func'](tmp_df)
            
            report_package[sheet_name] = tmp_df.rename(columns=cfg['columns_map'])[display_cols]

    return report_package

# 处理特殊逻辑
def process_306_data(dfs):
    """
    dfs[0] 是 RESULT_1 (日期范围)
    dfs[1] 是 RESULT_2 (应收数据)
    dfs[2] 是 RESULT_3 (实收数据)
    dfs[3] 是 RESULT_4 (调整数据)
    """

    # 提取与费用相关的游标数据
    df_sj, df_ys, df_ss, df_tz = dfs[0], dfs[1], dfs[2], dfs[3]
    t = df_sj.iloc[0] # bill_month, start_month 等等信息都在这里

    # 数据清洗：统一转大写，处理空值
    for d in [df_ys, df_ss, df_tz]:
        d.columns = [c.upper() for c in d.columns]
    
    # 预计算所有基础维度的数据块 (Data Blocks)
    def get_sums(df, cond, cols=PI_COLS):
        return df.loc[cond, cols].sum() if cond is not None else df[cols].sum()
    
    # 实收条件定义
    is_stat_curr = df_ss['STATISTIC_BILLING_MONTH'] == t['BILLING_MONTH']
    is_bill_curr = df_ss['BILLING_MONTH'] == t['BILLING_MONTH']
    is_bill_year = df_ss['BILLING_MONTH'].between(t['START_BILLING_MONTH'], t['END_BILLING_MONTH'])

    # 核心数据字典
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

    # 2. 派生指标计算 (Derived Metrics)
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
        '本年收回率 (%)': (raw_data['本年实收当年'] / raw_data['本年应收'].replace(0, np.nan) * 100).fillna(0).round(2)
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
        data = data_map.get(item, pd.Series(0.0, index=PI_COLS)).copy()

        # 2. 针对不同类型的行进行“内容重塑”
        # --- 情况 A: 违约金行 ---
        current_late_fee = 0
        if "违约金" in item:
            # 提取数值（标量）
            val = data_map.get('当月违约金' if "当月" in item else '本年违约金', 0)
            current_late_fee = float(val.sum() if hasattr(val, 'sum') else val)

            # 违约金行本身：清空六费，只在第一列显示违约金
            data = pd.Series(0.0, index=PI_COLS)
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
                'ACTUAL_LATEFEE': "", 
                'SIX_TOTAL': f"{row_total_val:.2f}%"
            }
        
        # --- 情况 C: 普通金额行 (如应收、实收、调整、欠费) ---
        return {
            'C1': c1, 'C2': c2, 'FEE_TYPE': item,
            **data.to_dict(),
            'ACTUAL_LATEFEE': current_late_fee,
            'SIX_TOTAL': row_total
        }

    return pd.DataFrame([build_row(*item, data_map) for item in report_structure])

def process_313_data(dfs):
    """
    dfs[0] 是 RESULT_1 (日期范围)
    dfs[1] 是 RESULT_2 (明细)
    """

    # 指定第二个游标作为数据源
    df_main = dfs[1].copy()  # 复制一份，避免修改原数据
    if df_main.empty:
        return df_main

    # 强制转大写，防止大小写坑
    df_main.columns = [c.upper() for c in df_main.columns]
    
    # 定义内部处理函数：处理每一个收费方式（如：预收、银行）
    def reformat_group(group_df, pay_method):
        rows = []
        
        # 1. 提取业务行（假设存储过程中 FEE_ITEM 已经区分了类别）
        # 如果 FEE_ITEM 包含你提到的：当月、当年未报、以前年度等，需要在这里做加总
        
        # 模拟业务逻辑：将组内数据按 FEE_ITEM 分类汇总
        def get_sum(item_name_list):
            mask = group_df['FEE_ITEM'].isin(item_name_list)
            return group_df.loc[mask, PI_COLS + ['ACTUAL_LATEFEE']].sum()

        # --- 构造目标行的每一项 ---
        # A. 本月收回当月各项费用
        curr_month = get_sum(['本月收回当月各项费用']) 
        
        # B. 本月收回以前年度各项费用 (对应你公式中的历史部分)
        prev_years = get_sum(['本月收回以前年度各项费用'])
        
        # C. 违约金行 (提取该组下的违约金总额)
        latefee_total = group_df['ACTUAL_LATEFEE'].sum()

        # D. 计算小计行 (核心逻辑：对应图一公式)
        # 小计 = 当月 + 当年各项 + 当年未报 - 当年已报 + 以前年度 + 不划账 
        # 假设 group_df 已经通过 SQL 的逻辑包含了这些所有行，直接全选 sum 即可
        subtotal = group_df[PI_COLS].sum() 

        # --- 组装成新行 ---
        res_data = [
            {'收费方式': pay_method, '费用项目': '本月收回当月各项费用', **curr_month},
            {'收费方式': pay_method, '费用项目': '本月收回以前年度各项费用', **prev_years},
            {'收费方式': pay_method, '费用项目': '小计', **subtotal, 'SIX_TOTAL': subtotal.sum()},
            {'收费方式': pay_method, '费用项目': '违约金', 'PI1_MONEY': latefee_total, 'SIX_TOTAL': latefee_total}
        ]
        return pd.DataFrame(res_data)

    # 2. 按收费方式分组循环处理
    all_groups = []
    
    # 首先处理“汇总”块（即所有数据的总和）
    total_block = reformat_group(df_main, '汇总')
    all_groups.append(total_block)
    
    # 接着处理各个明细收费方式
    unique_methods = df_main['PAY_METHOD'].unique()
    for method in unique_methods:
        all_groups.append(reformat_group(df_main[df_main['PAY_METHOD'] == method], method))

    # 合并所有块
    final_df = pd.concat(all_groups, ignore_index=True)
    
    # 补齐应收费用（SIX_TOTAL）计算列
    final_df['SIX_TOTAL'] = final_df[PI_COLS].sum(axis=1)
    
    return final_df

def process_314_data(dfs):
    """
    dfs[0] 是 RESULT_1 (明细)
    dfs[1] 是 RESULT_2 (日期范围)
    """
    # 指定第1个游标作为数据源
    df_main = dfs[0]
    
    # 计算应收合计和集团划账
    df_main = df_main.assign(
        # 应收费用 = PI1到PI6的累加
        SIX_TOTAL = lambda x: x[PI_COLS].fillna(0).sum(axis=1)
    ).assign(
        # 集团划账 = 六费合计 + 违约金 - 账户支出 + 账户存入 + 纯账户预存/支出
        TOTAL_TRANSFER = lambda x: (
            x['SIX_TOTAL'] + 
            x['ACTUAL_LATEFEE'].fillna(0) - 
            x['PT_PRESTORE_OUT_MONEY'].fillna(0) + 
            x['PT_PRESTORE_IN_MONEY'].fillna(0) + 
            x['RATE'].fillna(0)
        )
    ).round(2)
    
    return df_main # 最终返回给导出模块的 DataFrame
