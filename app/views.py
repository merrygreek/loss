from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from flask_appbuilder import AppBuilder, expose, BaseView,has_access
from app import appbuilder,db
from flask_appbuilder.views import ModelView, CompactCRUDMixin
from app.models import Project, ProjectFiles

from pyecharts.charts import Page
from pyecharts import options as opts
from pyecharts.charts import Bar
from jinja2 import Markup
from . import cal

from flask import flash, render_template
from flask_appbuilder import SimpleFormView
from flask_babel import lazy_gettext as _

from . import appbuilder, db
from .forms import MyForm
import os

from . import judge


from . import tree_com

from . import add_day

from . import cal_dl

from . import cal_dy

from flask import request

from flask_dropzone import utils


def draw_sxdl():
    k = []
    kj = []
    sea = {}
    seaj = {}
    io = judge.classfiy()['sxdl']
    io1 = judge.classfiy()['tqxs']

    mc = cal_dl.data_sxdl(io)
    mc1 = cal.data(io1)

    for i in mc.region:
        x,a,b,c,j= mc.day_sxdl(i)

        kxy = mc1.day_lineloss(i)
        rca = cal_dl.relation().curr_relation(x,a,kxy[0],kxy[1])
        rcb = cal_dl.relation().curr_relation(x,b,kxy[0],kxy[1])
        rcc = cal_dl.relation().curr_relation(x,c,kxy[0],kxy[1])

        rcj = cal_dl.relation().curr_relation(x,j,kxy[0],kxy[1])

        c,d = cal_dl.draw_sxdl().day_sxdl(x,i,a,b,c,kxy[0],kxy[1],rca,rcb,rcc,j,rcj)
        k.append(c)
        kj.append(d)
        sea[i] = c
        seaj[i] = d
    return k,kj,sea,seaj


def draw_sxdy():
    k = []
    sea = {}
    io = judge.classfiy()['sxdy']
    mc = cal_dy.data_sxdl(io)
    for i in mc.region:
        x,a,b,c,fc = mc.day_sxdl(i)
        c = cal_dy.draw_sxdl().day_sxdl(x,i,a,b,c,fc)
        k.append(c)
        sea[i] = c
    return k,sea





def draw_all_region():
    IO = judge.classfiy()['tqxs']
    k = []
    sea = {}
    day_loss = cal.data(IO)

    tq_index = day_loss.day_lineloss_index()

    for i in tq_index:
        x,y,a,z,m = day_loss.day_lineloss(i)
        nc = cal.relation().curr_relation(x,y,x,z)
        c = cal.drawing().day_loss_1(x,y, a,'相关性系数 '+str(nc)[:12],z,m)
        sea[a] = c
        k.append(c)
    return k,sea


def all_day_region():

    IO = judge.classfiy()['tqxs']
    name = judge.classfiy()['tqdl']
    num = cal.electricity(name).measure_num()
    day_loss = cal.data(IO)
    a,b,j,z,m = cal.data(IO).day_lineloss('沙垌村四')

    k1 = {}
    k2 = []
    for i in num:
        x,y,t = cal.electricity(name).day_data(i)
        c = cal.relation().curr_relation(a,b,x,y)
        k1[i] = c

    k3 = sorted(k1.items(),key = lambda item:item[1])

    for j in k3:
        x,y,t = cal.electricity(name).day_data(j[0])
        c1 = cal.drawing().day_loss_2(a,b,'测量点号: '+str(t)[:-2],'相关性系数 '+str(j[1])[:12],x,y)
        k2.append(c1)


    return k2

class regoin(BaseView):

    default_view = 'all_region'

    @expose('/all_region')
    @has_access
    def all_region(self):
        k =  draw_all_region()
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k[0]]).render_embed()
        , base_template=appbuilder.base_template, appbuilder=appbuilder)

    @expose('/topten')
    @has_access
    def ten_region(self):
        k =  draw_all_region()
        # return Markup(k[0])
        # return Markup(c)

        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k[0][:10]]).render_embed()
                , base_template=appbuilder.base_template, appbuilder=appbuilder)
        # return Markup(Page(layout=Page.SimplePageLayout).add(*[i for i in k[:10]]).render_embed())

class people_day(BaseView):

    default_view = 'positive'

    @expose('/positive')
    @has_access
    def positive(self):
        k =  all_day_region()
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k[:10]]).render_embed()
        , base_template=appbuilder.base_template, appbuilder=appbuilder)

    @expose('/negative')
    @has_access
    def negative(self):
        k =  all_day_region()
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k[-10:]]).render_embed()
                , base_template=appbuilder.base_template, appbuilder=appbuilder)



    @expose('/all')
    @has_access
    def all(self):
        k =  all_day_region()
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k]).render_embed()
                , base_template=appbuilder.base_template, appbuilder=appbuilder)





class MyFormView(SimpleFormView):
    form = MyForm
    form_title = "搜索"
    message = "提交"

    def form_get(self,form):
        pass



    def form_post(self, form):
        # post process form
        d = []
        mc = form.field1.data
        flash(mc, "info")
        kxy =  draw_all_region()
        d.append(kxy[1][mc])
        kdl =  draw_sxdl()
        d.append(kdl[2][mc]) 
        d.append(kdl[3][mc])
        kdy = draw_sxdy()
        d.append(kdy[1][mc])
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in d]).render_embed()
                , base_template=appbuilder.base_template, appbuilder=appbuilder)



class compare_two(BaseView):

    default_view = 'comtwo'
    @expose('/file')
    @has_access
    def comtwo(self):
        k =  tree_com.tree_map()
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k]).render_embed(), base_template=appbuilder.base_template, appbuilder=appbuilder)

class minusTwo(BaseView):

    default_view = 'two'
    @expose('/two')
    @has_access
    def two(self):
        k =  add_day.draw()
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k]).render_embed(), base_template=appbuilder.base_template, appbuilder=appbuilder)

class sxdl_day(BaseView):

    default_view = 'one'
    @expose('/one')
    @has_access
    def one(self):
        k =  draw_sxdl()
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k[0]]).render_embed(), base_template=appbuilder.base_template, appbuilder=appbuilder)
    
    @expose('/two')
    @has_access
    def two(self):
        k =  draw_sxdl()        
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k[1]]).render_embed()
                , base_template=appbuilder.base_template, appbuilder=appbuilder)

class sxdy_day(BaseView):

    default_view = 'one'
    @expose('/one')
    @has_access
    def one(self):
        k =  draw_sxdy()
        # return Markup(k[0])
        # return Markup(c)
        return render_template("charts.html", myechart = Page(layout=Page.SimplePageLayout).add(*[i for i in k[0]]).render_embed(), base_template=appbuilder.base_template, appbuilder=appbuilder)

class MyFileView(BaseView):
    default_view = 'upload'
    @expose('/one',methods = ['get','post'])
    @has_access
    def upload(self):
        if request.method == 'POST':
            for key, f in request.files.items():
                if key.startswith('file'):
                    f.save(os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads'), utils.random_filename(f.filename)))
        return render_template("upload.html",base_template=appbuilder.base_template, appbuilder=appbuilder)





db.create_all()

appbuilder.add_view(
    MyFileView, "上传文件", icon="fa-table"
)
appbuilder.add_view(
    compare_two, "档案对比", icon="fa-table"
)
appbuilder.add_view(
    minusTwo, "电量对比", icon="fa-table"
)


appbuilder.add_view(sxdl_day, "三相电流", category='电流')
appbuilder.add_link("方差",href = '/sxdl_day/two' , category='电流')

appbuilder.add_view(
    sxdy_day, "三相电压", icon="fa-table"
)




appbuilder.add_view(regoin, "所有台区", category='台区')
appbuilder.add_link("前十台区",href = '/regoin/topten' , category='台区')

appbuilder.add_view(people_day, "正相关前十", category='用户')
appbuilder.add_link("负相关前十",href = '/people_day/negative' , category='用户')
appbuilder.add_link("全部用户",href = '/people_day/all' , category='用户')

appbuilder.add_view(
    MyFormView,"台区数据搜索", icon="fa-table"
)






@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )



db.create_all()
