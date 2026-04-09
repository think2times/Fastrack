import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from styles import export_sheet_excel
from db_helper import init_client, call_procedure
from config import REPORTS, DB_CONFIG
from processors import standard_preprocess


def add_group_subtotals(df, config, subtotal_label_col='PARENT_SUBCOM_NAME'):
    """
    计算小计值并插入小计行，
    通过传入整个 config 字典，自动处理列名转换
    """
    col_map = config.get('columns_map', {})
    
    # 获取配置的分组列（可能是英文名也可能是中文名）
    target_group = config.get('group_by')
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
        new_rows.append(group)
        
        # 计算小计
        subtotal_series = group[sum_cols].sum()
        subtotal_row = {col: '' for col in df.columns}
        
        for col in sum_cols:
            subtotal_row[col] = subtotal_series[col]
        
        # 填充标识
        subtotal_row[group_col] = name
        subtotal_row[label_col] = "小计"
        
        # --- 针对 3-4 报表的特殊列重算 (使用映射后的中文名) ---
        if config.get('subtotal_hooks'):
            subtotal_row = config['subtotal_hooks'](subtotal_row)
            # subtotal_row['集团划账'] = subtotal_row.get('账单金额', 0) + subtotal_row.get('需划账违约金', 0)

        new_rows.append(pd.DataFrame([subtotal_row]))
    
    return pd.concat(new_rows, ignore_index=True)

def main(report_id, subcoms=None, bill_month=None):
    if subcoms is None:
        subcoms = ''
    
    if bill_month is None:
        # 获取上个月的年月，格式为 YYYY-MM
        last_month = datetime.now() - relativedelta(months=1)
        bill_month = last_month.strftime('%Y-%m')

        # 获取当前年月，格式为 YYYY-MM
        # bill_month = datetime.now().strftime('%Y-%m')

    # 连接数据库，使用本地驱动而不是内置的 Thin 驱动
    lib_dir = r'F:\app\pluto\product\instantclient_11_2'
    init_client(lib_dir)
    
    # 取数
    cfg = REPORTS[report_id]
    proc_params = cfg['params'](subcoms, bill_month)

    # 调用新的支持多数据源的函数，返回的是一个 list
    dfs = call_procedure(cfg['proc'], proc_params, DB_CONFIG)
    
    # 如果配置了 multi_source，则把整个列表 dfs 传给 calc_func 处理
    # 否则，默认取第一个游标作为主 df 传给后续逻辑
    if cfg.get('multi_source'):
        if 'calc_func' in cfg:
            # 多数据源模式：如果 3-13 这种已经在函数里处理了全流程，直接拿结果
            # 否则默认取第一个游标
            df = cfg['calc_func'](dfs) if 'calc_func' in cfg else (dfs[0] if dfs else pd.DataFrame())
    else:
        # 对于只有一个游标的存储过程：取第一个游标的数据
        df = dfs[0] if dfs else pd.DataFrame()

        # 执行通用预处理（计算 SIX_TOTAL, 大写转换等）
        df = standard_preprocess(df)

        # 执行报表特有的 calc_func（如计算 UNIT_PRICE）
        if 'calc_func' in cfg:
            df = cfg['calc_func'](df)
            
    # 准备展示列名单，首先获取配置中定义的中文列名顺序
    display_cols = list(cfg['columns_map'].values())
    # 重命名列名, rename 会把英文 Key 替换为中文 Value
    df = df.rename(columns=cfg['columns_map'])[display_cols]

    # 检查是否需要增加组内小计
    # 从字典获取配置
    sub_col = cfg.get('group_by', '')
    if sub_col and report_id != '3-13':  # 3-13 的小计逻辑比较特殊，已经在 calc_func 中处理了
        df = add_group_subtotals(df, cfg, sub_col)

    # 保存
    full_path = os.path.join(base_dir, cfg['folder'], cfg['file_name'])
    export_sheet_excel(df, cfg, full_path)
    print(f"{report_id}报表已生成！")

if __name__ == '__main__':
    # 定义基础目录
    base_dir = r'F:\NewSystem\Reports'

    # 如果文件夹不存在，则自动创建（避免报错）
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    for report_id in REPORTS.keys():
        # if report_id == '3-4':
        #     main(report_id)
        main(report_id)
