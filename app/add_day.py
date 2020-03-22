import pandas as pd
from . import judge
from pyecharts import options as opts
from pyecharts.charts import Bar


def change(df):
    df.apply(pd.to_numeric, errors='ignore')

def minus_two():
    k = judge.classfiy()
    yhdf = k['tqdl'].iloc[1:,:][['数据时间','正向']]
    tqdf = k['tqxs']
    change(yhdf)
    change(tqdf)

    df=  tqdf.sort_values(by='日期')
    ndf =df[df['台区名称']=='沙垌村四'][['日期','供出电量(kWh)']]

    yhdf.正向 = yhdf.正向.astype('float')


    minus = ndf.set_index('日期')['供出电量(kWh)']-yhdf.groupby('数据时间').sum()['正向']
    complete = df[df['台区名称']=='沙垌村四'].set_index('日期')['数据完整率(%)']
    return minus,complete,ndf.日期

k = minus_two()
x = []
y = []
for i in k[0]:
    y.append(i)
for i in k[2]:
    x.append(i[-5:])


def draw():
    c = (
        Bar(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add_xaxis(x
         )
        .add_yaxis('相差电量',y)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90)),
            title_opts=opts.TitleOpts(title="电量对比", subtitle="计量系统台区供出电量与台区用户用电量对比"),
            yaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} kWh")),
        )         
        .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),

                ))
    m = []
    m.append(c)

    return m
