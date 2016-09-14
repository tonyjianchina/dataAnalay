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
    
# annual_return(capital_line1,date_line1)

# 计算最大回撤

def max_draw_back(date_line,capital_line):
    new_frame = pd.DataFrame({'date':date_line,'capital':capital_line})
    new_frame.sort_values(by='date',inplace=True)
    new_frame.reset_index(drop=True,inplace=True)

    new_frame['max2here']=pd.expanding_max(new_frame['capital']) #计算该日之前的最大受益
    new_frame['todayDrawBack']=new_frame['capital']/new_frame['max2here']-1

    # 计算最大回撤和结束时间
    temp=new_frame.sort_values(by='todayDrawBack').iloc[0][['date','todayDrawBack']]
    max_dd = temp['todayDrawBack']
    end_date=temp['date']


    # 计算开始时间
    pre_date = new_frame[new_frame['date']<=end_date]
    start_date = pre_date.sort_values(by='todayDrawBack',ascending=False).iloc[0]['date']

    print '最大回撤为%f,回撤开始时间为%s,回撤结束时间为%s' % (max_dd,start_date,end_date)

    # 画图
    new_frame.set_index('date',inplace=True)
    new_frame.plot()
    plt.show()

max_draw_back(date_line1,capital_line1)