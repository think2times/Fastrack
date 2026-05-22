import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

from utils.processor import process_306_data, process_313_data


# 0. 定义基础目录
BASE_DIR = r'F:\NewSystem\Reports'

# 1. 数据库配置
DB_CONFIG = {
    'user': 'CSM_BM_REPORT',
    'password': 'JT2mlDMaYXR7oHz',
    'dsn': '172.16.16.11:1521/CSM_BM'
}

# 2. 定义所有报表的元数据
# 定义账期
year_month = f"{datetime.now().strftime('%Y年%m月')}"
time = datetime.now()
create_time = time.strftime('%Y-%m-%d')
# 根据日期确定账期，如果是1-25号，则账期为上个月；如果是26号以后，则账期为当前月
today = datetime.now().strftime('%d')
if int(today) <= 25:
    year_month = (time - relativedelta(months=1)).strftime('%Y年%m月')
else:
    year_month = time.strftime('%Y年%m月')

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
BASE_FEE_COLS = list(BASE_FEE_MAP.keys())

REPORTS_CONFIG = {
    '2-8': {
        'proc_name': 'RPT_WLMQ_208',
        'title': '抄表统册用水信息',
        'folder': '【应】抄表水量表（2-8号）（1）',
        'file_name': f"{year_month}抄表水量.xlsx",
        'columns_map': {
            'ROW_INDEX': '序号',
            'BOOK_ID': '统册编号',
            'BOOK_NAME': '统册名称',
            'BILLING_MONTH': '账期',
            'TOTAL_COUNT': '应抄户数',
            'READ_COUNT': '实抄户数',
            'READ_WATER': '抄见水量',
            'ACC_WATER': '开账水量',
            'ADJUST_WATER': '减免水量',
            'ACTUAL_WATER': '实际水量',
            'METER_READER': '抄表员',
        },
        'sum_cols': ['TOTAL_COUNT', 'READ_COUNT', 'READ_WATER', 'ACC_WATER', 'ADJUST_WATER', 'ACTUAL_WATER'],
        'sum_position': 'top',
        # 定义该存储过程需要的参数“值”列表（不含最后的游标）
        'params': lambda sub, month: [sub, month, month, ''],
        'processor': lambda buffers: buffers[0].assign(
            ACTUAL_WATER = lambda x: (x['ACC_WATER'].fillna(0) - x['ADJUST_WATER'].fillna(0)).round(2)
        ),
    },
    '3-10': {
        'proc_name': 'RPT_WLMQ_310',
        'title': f"{year_month}应收报表(按费用项目)",
        'folder': '【应】费用项目汇总（3-10号）（1）',
        'file_name': f"{year_month}应收报表（按费用项目）.xlsx",
        'columns_map': {
            'FEE_TYPE': '业务类型',
            'ACC_COUNT': '户数',
            'ACC_WATER': '售水量',
            **BASE_FEE_MAP, # 自动展开六费映射
            'ACC_MONEY': '应收费用'
        },
        'sum_cols': ['ACC_COUNT', 'ACC_WATER', 'ACC_MONEY'] + BASE_FEE_COLS,
        'sum_position': 'top',
    },
    '3-7': {
        'proc_name': 'RPT_WLMQ_307',
        'title': f"售水量汇总报表",
        'folder': '【应】水量报表（3-7号）（1）',
        'file_name': f"{year_month}水量报表.xlsx",
        'columns_map': {
            'PARENT_SUBCOM_NAME': "分公司",
            'SUBCOM_NAME': "站点",
            'ACC_WATER': '售水量',
            **BASE_FEE_MAP,
            'FEE_TOTAL': "应收费用"
        },
        'group_by': "PARENT_SUBCOM_NAME",   # 按此列分组计算小计
        'merge_cols': [0],              # 按配置指定需要合并单元格的列（这里是第一列，即分公司列）
        'sum_cols': ['ACC_WATER', 'FEE_TOTAL'] + BASE_FEE_COLS,
        'sum_position': 'top',
    },
    '3-11': {
        'proc_name': 'RPT_WLMQ_311',
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
            'FEE_TOTAL': "应收费用",
            'UNIT_PRICE': "单价"
        },
        'sum_cols': ['ACC_COUNT', 'ACC_WATER', 'FEE_TOTAL'] + BASE_FEE_COLS,
        'sum_position': 'top', # 合计行在第一行
        'split_by': 'PARENT_SUBCOM_NAME',
        'processor': lambda buffers: buffers[0].assign(
            UNIT_PRICE = lambda x: np.where(x['ACC_WATER'] != 0, x['FEE_TOTAL'] / x['ACC_WATER'], 0).round(2)
        ),
    },
    '3-4': {
        'proc_name': 'RPT_WLMQ_304',
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
        'merge_cols': [0, 1],   # 指定需要合并单元格的列（这里是第一列和第二列，即银行和分公司列）
        'sum_cols': [
            'BANK_IN_MONEY', 'ACC_MONEY', 'PST_ACTUAL_MONEY', 'ACTUAL_LATEFEE', 
            'PST_PRESTORE_OUT_MONEY', 'TURN_PRESTORE_IN_MONEY', 'PST_PRESTORE_IN_MONEY', 'TOTAL_TRANSFER'
        ],
        'sum_position': 'top',
        'processor': lambda buffers: buffers[0].assign(
            # 本月银行入账 = 需划账费用
            BANK_IN_MONEY = lambda x: x['PST_ACTUAL_MONEY'],
            # 集团划账 = 账单金额 + 需划账违约金
            TOTAL_TRANSFER = lambda x: x['ACC_MONEY'] + x['ACTUAL_LATEFEE']
        ).sort_values(
            # 排序：确保银行内部的分公司是连续的，方便后续合并单元格
            by=['HEADOFFICE_NAME', 'COMPANY_NAME'], 
            ascending=[True, True]
        ).round(2),
    },
    '3-14': {
        'proc_name': 'RPT_WLMQ_012',
        'title': f"{year_month}实付集团各项费用汇总",
        'folder': "【实】付账报表（3-14号）（1）",
        'file_name': f"{year_month}付账报表.xlsx",
        'columns_map': {
            'SUBCOM_NAME1': "用户归属地",
            'SUBCOM_NAME2': "营业网点",
            **BASE_FEE_MAP,
            'FEE_TOTAL': "应收费用",
            'ACTUAL_LATEFEE': "违约金",
            'PT_PRESTORE_OUT_MONEY': "账户支出",
            'PT_PRESTORE_IN_MONEY': "账户存入",
            'RATE': "纯账户预存/支出",
            'TOTAL_TRANSFER': "集团划账" # 计算列
        },
        'sum_cols': ['FEE_TOTAL', 'ACTUAL_LATEFEE', 'PT_PRESTORE_OUT_MONEY', 'PT_PRESTORE_IN_MONEY', 'RATE', 'TOTAL_TRANSFER'] + BASE_FEE_COLS,
        'sum_position': 'top',
        'multi_cursors': 2,  # 启用多游标模式，个数表示游标个数
        # 只要第一个游标的数据
        'processor': lambda buffers: (
            buffers[0].assign(
                # 集团划账 = 应收费用 + 违约金 - 账户支出 + 账户存入 + 纯账户预存/支出
                TOTAL_TRANSFER = lambda x: (x['FEE_TOTAL'] 
                + x['ACTUAL_LATEFEE'].fillna(0) 
                - x['PT_PRESTORE_OUT_MONEY'].fillna(0) 
                + x['PT_PRESTORE_IN_MONEY'].fillna(0) 
                + x['RATE'].fillna(0)).round(2)
            )
        ),
    },
    '3-6': {
        'proc_name': 'RPT_WLMQ_306',
        'title': f"{year_month}水费各项目收入汇总表",
        'folder': "【实】实收报表（3-6号）（7）",
        'file_name': f"{year_month}实收报表.xlsx",
        'columns_map': {
            # 基础维度
            'C1': '统计日期',            # 对应“本月/本年”合并列
            'C2': '费用类型',            # 对应“应收金额/实际收回”合并列
            'FEE_TYPE': "费用项目",
            **BASE_FEE_MAP,
            'FEE_TOTAL': "应收费用"
        },
        'multi_cursors': 4,  # 启用多游标模式，个数表示游标个数
        'sum_cols': ['FEE_TOTAL'] + BASE_FEE_COLS,
        'sum_position': 'none', # 该报表不需要框架自动插入的合计行，因为在 processor 内部会自己计算并插入
        'group_by': '',   # 禁用通用小计，改用下面的特殊逻辑
        'merge_cols': [0, 1],  # 按统计账期合并单元格
        'processor': lambda buffers: process_306_data(buffers, PI_COLS) # 传入整个 buffers 以便在 processor 内部进行跨游标计算
    },
    '3-13': {
        'proc_name': 'RPT_WLMQ_313',
        'title': f"{year_month}全额费用汇总表",
        'folder': '【实】全额费用实收报表（3-13号）（7）',
        'file_name': f"{year_month}全额费用报表.xlsx",
        # 这里的 columns_map 对应存储过程 result_2 输出的字段名与 Excel 表头的映射
        'columns_map': {
            'PAY_METHOD': '收费方式',
            'FEE_ITEM': '费用项目',
            **BASE_FEE_MAP,
            'FEE_TOTAL': '应收费用'
        },
        'multi_cursors': 2,  # 启用多游标模式，个数表示游标个数
        'sum_cols': ['FEE_TOTAL'] + BASE_FEE_COLS,
        'sum_position': 'none', # 该报表不需要框架自动插入的合计行，因为在 processor 内部会自己计算并插入
        'group_by': 'PAY_METHOD',
        'merge_cols': [0],
        'processor': lambda buffers: process_313_data(buffers, PI_COLS), # 只处理第二个游标的数据，传入整个 buffers 以便在 processor 内部进行跨游标计算
    },
    '3-23': {
        'proc_name': 'RPT_WLMQ_014',
        'title': f"{year_month}应收按费用项目明细报表",
        'folder': "【应】应收明细（3-23号）（1）",
        'file_name': f"{year_month}应收明细.xlsx",
        'columns_map': {
            'SUBCOM_NAME': "站点",
            'CARD_ID': "用户号",
            'CARD_NAME': "用户名称",
            'PRICE': "用水性质",
            'BILLING_MONTH': "账期",
            'LAST_READING': "上次表底",
            'READING': "本次表底",
            'FEE_TYPE': "业务类型",
            'ACC_WATER': "水量",
            **BASE_FEE_MAP,
            'FEE_TOTAL': "应收费用",
            'PI9_MONEY': "损耗分摊费",
            'ACC_MONEY': "七费合计",
            'BOOK_ID': "抄表册",
            'METER_READER': "抄表员",
            'CHECK_TIME': "计费日期",
        },
        'sum_cols': ['ACC_WATER', 'FEE_TOTAL', 'PI9_MONEY', 'ACC_MONEY'] + BASE_FEE_COLS,
        'sum_position': 'top',
        'params_extra': 1,  # 表示除了默认的 [sub, month] 之外，还需要额外补一个空字符串占位
    },
    '3-47': {
        'proc_name': 'RPT_WLMQ_047',
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
            'PST_TIME': "操作日期"
        },
    },
    '3-15': {
        'proc_name': 'RPT_WLMQ_315',
        'title': f"{year_month}全部水费实收明细表",
        'folder': "【实】实收明细（3-15号）",
        'file_name': f"{year_month}实收明细报表.xlsx",
        'columns_map': {
            'SUBCOM_NAME': "站点",
            'CARD_ID': "表卡编号",
            'CARD_NAME': "表卡名称",
            'CUSTOMER_TYPE': '客户类型',
            'FEE_TYPE': "业务类型",
            'BILLING_MONTH': "账期",
            'LAST_READING': "上次表底",
            'READING': "本次表底",
            'CHECK_TIME': '计费日期',
            'ACC_WATER': "水量",
            **BASE_FEE_MAP,
            'FEE_TOTAL': "应收费用",
            'ACTUAL_LATEFEE': "违约金",
            'PST_PRESTORE_OUT_MONEY': "账户支出",
            'PST_PRESTORE_IN_MONEY': "账户存入",
            'PST_ACTUAL_MONEY': "实际缴费额",
            'CASHIER': "收费员",
            'PAY_TIME': "收费日期",
            'PAY_METHOD': "缴费方式",
            'PAY_SUBCOM': '缴费网点'
        },
        'sum_cols': ['ACC_WATER', 'FEE_TOTAL', 'ACTUAL_LATEFEE', 'PST_PRESTORE_OUT_MONEY', 'PST_PRESTORE_IN_MONEY', 'PST_ACTUAL_MONEY'] + BASE_FEE_COLS,
        'sum_position': 'top',
    },
    '3-20': {
        'proc_name': 'RPT_WLMQ_013',
        'title': f"{year_month}全部欠费明细表",
        'folder': "【实】当月欠费报表（3-20号）（1）",
        'file_name': f"{year_month}未收回欠费.xlsx",
        'columns_map': {
            'BOOK_ID': "抄表册",
            'CARD_ID': "表卡编号",
            'CARD_NAME': "表卡名称",
            'CARD_ADDRESS': "表卡地址",
            'BILLING_MONTH': "账期",
            'LAST_READING': "上次表底",
            'READING': "本次表底",
            'CHECK_TIME': "计费日期",
            'ACC_WATER': "水量",
            **BASE_FEE_MAP,
            'FEE_TOTAL': "应收费用"
        },
        'sum_cols': ['ACC_WATER', 'FEE_TOTAL'] + BASE_FEE_COLS,
        'sum_position': 'top',
        'params_extra': 1,
    },
}
