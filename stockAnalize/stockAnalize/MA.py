#-*-coding:utf-8-*-

import pandas as pd
import matplotlib.pyplot as  plt
# 5日，10日移动平均线

stock_data= pd.read_csv('../data/stock data/sh600106.csv')
index_date = stock_data['date']
stock_data.set_index(index_date,inplace=True)
# print stock_data[:4]
print stock_data.index
print stock_data[:5]

stock_data.sort('date',inplace=True)

ma_param=[5,10,30]

for m in ma_param:
    stock_data['MA'+str(m)]=pd.rolling_mean(stock_data['close'],m)

for ma in  ma_param:
    stock_data['EMA'+str(ma)]=pd.ewma(stock_data['close'],span=ma)

stock_data.sort('date',ascending=True,inplace=True)
# stock_data.to_csv('shsh600107.csv',index=True)

stock_data['MA5'].plot()
plt.show()