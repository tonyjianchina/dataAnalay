#-*-coding:utf-8-*-
import pandas as  pd

# 读取股票&指数数据
def get_stock_data(stock_code ,index_code ,start_time ,end_time):
    #
    # stock_code:股票代码
    # index_code：指数代码
    # start_time：回测开始时间
    # end_time：回测结束时间

    # 读取股票数据
    stock_datas = pd.read_csv( '../data/stock data/' +str(stock_code ) +'.csv' ,parse_dates=['date'])
    # 读取指数数据
    index_datas = pd.read_csv('../data/stock data/' + str(index_code) + '.csv', parse_dates=['date'])
    date = pd.date_range(start_time ,end_time)

    # 读取回测期间的股票数据
    stock_data = stock_datas.ix[stock_datas['date'].isin(date) ,['date' ,'change' ,'adjust_price']]
    stock_data.sort_values(by='date' ,inplace=True)

    # 选取回测期间的指数数据
    date_list = list(stock_data['date'])
    index_data = index_datas.ix[index_datas['date'].isin(date_list) ,['date' ,'change' ,'close']]
    index_data.sort_values(by='date' ,inplace=True)
    index_data.set_index('date' ,inplace=True)
    # print index_data.index
    # print index_data.index.strftime('%Y-%m-%d')

    # 将数据序列转成list
    date_line = list(index_data.index.strftime('%Y-%m-%d'))  # 时间序列
    capital_line = list(stock_data['adjust_price'])  # 账户价值
    return_line = list(stock_data['change'])  # 收益率
    indexchange_line = list(index_data['change'])  # 指数变化序列
    index_line = list(index_data['close'])  # 指数序列

    return date_list ,capital_line ,return_line ,indexchange_line ,index_line
