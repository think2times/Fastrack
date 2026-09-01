 SELECT 
   -- T.TABLE_NAME                                    AS 表名,
   -- T.COMMENTS                                      AS 中文表名,
    C.COLUMN_NAME                                   AS 字段名,
    -- 格式化拼接数据类型与长度
    CASE 
        WHEN C.DATA_TYPE IN ('VARCHAR2', 'CHAR', 'NVARCHAR2', 'NCHAR') THEN C.DATA_TYPE || '(' || C.DATA_LENGTH || ')'
        WHEN C.DATA_TYPE = 'NUMBER' AND C.DATA_PRECISION IS NOT NULL AND C.DATA_SCALE IS NOT NULL AND C.DATA_SCALE > 0 
            THEN C.DATA_TYPE || '(' || C.DATA_PRECISION || ',' || C.DATA_SCALE || ')'
        WHEN C.DATA_TYPE = 'NUMBER' AND C.DATA_PRECISION IS NOT NULL 
            THEN C.DATA_TYPE || '(' || C.DATA_PRECISION || ')'
        ELSE C.DATA_TYPE 
    END                                             AS 数据类型格式,
    C.DATA_TYPE                                     AS 基础类型,
    C.DATA_LENGTH                                   AS 字节长度,
    C.DATA_PRECISION                                AS 整数精度,
    C.DATA_SCALE                                    AS 小数位数,
    C.NULLABLE                                      AS 是否可为空,
    M.COMMENTS                                      AS 字段注释

FROM 
    USER_TAB_COLUMNS C
LEFT JOIN 
    USER_COL_COMMENTS M 
    ON C.TABLE_NAME = M.TABLE_NAME 
   AND C.COLUMN_NAME = M.COLUMN_NAME
LEFT JOIN 
    USER_TAB_COMMENTS T
    ON C.TABLE_NAME = T.TABLE_NAME
WHERE 
    C.TABLE_NAME = UPPER('PRICE_CATEGORY')  -- 注意：ORACLE 默认表名为大写
ORDER BY 
    C.COLUMN_ID;
