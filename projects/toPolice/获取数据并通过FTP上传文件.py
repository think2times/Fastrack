import os
import time
from ftplib import FTP
import cx_Oracle as ora
import pandas as pd

# 1. 配置文件名前缀映射，方便以后扩展新的 SQL 文件
FILE_PREFIX_MAP = {
    'get_customer.sql': 'syjt_yhxx_',
    'get_water.sql': 'syjt_ysxx_'
}

def clean_sql_text(sql_text):
    """清理 SQL 文本中的 BOM、尾随分号及注释行"""
    sql_text = sql_text.strip()
    if sql_text.startswith('\ufeff'):
        sql_text = sql_text[1:]
    sql_text = sql_text.rstrip(';')
    
    sql_lines = []
    for line in sql_text.split('\n'):
        line = line.strip()
        # 过滤空行和纯注释行（注意：若业务数据含 '--' 请避免写在行尾注释中）
        if line and not line.startswith('--'):
            sql_lines.append(line)
            
    return '\n'.join(sql_lines)

if __name__ == '__main__':
    work_path = r'D:\Tasks\toPolice'
    if not os.path.exists(work_path):
        os.makedirs(work_path)
    os.chdir(work_path)
    
    conn = None
    try:
        # 创建数据库连接
        conn = ora.connect('CSM_PUBLIC/*2tQ}Ek,7mPh@172.16.16.11:1521/CSM_BM')
        print("数据库连接成功")
        
        for file in os.listdir('.'):
            # 仅处理映射表内已配置的 sql 文件
            if file not in FILE_PREFIX_MAP:
                continue
                
            print(f"处理文件: {file}")
            try:
                with open(file, 'r', encoding='utf-8-sig') as f:
                    sql_text = f.read()
                
                sql_text = clean_sql_text(sql_text)
                
                print(f"执行SQL查询...")
                cursor = conn.cursor()
                try:
                    cursor.execute(sql_text)
                    # 获取所有行数据
                    rows_data = cursor.fetchall()
                    # 获取列名
                    columns = [col[0] for col in cursor.description]
                    
                    # 直接转为 pandas DataFrame
                    rows = pd.DataFrame(rows_data, columns=columns)
                    print(f"查询到 {len(rows)} 条记录")
                    
                    # 后续的转JSON、写文件逻辑保持不变...
                    
                finally:
                    cursor.close()  # 确保游标正确关闭
                
                # 转换为 JSON
                json_data = rows.to_json(orient='records', force_ascii=False)
                
                # 生成带时间戳的目标文件名
                prefix = FILE_PREFIX_MAP[file]
                today = time.strftime('%Y%m%d%H%M%S', time.localtime())
                file_path = f"{prefix}{today}.txt"
                
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(json_data)
                
                print(f"生成文件: {file_path}")
                
            except Exception as e:
                print(f"处理文件 {file} 时出错: {e}")
                
    except Exception as e:
        print(f"数据库连接或操作出错: {e}")
        
    finally:
        if conn:
            conn.close()
            print("数据库连接已关闭")
    
    # ==================== FTP 上传部分 ====================
    host = '172.27.246.1'
    user = 'sy'
    pwd = 'sy@123'
    
    try:
        print("开始FTP上传...")
        ftp = FTP()
        # 增加超时控制，防止网络卡死
        ftp.connect(host, 21, timeout=30)
        ftp.login(user, pwd)
        ftp.set_pasv(True)  # 开启被动模式，防止由于防火墙阻挡导致传输失败
        
        upload_count = 0
        valid_prefixes = tuple(FILE_PREFIX_MAP.values())
        
        for file in os.listdir('.'):
            # 仅上传由本脚本生成的、符合前缀规范的 .txt 文件
            if file.endswith('.txt') and file.startswith(valid_prefixes):
                try:
                    print(f"上传文件: {file}")
                    with open(file, 'rb') as local_file:
                        ftp.storbinary(f'STOR {file}', local_file)
                    os.remove(file)
                    upload_count += 1
                    print(f"文件 {file} 上传成功并已删除")
                except Exception as e:
                    print(f"上传文件 {file} 失败: {e}")
        
        ftp.quit()
        print(f"FTP上传完成，共上传 {upload_count} 个文件")
        
    except Exception as e:
        print(f"FTP连接或上传出错: {e}")


    print("脚本执行完成")