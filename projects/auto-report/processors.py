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

def add_group_subtotals(df, config, subtotal_label_col='PARENT_SUBCOM_NAME'):
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
    
    # label_col 是放置“小计”二字的列，也需要确保存在
    if subtotal_label_col in df.columns:
        label_col = subtotal_label_col
    else:
        label_col = col_map.get(subtotal_label_col, subtotal_label_col)

    new_rows = []
    for name, group in df.groupby(group_col, sort=False):
        # 1. 明细行权重设为 0
        group = group.copy()
        group['SORT_WEIGHT'] = 0
        new_rows.append(group)
        
        # 2. 计算小计
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
        subtotal_row['SORT_WEIGHT'] = 1  # 小计行权重设为 1，确保它在 0 之后
        new_rows.append(pd.DataFrame([subtotal_row]))

        # --- 针对 3-4 报表的特殊列重算 (使用映射后的中文名) ---
        if config.get('subtotal_hooks'):
            subtotal_row = config['subtotal_hooks'](subtotal_row)
    
    # 合并后强制按 [分组列, 权重] 排序
    df_result = pd.concat(new_rows, ignore_index=True)
    df_result = df_result.sort_values(by=[group_col, 'SORT_WEIGHT'], kind='stable')
    
    # 删掉辅助列，防止出现在 Excel 里
    return df_result.drop(columns=['SORT_WEIGHT'])

def add_summary(df, cfg, sum_cols=None):
    """
    添加合计
    report_df: 处理完后的 DataFrame
    cfg: 当前报表的字典配置
    sum_cols: 需要求和的列名列表
    """

    if cfg.get('proc') in ['RPT_WLMQ_306', 'RPT_WLMQ_313']:
        return df

    # 准备数据
    report_df = df.copy()

    # 如果没传 sum_cols，就自动从 cfg 里拿
    if sum_cols is None:
        sum_cols = cfg.get('sum_cols', [])

    if cfg.get('sum_cols'):
        summary_row = {}

        # 动态获取分组列（用于排除小计）
        group_col_raw = cfg.get('group_by')

        # 排除所有包含“小计”的行
        if not group_col_raw:
            # 情况 1：如果没有配置 group_by，说明全表都是明细，不做任何排除
            mask = [True] * len(report_df)
        elif group_col_raw not in report_df.columns:
            # 情况 2：配置了 group_by 但在当前 DataFrame 中找不到（可能是列名还没 rename）
            # 尝试检查一下 col_map，看是否能对上中文名
            col_map = cfg.get('columns_map', {})
            mapped_col = col_map.get(group_col_raw)

            if mapped_col in report_df.columns:
                mask = ~report_df[mapped_col].astype(str).str.contains('小计', na=False)
            else:
                # 实在找不到了，保底不排除
                mask = [True] * len(report_df)
        else:
            # 情况 3：正常找到了 group_by 列
            mask = ~report_df[group_col_raw].astype(str).str.contains('小计', na=False)

        for col in sum_cols:
            if col in report_df.columns:
                # 只有在明细行中进行 sum
                summary_row[col] = report_df.loc[mask, col].sum()

        if group_col_raw and group_col_raw in df.columns:
            # 使用英文 ID 赋值
            summary_row[group_col_raw] = '合计'
        else:
            # 保底逻辑：如果没设 group_by，就填在第一列
            first_col = df.columns[0]
            summary_row[first_col] = '合计'

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
    if isinstance(dfs, list):
        # 此时 dfs 里的数据全是刚从数据库出来的数字，计算 SIX_TOTAL 极其安全
        dfs = [standard_preprocess(d) for d in dfs]
    else:
        dfs = standard_preprocess(dfs)

    # --- 第二步：组装与计算 (Assembly & Calculation) ---    
    report_package = {}

    # 标记是否已经在 calc_func 里处理过了
    has_processed = False 
    if cfg.get('multi_source'):
        # 既然是多数据源，就把选择权交给 calc_func
        if 'calc_func' in cfg:
            # 已经把游标处理、合并、计算全部做完了
            df = cfg['calc_func'](dfs)
            # 标记一下，防止后面重复跑 calc_func
            has_processed = True
        else:
            # 如果没写函数，默认保底取第一个，防止程序崩溃
            df = dfs[0] if dfs else pd.DataFrame()
    else:
        # 标准模式：只取第一个游标
        df = dfs[0] if dfs else pd.DataFrame()# 假设第一个游标是核心明细数据

    # --- 第三步：后续处理 (Post-processing) ---
    # 检查是否需要增加组内小计
    # 从字典获取配置
    sub_col = cfg.get('group_by', '')
    if sub_col and cfg.get('proc') != 'RPT_WLMQ_313':  # 3-13 的小计逻辑比较特殊，已经在 calc_func 中处理了
        df = add_group_subtotals(df, cfg, sub_col)

    # --- 计算全表合计 ---
    all_df = add_summary(df, cfg)

    # --- 处理各报表的特殊逻辑 ---
    if cfg.get('calc_func') and not has_processed:
        all_df = cfg['calc_func'](all_df)
    
    # --- 第四步：翻译与装箱 (Renaming) ---
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
            # 同样：先加合计 -> 再算单价 -> 最后改名
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
    df_sj = dfs[0].copy()  # 日期范围，可能用来区分本月/本年
    df_ys = dfs[1].copy()
    df_ss = dfs[2].copy()
    df_tz = dfs[3].copy()

    # 1. 数据清洗：统一转大写，处理空值
    for d in [df_ys, df_ss, df_tz]:
        d.columns = [c.upper() for c in d.columns]
    
    # 2. 建立标签索引 (核心：利用 SQL 已有的 FEE_TYPE 标签)
    # 将所有数据汇总到一个以 FEE_TYPE 为 Key 的字典中
    data_map = {}

    # 获取账期
    bill_month = df_sj['BILLING_MONTH'].iloc[0]
    start_month = df_sj['START_BILLING_MONTH'].iloc[0]
    end_month = df_sj['END_BILLING_MONTH'].iloc[0]

    # 基础条件定义 (将判断逻辑抽离，更直观) 
    # 针对统计月 (Statistic)
    is_stat_curr = df_ss['STATISTIC_BILLING_MONTH'] == bill_month
    
    # 针对账务月 (Billing)
    is_bill_curr = df_ss['BILLING_MONTH'] == bill_month
    is_bill_not_curr = df_ss['BILLING_MONTH'] != bill_month
    is_bill_in_year = df_ss['BILLING_MONTH'].between(start_month, end_month)
    is_bill_before_year = df_ss['BILLING_MONTH'] < start_month

    # 处理实收 (result_3) 
    # 本月收回当月：统计是本月 且 账期是本月
    data_map['本月收回当月各项费用'] = df_ss.loc[is_stat_curr & is_bill_curr, PI_COLS].sum()
    
    # 本月收回当年：统计是本月 且 账期不是本月 且 账期在财年内
    data_map['本月收回当年各项费用'] = df_ss.loc[is_stat_curr & is_bill_not_curr & is_bill_in_year, PI_COLS].sum()
    
    # 本月收回往年：统计是本月 且 账期在财年之前
    data_map['本月收回往年各项费用'] = df_ss.loc[is_stat_curr & is_bill_before_year, PI_COLS].sum()
    
    # 本年收回当年：账期在财年内 (不限统计月，即累计)
    data_map['本年收回当年各项费用'] = df_ss.loc[is_bill_in_year, PI_COLS].sum()
    
    # 本年收回往年：账期在财年之前 (不限统计月，即累计)
    data_map['本年收回往年各项费用'] = df_ss.loc[is_bill_before_year, PI_COLS].sum()

    # 处理应收与调整
    # 应收部分
    data_map['本月应收各项费用'] = df_ys.loc[df_ys['BILLING_MONTH'] == bill_month, PI_COLS].sum()
    data_map['本年应收小计'] = df_ys[PI_COLS].sum()

    # 调整部分 (SQL 已打标签)
    data_map['本月调整当年各项费用'] = df_tz.loc[(df_tz['FEE_TYPE'] == '本月调整当年各项费用') & (df_tz['STATISTIC_BILLING_MONTH'] == bill_month), PI_COLS].sum()
    data_map['本月调整往年各项费用'] = df_tz.loc[(df_tz['FEE_TYPE'] == '本月调整往年各项费用') & (df_tz['STATISTIC_BILLING_MONTH'] == bill_month), PI_COLS].sum()

    # 处理小计数据
    data_map['本月应收小计'] = data_map['本月应收各项费用'] + data_map['本月调整当年各项费用'] + data_map['本月调整往年各项费用']
    data_map['本月实收小计'] = data_map['本月收回当月各项费用'] + data_map['本月收回当年各项费用'] + data_map['本月收回往年各项费用']
    data_map['本年实收小计'] = data_map['本年收回当年各项费用'] + data_map['本年收回往年各项费用']

    # 违约金计算
    data_map['当月违约金'] = df_ss.loc[is_stat_curr, 'ACTUAL_LATEFEE'].sum()
    data_map['本年违约金'] = df_ss['ACTUAL_LATEFEE'].sum()

    # 计算欠费
    data_map['未收回的当月水费'] = data_map['本月应收小计'] - data_map['本月收回当月各项费用']
    data_map['本年累计欠费'] = data_map['本年应收小计'] - data_map['本年收回当年各项费用']

    # 计算当月收回率
    # 逻辑：实收 / 应收，处理分母为 0 的情况
    data_map['当月收回率 (%)'] = (
        data_map['本月收回当月各项费用'] / 
        data_map['本月应收小计'].replace(0, np.nan) * 100
    ).fillna(0).round(2)

    # 计算本年收回率
    data_map['本年收回率 (%)'] = (
        data_map['本年收回当年各项费用'] / 
        data_map['本年应收小计'].replace(0, np.nan) * 100
    ).fillna(0).round(2)

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

    rows = []
    for c1, c2, item_name in report_structure:
        data = data_map.get(item_name, pd.Series(0, index=PI_COLS))

        # 检查 data 是否为纯数字 (float 或 int)
        if isinstance(data, (float, int, np.float64, np.int64)):
            # 如果是纯数字（如收回率或违约金），将其转换为 Series
            # 假设我们将这个数字放在第一列（纯水费），其他列补 0
            temp_val = data
            # 创建 Series 时直接指定 np.dtype，省去后续把float类型的数据写入int64列的警告
            data = pd.Series(0.0, index=PI_COLS, dtype=float)

            # 业务逻辑判断：如果是违约金，通常放第一列；如果是收回率，通常全行显示一样或只显合计
            if '率' in item_name:
                data[:] = temp_val # 收回率整行填充
            else:
                data['PI1_MONEY'] = temp_val # 违约金等只放第一列

        # --- 违约金处理逻辑 ---
        current_late_fee = 0
    
        if item_name == "违约金":
            # 如果是应收相关的行，取应收违约金（或者根据财务要求不显示）
            current_late_fee = data_map.get('当月违约金', 0) if "当月" in item_name else data_map.get('本年违约金', 0)
        # --------------------

        # 默认合计是 6 费之和
        row_total = data.sum()
    
        # --- 特殊处理收回率行 ---
        if '收回率' in item_name:
            # 1. 此时 data 已经是上面算好的比例 Series (PI1_MONEY 到 PI6_MONEY)
            # 2. 我们需要覆盖掉 row_total，改用刚才算的“合计收回率”
            if '当月' in item_name:
                row_total = (data_map['本月收回当月各项费用'].sum() / data_map['本月应收小计'].sum() * 100).round(2) if data_map['本月应收小计'].sum() != 0 else 0
            else:
                row_total = (data_map['本年收回当年各项费用'].sum() / data_map['本年应收小计'].sum() * 100).round(2) if data_map['本年应收小计'].sum() != 0 else 0

        if '收回率' in item_name:
            # 确保 data 是计算好的标量或 Series，然后转字符串并加 %
            # 注意：如果加了 %，该单元格在 Excel 里会变成“文本”格式
            row = {
                'C1': c1, 
                'C2': c2, 
                'FEE_TYPE': item_name, 
                **{k: f"{v:.2f}%" for k, v in data.to_dict().items()},
                'ACTUAL_LATEFEE': "", # 费率行违约金通常为空
                'SIX_TOTAL': f"{row_total:.2f}%"
                }
        else:
            row = {
                'C1': c1, 
                'C2': c2, 
                'FEE_TYPE': item_name, 
                **data.to_dict(), 
                'ACTUAL_LATEFEE': current_late_fee, # 映射到 columns_map 里的“违约金”
                'SIX_TOTAL': row_total + current_late_fee # 合计包含违约金
            }
        rows.append(row)

    return pd.DataFrame(rows)

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
