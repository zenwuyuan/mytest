import scrapy
from scrapy import Selector
import requests
import re

class mingyanSpider(scrapy.Spider):
    name = "test01"
    def start_requests(self):
        urls = [
            'https://search.jd.com/Search?keyword=123&enc=utf-8&pvid=b66eab1d2749198d849924ce8aa8ee',
            #'http://lab.scrapyd.cn/page/2/',
        ]
        yield scrapy.Request(urls[0],callback=self.parse)

    def parse(self, response):
        print('------------------------------')
        ss = response.body.decode('utf-8')
        print(type(ss))
        #yield re.find(r'SEARCH.adv_param=(.+*)',ss)
        yield ss
        print('-------------------------------')


def get_content_css(url):
    req = requests.get(url)
    content = req.content.decode('utf-8')
    selector = Selector(text=content)
    return selector

def get_one_page_dict(url):
    selector = get_content_css(url)
    for quote in selector.css('div.quote'):
        yield {
            '1': quote.css('span.text::text').extract_first(),
            '2': quote.xpath('span/small/text()').extract_first(),
        }
    next_page = selector.css('li.next a::attr("href")').extract_first()
    if next_page is not None:
        print(type(scrapy.Request(next_page,get_one_page_dict(next_page))))
        yield scrapy.Request(next_page,get_one_page_dict(next_page))
        #yield get_one_page_dict(next_page)



