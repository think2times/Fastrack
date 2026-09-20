WITH mapped_data AS
 (SELECT -- 1. 统一先将 SUBCOM_CODE 映射为标准的 6 位行政区划代码
         CASE r.SUBCOM_CODE
           WHEN '011' THEN
            '650102' -- 天山区
           WHEN '021' THEN
            '650104' -- 新市区
           WHEN '031' THEN
            '650105' -- 水磨沟区
           WHEN '032' THEN
            '650105' -- 水磨河
           WHEN '041' THEN
            '650106' -- 头屯河区
           WHEN '051' THEN
            '650103' -- 沙依巴克区
           WHEN '061' THEN
            '650109' -- 米东区
           WHEN '062' THEN
            '650109' -- 米东供排水
           ELSE
            '650101' -- 默认值
         END AS REGION_ID,
         r.card_id,
         r.last_reading,
         r.reading,
         r.read_water 
    FROM csm.mr_record r
   WHERE r.record_state <> -1
        -- 直接在 SQL 中自动获取上个月的年月（无需 Python 传参）
        -- 注意：如果您的 billing_month 是数字类型（如 202608），用下面这行：
     AND r.billing_month =
         TO_NUMBER(TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -1), 'YYYYMM'))
  -- 如果您的 billing_month 是字符串类型（如 '202608'），请解开下面这行的注释并注释掉上面一行：
  -- AND r.billing_month = TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -1), 'YYYYMM')
  )
-- 第一部分：水量大于 1700 的用户，保持明细数据不变
SELECT REGION_ID, r.card_id, r.last_reading, r.reading, r.read_water
  FROM mapped_data r
 WHERE r.read_water > 1700

UNION ALL

-- 第二部分：水量小于等于 1700 的用户，按区汇总打包
SELECT REGION_ID,
       '1000' || REGION_ID AS card_id,
       NULL AS last_reading,
       NULL AS reading,
       SUM(read_water) AS read_water
  FROM mapped_data r
 WHERE r.read_water <= 1700
 GROUP BY REGION_ID;
