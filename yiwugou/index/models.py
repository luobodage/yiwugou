from django.db import models


# Create your models here.

class Shop(models.Model):
    shop_title = models.CharField(max_length=100, verbose_name='商品标题')
    shop_price = models.CharField(max_length=20, verbose_name='商品价格')
    shop_address = models.CharField(max_length=100, verbose_name='商品网址')
    shop_factory = models.CharField(max_length=100, verbose_name='出厂商')
    shop_store = models.CharField(max_length=100, verbose_name='门店地址')
