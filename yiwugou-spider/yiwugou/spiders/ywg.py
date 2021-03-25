import re

import scrapy
from urllib.parse import urlencode
from yiwugou.items import YiwugouItem


class YwgSpider(scrapy.Spider):
    name = 'ywg'
    allowed_domains = ['https://www.yiwugo.com/']

    # start_urls = ['https://www.yiwugo.com//']

    def start_requests(self):
        """
        分页
        :return:返回网址
        """
        data = {
            'searchMethod': 'original',
            'q': '%E5%8F%91%E5%85%89%E7%8E%A9%E5%85%B7',
            'spm': 'd3d3Lnlpd3Vnby5jb20v',
        }
        base_url = 'https://www.yiwugo.com/search/s.html?'
        for page in range(1, 47):
            data['cpage'] = page
            params = urlencode(data)
            url = base_url + params
            # print(url)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        # normalize-space去掉 空格 \n \t
        item = YiwugouItem()
        title = []
        shop_url = []
        price = []
        company = []
        address = []
        content = response.xpath('//div[@class=\'pro_list_product_img2\']/ul')
        for i in range(len(content)):
            title_ = content.xpath('normalize-space(li[1]/a/text())').extract()[i]
            title.append(title_)
            companyName = content.xpath('normalize-space(li[3]/font/a/text())').extract()[i]
            company.append(companyName)
            companyAddress = content.xpath('normalize-space(li[4]/text())').extract()[i]
            address.append(companyAddress)
        href_ = content.xpath('li[1]/a/@href').extract()
        for href in href_:
            shop_url_ = 'https://www.yiwugo.com' + href
            shop_url.append(shop_url_)

        piece_list = content.xpath('li[2]/span[1]/em').extract()
        for price_ in piece_list:
            a = re.findall(r'>(.*?)<', price_)
            while '' in a:
                a.remove('')
            price.append(''.join(a))
        print(company)
        print(address)
        item['title'] = title
        item['shop_url'] = shop_url
        item['price'] = price
        item['company'] = company
        item['address'] = address
        yield item
        # print(title)
        # print(len(title))
        # print(len(shop_url))
        # print(shop_url)
        # print(len(price))
        # print(price)
        # print(response.text)
