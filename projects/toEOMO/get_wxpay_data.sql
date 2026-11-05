WITH date_params AS (
    SELECT 
        -- 1. 上月年月（例如：当前是2026年1月，上月为 '202512'）
        TO_CHAR(ADD_MONTHS(SYSDATE, -1), 'YYYYMM') AS last_month,
        
        -- 2. 今年截止到上月（核心业务规则：若当前是1月，则取上年全年 01 至 12；否则取当年01至上月）
        CASE 
            WHEN TO_CHAR(SYSDATE, 'MM') = '01' 
            THEN TO_CHAR(ADD_MONTHS(SYSDATE, -1), 'YYYY') || '01' -- 去年的01月
            ELSE TO_CHAR(TRUNC(SYSDATE, 'YEAR'), 'YYYYMM')        -- 当年01月
        END AS year_start,
        
        TO_CHAR(ADD_MONTHS(SYSDATE, -1), 'YYYYMM') AS year_to_last_month,
        
        -- 3. 去年同期开始月份（若当前是1月，去年同期即前年01月；否则为去年01月）
        CASE 
            WHEN TO_CHAR(SYSDATE, 'MM') = '01' 
            THEN TO_CHAR(ADD_MONTHS(SYSDATE, -13), 'YYYY') || '01' -- 前年的01月
            ELSE TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE, 'YEAR'), -12), 'YYYYMM') -- 去年的01月
        END AS last_year_start,
        
        -- 4. 去年同期结束月份（若当前是1月，去年同期结束即前年12月；否则为去年上月）
        CASE 
            WHEN TO_CHAR(SYSDATE, 'MM') = '01' 
            THEN TO_CHAR(ADD_MONTHS(SYSDATE, -13), 'YYYY') || '12' -- 前年的12月
            ELSE TO_CHAR(ADD_MONTHS(ADD_MONTHS(SYSDATE, -1), -12), 'YYYYMM') -- 去年上月
        END AS last_year_to_last_month
    FROM DUAL
),
-- 子表1：微信水费收入统计
revenue_agg AS (
    SELECT 
        SUM(CASE WHEN charge.statistic_billing_month = p.last_month 
                 THEN round(charge.pst_actual_money / 10000, 2) ELSE 0 END) AS last_month_revenue,        -- 上月交易额
                 
        SUM(CASE WHEN charge.statistic_billing_month BETWEEN p.year_start AND p.year_to_last_month 
                 THEN round(charge.pst_actual_money / 10000, 2) ELSE 0 END) AS total_revenue,             -- 今年截止上月（1月时为去年全年）交易额
                 
        SUM(CASE WHEN charge.statistic_billing_month = p.last_year_to_last_month 
                 THEN round(charge.pst_actual_money / 10000, 2) ELSE 0 END) AS last_year_last_month_revenue, -- 去年上月交易额
                 
        SUM(CASE WHEN charge.statistic_billing_month BETWEEN p.last_year_start AND p.last_year_to_last_month 
                 THEN round(charge.pst_actual_money / 10000, 2) ELSE 0 END) AS last_year_total_revenue    -- 去年同期交易额
    FROM csm_bm_report.rpt_water_charges_ss charge
    CROSS JOIN date_params p
    WHERE charge.pay_method = '微信'
      AND (
           charge.statistic_billing_month BETWEEN p.year_start AND p.year_to_last_month
           OR charge.statistic_billing_month BETWEEN p.last_year_start AND p.last_year_to_last_month
          )
      AND charge.fee_type IN ('普表-实收', '预存款-重笔转', '预存款-疑难转', '预存款-实收')
),
-- 子表2：关注绑定数统计
bind_agg AS (
    SELECT 
        -- 今年截止上月累计绑定数（1月时为去年全年绑定数）
        COUNT(CASE WHEN TO_CHAR(SYSDATE, 'MM') = '01' 
                    AND b.bind_time < TRUNC(SYSDATE, 'MM')
                    THEN 1 
                   WHEN TO_CHAR(SYSDATE, 'MM') <> '01' 
                    AND b.bind_time < TRUNC(SYSDATE, 'MM')
                    THEN 1 
              END) AS total_bind_count,
                   
        -- 去年同期累计绑定数
        COUNT(CASE WHEN TO_CHAR(SYSDATE, 'MM') = '01'
                    AND b.bind_time < ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -12)
                    THEN 1
                   WHEN TO_CHAR(SYSDATE, 'MM') <> '01'
                    AND b.bind_time < ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -12)
                    THEN 1
              END) AS last_year_total_bind_count
    FROM CSM.CM_CUSTOMERBIND_RECORD b
    CROSS JOIN date_params p
)
-- 汇总输出单行结果
SELECT 
    r.*, 
    b.total_bind_count,
    b.last_year_total_bind_count
FROM revenue_agg r
CROSS JOIN bind_agg b