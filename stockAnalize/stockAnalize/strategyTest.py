#-*-coding:utf-8-*-

import  pandas as pd
import numpy as  np
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

    # # 画图
    # new_frame.set_index('date',inplace=True)
    # new_frame.plot()
    # plt.show()

# max_draw_back(date_line1,capital_line1)

# 计算平均涨幅
def average_change(date_line,return_line):
    df = pd.DataFrame({'date':date_line,'change':return_line})
    ave = df['change'].mean()
    print '平均涨幅为：%f'%ave

# average_change(date_line1,return_line1)


# 上涨概率
def prob_up(date_line, return_line):
    df = pd.DataFrame({'date': date_line, 'change': return_line})

    up = len(df[df['change'] > 0]['change'])
    up_f = float(up)
    titalCount = len(df['change'])
    prob = up_f / titalCount
    print format(prob,'.2%')  #以百分比方式输出
# prob_up(date_line1,return_line1)

# 计算最大涨跌天数
def max_success_up(dateline,return_line):
    df = pd.DataFrame({'date':dateline,'return':return_line})
    df['up']=np.nan
    # 将收益率大于零的up设为1
    df.ix[df['return']>0,'up']=1
    df.ix[df['return']<0,'up']=0
    df['up'].fillna(method='ffill',inplace=True)
    # print df

    # 计算最大上涨下跌天数
    sum_day = 1
    df['max_success']=pd.Series(np.nan)
    for i in range(len(df['up'])):
        if i==0:
            df.loc[i,'max_success']=sum_day
        elif (df['up'].iloc[i]==df['up'].iloc[i-1]==1) or (df['up'].iloc[i]==df['up'].iloc[i-1]==0):
            sum_day+=1
            df.loc[i, 'max_success'] = sum_day
        else:
            sum_day=1
            df.loc[i, 'max_success'] = sum_day

    # 画图
    # df.set_index('date',inplace=True)
    # df['max_success'].plot()
    # plt.show()

    # 获取最大上涨下跌天数
    max_up = df[df['up']==1].sort_values(by='max_success',ascending=False)['max_success'].iloc[0]
    max_down = df[df['up'] == 0].sort_values(by='max_success', ascending=False)['max_success'].iloc[0]
    print '最大上涨天数 ：%s,最大下跌天数：%s' %(max_up,max_down)

# max_success_up(date_line1,return_line1)


# 计算收益波动率和贝塔值

def volatility(date_line,return_line):
    df = pd.DataFrame({'date':date_line,'rtn':return_line})
    from math import sqrt
    # 计算受益波动率
    vol = df['rtn'].std() * sqrt(250)
    print '受益波动率为：%s' % format(vol,'.2%')

# volatility(date_line1,return_line1)

def beta(date_line,return_line,indexreturn_line):
    df = pd.DataFrame({'date':date_line,'rtn':return_line,'benchmark_rtn':indexreturn_line})
    # 账户收益和基准收益的协方差除以基准收益的方差
    b=df['rtn'].cov(df['benchmark_rtn'])/df['benchmark_rtn'].var()
    print 'beta值是：%s' %b


beta(date_line1)