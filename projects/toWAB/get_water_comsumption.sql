WITH mapped_data AS
 (SELECT
  -- 1. 统一先将 SUBCOM_CODE 映射为标准的 6 位行政区划代码
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
   END AS region_code,
   
   -- 2. 修正后的行业分类代码映射（严格对应图1与图4）
   CASE
     WHEN p.price_category = 1 THEN
      '04' -- 生活 (04)
     WHEN p.price_category = 7 THEN
      '03' -- 基建 -> 建筑业 (03)
     WHEN p.price_category IN (6, 10) THEN
      '02' -- 工业、热力 -> 工业 (02)
     WHEN p.price_category IN (2, 3, 8, 9, 11, 12) THEN
      '05' -- 商业、公益、消防、特殊、混合、协议 -> 服务业 (05)
     WHEN p.price_category IN (4, 5) THEN
      '06' -- 绿化、环卫 -> 城乡环境 (06)
     ELSE
      '05' -- 默认归类
   END AS industry_code,
   
   r.card_id,
   r.last_read_date,
   r.read_date,
   r.acc_water
    FROM csm.mr_record r
    LEFT JOIN csm.cm_metercards m
      ON r.card_id = m.card_id
    LEFT JOIN csm.price_info p
      ON m.price_code = p.price_code
     AND p.price_list_id = 10
   WHERE r.record_state = 4
     AND REGEXP_like(r.subcom_code, '0[1-6][12]')
     AND r.billing_month =
         TO_NUMBER(TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -1), 'YYYYMM')))

-- 3. 获取指定用户（水务局）的水量明细
SELECT r.region_code, r.card_id, r.last_read_date, r.read_date, r.acc_water
  FROM mapped_data r
 WHERE EXISTS (SELECT 1
          FROM csm.temp_pwding t
         WHERE t.card_id = r.card_id
           AND t.type = '水务局')

UNION ALL

-- 4. 按照编码规则拼接并按打捆维度（区域 + 行业）求和
SELECT r.region_code,
       '10' || r.region_code || r.industry_code AS card_id,
       NULL AS last_read_date,
       NULL AS read_date,
       SUM(acc_water) AS acc_water
  FROM mapped_data r
 WHERE NOT EXISTS (SELECT 1
    FROM csm.temp_pwding t
   WHERE t.card_id = r.card_id
     AND t.type = '水务局')
-- 【核心修复】：将 industry_code 加入 GROUP BY，与 SELECT 保持一致
 GROUP BY r.region_code, r.industry_code
