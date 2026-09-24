import os
import time
import base64
import hashlib
import logging
import requests
import oracledb
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# ==================== 1. 全局配置区（配置在最外层） ====================
BASE_URL = "http://111.40.31.237:12223"  # 统一的基础域名
REGISTER_CODE = "NjUwMTAw"     # 统一的注册码
FIXED_SALT = "a3f8d9c2e1b4a7c6d5f0e9b8a7c6d5f4"           # 统一的密钥盐值

# Oracle 数据库配置
ORACLE_USER = "CSM_PUBLIC"
ORACLE_PASSWORD = "*2tQ}Ek,7mPh"
ORACLE_DSN = "172.16.16.11:1521/CSM_BM"      # 格式: "IP:端口/服务名或SID"

BATCH_SIZE = 500                        # 每批推送的数据条数

# 配置日志记录到本地文件
logging.basicConfig(
    filename='task_execution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==================== 核心修改：启用 Thick 模式 ====================
try:
    # Windows 系统下，将路径替换为您实际解压 Instant Client 的文件夹路径
    oracledb.init_oracle_client(lib_dir=r"F:\app\pluto\product\instantclient_19_32")
except Exception as e:
    print(f"初始化 Oracle 客户端失败，请检查 lib_dir 路径: {e}")

def derive_key(password: str, fixed_salt: str) -> bytes:
    """第一步：通过 PBKDF2 派生 32 字节密钥"""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        fixed_salt.encode('utf-8'), 
        10000,  # 迭代次数
        32      # 密钥长度 32 字节
    )

def encrypt_security_code(text: str, key: bytes) -> str:
    """第二步：AES-256-CBC 加密并进行 Base64 编码"""
    # 1. 生成 16 字节随机 IV (对应 Node.js 的 crypto.randomBytes(16))
    iv = os.urandom(16)
    
    # 2. 实行 PKCS7 填充 (Node.js CBC 模式默认行为)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(text.encode('utf-8')) + padder.finalize()
    
    # 3. 创建 AES-256-CBC 加密器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    # 4. 将 IV 和密文拼接：IV 在前，密文在后
    iv_and_cipher = iv + encrypted
    
    # 5. 第二层：Base64 编码
    return base64.b64encode(iv_and_cipher).decode('utf-8')

# ==================== 2. 接口 A：获取 Token ====================
def get_token():
    # 动态拼接 URL
    url = f"{BASE_URL}/holdAllow/getToken"
    
    # 生成加密的 securityCode
    current_time_ms = str(int(time.time() * 1000))
    key = derive_key(REGISTER_CODE, FIXED_SALT)
    security_code = encrypt_security_code(current_time_ms, key)
    
    headers = {
        "Content-Type": "application/json",
        "registerCode": REGISTER_CODE,
        "securityCode": security_code
    }
    
    try:
        response = requests.post(url, headers=headers, json={}, timeout=30)
        if response.status_code == 200:
            res_data = response.json()  # 解析 JSON 响应

            # 1. 提取接口返回的提示信息
            is_success = res_data.get("isSuccess")
            message = res_data.get("resultMessage")
            
            if is_success:
                # 2. 提取 token (注意：result 是列表，所以要取 [0])
                result_list = res_data.get("result", [])
                if result_list and len(result_list) > 0:
                    token = result_list[0].get("token")
                    return token
                    # logging.info(message)
                else:
                    logging.error(f"提示信息: {message}，但返回结果为空")
                    return None
        else:
            logging.error(f"获取 Token 失败，提示信息: {message}")
            return None
    except Exception as e:
        logging.error(f"获取 Token 异常: {str(e)}")
        return None

# ==================== 3. 第二步：数据接收接口 ====================
def load_sql_from_file(file_path="query.sql"):
    """读取外部 SQL 文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error(f"读取 SQL 文件失败: {str(e)}")
        return None

def fetch_data_from_oracle():
    """从 Oracle 数据库动态拉取水表数据（使用外部 SQL 文件）"""
    datas_list = []
    
    # 1. 加载外部 SQL
    sql = load_sql_from_file("get_water_comsumption.sql")
    if not sql:
        return datas_list
        
    try:
        # 2. 连接 Oracle (Thick 模式)
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        cursor = connection.cursor()
        
        # 3. 直接执行 SQL（无需再传参）
        cursor.execute(sql)
        
        for row in cursor:
            datas_list.append({
                "REGION_ID": str(row[0] or ""),
                "RTU_ID": str(row[1] or ""),
                "BEGIN_DATE": str(row[2] or ""),
                "END_DATE": str(row[3] or ""),
                "WATER": str(row[4] or "0")
            })
            
        cursor.close()
        connection.close()
        logging.info(f"从 Oracle 成功读取到合并后的有效数据共 {len(datas_list)} 条。")
    except Exception as e:
        logging.error(f"Oracle 数据库读取异常: {str(e)}")
        
    return datas_list

def push_water_data(token: str, all_datas: list):
    # 拼接 URL: 服务名/方法名
    url = f"{BASE_URL}/EIDSApi_WB/ReceiveDataAPI/ReceiveWaterData"

    total = len(all_datas)

    if total == 0:
        logging.warning("没有需要推送的水表数据。")
        return

    # 按 BATCH_SIZE 进行切片循环
    for i in range(0, total, BATCH_SIZE):
        batch = all_datas[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        
        payload = {
            "token": token,
            "EntityData": [
                {
                    "Datas": batch
                }
            ]
        }
    
        # Headers 参数
        headers = {
            "Content-Type": "application/json",
            "token": token,
            "registerCode": REGISTER_CODE
        }
    
        # Body 参数（根据您的表格数据按需修改变量）
        payload = {
                "token": token,
                "EntityData": [
                    {
                        "Datas": batch
                    }
                ]
            }
    
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                logging.info(f"第 {batch_num} 批数据推送成功（包含 {len(batch)} 条），响应: {response.text}")
            else:
                logging.warning(f"第 {batch_num} 批数据推送失败，状态码: {response.status_code}, 响应: {response.text}")
        except Exception as e:
            logging.error(f"第 {batch_num} 批数据请求异常: {str(e)}")
        
        # 批次之间稍微暂停 0.5 秒，避免对目标接口造成瞬时并发压力
        time.sleep(0.5)

# ==================== 4. 主控逻辑（定时任务入口） ====================
def main():
    logging.info("===== 每月定时任务开始执行（Oracle 模式） =====")

    # 1. 从 Oracle 批量获取动态数据
    all_datas = fetch_data_from_oracle()
    if not all_datas:
        logging.warning("未查询到任何有效数据，任务终止。")
        return

    # 2. 获取 Token
    token = get_token()
    if not token:
        logging.error("终止流程：未获取到有效的 Token。")
        return

    # 3. 拿着 Token 和数据开始分批推送
    push_water_data(token, all_datas)
    
    logging.info("===== 每月定时任务执行结束 =====\n")

if __name__ == "__main__":
    main()