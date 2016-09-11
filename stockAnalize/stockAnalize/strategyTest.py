#-*-coding:utf-8-*-

import  pandas as pd
import  matplotlib.pyplot as  plt
from until import readStockAndIndexData as read


date_line1 ,capital_line1 ,return_line1 ,index_change_line1 ,index_line1 = read.get_stock_data('sh600020','sz000002','2013-01-01','2014-12-31')

# 计算年化收益率函数
def annual_return(capital_line,date_line):
    # type: (list, list) -> object
    df = pd.DataFrame({'date':date_line,'capital':capital_line})
    df.sort_values(by='date',inplace=True)
    df.reset_index(drop=False,inplace=True)
    print df.head()
    rng = pd.period_range(df['date'].iloc[0],df['date'].iloc[-1],freq='D')
    print rng

    # 计算年化收益率
    annual=pow(df.ix[len(df.index)-1,'capital']/df.ix[0,'capital'],250/len(rng)-1)
    print '年化收益率：%s' %annual
    
annual_return(capital_line1,date_line1)