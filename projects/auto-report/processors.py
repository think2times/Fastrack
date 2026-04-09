import pandas as pd
import numpy as np


PI_COLS = ['PI1_MONEY', 'PI2_MONEY', 'PI3_MONEY', 'PI4_MONEY', 'PI5_MONEY', 'PI6_MONEY']

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
        df['SIX_TOTAL'] = df[existing_pi_cols].fillna(0).sum(axis=1)
    
    # 3. 统一精度控制
    return df.round(2)

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
                'SIX_TOTAL': f"{row_total + current_late_fee:.2f}%" # 合计包含违约金
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
