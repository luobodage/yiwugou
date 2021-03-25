# -*- coding: UTF-8 -*-
import random
import time
import lxml.etree as le
import pandas as pd
import pymongo
import requests
import threading
from threading import Lock, Thread
import os

conn = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = conn.dog
my_set = db.dog_message_multithreading


def dataCollection(originate, page, stride):
    """
    爬取页面内容 并且存入mongodb数据库
    :param originate: 起始页
    :param page: 页数
    :param stride: 步长
    :return:
    """
    for i in range(originate, page, stride):
        time.sleep(random.randint(1, 2))
        url = f'http://www.whippet.cn/forum.php?mod=forumdisplay&fid=260&page={i}'
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        content = requests.get(url, headers=headers).content
        respond = le.HTML(content)
        title = respond.xpath('//*[@id="moderate"]/li/div/div/a/text()')  # 获取标题
        area_a = respond.xpath('//*[@id="moderate"]/li/div/p/text()')  # 获取地点
        area = []
        for a in area_a:
            area.append(a.split(' - ')[0])  # 分割地点
        # print(area)
        variety_a = respond.xpath('//*[@id="moderate"]/li/div/ul/li[1]/text()')  # 获取品种
        variety = []
        for v in variety_a:
            variety.append(v.split(' : ')[1])  # 分割品种 源文件为 狗狗品种 : 波音达 只需要后者
        age_a = respond.xpath('//*[@id="moderate"]/li/div/ul/li[2]/text()')  # 获取狗狗年龄
        age = []
        for ag in age_a:
            age.append(ag.split(' : ')[1])  # 分割出年龄 源数据为 狗狗年龄 : 两年 我们只需要后者
        vaccine_a = respond.xpath('//*[@id="moderate"]/li/div/ul/li[3]/text()')  # 获取疫苗情况
        vaccine = []
        for va in vaccine_a:
            vaccine.append(va.split(' : ')[1])  # 分割出疫苗情况 源数据为 狗狗年龄 : 两年 我们只需要后者
        promulgator = respond.xpath('//*[@id="moderate"]/li/div/p/span/a[2]/text()')  # 发布人
        money_a = respond.xpath('//*[@id="moderate"]/li/div/span/em/text()')  # 狗狗价钱
        money = []
        for m in money_a:
            money.append(int(m[0:-1]))
        sellerPromise = respond.xpath('//*[@id="moderate"]/li/div/p/font/text()')  # 卖家承诺
        href_a = respond.xpath('//*[@id="moderate"]/li/div[2]/div[1]/a/@href')
        href = []
        for h in href_a:
            href.append('http://www.whippet.cn/' + h)

        data = pd.DataFrame()
        data['标题'] = title
        data['地点'] = area
        data['品种'] = variety
        data['年龄'] = age
        data['疫苗情况'] = vaccine
        data['发布人'] = promulgator
        data['狗狗价钱'] = money
        data['卖家承诺'] = sellerPromise
        data['详情页面'] = href
        print(data.head())
        data = data.to_dict(orient='record')
        try:
            my_set.insert_many(data)
        except:
            print(f'第{i}页爬取失败')
        time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    """
    五个线程同时进行加快爬虫速率
    """
    t1 = threading.Thread(target=dataCollection, args=(1, 200, 5))  # target是要执行的函数名（不是函数），args是函数对应的参数，以元组的形式存在
    t2 = threading.Thread(target=dataCollection, args=(2, 200, 5))
    t3 = threading.Thread(target=dataCollection, args=(3, 200, 5))
    t4 = threading.Thread(target=dataCollection, args=(4, 200, 5))
    t5 = threading.Thread(target=dataCollection, args=(5, 200, 5))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    # dataCollection(1, 200, 5)
    # dataCollection(2, 200, 5)
    # dataCollection(3, 200, 5)
    # dataCollection(4, 200, 5)
    # dataCollection(5, 200, 5)
