import os
import re
from bs4 import BeautifulSoup

# ---------- 过滤词 ----------
FILTER_WORDS = {
    'VARCHAR2', 'NUMBER', 'DATE', 'INT', 'BIT', 'FLOAT', 'NVARCHAR2',
    'VARCHAR', 'DATETIME', 'TIMESTAMP', 'DECIMAL', 'DOUBLE', 'CHAR',
    'CARD_ID', 'CUSTOMER_ID', 'TASK_ID', 'BM_TYPE', 'PK', 'NULL', 'DEFAULT',
    'COMMENT', 'COLUMN', 'TABLE', 'INDEX', 'KEY', 'PRIMARY', 'FOREIGN'
}

def extract_table_name_from_context(context_text):
    patterns = [
        r'\*([A-Z_][A-Z0-9_]+)\*',
        r'`([A-Z_][A-Z0-9_]+)`',
        r'<em>([A-Z_][A-Z0-9_]+)</em>',
        r'<strong>([A-Z_][A-Z0-9_]+)</strong>',
        r'(?:表名|表格)[：:]\s*([A-Z_][A-Z0-9_]+)',
        r'\b([A-Z_][A-Z0-9_]{2,})\b'
    ]
    for pat in patterns:
        matches = re.findall(pat, context_text, re.IGNORECASE)
        for m in matches:
            upper = m.upper()
            if upper not in FILTER_WORDS and not upper.startswith('UNKNOWN'):
                return upper
    return None

def get_table_name_from_html(table, soup, filepath, table_index):
    prev_elements = []
    for sibling in table.previous_siblings:
        if sibling.name in ['blockquote', 'p', 'div', 'h1', 'h2', 'h3', 'h4']:
            prev_elements.append(sibling)
        if sibling.name == 'table' or sibling.name == 'hr':
            break
    context = ''
    for el in prev_elements:
        context += el.get_text(separator=' ', strip=True) + ' '
    next_elements = []
    for sibling in table.next_siblings:
        if sibling.name in ['blockquote', 'p', 'div']:
            next_elements.append(sibling)
        if sibling.name == 'table':
            break
    for el in next_elements:
        context += el.get_text(separator=' ', strip=True) + ' '
    table_name = extract_table_name_from_context(context)
    if table_name:
        return table_name
    full_text = soup.get_text(separator=' ', strip=True)
    all_candidates = re.findall(r'\b([A-Z_][A-Z0-9_]{2,})\b', full_text)
    for cand in all_candidates:
        if cand not in FILTER_WORDS and not cand.startswith('UNKNOWN'):
            return cand
    return f"TBL_{table_index+1:03d}"

def get_table_name_from_markdown(context_lines, filepath, table_index):
    context = '\n'.join(context_lines)
    table_name = extract_table_name_from_context(context)
    if table_name:
        return table_name
    full_text = '\n'.join(context_lines)
    all_candidates = re.findall(r'\b([A-Z_][A-Z0-9_]{2,})\b', full_text)
    for cand in all_candidates:
        if cand not in FILTER_WORDS and not cand.startswith('UNKNOWN'):
            return cand
    return f"TBL_{table_index+1:03d}"

def parse_html_tables(html_content, filepath):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    results = []
    for idx, table in enumerate(tables):
        table_name = get_table_name_from_html(table, soup, filepath, idx)

        thead = table.find('thead')
        if not thead:
            first_row = table.find('tr')
            if first_row:
                ths = first_row.find_all(['th', 'td'])
                headers = [th.get_text(strip=True) for th in ths]
            else:
                continue
        else:
            headers = [th.get_text(strip=True) for th in thead.find_all('th')]

        field_idx = -1
        desc_idx = -1
        name_idx = -1
        for i, h in enumerate(headers):
            if h in ['字段', 'Field', '字段名']:
                field_idx = i
            elif h in ['描述', 'Description', '说明']:
                desc_idx = i
            elif h in ['列名', '中文名', '名称', 'Column Name']:
                name_idx = i

        if field_idx == -1:
            continue

        tbody = table.find('tbody') or table
        rows = []
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) > field_idx:
                cols = [td.get_text(strip=True) for td in tds]
                rows.append(cols)

        field_desc = []
        for row in rows:
            field = row[field_idx] if field_idx < len(row) else ''
            name = row[name_idx] if name_idx != -1 and name_idx < len(row) else ''
            desc = row[desc_idx] if desc_idx != -1 and desc_idx < len(row) else ''
            # 组装注释：优先列名，若有描述则追加括号
            if name:
                if desc:
                    comment = f"{name}（{desc}）"
                else:
                    comment = name
            else:
                if desc:
                    comment = desc
                else:
                    comment = field
            field_desc.append((field, comment))
        results.append((table_name, field_desc))
    return results

def parse_markdown_tables(text, filepath):
    lines = text.splitlines()
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if '|' in line and i+1 < len(lines) and '---' in lines[i+1]:
            start = max(0, i-30)
            end = min(len(lines), i+30)
            context_lines = lines[start:end]
            table_name = get_table_name_from_markdown(context_lines, filepath, len(results))

            header = [h.strip() for h in line.split('|') if h.strip() != '']
            field_idx = -1
            desc_idx = -1
            name_idx = -1
            for j, h in enumerate(header):
                if h in ['字段', 'Field', '字段名']:
                    field_idx = j
                elif h in ['描述', 'Description', '说明']:
                    desc_idx = j
                elif h in ['列名', '中文名', '名称', 'Column Name']:
                    name_idx = j

            if field_idx == -1:
                i += 1
                continue

            rows = []
            j = i + 2
            while j < len(lines) and '|' in lines[j]:
                cols = [c.strip() for c in lines[j].split('|') if c.strip() != '']
                if len(cols) > field_idx:
                    rows.append(cols)
                j += 1

            field_desc = []
            for row in rows:
                field = row[field_idx] if field_idx < len(row) else ''
                name = row[name_idx] if name_idx != -1 and name_idx < len(row) else ''
                desc = row[desc_idx] if desc_idx != -1 and desc_idx < len(row) else ''
                if name:
                    if desc:
                        comment = f"{name}（{desc}）"
                    else:
                        comment = name
                else:
                    if desc:
                        comment = desc
                    else:
                        comment = field
                field_desc.append((field, comment))
            results.append((table_name, field_desc))
            i = j
        else:
            i += 1
    return results

def generate_oracle_comments(table_name, field_desc_list):
    sqls = []
    for field, comment in field_desc_list:
        comment_escaped = comment.replace("'", "''")
        sql = f"COMMENT ON COLUMN {table_name}.{field} IS '{comment_escaped}';"
        sqls.append(sql)
    return sqls

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<table' in content.lower():
        tables = parse_html_tables(content, filepath)
    else:
        tables = parse_markdown_tables(content, filepath)
    all_sql = []
    for table_name, field_desc in tables:
        print(f"识别表名: {table_name} (文件: {os.path.basename(filepath)})")
        all_sql.extend(generate_oracle_comments(table_name, field_desc))
    return all_sql

def batch_process(directory, output_file='oracle_comments.sql'):
    all_sql = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.html', '.htm')):
                filepath = os.path.join(root, file)
                print(f"处理 {filepath} ...")
                sqls = process_file(filepath)
                all_sql.extend(sqls)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Oracle 列注释（自动生成）\n")
        f.write(f"-- 共 {len(all_sql)} 条注释\n\n")
        for sql in all_sql:
            f.write(sql + '\n')
    print(f"完成，输出文件：{output_file}")

if __name__ == '__main__':
    # 请将 'your_html_dir' 修改为您的文件夹路径
    batch_process(r'C:\Users\pluto\Desktop\数据字典\批量处理', 'oracle_comments.sql')