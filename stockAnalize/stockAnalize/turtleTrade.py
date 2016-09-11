#-*-coding:utf-8-*-

import pandas as  pd
import matplotlib.pyplot as  plt
import numpy as  np

index_data = pd.read_csv('../all_trading_data/stock data/sh600011.csv',parse_dates=['date'])
index_data.sort('date',inplace=True)

N1=10
N2=20

index_data = index_data[['date','high','low','change','close']]
index_data['最近N1个交易日的最高点'] = pd.rolling_max(index_data['high'],N1)
index_data['最近N1个交易日的最高点'].fillna(value=pd.expanding_max(index_data['high']),inplace=True)

index_data['最近N2个交易日的最低点']=pd.rolling_min(index_data['low'],N2)
index_data['最近N2个交易日的最低点'].fillna(value=pd.expanding_max(index_data['low']),inplace=True)

# 当当天的收盘价高于昨日的‘最近N1个交易日的最高点’时，将收盘发出的信号设定为1
buy_index = index_data[index_data['close']>index_data['最近N1个交易日的最高点'].shift(1)].index
# print index_data.loc[buy_index]
index_data['收盘发出的信号']=np.nan
index_data.loc[buy_index,'收盘发出的信号']=1
# print index_data[:60]

# 当当天的收盘价低于昨日的‘最近N2个交易日的最低点’时，将收盘发出的信号设定为0
sell_index = index_data[index_data['close']<index_data['最近N2个交易日的最低点'].shift(1)].index
index_data.loc[sell_index,'收盘发出的信号']=0

# print index_data[:-1]


# 计算当天的仓位,当天持有上证指数仓位为1，不持有仓位为0
index_data['当天的仓位']=index_data['收盘发出的信号'].shift(1)
index_data['当天的仓位'].fillna(method='ffill',inplace=True)

#
#
# # 当仓位为1时买入股票，当仓位为0时，空仓。计算股票指数
# index_data['资金指数']=(index_data['change']*index_data['当天的仓位']+1.0).cumprod
# initial_idx = index_data.iloc[0]['close']/(1+index_data.iloc[0]['change'])
# index_data['资金指数']*=initial_idx
# #
# print index_data[:30]


# 当仓位为1时，买入上证指数，当仓位为0时，空仓。计算从19920101至今的资金指数
index_data['资金指数'] = (index_data['change'] * index_data['当天的仓位'] + 1.0).cumprod()
initial_idx = index_data.iloc[0]['close'] / (1 + index_data.iloc[0]['change'])
index_data['资金指数'] *= initial_idx

print index_data[:40]
# 输出数据到指定文件
# index_data[['date', 'high', 'low', 'close', 'change', '最近N1个交易日的最高点',
#             '最近N2个交易日的最低点', '当天的仓位', '资金指数']].to_csv('turtle.csv', index=False, encoding='gbk')

# ==========计算每年指数的收益以及海龟交易法则的收益
index_data['海龟法则每日涨跌幅'] = index_data['change'] * index_data['当天的仓位']
year_rtn = index_data.set_index('date')[['change', '海龟法则每日涨跌幅']].\
               resample('A', how=lambda x: (x+1.0).prod() - 1.0) * 100
print year_rtn
index_data.set_index('date',inplace=True)


index_data[['资金指数','change']].plot()
plt.show()
