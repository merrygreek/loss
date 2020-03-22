from pyecharts import options as opts
from pyecharts.charts import Tree
from . import com

k =  com.compare()


data = [
    {
        "children": [
            {
                "children": [{"name": k[0]}],
                "name": "不一致的电表",
            },
            {
                "children": [{"name": k[1]}],
                "name": "重复的测量点号",
            },
            {
                "children": [{"name": k[2]}],
                "name": "营销系统台区",
            },            
            {
                "children": [{"name": k[3]}],
                "name": "计量系统台区",
            },

        ],
        "name": "营销计量档案比对结果",
    }
]
def tree_map():
    c = (
        Tree()
        .add("", data)
        .set_global_opts(title_opts={'text':'档案信息比对结果:'})
    )
    m = []
    m.append(c)
    return m