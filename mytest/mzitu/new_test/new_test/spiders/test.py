import scrapy
from scrapy import Selector
import requests

class mingyanSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://lab.scrapyd.cn/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                '1': quote.css('span.text::text').extract_first(),
                '2': quote.xpath('span/small/text()').extract_first(),
            }
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, self.parse)

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



