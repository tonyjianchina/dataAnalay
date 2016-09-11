#-*-coding:utf-8-*-

import  pandas as  pd
import matplotlib.pyplot as  plt
# 将日线数据转为周线


stock_data = pd.read_csv('../all_trading_data/stock data/sh600106.csv',parse_dates=[1])

# set index as date
stock_data.set_index('date',inplace=True)

period_type='W'

period_stock_data = stock_data.resample(period_type,how='last')
# print period_stock_data[:5]

# period_stock_data['change'] = stock_data.resample(period_type,how=lambda x : (x+1.0).prod()-1.0)

# 周线的【change】等于那一周中每日【change】的连续相乘
period_stock_data['change'] = stock_data['change'].resample(period_type, how=lambda x: (x+1.0).prod() - 1.0)
# 周线的【open】等于那一周中第一个交易日的【open】
period_stock_data['open'] = stock_data['open'].resample(period_type, how='first')
# 周线的【high】等于那一周中【high】的最大值
period_stock_data['high'] = stock_data['high'].resample(period_type, how='max')
# 周线的【low】等于那一周中【low】的最小值
period_stock_data['low'] = stock_data['low'].resample(period_type, how='min')
# 周线的【volume】和【money】等于那一周中【volume】和【money】各自的和
period_stock_data['volume'] = stock_data['volume'].resample(period_type, how='sum')
period_stock_data['money'] = stock_data['money'].resample(period_type, how='sum')

# 计算周线turnover
period_stock_data['turnover'] = period_stock_data['volume'] / \
                                (period_stock_data['traded_market_value']/period_stock_data['close'])

# 股票在有些周一天都没有交易，将这些周去除
period_stock_data = period_stock_data[period_stock_data['code'].notnull()]
period_stock_data.reset_index(inplace=True)


period_stock_data['high'].plot()
plt.show()

