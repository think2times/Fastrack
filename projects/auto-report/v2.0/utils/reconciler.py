import pandas as pd
import numpy as np

def reconcile_metrics(report_a_id, report_b_id, check_map):
    """通用对账函数，处理精度并打印结果"""
    print(f"\n[核对] {report_a_id} ↔ {report_b_id} ...")
    all_pass = True
    errors = []

    for label, (val_a, val_b) in check_map.items():
        # 确保参与计算的是标量数值
        v1 = float(val_a.sum() if hasattr(val_a, 'sum') else val_a)
        v2 = float(val_b.sum() if hasattr(val_b, 'sum') else val_b)
        
        diff = round(abs(v1 - v2), 2)
        if diff >= 0.01:
            errors.append(f"  ❌ {label}: {v1:,.2f} vs {v2:,.2f} (偏离: {diff:,.2f})")
            all_pass = False
        else:
            print(f"  ✅ {label}: 一致 ({v1:,.2f})")

    if not all_pass:
        print("\n".join(errors))
    return all_pass

def run_full_reconciliation(report_package):
    """
    总调度入口
    report_package 为字典，包含所有已处理好的 final_df
    """
    results = []

    # --- 1. 2-8 vs 3-10 水量核对 ---
    df_28 = report_package.get('2-8')
    df_310 = report_package.get('3-10')
    if df_28 is not None and df_310 is not None:
        # 2-8 实际水量 (开账 - 减免)
        water_28 = df_28['ACTUAL_WATER'].sum()
        # 3-10 排除 IC卡购水后的售水量总和
        water_310 = df_310[df_310['FEE_TYPE'] != 'IC卡购水']['ACC_WATER'].sum()
        map_28_310 = {
            "2-8实际水量 vs 3-10非IC卡售水量": (water_28, water_310)
        }

        results.append(reconcile_metrics('2-8', '3-10', map_28_310))
    
    # --- 2. 3-7 vs 3-10 合计核对 ---
    df_37 = report_package.get('3-7')
    if df_310 is not None and df_37 is not None:
        map_37_310 = {
            "3-7合计金额 vs 3-10合计金额": (df_37['FEE_TOTAL'].sum(), df_310['ACC_MONEY'].sum())
        }

        results.append(reconcile_metrics('3-7', '3-10', map_37_310))

    # --- 3. 3-10 vs 3-23 (应收项目核对) ---
    df_323 = report_package.get('3-23')

    def get_323_val(item_names):
        if isinstance(item_names, str):
            item_names = [item_names]
        return df_323[df_323['FEE_TYPE'].isin(item_names)]['FEE_TOTAL'].sum()

    if df_310 is not None and df_323 is not None:
        # 3-10中普表、IC卡、补收、订正及合计数据与3-23中对应业务类型的六费合计是否一致
        map_310_323 = {
            "普表收费一致性": (df_310[df_310['FEE_TYPE'] == '普表收费']['ACC_MONEY'].sum(), get_323_val('普表收费')),
            "IC卡购水一致性": (df_310[df_310['FEE_TYPE'] == 'IC卡购水']['ACC_MONEY'].sum(), get_323_val('IC卡购水')),
            "补收费用一致性": (df_310[df_310['FEE_TYPE'] == '补收费用']['ACC_MONEY'].sum(), get_323_val('补收费用')),
            # 核心需求：3-23 的两个订正合并对比 3-10 的订正
            "订正数据总额一致性": (
                df_310[df_310['FEE_TYPE'] == '订正数据']['ACC_MONEY'].sum(), 
                get_323_val(['订正数据-普表', '订正数据-特账'])
            ),
            "全报表总合计": (df_310['ACC_MONEY'].sum(), df_323['FEE_TOTAL'].sum())
        }
        results.append(reconcile_metrics('3-10', '3-23', map_310_323))

    # --- 4. 3-4 vs 3-14 金额核对 ---
    df_34 = report_package.get('3-4')
    df_314 = report_package.get('3-14')
    # 检查3-4中账单金额、需划账费用、集团划账、账户支出、账户存入、纯账户存入
    # 与 3-14 中应收费用、集团划账、应收费用加违约金、账户支出、账户存入、纯账户预存/支出是否一致；
    if df_34 is not None and df_314 is not None:
        # 3-4 账单金额、需划账费用、集团划账、账户支出、账户存入和纯账户存入
        # 3-14 应收费用、集团划账、应收费用加违约金、账户支出、账户存入、纯账户预存/支出
        # 营业网点列只需要第三方代收机构所在行
        include_sites = ['微信', '支付宝', '银联', '利安', '农行', '建行', '光大银行', '广发', '乌鲁木齐银行']
        df_314_filtered = df_314[df_314['SUBCOM_NAME2'].isin(include_sites)]
        # 准备对比数据集 (封装成字典，Key 是描述，Value 是 (3-4值, 3-14值))
        map_34_314 = {
            "应收费用 vs 账单金额": (df_34['ACC_MONEY'].sum(), df_314_filtered['FEE_TOTAL'].sum()),
            "需划账费用 vs 集团划账": (df_34['PST_ACTUAL_MONEY'].sum(), df_314_filtered['TOTAL_TRANSFER'].sum()),
            "集团划账 vs 应收+违约金": (df_34['TOTAL_TRANSFER'].sum(), df_314_filtered['FEE_TOTAL'].sum() + df_314_filtered['ACTUAL_LATEFEE'].sum()),
            "账户支出": (df_34['PST_PRESTORE_OUT_MONEY'].sum(), df_314_filtered['PT_PRESTORE_OUT_MONEY'].sum()),
            "账户存入": (df_34['TURN_PRESTORE_IN_MONEY'].sum(), df_314_filtered['PT_PRESTORE_IN_MONEY'].sum()),
            "纯账户存入/预存支出": (df_34['PST_PRESTORE_IN_MONEY'].sum(), df_314_filtered['RATE'].sum())
        }

        results.append(reconcile_metrics('3-4', '3-14', map_34_314))

    # --- 5. 3-6 vs 3-14 金额核对 ---
    df_36 = report_package.get('3-6')
    if df_36 is not None and df_314 is not None:
        # 检查3-14中应收费用、违约金合计与3-6中实际收回小计、违约金是否一致
        map_36_314 = {
            "实际收回小计 vs 应收费用+违约金": (df_36[df_36['FEE_TYPE'] == '本月实收小计']['FEE_TOTAL'].sum(), df_314['FEE_TOTAL'].sum()),
            "违约金": (df_36[df_36['FEE_TYPE'] == '当月违约金']['PI1_MONEY'].sum(), df_314['ACTUAL_LATEFEE'].sum())
        }

        results.append(reconcile_metrics('3-6', '3-14', map_36_314))

    # --- 6. 3-6 vs 3-13  ---
    df_313 = report_package.get('3-13')
    if df_36 is not None and df_313 is not None:
        # 检查3-13中数据（各项当月、当年未报、以前年度）与3-6中对应数据是否一致
        not_sum = df_313['收费方式'] != '汇总'
        map_36_313 = {
            "本月收回当月各项费用": (df_36[df_36['FEE_TYPE'] == '本月收回当月各项费用']['FEE_TOTAL'].sum(), df_313[(df_313['费用项目'] == '本月收回当月各项费用') & not_sum]['FEE_TOTAL'].sum()),
            "本月收回当年各项费用": (df_36[df_36['FEE_TYPE'] == '本月收回当年各项费用']['FEE_TOTAL'].sum(), df_313[(df_313['费用项目'] == '本月收回当年各项费用') & not_sum]['FEE_TOTAL'].sum()),
            "本月收回往年各项费用": (df_36[df_36['FEE_TYPE'] == '本月收回往年各项费用']['FEE_TOTAL'].sum(), df_313[(df_313['费用项目'] == '本月收回以前年度各项费用') & not_sum]['FEE_TOTAL'].sum()),
            "本月实收小计": (df_36[df_36['FEE_TYPE'] == '本月实收小计']['FEE_TOTAL'].sum(), df_313[(df_313['费用项目'] == '小计') & not_sum]['FEE_TOTAL'].sum()),
            "违约金": (df_36[df_36['FEE_TYPE'] == '当月违约金']['PI1_MONEY'].sum(), df_313[(df_313['费用项目'] == '违约金') & not_sum]['FEE_TOTAL'].sum())
        }

        results.append(reconcile_metrics('3-6', '3-13', map_36_313))

    # --- 7. 3-6 vs 3-15 实收明细核对 ---
    df_315 = report_package.get('3-15')
    if df_36 is not None and df_315 is not None:
        # 3-6 中实际收回小计、违约金 与 3-15 中应缴额、违约金合计
        map_36_315 = {
            "实收总金额(不含违约金)": (df_36[df_36['FEE_TYPE'] == '本月实收小计']['FEE_TOTAL'].sum(), df_315['FEE_TOTAL'].sum()),
            "违约金": (df_36[df_36['FEE_TYPE'] == '当月违约金']['PI1_MONEY'].sum(), df_315['ACTUAL_LATEFEE'].sum())
        }
        results.append(reconcile_metrics('3-6', '3-15', map_36_315))

    # --- 8. 3-6 vs 3-20 欠费核对 ---
    df_320 = report_package.get('3-20')
    if df_36 is not None and df_320 is not None:
        # 3-6 中本月应收各项费用减去 3-6 中本月收回当月各项费用 与 3-20 中欠费合计
        map_36_320 = {
            "实收总金额(不含违约金)": (
                df_36[df_36['FEE_TYPE'] == '本月应收各项费用']['FEE_TOTAL'].sum() - df_36[df_36['FEE_TYPE'] == '本月收回当月各项费用']['FEE_TOTAL'].sum(), 
                df_320['FEE_TOTAL'].sum()
            ),
        }
        results.append(reconcile_metrics('3-6', '3-20', map_36_320))

    # --- 9. 3-14 vs 3-47 预存金额核对 ---
    df_314 = report_package.get('3-14')
    df_347 = report_package.get('3-47')
    if df_314 is not None and df_347 is not None:
        # 多付转存对应账户存入，预存抵扣对应账户支出，纯预存和纯支出之差对应纯账户预存/支出
        map_314_347 = {
            "账户存入 vs 多付转存": (df_314['PT_PRESTORE_IN_MONEY'].sum(), df_347[df_347['ACC_TYPE'] == '多付转存']['PST_MONEY'].sum()),
            "账户支出 vs 预存抵扣": (df_314['PT_PRESTORE_OUT_MONEY'].sum(), df_347[df_347['ACC_TYPE'] == '预存抵扣']['PST_MONEY'].sum()),
            "纯账户预存/支出 vs 纯预存-纯支出": (
                df_314['RATE'].sum(), 
                df_347[df_347['ACC_TYPE'] == '纯预存']['PST_MONEY'].sum() + df_347[df_347['ACC_TYPE'] == '纯支出']['PST_MONEY'].sum()
            ),
        }
        results.append(reconcile_metrics('3-14', '3-47', map_314_347))

    return all(results)