import requests
from scrapy import Selector

def get_page_items(*, start_page_num: int=1, end_page_num: int=400, step: int=1):
    items = []
    for page_num in range(start_page_num, end_page_num + 1, step):
        base_url = 'http://www.meizitu.com/a/{genre}_{page_num}.html'
        req = requests.get(base_url.format(genre='cute', page_num=1))
        content = req.content.decode('gbk')
        selector = Selector(text=content)
        item_urls = list(set(selector.css('#maincontent a::attr(href)').extract()))
        items.extend(url for url in item_urls if url.startswith('http://www.meizitu.com/a/'))
    print(items.__len__())
    return items

print(get_page_items())


def get_images(item):
    req = requests.get(item)
    content = req.content.decode('gbk')
    selector = Selector(text=content)
    image_urls = list(set(selector.css('#maincontent p img::attr(src)').extract()))
    print(image_urls)


#for item in get_page_items():
#    get_images(item)