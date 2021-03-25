# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pandas as pd
from sqlalchemy import create_engine

connect = create_engine('mysql+pymysql://root:1334@127.0.0.1:3306/yiwugou?charset=utf8')


class YiwugouPipeline:
    def process_item(self, item, spider):
        data = pd.DataFrame()
        data['商品标题'] = item['title']
        data['商品价格'] = item['price']
        data['商品地址'] = item['shop_url']
        data['出厂商'] = item['company']
        data['门店地址'] = item['address']
        data.to_sql('yiwugou_data', con=connect.engine, if_exists='append', index=False)
        print(data.head())
        return item
