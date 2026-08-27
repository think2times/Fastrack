import glob
import os
import re


def parse_md_to_oracle_sql_v4(md_content):
    sqls = []

    current_table = ""
    current_table_comment = ""
    in_field_table = False

    lines = md_content.split("\n")

    for line in lines:
        line_str = line.strip()

        # 1. 遇到新表标题（### 外勤人员）
        if line_str.startswith("### "):
            current_table_comment = line_str.replace("### ", "").strip()
            current_table = ""  # 重置表名，等待抓取真正的表名
            in_field_table = False
            continue

        # 2. 遇到子标题（#### 记录状态），退出列解析
        if line_str.startswith("#### "):
            in_field_table = False
            continue

        # 3. 匹配表英文名（仅在 current_table 为空时提取，防止被后续引用文本覆盖）
        if line_str.startswith(">") and not current_table:
            # 匹配 > *CSM_FIELDPERSONNEL* 或 > CSM_FIELDPERSONNEL 等格式
            match = re.search(r"[\*`]?([A-Za-z0-9_]{3,})[\*`]?", line_str)
            if match:
                candidate = match.group(1).upper()
                # 排除可能误匹配到的通用 SQL 词汇
                if candidate not in ["DISTINCT", "SELECT", "WHERE", "FROM"]:
                    current_table = candidate
                    if current_table_comment and current_table:
                        tbl_cmt = current_table_comment.replace("'", "''")
                        sqls.append(
                            f"COMMENT ON TABLE {current_table} IS '{tbl_cmt}';"
                        )
            continue

        # 4. 判断表格头：包含“字段”或“列名”
        if line_str.startswith("|") and (
            "字段" in line_str or "列名" in line_str
        ):
            in_field_table = True
            continue

        # 5. 跳过分隔线
        if "---" in line_str:
            continue

        # 6. 解析字段
        if in_field_table and line_str.startswith("|") and current_table:
            cols = [c.strip() for c in line_str.split("|")[1:-1]]

            if len(cols) >= 2:
                cn_name = cols[0]
                col_name = cols[1].upper()
                desc = cols[6] if len(cols) > 6 else ""

                # 校验字段名合法性
                if not re.match(r"^[A-Za-z0-9_]+$", col_name) or col_name in [
                    "字段",
                    "COLUMN",
                ]:
                    continue

                full_comment = cn_name
                if desc:
                    clean_desc = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", desc).strip()
                    if clean_desc:
                        full_comment += f"（{clean_desc}）"

                clean_col_comment = full_comment.replace("'", "''")
                sqls.append(
                    f"COMMENT ON COLUMN {current_table}.{col_name} IS '{clean_col_comment}';"
                )

    return "\n".join(sqls)


def batch_process(md_dir, output_sql="oracle_comments_fixed.sql"):
    all_sqls = ["-- Oracle 11g 自动生成注释脚本\n"]
    for md_file in glob.glob(os.path.join(md_dir, "*.md")):
        with open(md_file, "r", encoding="utf-8") as f:
            sql = parse_md_to_oracle_sql_v4(f.read())
            if sql:
                all_sqls.append(
                    f"-- 文件来源: {os.path.basename(md_file)}\n{sql}\n"
                )

    with open(output_sql, "w", encoding="utf-8") as f:
        f.write("\n".join(all_sqls))
    print(f"解析完成，输出至: {output_sql}")



# 执行转换
batch_process(r"C:\Users\pluto\Desktop\数据字典\可编辑版")  # 填写你 md 文件所在的文件夹路径