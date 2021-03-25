from django.contrib import admin
from index.models import Shop
from .models import *


# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_title', 'shop_price', 'shop_factory', 'shop_store', 'shop_address')


admin.site.register(Shop, ShopAdmin)
