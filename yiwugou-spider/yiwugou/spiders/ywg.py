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
            'q': '%E5',
            'spm': 'd3d3Lnlpd3Vnby5jb20v',
        }
        base_url = 'https://www.yiwugo.com/search/s.html?'
        for page in range(1, 2):
            data['cpage'] = page
            params = urlencode(data)
            url = base_url + params
            # print(url)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        # normalize-space去掉 空格 \n \t
        # item = YiwugouItem()
        title = []
        shop_url = []
        price = []
        company = []
        address = []
        content = response.xpath('//div[@class=\'pro_list_product_img2\']/ul')
        # for i in range(len(content)):
        #     title_ = content.xpath('normalize-space(li[1]/a/text())').extract()[i]
        #     title.append(title_)
        #     companyName = content.xpath('normalize-space(li[3]/font/a/text())').extract()[i]
        #     company.append(companyName)
        #     companyAddress = content.xpath('normalize-space(li[4]/text())').extract()[i]
        #     address.append(companyAddress)
        href_ = content.xpath('li[1]/a/@href').extract()
        # print(href_)
        for href in href_:
            shop_url_ = 'https://www.yiwugo.com' + href
            shop_url.append(shop_url_)

        # piece_list = content.xpath('li[2]/span[1]/em').extract()
        # for price_ in piece_list:
        #     a = re.findall(r'>(.*?)<', price_)
        #     while '' in a:
        #         a.remove('')
        #     price.append(''.join(a))

        for url in shop_url:
            print(url)
            # yield scrapy.Request(url, callback=self.parse)
            yield scrapy.Request(url, callback=self.parse1, dont_filter=True)

    def parse1(self, response):
        # print(response.body)
        # content = response.xpath('//div[@class=\'view_tem_rightbord mt12px\']')
        # print(content)
        # shop_title = content.xpath(r
        #     'normalize-space(/div[@class=\'view_pro_con_about\']/div[@class=\'pro10_view_tit\']/span[1])').extract_first
        # print(shop_title)
        item = YiwugouItem()
        # shop_title = response.xpath("normalize-space(/html/body/div[6]/div[2]/div[3]/div[1]/span[1]/text())").extract_first()
        shop_title = response.xpath(
            "normalize-space(//div[@class='view_tem_rightbord mt12px']/div[@class='view_pro_con_about']/div[@class='pro10_view_tit']/span[1]/text())"
        ).extract_first()
        shop_briefIntroduction = response.xpath(
            "normalize-space(//div[@class='view_tem_rightbord mt12px']/div[@class='view_pro_con_about']/p[1]/text())"
        ).extract_first()
        shop_model = response.xpath(
            "normalize-space(//div[@class='view_tem_rightbord mt12px']/div[@class='view_pro_con_about']/div/ul/li["
            "1]/span[2]/text())"
        ).extract_first()
        # piece_list = content.xpath('li[2]/span[1]/em').extract()
        # for price_ in piece_list:
        #     a = re.findall(r'>(.*?)<', price_)
        #     while '' in a:
        #         a.remove('')
        #     price.append(''.join(a))
        shop_price_list = response.xpath(
            "//tr[@class='price-one'][1]/td/span/font/text()").extract()
        if shop_price_list == []:
            shop_price = 0
        else:
            shop_price = shop_price_list[0] + '.' + shop_price_list[1]

        # item['shop_title'] = shop_title
        # item['shop_briefIntroduction'] = shop_briefIntroduction
        # item['shop_model'] = shop_model

        print(shop_title)
        print(shop_briefIntroduction)
        print(shop_model)
        print(shop_price)
