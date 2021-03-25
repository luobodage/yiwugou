from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Line
from index.models import *
import pandas as pd

# Create your views here.
"""
数据预处理
"""
data = Shop.objects.all().values()
df = pd.DataFrame(data)  # 获取数据
row = df.index.size  # 获取数据行数
df = df[~(df['shop_price'].isin(['价格联系商家']))]  # 删除价格里面的‘价格联系商家’行
y = df[df['shop_price'].str.contains(',')]  # 找出shop_price里面有‘,’的行数
t1 = list(y.shop_price)  # 将含有','的所有元素以列表表示为t1
t2 = list(df.shop_price)  # 将所有数据以列表表示t2
ret = list(set(t2) ^ set(t1))  # 采用列表求差集的方法可将b列中所有含有','的元素去除去
df = df[df.shop_price.isin(ret)]  # 通过isin方法实现最终效果
df['shop_price'] = df['shop_price'].astype("float")
shop_price_mean = df['shop_price'].mean()  # 平均值
shop_data = df.groupby("shop_factory", as_index=False).agg(
    count=pd.NamedAgg(column="id", aggfunc="count", ))
# 店家数量
shop_number = shop_data.index.size
"""
分组之后形成新的DataFrame
 shop_factory  count
0                   91产品摄影      3
1                 MILANLUX      1
2      MOTARRO文具（全球招商代理加盟)      7
3               Sex player      2
4    【厂家直销】科美电器贸易有限公司（小家电)      1
..                     ...    ...
456                  黄美娟玩具      1
457            黑猫神日化股份有限公司      1
458                 默轩礼品笔业     13
459                   龙威帽业      2
460            龙泉市金茂五金有限公司      1
"""
shop_data = shop_data.sort_values(by="count", ascending=False)  # 排序
"""
 shop_factory  count
157            台州阿凡达胶业源头厂家     73
20                丹妮百货有限公司     64
251                  新华升贸易     54
36   义乌姐弟2元10元多元配货饰品百货美妆文具     51
409                   金财文具     49
..                     ...    ...
200                   少祥电筒      1
197                   小烽内裤      1
195                   家虹花叶      1
192             宏康劳保手套贸易公司      1
460            龙泉市金茂五金有限公司      1
"""
# 同上 这个是价格分组
shop_price = df.groupby("shop_price", as_index=False).agg(
    count=pd.NamedAgg(column="id", aggfunc="count", ))

# print(shop_price)
# 地址分组
shop_store = df.groupby("shop_store", as_index=False).agg(
    count=pd.NamedAgg(column="id", aggfunc="count", ))
data = {
    'row': row,
    'shop_price_mean': shop_price_mean,
    'shop_data_name': shop_data,
    'shop_price_name': shop_price['shop_price'],
    'shop_price_number': shop_price['count'],
    'shop_store_name': shop_store['shop_store'],
    'shop_store_number': shop_store['count'],
    'shop_number': shop_number

}
"""
数据处理结束 返回data
"""


def pie_html():
    """
    生成第一个饼图的html
    利用pyecharts
    :return:
    """
    c = (
        Pie(init_opts=opts.InitOpts(width="1800px", height="800px"))
            .add(
            "",
            [
                list(z)
                for z in zip(
                shop_data['shop_factory'][:20],
                shop_data['count'][:20]
            )
            ],
            center=["40%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="义务实体店分布数据"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("./templates/pie.html")
    )


def two_line_html():
    """
    通过数据库数据进行读取数据
    生成第二个line图
    :return: 返回一个html文件
    """
    all_data = []
    for row in shop_data.itertuples():
        # now_name 为列名
        a = [getattr(row, 'shop_factory'), getattr(row, 'count')]

        # print(type(getattr(row, 'shop_factory')))
        all_data.append(a)

    (
        Line(init_opts=opts.InitOpts(width="1680px", height="800px"))
            .add_xaxis(xaxis_data=[item[0] for item in all_data])
            .add_yaxis(
            series_name="",
            y_axis=[item[1] for item in all_data],
            yaxis_index=0,
            is_smooth=True,
            is_symbol_show=False,
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="出厂商主要分布"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[
                opts.DataZoomOpts(yaxis_index=0),
                opts.DataZoomOpts(type_="inside", yaxis_index=0),
            ],
            visualmap_opts=opts.VisualMapOpts(
                pos_top="10",
                pos_right="10",
                is_piecewise=True,
                pieces=[
                    {"gt": 0, "lte": 5, "color": "#096"},
                    {"gt": 5, "lte": 10, "color": "#ffde33"},
                    {"gt": 10, "lte": 20, "color": "#ff9933"},
                    {"gt": 20, "lte": 50, "color": "#cc0033"},
                    {"gt": 50, "lte": 100, "color": "#660099"},
                    {"gt": 100, "color": "#7e0023"},
                ],
                out_of_range={"color": "#999"},
            ),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name_location="start",
                min_=0,
                max_=100,
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
            ),
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": 5},
                    {"yAxis": 10},
                    {"yAxis": 30},
                    {"yAxis": 50},
                    {"yAxis": 100},
                ],
                label_opts=opts.LabelOpts(position="end"),
            )
        )
            .render("./templates/line.html")
    )


df['shop_title'] = df['shop_title'].astype(str).str[10:]
print(df.head())

print(df['shop_title'][:6])
print(df['shop_price'][:6])


def three_price_html():
    """
    生成第三个价格折线图
    :return:
    """

    c = (
        Line(init_opts=opts.InitOpts(width="1800px", height="800px"))

            .add_xaxis(list(df['shop_title']))
            .add_yaxis("商家", df['shop_price'], is_smooth=True)

            .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="价格区间面积图（紧贴 Y 轴）"),
            xaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                is_scale=False,
                boundary_gap=False,
            ),
        )
            .render("./templates/line_price.html")
    )


three_price_html()


def index(request):
    return render(request, 'index.html', data)


def pie(request):
    return render(request, 'pie.html')


def line(request):
    return render(request, 'line.html')


def line_price(request):
    return render(request, 'line_price.html')
