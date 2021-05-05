from django.db import models


# Create your models here.

class Shop(models.Model):
    shop_title = models.CharField(max_length=100, verbose_name='商品标题')
    shop_price = models.CharField(max_length=20, verbose_name='商品价格')
    shop_address = models.CharField(max_length=100, verbose_name='商品网址')
    shop_factory = models.CharField(max_length=100, verbose_name='出厂商')
    shop_store = models.CharField(max_length=100, verbose_name='门店地址')


class ShowData(Shop):
    class Meta():
        proxy = True  # 使用代理
        verbose_name = "义乌购小商品数据展示"
        verbose_name_plural = verbose_name


class JiaQian(Shop):
    class Meta():
        proxy = True  # 使用代理
        verbose_name = "价钱数据区间统计"
        verbose_name_plural = verbose_name


class DiZhi(Shop):
    class Meta():
        proxy = True
        verbose_name = "厂家分布统计"
        verbose_name_plural = verbose_name


class ShouMai(Shop):
    class Meta():
        proxy = True  # 使用代理
        verbose_name = "售卖地点分布饼图"
        verbose_name_plural = verbose_name


class QiShou(Shop):
    class Meta():
        proxy = True  # 使用代理
        verbose_name = "起售量统计散点图"
        verbose_name_plural = verbose_name


class KuCun(Shop):
    class Meta():
        proxy = True
        verbose_name = "库存量对比统计图"
        verbose_name_plural = verbose_name


class GcJq(Shop):
    class Meta():
        proxy = True
        verbose_name = "工厂与价格对比"
        verbose_name_plural = verbose_name
