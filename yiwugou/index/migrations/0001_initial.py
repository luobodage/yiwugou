# Generated by Django 3.1.7 on 2021-03-18 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_title', models.CharField(max_length=100, verbose_name='商品标题')),
                ('shop_price', models.CharField(max_length=20, verbose_name='商品价格')),
                ('shop_address', models.CharField(max_length=100, verbose_name='商品网址')),
                ('shop_factory', models.CharField(max_length=100, verbose_name='出厂商')),
                ('shop_store', models.CharField(max_length=100, verbose_name='门店地址')),
            ],
        ),
    ]
