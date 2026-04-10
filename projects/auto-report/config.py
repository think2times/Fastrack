import numpy as np
from datetime import datetime
from processors import process_306_data, process_313_data, process_314_data


# 1. 数据库配置
DB_CONFIG = {
    'user': 'CSM_BM_REPORT',
    'password': 'JT2mlDMaYXR7oHz',
    'dsn': '172.16.16.11:1521/CSM_BM'
}

# 2. 定义所有报表的元数据
year_month = f"{datetime.now().strftime('%Y年%m月')}"
# 明确要累加的 6 个费用项
PI_COLS = ['PI1_MONEY', 'PI2_MONEY', 'PI3_MONEY', 'PI4_MONEY', 'PI5_MONEY', 'PI6_MONEY']

# 全局标准映射
BASE_FEE_MAP = {
    'PI1_MONEY': '纯水费',
    'PI4_MONEY': '水资源税',
    'PI5_MONEY': '水利投资费',
    'PI6_MONEY': '管网维护费',
    'PI2_MONEY': '污水处理费',
    'PI3_MONEY': '垃圾处理费'
}

# 自动推导需要合计的六费列名
SIX_FEE_COLS = list(BASE_FEE_MAP.keys())

REPORTS = {
    '2-8': {
        'proc': 'RPT_WLMQ_208',
        'title': '抄表统册用水信息',
        'folder': '【应】抄表水量表（2-8号）（1）',
        'file_name': f"{year_month}抄表水量.xlsx",
        'columns_map': {
            'ROW_INDEX': '序号',
            'BOOK_ID': '统册编号',
            'BOOK_NAME': '统册名称',
            'TOTAL_COUNT': '应抄户数',
            'READ_COUNT': '实抄户数',
            'BILLING_MONTH': '抄表时间',
            'READ_WATER': '抄见水量',
            'ACC_WATER': '开账水量',
            'ADJUST_WATER': '减免水量',
            'ACTUAL_WATER': '实际水量',
            'METER_READER': '抄表员'
        },
        'sum_cols': ['TOTAL_COUNT', 'READ_COUNT', 'READ_WATER', 'ACC_WATER', 'ADJUST_WATER', 'ACTUAL_WATER'],
        'sum_first': True,
        'calc_func': lambda df: df.assign(
            # 使用 fillna(0) 防止 ACC_WATER 或 ADJUST_WATER 为空时计算出 NaN
            ACTUAL_WATER = lambda x: x['ACC_WATER'].fillna(0) - x['ADJUST_WATER'].fillna(0)
        ).round(2),
        # 定义该存储过程需要的参数“值”列表（不含最后的游标）
        'params': lambda sub, month: [sub, month, month, '']
    },
    '3-10': {
        'proc': 'RPT_WLMQ_310',
        'title': f"{year_month}应收报表(按费用项目)",
        'folder': '【应】费用项目汇总（3-10号）（1）',
        'file_name': f"{year_month}应收报表（按费用项目）.xlsx",
        'columns_map': {
            'FEE_TYPE': '业务类型',
            'ACC_COUNT': '户数',
            'ACC_WATER': '售水量',
            **BASE_FEE_MAP, # 自动展开六费映射
            'ACC_MONEY': '六费合计'
        },
        'sum_cols': ['ACC_COUNT', 'ACC_WATER', 'ACC_MONEY'] + SIX_FEE_COLS,
        'params': lambda sub, month: [sub, month]
    },
    '3-7': {
        'proc': 'RPT_WLMQ_307',
        'title': f"售水量汇总报表",
        'folder': '【应】水量报表（3-7号）（1）',
        'file_name': f"{year_month}水量报表.xlsx",
        'columns_map': {
            'PARENT_SUBCOM_NAME': "分公司",
            'SUBCOM_NAME': "站点",
            'ACC_WATER': '售水量',
            **BASE_FEE_MAP,
            'SIX_TOTAL': "六费合计"
        },
        'group_by': "PARENT_SUBCOM_NAME",   # 按此列分组计算小计
        'merge_cols': ['分公司'],
        'sum_cols': ['ACC_WATER', 'SIX_TOTAL'] + SIX_FEE_COLS,
        'params': lambda sub, month: [sub, month]
    },
    '3-11': {
        'proc': 'RPT_WLMQ_311',
        'title': f"{year_month}应收报表(按用水性质)",
        'folder': "【应】应收报表（3-11号）（7）",
        'file_name': f"{year_month}应收报表.xlsx",
        'columns_map': {
            'PARENT_SUBCOM_NAME': "分公司",
            'SUBCOM_NAME': "站点",
            'FEE_TYPE': "业务类型",
            'PRICE_CATEGORY_NAME': "价格类别",
            'PRICE_NAME': "用水性质",
            'ACC_COUNT': "户数",
            'ACC_WATER': "水量",
            **BASE_FEE_MAP,
            'SIX_TOTAL': "六费合计",
            'UNIT_PRICE': "单价"
        },
        'sum_cols': ['ACC_COUNT', 'ACC_WATER', 'SIX_TOTAL'] + SIX_FEE_COLS,
        'sum_first': True, # 合计行在第一行
        'split_by': 'PARENT_SUBCOM_NAME',
        'calc_func': lambda df: df.assign(
            # 单价 = 六费合计 / 水量，使用 np.where 处理售水量为 0 的情况防止报错
            UNIT_PRICE = lambda x: np.where(x['ACC_WATER'] != 0, x['SIX_TOTAL'] / x['ACC_WATER'], 0)
        ).round(2),
        'params': lambda sub, month: [sub, month]
    },
    '3-4': {
        'proc': 'RPT_WLMQ_304',
        'title': f"{year_month}全部银行收费汇总统计表.xlsx",
        'folder': "【实】银行报表（3-4号）（1）",
        'file_name': f"{year_month}银行收费.xlsx",
        'columns_map': {
            'HEADOFFICE_NAME': "银行",
            'COMPANY_NAME': "分公司",
            'SUBCOM_NAME': "站点",
            'BANK_IN_MONEY': "本月银行入账",
            'ACC_MONEY': "账单金额",
            'PST_ACTUAL_MONEY': "需划账费用",
            'ACTUAL_LATEFEE': "需划账违约金",
            'PST_PRESTORE_OUT_MONEY': "账户支出",
            'TURN_PRESTORE_IN_MONEY': "账户存入",
            'PST_PRESTORE_IN_MONEY': "纯账户存入",
            'TOTAL_TRANSFER': "集团划账"
        },
        'group_by': 'HEADOFFICE_NAME', # 按银行分组并合并单元格
        'merge_cols': ['银行', '分公司'],   # 指定需要合并的中文列名
        'sum_cols': [
            'BANK_IN_MONEY', 'ACC_MONEY', 'PST_ACTUAL_MONEY', 'ACTUAL_LATEFEE', 
            'PST_PRESTORE_OUT_MONEY', 'TURN_PRESTORE_IN_MONEY', 'PST_PRESTORE_IN_MONEY', 'TOTAL_TRANSFER'
        ],
        'sum_first': True,
        'subtotal_hooks': lambda row: (
            row.update({'集团划账': row.get('账单金额', 0) + row.get('需划账违约金', 0)}),
            row # 注意：update返回None，所以要用元组并返回row本身
        )[1],
        'calc_func': lambda df: df.assign(
            # 本月银行入账 = 需划账费用
            BANK_IN_MONEY = lambda x: x['PST_ACTUAL_MONEY'],
            # 集团划账 = 账单金额 + 需划账违约金
            TOTAL_TRANSFER = lambda x: x['ACC_MONEY'] + x['ACTUAL_LATEFEE']
        ).sort_values(
            # 排序：确保银行内部的分公司是连续的，方便后续合并单元格
            by=['HEADOFFICE_NAME', 'COMPANY_NAME'], 
            ascending=[True, True]
        ).round(2),
        'params': lambda sub, month: [sub, month]
    },
    '3-14': {
        'proc': 'RPT_WLMQ_012',
        'multi_source': True, # 标记位，True 表示存在多个游标
        'title': f"{year_month}实付集团各项费用汇总",
        'folder': "【实】付账报表（3-14号）（1）",
        'file_name': f"{year_month}付账报表.xlsx",
        'columns_map': {
            'SUBCOM_NAME1': "用户归属地",
            'SUBCOM_NAME2': "营业网点",
            **BASE_FEE_MAP,
            'SIX_TOTAL': "六费合计", # 计算列
            'ACTUAL_LATEFEE': "违约金",
            'PT_PRESTORE_OUT_MONEY': "账户支出",
            'PT_PRESTORE_IN_MONEY': "账户存入",
            'RATE': "纯账户预存/支出",
            'TOTAL_TRANSFER': "集团划账" # 计算列
        },
        'sum_cols': ['SIX_TOTAL', 'ACTUAL_LATEFEE', 'PT_PRESTORE_OUT_MONEY', 'PT_PRESTORE_IN_MONEY', 'RATE', 'TOTAL_TRANSFER'] + SIX_FEE_COLS,
        'sum_first': True,
        'calc_func': process_314_data,
        'params': lambda sub, month: [sub, month]
    },
    '3-6': {
        'proc': 'RPT_WLMQ_306',
        'multi_source': True,  # 存在 4 个游标：时间范围、应收、实收、往期调整
        'title': f"{year_month}水费各项目收入汇总表",
        'folder': "【实】实收报表（3-6号）（7）",
        'file_name': f"{year_month}实收报表.xlsx",
        'columns_map': {
            # 基础维度
            'C1': '统计时间',            # 对应“本月/本年”合并列
            'C2': '费用类型',            # 对应“应收金额/实际收回”合并列
            'FEE_TYPE': "费用项目",
            **BASE_FEE_MAP,
            'SIX_TOTAL': "六费合计"
        },
        'sum_cols': [],   # 禁用框架合计行
        'group_by': '',   # 禁用通用小计，改用下面的特殊逻辑
        'merge_cols': ['统计时间', '费用类型'],  # 按统计账期合并单元格
        'calc_func': process_306_data,  # 核心：需要处理 4 个游标的逻辑函数
        'params': lambda sub, month: [sub, month]
    },
    '3-13': {
        'proc': 'RPT_WLMQ_313',
        'multi_source': True,
        'title': f"{year_month}全额费用汇总表",
        'folder': '【实】全额费用实收报表（3-13号）（7）',
        'file_name': f"{year_month}全额费用报表.xlsx",
        # 这里的 columns_map 对应存储过程 result_2 输出的字段名与 Excel 表头的映射
        'columns_map': {
            'PAY_METHOD': '收费方式',
            'FEE_ITEM': '费用项目',
            **BASE_FEE_MAP,
            'SIX_TOTAL': '应收费用'
        },
        'sum_cols': [],     # 不需要在这里定义 sum_cols，因为我们会在 calc_func 中自定义计算逻辑
        'group_by': 'PAY_METHOD', 
        'merge_cols': ['收费方式'],
        'calc_func': process_313_data,
        'params': lambda sub, month: [sub, month]
    },
    '3-23': {
        'proc': 'RPT_WLMQ_014',
        'title': f"{year_month}应收按费用项目明细报表",
        'folder': "【应】应收明细（3-23号）（1）",
        'file_name': f"{year_month}应收明细.xlsx",
        'columns_map': {
            'SUBCOM_NAME': "站点",
            'CARD_ID': "用户号",
            'CARD_NAME': "用户名称",
            'FEE_TYPE': "业务类型",
            'PRICE': "用水性质",
            'BILLING_MONTH': "账期",
            'ACC_WATER': "水量",
            'LAST_READING': "上次表底",
            'READING': "本次表底",
            **BASE_FEE_MAP,
            'SIX_TOTAL': "六费合计",
            'EXTRA_MONEY': "损耗分摊费",
            'SEVEN_TOTAL': "七费合计",
            'BOOK_ID': "抄表册",
            'METER_READER': "抄表员",
            'CHECK_TIME': "计费日期"
        },
        'sum_cols': ['ACC_WATER', 'SIX_TOTAL', 'EXTRA_MONEY', 'SEVEN_TOTAL'] + SIX_FEE_COLS,
        'sum_first': True,
        'calc_func': lambda df: df.assign(
            SEVEN_TOTAL = lambda x: x['SIX_TOTAL'] + x['EXTRA_MONEY'].fillna(0)
        ).round(2),
        'params': lambda sub, month: [sub, month, '']
    },
    '3-47': {
        'proc': 'RPT_WLMQ_047',
        'title': f"{year_month}全部预存明细报表",
        'folder': "【实】预存明细报表（3-47号）（1）",
        'file_name': f"{year_month}预存明细报表.xlsx",
        'columns_map': {
            'SUBCOM_NAME': "站点",
            'CARD_ID': "表卡编号",
            'CARD_NAME': "表卡名称",
            'ACC_TYPE': "预存变动类型",
            'PST_MONEY': "变动金额",
            'FEE_TYPE': "支付途径",
            'USER_NAME': "操作人",
            'PST_TIME': "操作时间"
        },
        'calc_func': lambda df: df.assign(
            # 预存报表通常直接取存储过程计算好的金额，此处可做简单的四舍五入
            PST_MONEY = lambda x: x['PST_MONEY'].fillna(0).round(2)
        ),
        'params': lambda sub, month: [sub, month]
    },
    '3-15': {
        'proc': 'RPT_WLMQ_315',
        'title': f"{year_month}全部水费实收明细表",
        'folder': "【实】实收明细（3-15号）",
        'file_name': f"{year_month}实收明细报表.xlsx",
        'columns_map': {
            'SUBCOM_NAME': "站点",
            'CARD_ID': "表卡编号",
            'CARD_NAME': "表卡名称",
            'CUSTOMER_TYPE': '客户类型',
            'LAST_READING': "上次表底",
            'READING': "本次表底",
            'CHECK_TIME': '开账日期',
            'BILLING_MONTH': "账期",
            'ACC_WATER': "水量",
            **BASE_FEE_MAP,
            'SIX_TOTAL': "六费合计",
            'ACTUAL_LATEFEE': "违约金",
            'PST_PRESTORE_OUT_MONEY': "账户支出",
            'PST_PRESTORE_IN_MONEY': "账户存入",
            'PST_ACTUAL_MONEY': "实际缴费额",
            'PAY_TIME': "收费时间",
            'CASHIER': "收费员",
            'FEE_TYPE': "业务类型",
            'PAY_METHOD': "缴费方式",
            'PAY_SUBCOM': '缴费网点'
        },
        'sum_cols': ['ACC_WATER', 'SIX_TOTAL', 'ACTUAL_LATEFEE', 'PST_PRESTORE_OUT_MONEY', 'PST_PRESTORE_IN_MONEY', 'PST_ACTUAL_MONEY'] + SIX_FEE_COLS,
        'sum_first': True,
        'params': lambda sub, month: [sub, month]
    },
    '3-20': {
        'proc': 'RPT_WLMQ_013',
        'title': f"{year_month}全部欠费明细表",
        'folder': "【实】当月欠费报表（3-20号）（1）",
        'file_name': f"{year_month}未收回欠费.xlsx",
        'columns_map': {
            'BOOK_ID': "抄表册",
            'CARD_ID': "表卡编号",
            'CARD_NAME': "表卡名称",
            'CARD_ADDRESS': "地址",
            'CHECK_TIME': "计费日期",
            'BILLING_MONTH': "账期",
            'LAST_READING': "上次表底",
            'READING': "本次表底",
            'ACC_WATER': "水量",
            **BASE_FEE_MAP,
            'SIX_TOTAL': "六费合计"
        },
        'sum_cols': ['ACC_WATER', 'SIX_TOTAL'] + SIX_FEE_COLS,
        'sum_first': True,
        'params': lambda sub, month: [sub, month, '']
    },
}
