import pandas as pd
import numpy as np
from pyecharts.charts import Page,Line
import pyecharts.options as opts

class data():

    def __init__(self,df):
        self.df = df
        self.region = set(i for i in self.df.台区名称)

    def day_lineloss(self,a):
        
        tq = self.df[self.df.台区名称== a ][['日期','线损率(%)','供入电量(kWh)','数据完整率(%)']].set_index('日期').sort_values(by='日期')
        x  = [i[-5:] for i in tq.index]
        y  = [i[0] for i in tq.values]
        z  = [i[1] for i in tq.values]
        m  = [i[2] for i in tq.values]

        return x,y,a,z,m

    def day_lineloss_index(self):
        num = {}
        for i in self.region:
            ndf = self.df[self.df.台区名称 == i][['日期','线损率(%)']]
            ndf.columns = ['日期','线损率']
            num[i] = ndf[ndf.线损率>6].count()[0]

        list_index = sorted(num.items(),key=lambda x:x[1],reverse=True)

        return [ i[0] for i in list_index]

    def day_electricity(self):
        pass


class drawing():
    def __init__(self):
        pass

    def all_day_lineloss(self,k,name):
        Page().add(*[i for i in k]).render(name + '.html')

    def dayloss_line_base(self,x,y,t,st):
        c = (
            Line(init_opts=opts.InitOpts(width="1000px", height="500px"))
            .add_xaxis(x)
            .add_yaxis("线损率(%)", y,is_smooth=True)
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
                ),
                title_opts=opts.TitleOpts(title=t, subtitle=st),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90),max_interval=366,
                            type_="category",axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),),
                yaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),

                ),
                toolbox_opts=opts.ToolboxOpts(feature = opts.ToolBoxFeatureOpts(save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio= 2,background_color= 'white'),restore= opts.ToolBoxFeatureRestoreOpts(is_show=False), data_view= opts.ToolBoxFeatureDataViewOpts(is_show=False),data_zoom= opts.ToolBoxFeatureDataZoomOpts(is_show=False), magic_type= opts.ToolBoxFeatureMagicTypeOpts(is_show=False), brush= opts.ToolBoxFeatureBrushOpts(type_= 'clear')
                ,))
               )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(y=6),
                         ],
                    label_opts=opts.LabelOpts(is_show=False),

                ),

            )

        )
        return c

    def day_loss_1(self,x,y,t,st,z,m):
        c = self.dayloss_line_base(x,y,t,st)
        c = c.extend_axis(
                yaxis=opts.AxisOpts(name = '供电量',
                    axislabel_opts=opts.LabelOpts(formatter="{value} kWh")
                )
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name = '数据完整率',
                    position = 'right',
                    offset = 62,
                    axislabel_opts=opts.LabelOpts(formatter="{value} "),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color="#675bba")
                    ),

                )
            )

        line = Line().add_xaxis(x).add_yaxis("供入电量", z,yaxis_index=1,is_smooth=True).set_series_opts(
                label_opts=opts.LabelOpts(is_show=False), )
        
        line_1 = Line().add_xaxis(x).add_yaxis("数据完整率", m,yaxis_index=2).set_series_opts(
                label_opts=opts.LabelOpts(is_show=False), )
        
        
        c.overlap(line)
        c.overlap(line_1)
        return c

    def day_loss_2(self,x,y,t,st,a,b):
        c = self.dayloss_line_base(x,y,t,st)
        c = c.extend_axis(
                yaxis=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} kWh")
                )
            )
        line = Line().add_xaxis(a).add_yaxis("用电量", b,yaxis_index=1,is_smooth=True).set_series_opts(
            label_opts=opts.LabelOpts(is_show=False), )  
    
        c.overlap(line)
        return c

class electricity():
    """docstring for electricity"""
    def __init__(self,df):
        self.df = df

    def day_data(self,a):
        tq = self.df[self.df.测量点号==a][['数据时间','正向']].set_index('数据时间').sort_values(by='数据时间')
        x = [i[-5:] for i in tq.index]
        y = [float(i[0]) for i in tq.values]
        t = a
        return x,y,t

    def measure_num(self):
        num = set(i for i in self.df.测量点号)
        num = list(num)[1:]
        return num

class relation(object):
    """docstring for relation"""

    def curr_relation(self,x,y,a,b):
        lineloss = pd.Series(y,index=x)
        day_electricity = pd.Series(b,index= a)
        c = lineloss.corr(day_electricity)
#         c1 = lineloss.cov(day_electricity)
        return c
        
# IO = '石鼓12月.xls'
# k = []
# day_loss = data(IO)

# tq_index = day_loss.day_lineloss_index()

# for i in tq_index:
#     x,y,a,z,m = data(IO).day_lineloss(i)
#     nc = relation().curr_relation(x,y,x,z)
#     c = drawing().day_loss_1(x,y, a+ str(nc),z,m)
    
#     k.append(c)

# drawing().all_day_lineloss(k,'石鼓12')

# IO = '石鼓12月.xls'
# name = '宝丰12.xlsx'
# num = electricity(name).measure_num()
# day_loss = data(IO)
# a,b,j,z,m = data(IO).day_lineloss('宝丰公用台变')



# k1 = []
# for i in num:
#     x,y,t = electricity(name).day_data(i)
#     c = relation().curr_relation(a,b,x,y)
#     c1 = drawing().day_loss_2(a,b,str(t)+' & '+str(c),x,y)
#     k1.append(c1)
    
# ny = np.array(electricity(name).day_data(92)[1]) + np.array(electricity(name).day_data(37)[1])


# c = relation().curr_relation(a,b,x,ny)


# c1 = drawing().day_loss_2(a,b,'9237'+str(c),x,ny)

# k1.append(c1)

# drawing().all_day_lineloss(k1,'宝丰12')

# k2 = []
# for i in num:
#     x,y,t = electricity(name).day_data(i)
#     c = relation().curr_relation(a,b,x,y)
#     k2.append(c)
#     print(str(c) + 10*'-'+str(i))
#     print(10*'--')

# k3 = []
# nyy= []
# for i in num:
#     x,y,t = electricity(name).day_data(i)
#     c = relation().curr_relation(a,b,x,y)
#     print(c[0])
#     if c[0] > 0.5:
#         nyy.append(np.array(y))
#         c1 = drawing().day_loss_2(a,b,t,x,y)
#         k3.append(c1)

# c2 = drawing().day_loss_2(a,b,'all',x,sum(nyy))
# k3.append(c2)

# drawing().all_day_lineloss(k3,'test_class_5')
# c = relation().curr_relation(a,b,x,sum(nyy))
# print(c)