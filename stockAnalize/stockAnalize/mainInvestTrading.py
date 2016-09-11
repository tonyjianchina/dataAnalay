#-*-coding:utf-8-*-

import pandas as  pd
import os
import numpy as np
import matplotlib.pyplot as  plt
from until import readFiles as rf

files = rf.get_all_stock('../data/dailyData')

all_stocks=[]
for f in files:
    if '.csv' in f:
        all_stocks.append(f.split(' ')[1])


print all_stocks

output = pd.DataFrame()

for stock in all_stocks:
    code = stock.split('.csv')[0].strip()
    print code
    stock_data = pd.read_csv('../data/dailyData/2015-05-19 '+stock,parse_dates=[0])
    stock_data['money']=stock_data['Volume']*stock_data['Price']
    # print stock_data[:4]

    l=len(output)
    output.loc[l,'code']=code
    output.loc[l,'mean']=stock_data['Volume'].mean()

    data = stock_data.groupby('BuySell')['money'].sum()
    if 'B' in data.index:
        output.loc[l,'Buy']=data['B']
    if 'S' in data.index:
        output.loc[l,'Sell']=data['S']

    data2 = stock_data[stock_data['Volume']>5000].groupby('BuySell')["money"].sum()
    if 'B' in data2.index:
        output.loc[l,'mainBuy']=data2['B']
    if 'S' in data2.index:
        output.loc[l,'mainSell']=data2['S']

# output.to_csv('mainInvestTrading.csv',index=False,encoding='gbk')

# plt.figure(figsize=(2,1))
output.set_index('code',inplace=True)
output[['Buy','mainBuy','Sell','mainSell']].plot()
plt.title('stocks')
plt.legend(loc='best')
plt.xlabel("money")
plt.ylabel("stock_code")
plt.show()