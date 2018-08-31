import scrapy


class QuotesSpider(scrapy.Spider):
    name = "test02"
    start_urls = [
        'http://quotes.toscrape.com',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            print('----------------------')
            print(next_page)
            next_page = response.urljoin(next_page)
            print(next_page)
            print('-----------------------')
            yield scrapy.Request(next_page, callback=self.parse)