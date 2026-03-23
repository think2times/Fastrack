import pandas as pd
from collections import Counter
import re

def extract_wechat_questions(input_file, output_file):
    # 1. 加载数据
    # 如果你的 CSV 没有表头，请根据实际情况添加 names=['时间', '昵称', '内容']
    df = pd.read_csv(input_file, encoding='utf-8-sig')
    
    # 2. 提取内容列
    raw_texts = df['内容摘要'].astype(str).tolist()

    # 3. 定义核心业务分类（根据你的数据样本提炼）
    # 只要内容包含以下关键词，就打上对应的“分类标签”
    categories = {
        "缴费/充值问题": ["缴费", "交费", "充值", "钱", "支付", "买水", "扣款", "余额"],
        "停水/无水咨询": ["停水", "没水", "不来水", "停了", "无水"],
        "发票/账单索取": ["发票", "开票", "账单", "电子票"],
        "户号/编号查询": ["户号", "用户号", "编号", "账号", "卡号", "表号"],
        "业务办理/过户": ["过户", "更名", "更名", "更名", "更名", "办理", "业务"],
        "故障报修/水表": ["水表", "坏了", "漏水", "维修", "故障", "水压"],
        "客服/人工咨询": ["人工", "客服", "电话", "没人接", "联系方式"],
        "水价查询": ["单价", "多少钱一方", "水价", "标准"]
    }

    # 4. 统计逻辑
    results = []
    
    for text in raw_texts:
        text = text.strip()
        # 跳过过短且无意义的（如 1, 11, 你好, 。）
        if len(text) < 2 and not text.isdigit():
            continue
        if text in ["你好", "您好", "有人吗", "1", "。"]:
            continue
            
        matched = False
        for cat, keywords in categories.items():
            if any(k in text for k in keywords):
                results.append(cat)
                matched = True
                break
        
        # 如果没匹配到预设分类，且字数适中，归为“其他具体问题”
        if not matched and 2 <= len(text) <= 20:
            results.append("其他提问: " + text)

    # 5. 统计频次
    counts = Counter(results)
    
    # 6. 整理并保存
    summary_df = pd.DataFrame(counts.most_common(), columns=['问题类别/具体内容', '提及频次'])
    
    # 计算百分比
    total = sum(counts.values())
    summary_df['占比'] = summary_df['提及频次'].apply(lambda x: f"{round(x/total*100, 2)}%")

    summary_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ 统计完成！前 10 大高频诉求是：\n{summary_df.head(10)}")

if __name__ == "__main__":
    extract_wechat_questions('data/1. cleaned_msgs.csv', 'data/2. msgs_faq.csv')