import os
import logging
import zipfile
import openpyxl
import oracledb
from datetime import datetime

import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr  # <--- 导入标准格式化工具

# Oracle 数据库配置
ORACLE_USER = "CSM_PUBLIC"
ORACLE_PASSWORD = "*2tQ}Ek,7mPh"
ORACLE_DSN = "172.16.16.11:1521/CSM_BM"      # 格式: "IP:端口/服务名或SID"

# 邮件配置参数
SMTP_SERVER = "smtp.qq.com"  # QQ 邮箱 SMTP 服务器
SMTP_PORT = 465  # SSL 端口
SENDER_EMAIL = "2271921950@qq.com"  # 发件人 QQ 邮箱
# 注意：QQ 邮箱需要开启 SMTP 服务并在账户设置中获取“授权码”（不是 QQ 密码）
EMAIL_AUTH_CODE = "zuyxcsdsvgatebgc"
RECEIVER_EMAIL = "1140474804@qq.com"  # 收件人邮箱

now = datetime.now()

# 获取当前年份
current_year = now.year

# 获取上个月的月份及对应的年份（考虑跨年）
if now.month == 1:
    last_month = 12
    last_month_year = now.year - 1
else:
    last_month = now.month - 1
    last_month_year = now.year

def load_sql_from_file(file_path="query.sql"):
    """读取外部 SQL 文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error(f"读取 SQL 文件失败: {str(e)}")
        return None

def fetch_data_from_oracle():
    """
    连接 Oracle 数据库并查询 U201 / U207 所需各项指标
    """
    # 1. 加载外部 SQL
    sql = load_sql_from_file("get_wxpay_data.sql")
    if not sql:
        return {}  # 如果没加载到，返回空字典

    try:
        # 2. 连接 Oracle (Thick 模式)
        oracledb.init_oracle_client(lib_dir=r"F:\app\pluto\product\instantclient_19_32")
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        cursor = connection.cursor()
        
        # 3. 直接执行 SQL（无需再传参）
        cursor.execute(sql)
        row = cursor.fetchone()

        cursor.close()
        connection.close()

        return {
            "last_month_revenue": str(row[0] or ""),
            "total_revenue": str(row[1] or ""),
            "last_year_last_month_revenue": str(row[2] or ""),
            "last_year_total_revenue": str(row[3] or ""),
            "total_bind_count": str(row[4] or ""),
            "last_year_total_bind_count": str(row[5] or ""),
            "service_b2b": str("0.00")
        }

    except Exception as e:
        logging.error(f"Oracle 数据库读取异常: {str(e)}")

def update_excel_reports(data):
    # 1. 填报 U201《平台交易情况》
    wb201 = openpyxl.load_workbook('templates/U201_202603010_平台交易情况.xlsx')
    ws201 = wb201['Sheet1']

    # 填写年月
    ws201.cell(row=5, column=10, value=last_month_year)
    ws201.cell(row=5, column=12, value=last_month)

    # 平台交易情况
    ws201.cell(row=10, column=11, value=data["last_month_revenue"])       # 101 上月
    ws201.cell(row=10, column=13, value=data["total_revenue"])   # 101 1-上月
    ws201.cell(row=10, column=15, value=data["last_year_last_month_revenue"])       # 101 去年上月
    ws201.cell(row=10, column=17, value=data["last_year_total_revenue"])   # 101 1-去年上月
    ws201.cell(row=16, column=11, value=data["last_month_revenue"])           # 106 自营销售额 上月
    ws201.cell(row=16, column=13, value=data["total_revenue"])           # 106 自营销售额 1-上月
    ws201.cell(row=16, column=15, value=data["last_year_last_month_revenue"])           # 106 自营销售额 去年上月
    ws201.cell(row=16, column=17, value=data["last_year_total_revenue"])           # 106 自营销售额 去年1-上月
    ws201.cell(row=25, column=11, value=data["last_month_revenue"])       # 114 服务类上月
    ws201.cell(row=25, column=13, value=data["total_revenue"])   # 114 服务类1-上月
    ws201.cell(row=25, column=15, value=data["last_year_last_month_revenue"])       # 114 服务类 去年上月
    ws201.cell(row=25, column=17, value=data["last_year_total_revenue"])   # 114 服务类 去年1-上月
    ws201.cell(row=26, column=11, value=data["service_b2b"])          # 115 服务类B2B 上月
    ws201.cell(row=26, column=13, value=data["service_b2b"])     # 115 服务类B2B 1-上月
    ws201.cell(row=26, column=15, value=data["service_b2b"])          # 115 服务类B2B 去年上月
    ws201.cell(row=26, column=17, value=data["service_b2b"])     # 115 服务类B2B 去年1-上月
    ws201.cell(row=28, column=11, value=data["last_month_revenue"])          # 117 服务类B2C上月
    ws201.cell(row=28, column=13, value=data["total_revenue"])     # １１７ 服务类B2C １-上月
    ws201.cell(row=28, column=15, value=data["last_year_last_month_revenue"])          # 117 服务类B2C 去年上月
    ws201.cell(row=28, column=17, value=data["last_year_total_revenue"])     # １１７ 服务类B2C 去年１-上月
    
    # 分服务类别
    ws201.cell(row=72, column=11, value=data["last_month_revenue"])       # 301 服务类 上月
    ws201.cell(row=72, column=12, value=data["total_revenue"])        # 301 服务类 1-上月
    ws201.cell(row=72, column=13, value=data["last_year_last_month_revenue"])       # 301 服务类 去年上月
    ws201.cell(row=72, column=14, value=data["last_year_total_revenue"])        # 301 服务类 去年1-上月
    ws201.cell(row=72, column=15, value=data["service_b2b"])       # 301 服务类 B2B 上月
    ws201.cell(row=72, column=16, value=data["service_b2b"])        # 301 服务类 B2B 1-上月
    ws201.cell(row=72, column=17, value=data["total_revenue"])       # 301 服务类 B2C 去年上月
    ws201.cell(row=72, column=18, value=data["last_year_total_revenue"])  # 301 服务类 B2C 去年1-上月
    ws201.cell(row=87, column=11, value=data["last_month_revenue"])          # 316 居民和家庭服务类 上月
    ws201.cell(row=87, column=12, value=data["total_revenue"])     # 316 居民和家庭服务类 1-上月
    ws201.cell(row=87, column=13, value=data["last_year_last_month_revenue"])       # 316 居民和家庭服务类 去年上月
    ws201.cell(row=87, column=14, value=data["last_year_total_revenue"])        # 316 居民和家庭服务类 去年1-上月
    ws201.cell(row=87, column=15, value=data["service_b2b"])       # 316 居民和家庭服务类 B2B 上月
    ws201.cell(row=87, column=16, value=data["service_b2b"])        # 316 居民和家庭服务类 B2B 1-上月
    ws201.cell(row=87, column=17, value=data["total_revenue"])       # 316 居民和家庭服务类 B2C 去年上月
    ws201.cell(row=87, column=18, value=data["last_year_total_revenue"])  # 316 居民和家庭服务类 B2C 去年1-上月
    
    # 分地区 (总计与新疆)
    ws201.cell(row=100, column=5, value=data["total_revenue"])
    ws201.cell(row=100, column=6, value=data["last_year_total_revenue"])
    ws201.cell(row=100, column=7, value=data["service_b2b"])
    ws201.cell(row=100, column=8, value=data["service_b2b"])
    ws201.cell(row=100, column=9, value=data["service_b2b"])
    ws201.cell(row=100, column=10, value=data["service_b2b"])
    ws201.cell(row=100, column=11, value=data["service_b2b"])
    ws201.cell(row=100, column=12, value=data["service_b2b"])
    ws201.cell(row=100, column=13, value=data["total_revenue"])
    ws201.cell(row=100, column=14, value=data["last_year_total_revenue"])
    ws201.cell(row=100, column=15, value=data["total_revenue"])
    ws201.cell(row=100, column=16, value=data["last_year_total_revenue"])
    ws201.cell(row=100, column=17, value=data["service_b2b"])
    ws201.cell(row=100, column=18, value=data["service_b2b"])
    ws201.cell(row=131, column=5, value=data["total_revenue"])
    ws201.cell(row=131, column=6, value=data["last_year_total_revenue"])
    ws201.cell(row=131, column=7, value=data["service_b2b"])
    ws201.cell(row=131, column=8, value=data["service_b2b"])
    ws201.cell(row=131, column=9, value=data["service_b2b"])
    ws201.cell(row=131, column=10, value=data["service_b2b"])
    ws201.cell(row=131, column=11, value=data["service_b2b"])
    ws201.cell(row=131, column=12, value=data["service_b2b"])
    ws201.cell(row=131, column=13, value=data["total_revenue"])
    ws201.cell(row=131, column=14, value=data["last_year_total_revenue"])
    ws201.cell(row=131, column=15, value=data["total_revenue"])
    ws201.cell(row=131, column=16, value=data["last_year_total_revenue"])
    ws201.cell(row=131, column=17, value=data["service_b2b"])
    ws201.cell(row=131, column=18, value=data["service_b2b"])

    # 保存文件
    wb201.save('U201_202603010_平台交易情况.xlsx')
    
    # 2. 填报 U207《平台经营情况》
    wb207 = openpyxl.load_workbook('templates/U207_202603010_平台经营情况.xlsx')
    ws207 = wb207['Sheet1']

    # 填写年月
    ws207.cell(row=6, column=8, value=last_month_year)
    ws207.cell(row=6, column=11, value=last_month)
    
    # 平台经营情况
    ws207.cell(row=13, column=10, value=1)             # 14 当前活跃商家数
    ws207.cell(row=13, column=15, value=1)             # 14 去年同期活跃商家数
    ws207.cell(row=14, column=10, value=data["total_bind_count"]) # 15 当前活跃用户数
    ws207.cell(row=14, column=15, value=data["last_year_total_bind_count"]) # 15 去年同期活跃用户数

    wb207.save('U207_202603010_平台经营情况.xlsx')
    
    print("Oracle 数据库数据拉取并自动填报完成！")

def create_report_zip():
    """
    自动将生成的 U201 和 U207 报表打包为压缩包
    """
    # 需要打包的两个 Excel 文件名
    files_to_zip = [
        'U201_202603010_平台交易情况.xlsx',
        'U207_202603010_平台经营情况.xlsx'
    ]
    
    # 生成的压缩包文件名（可根据需要自定义命名）
    zip_filename = '平台统计报表_202610.zip'
    
    try:
        # 使用 zipfile 写入压缩包 (ZIP_DEFLATED 表示进行压缩)
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_zip:
                if os.path.exists(file):
                    zipf.write(file)
                    logging.info(f"已成功将 {file} 添加到压缩包")
                else:
                    logging.warning(f"警告：未找到文件 {file}，无法打包")
                    
        print(f"压缩包已成功生成：{zip_filename}")
        return zip_filename
        
    except Exception as e:
        logging.error(f"打包压缩文件时发生异常: {str(e)}")
        return None

def send_report_with_attachment():
    # 创建带附件的邮件对象
    message = MIMEMultipart()
    message['From'] = formataddr(("平台经济统计报表", SENDER_EMAIL))
    message['To'] = RECEIVER_EMAIL
    message['Subject'] = Header("【自动发送】2026年10月平台统计报表 (U201 & U207)", 'utf-8')

    # 邮件正文
    mail_body = "您好：\n\n附件为自动从数据库提取数据并填报生成的 2026 年 10 月 U201《平台交易情况》及 U207《平台经营情况》报表压缩包，请查收。\n\n数据来源：系统数据库自动查询。\n\n此为程序自动发送，请勿直接回复。"
    message.attach(MIMEText(mail_body, 'plain', 'utf-8'))

    # 3. 添加 ZIP 压缩包附件
    zip_filename = "平台统计报表_202610.zip"
    if os.path.exists(zip_filename):
        with open(zip_filename, "rb") as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=Header(zip_filename, 'utf-8').encode())
            message.attach(attachment)
    else:
        print(f"错误：找不到附件文件 {zip_filename}")
        return

    # 4. 连接 SMTP 服务器并发送
    try:
        print("正在连接 QQ 邮箱安全服务器...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, EMAIL_AUTH_CODE)
        
        print(f"正在发送邮件至 {RECEIVER_EMAIL}...")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], message.as_string())
        server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")

def cleanup_temporary_files():
    """清理生成的临时 Excel 报表和 ZIP 压缩包"""
    files_to_clean = [
        "U201_202603010_平台交易情况.xlsx",
        "U207_202603010_平台经营情况.xlsx",
        "平台统计报表_202610.zip"
    ]
    
    print("开始清理本地临时文件...")
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"  - 已成功删除: {file_path}")
            except Exception as e:
                print(f"  - 删除文件 {file_path} 失败: {str(e)}")
        else:
            print(f"  - 文件不存在，跳过: {file_path}")

if __name__ == "__main__":
    # 获取数据
    oracle_data = fetch_data_from_oracle()

    # 更新 Excel 报表
    update_excel_reports(oracle_data)

    # 执行打包
    zip_file = create_report_zip()

    # 发送邮件
    send_report_with_attachment()

    # 发送成功后，清理临时 Excel 报表和 ZIP 压缩包
    cleanup_temporary_files()