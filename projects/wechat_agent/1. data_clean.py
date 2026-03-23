import pandas as pd

def clean_wechat_data(input_file, output_file):
    # 1. 加载数据
    # encoding='utf-8-sig' 是为了处理 Excel 导出的 BOM 编码
    df = pd.read_csv(input_file, encoding='utf-8-sig')

    print(f"原始数据量: {len(df)} 条")

    # 2. 定义无效内容的特征字符串
    # 这里使用变量，方便你以后增加新的过滤词
    garbage_text = "市民可通过水业集团公众号->企业服务->在线客服反馈全市涉水类问题"
    
    # 3. 执行过滤
    # ~ 表示“取反”，即保留不包含该字符串的行
    # na=False 处理空值情况
    df_cleaned = df[~df['内容摘要'].str.contains(garbage_text, na=False, case=False)]
    
    # 4. 进一步清洗：删除内容为空或只有空格的行
    df_cleaned = df_cleaned.dropna(subset=['内容摘要'])
    df_cleaned = df_cleaned[df_cleaned['内容摘要'].str.strip() != ""]

    # 5. 可选：删除过短的无意义回复（比如只发了“收到”、“111”等，视需求而定）
    # df_cleaned = df_cleaned[df_cleaned['内容'].str.len() > 2]

    print(f"清洗后剩余数据量: {len(df_cleaned)} 条")

    # 6. 保存结果
    df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"🎉 清洗完成！已保存至: {output_file}")

if __name__ == "__main__":
    # 请确保文件名与你本地一致
    clean_wechat_data('data/0. wechat_complete_msgs.csv', 'data/1. cleaned_msgs.csv')