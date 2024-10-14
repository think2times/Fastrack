import pandas as pd
import yfinance as yf
import talib

# 获取五粮液的历史数据
stock_code = "000858.SZ"  # 或者 "WHL.SS"，根据实际情况选择股票代码
start_date = "2020-01-01"
end_date = "2023-07-24"
data = yf.download(stock_code, start=start_date, end=end_date)

# 使用talib计算移动平均线和RSI指标
data["MA20"] = talib.SMA(data["Close"], timeperiod=20)
data["MA50"] = talib.SMA(data["Close"], timeperiod=50)
data["RSI"] = talib.RSI(data["Close"])

# 分析数据
latest_data = data.iloc[-1]
latest_close = latest_data["Close"]
latest_ma20 = latest_data["MA20"]
latest_ma50 = latest_data["MA50"]
latest_rsi = latest_data["RSI"]

# 根据策略判断买入和卖出点
if latest_close > latest_ma20 and latest_close > latest_ma50 and latest_rsi > 70:
    decision = "卖出"
elif latest_close < latest_ma20 and latest_close < latest_ma50 and latest_rsi < 30:
    decision = "买入"
else:
    decision = "观望"

# 输出分析结果
print("最新收盘价: ", latest_close)
print("最新20日均线: ", latest_ma20)
print("最新50日均线: ", latest_ma50)
print("最新RSI指标: ", latest_rsi)
print("决策: ", decision)
