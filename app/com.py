import pandas as pd
from . import cal 
from . import judge

def compare():
    k = judge.classfiy()
    jl = k['cldh']
    yx = k['yxzl']
    jlsstq = k['sstq']

    jlbh=jl.电表资产编号
    yxbh=yx.资产编号

    m = []
    for i in jlbh.values:
        if i not in yxbh.values:
            m.append(i)

    for i in yxbh.values:
        if i not in jlbh.values:
            m.append(i)


    cldh = jl.测量点号
    cldh_count = cldh.value_counts()
    cldh_judge = cldh_count>1
    repr_cldh = [i for i in cldh_judge[cldh_judge.values == True].index]
    if not repr_cldh:
        repr_cldh = '无'
    tqmc = [i for i in yx.台区名称.unique()]

    sstq = [i for i in jlsstq.所属台区.unique()]


    return [m,repr_cldh,tqmc,sstq]






