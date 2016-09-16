#-*-coding:utf-8-*-

import pandas as pd
import tushare as ts

def get_data(stock_code,index_code,start_time,end_time):
    #
    # stock_code:股票代码
    # index_code：指数代码
    # start_time：回测开始时间
    # end_time：回测结束时间

    stock_datas = ts.get_h_data(str(stock_code),autype='hfq')
    stock_datas['date']=stock_datas.index
    stock_datas.sort_index(ascending=True,inplace=True)
    stock_datas['p_change'] = (stock_datas['close']-stock_datas['close'].shift(1))/stock_datas['close'].shift(1)
    # print stock_datas[['date','close']].shift(1)

    index_datas = ts.get_hist_data('sh')
    index_datas['date']=index_datas.index
    date=pd.date_range(start_time,end_time)
    # print stock_datas
    # print index_datas


    # 读取回测期间的股票数据
    stock_data = stock_datas.ix[stock_datas['date'].isin(date),['date','p_change','close']]
    stock_data.sort_values(by='date' ,inplace=True)
    # print stock_data


    # 选取回测期间的指数数据
    date_list = list(stock_data.index.strftime('%Y-%m-%d'))
    # print type(date_list)
    # print date_list
    index_data = index_datas.ix[index_datas['date'].isin(date_list) ,['date','p_change','close']]
    # print index_data
    index_data.sort_values(by='date' ,inplace=True)
    # index_data.set_index('date' ,inplace=True)



    # 将数据序列转成list
    # date_line = list(index_data['date'].strftime('%Y-%m-%d'))  # 时间序列
    date_line = list(index_data['date'])
    # print index_data['date']
    capital_line = list(stock_data['close'])  # 账户价值
    return_line = list(stock_data['p_change'])  # 收益率
    indexchange_line = list(index_data['p_change'])  # 指数变化序列
    index_line = list(index_data['close'])  # 指数序列
    # print date_line,capital_line,return_line ,indexchange_line ,index_line

    return date_line ,capital_line ,return_line ,indexchange_line ,index_line


