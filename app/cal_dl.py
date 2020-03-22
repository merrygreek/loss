import pandas as pd
import numpy as np
from pyecharts.charts import Page,Line
import pyecharts.options as opts


class data_sxdl():

    def __init__(self,df):
        self.df = df
        self.region = set(i for i in self.df.用户名称)

    def day_sxdl(self,mc):
        k = []
        tq = self.df[self.df.用户名称== mc ][['时间','A相电流','B相电流','C相电流']].set_index('时间')
        x  = [ i[5:10] for i in tq.index]
        a  = [ i[0] for i in tq.values]
        b  = [ i[1] for i in tq.values]
        c  = [ i[2] for i in tq.values]
        for i in range(len(a)):
            var = np.var([a[i],b[i],c[i]])
            k.append(var)



        return x,a,b,c,k

    def mc_sxdl(self):
        num = {}
        for i in self.region:
            ndf = self.df[self.df.用户名称 == i][['','线损率(%)']]
            ndf.columns = ['日期','线损率']
            num[i] = ndf[ndf.线损率>6].count()[0]

    #     list_index = sorted(num.items(),key=lambda x:x[1],reverse=True)

    #     return [ i[0] for i in list_index]




class draw_sxdl():
    def __init__(self):
        pass

    def all_day_lineloss(self,k,name):
        Page().add(*[i for i in k]).render(name + '.html')

    def day_sxdl(self,x,mc,a,b,c,m,n,rca,rcb,rcc,j,rcj):
        c = (
            Line(init_opts=opts.InitOpts(width="1000px", height="500px"))
            .add_xaxis(x)
            .add_yaxis("电流A",a,is_smooth=True,itemstyle_opts=opts.ItemStyleOpts(color='black'))
            .add_yaxis("电流B",b,is_smooth=True,itemstyle_opts=opts.ItemStyleOpts(color='blue'))
            .add_yaxis("电流C",c,is_smooth=True,itemstyle_opts=opts.ItemStyleOpts(color='green'))
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
                ),
                title_opts=opts.TitleOpts(title=mc, subtitle='A: ' + str(rca)[:12]+'  '+'B: ' + str(rcb)[:12]+'  '+'C: ' + str(rcc)[:12]+'  '),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90),max_interval=366,
                            type_="category",axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),),
                yaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} A"),
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),

                ),
                toolbox_opts=opts.ToolboxOpts(feature = opts.ToolBoxFeatureOpts(save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio= 2,background_color= 'white'),restore= opts.ToolBoxFeatureRestoreOpts(is_show=False), data_view= opts.ToolBoxFeatureDataViewOpts(is_show=False),data_zoom= opts.ToolBoxFeatureDataZoomOpts(is_show=False), magic_type= opts.ToolBoxFeatureMagicTypeOpts(is_show=False), brush= opts.ToolBoxFeatureBrushOpts(type_= 'clear')
                ,))
               )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
            ).extend_axis(
                yaxis=opts.AxisOpts( name= '线损率',
                    axislabel_opts=opts.LabelOpts(formatter="{value} %")
                )) )

        line = (Line(init_opts=opts.InitOpts(width="1000px", height="500px")).add_xaxis(m).add_yaxis("线损率", n,is_smooth=True,linestyle_opts=opts.LineStyleOpts(color="red", width=2, type_="solid")).set_series_opts(
                label_opts=opts.LabelOpts(is_show=False), ).set_global_opts(
                tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
                ),
                title_opts=opts.TitleOpts(title=mc, subtitle='相关性系数: '+str(rcj)[:12]),
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
            ).extend_axis(
                yaxis=opts.AxisOpts( name= '方差',
                    axislabel_opts=opts.LabelOpts(formatter="{value} ")
                )))

        line3 = (Line().add_xaxis(m).add_yaxis("线损率", n,yaxis_index=1,is_smooth=True,is_selected=False,linestyle_opts=opts.LineStyleOpts(color="red", width=2, type_="dotted")).set_series_opts(
        label_opts=opts.LabelOpts(is_show=False), ))

        line1 = Line().add_xaxis(x).add_yaxis("方差", j,yaxis_index=1,is_smooth=True,linestyle_opts=opts.LineStyleOpts(color="black", width=2, type_="solid")).set_series_opts(
        label_opts=opts.LabelOpts(is_show=False), )

        d = line.overlap(line1)

        c.overlap(line3)
        return c,d

#     def day_loss_1(self,x,y,t,st,z,m):
#         c = self.dayloss_line_base(x,y,t,st)
#         c = c.extend_axis(
#                 yaxis=opts.AxisOpts(
#                     axislabel_opts=opts.LabelOpts(formatter="{value} kWh")
#                 )
#             ).extend_axis(
#                 yaxis=opts.AxisOpts(
#                     name = '数据完整率',
#                     position = 'right',
#                     offset = 62,
#                     axislabel_opts=opts.LabelOpts(formatter="{value} "),
#                     axisline_opts=opts.AxisLineOpts(
#                         linestyle_opts=opts.LineStyleOpts(color="#675bba")
#                     ),

#                 )
#             )

#         line = Line().add_xaxis(x).add_yaxis("供入电量", z,yaxis_index=1,is_smooth=True).set_series_opts(
#                 label_opts=opts.LabelOpts(is_show=False), )
        
#         line_1 = Line().add_xaxis(x).add_yaxis("数据完整率", m,yaxis_index=2).set_series_opts(
#                 label_opts=opts.LabelOpts(is_show=False), )
        
        
#         c.overlap(line)
#         c.overlap(line_1)
#         return c

#     def day_loss_2(self,x,y,t,st,a,b):
#         c = self.dayloss_line_base(x,y,t,st)
#         c = c.extend_axis(
#                 yaxis=opts.AxisOpts(
#                     axislabel_opts=opts.LabelOpts(formatter="{value} kWh")
#                 )
#             )
#         line = Line().add_xaxis(a).add_yaxis("用电量", b,yaxis_index=1,is_smooth=True).set_series_opts(
#             label_opts=opts.LabelOpts(is_show=False), )  
    
#         c.overlap(line)
#         return c

# class electricity():
#     """docstring for electricity"""
#     def __init__(self,df):
#         self.df = df

#     def day_data(self,a):
#         tq = self.df[self.df.测量点号==a][['数据时间','正向']].set_index('数据时间').sort_values(by='数据时间')
#         x = [i[-5:] for i in tq.index]
#         y = [float(i[0]) for i in tq.values]
#         t = a
#         return x,y,t

#     def measure_num(self):
#         num = set(i for i in self.df.测量点号)
#         num = list(num)[1:]
#         return num

class relation(object):
    """docstring for relation"""

    def curr_relation(self,x,y,a,b):
        lineloss = pd.Series(y,index=x)
        day_electricity = pd.Series(b,index= a)
        c = lineloss.corr(day_electricity)
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