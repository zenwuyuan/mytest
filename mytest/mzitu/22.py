import os
import re
from time import perf_counter
from functools import wraps

import requests
from scrapy import Selector

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        cls_name = func.__name__
        fmt = '{cls_name} {args} spend time: {time:.5f}'
        print(fmt.format(cls_name=cls_name, args=args, time=end_time - start_time))
        return result
    return wrapper

def get_content_css(url):
    req = requests.get(url)
    content = req.content.decode('utf-8')
    selector = Selector(text=content)
    return selector

#获取最大页码
def get_page_items():
    items = []
    for num in range(1,192,1):
        selector = get_content_css('http://www.mzitu.com/page/' + str(num) +'/')
        item_urls = list(set(selector.css('#pins a::attr(href)').extract()))
        items.extend(item_urls)
    print("一共有 ",items.__len__(),' 组图片')
    return(items)

def get_images_detail(url):
    selector = get_content_css(url)
    print(url)
    title = str(selector.css('h2[class=main-title]::text').extract()[0]).replace(' ','')
    print(title)
    max_page = list(selector.css('.pagenavi span::text').extract())[-2]
    print('当前图集共有 ',max_page,' 张图片')
    dir_name = title.replace(':','').replace('?','').replace('"','').replace('|','').replace('>','').replace('<','')

    if os.path.exists(dir_name):
        print(dir_name,' 已存在，跳过')
    else:
        os.mkdir(dir_name)
        for num in range(1,int(max_page) + 1):
            image_url = get_image(url + '/' + str(num))
            download_image(dir_name, image_url)


def get_image(url):
    selector = get_content_css(url)
    image_url = str(selector.css('.main-image img::attr(src)').extract()[0])
    return(image_url)

@timer
def download_image(dir_name, image_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','Connection': 'Keep-Alive',
               'Referer': "http://www.mzitu.com/"}
    req = requests.get(image_url, headers=headers)
    image = req.content
    filename = dir_name + image_url.rsplit('/', 1)[-1]
    save_path = os.path.join(dir_name, filename)
    with open(save_path, 'wb') as f:
        f.write(image)

# get_images_detail('http://www.mzitu.com/26972')

if __name__ == "__main__":
    start = perf_counter()
    for item in get_page_items():
        get_images_detail(item)
    end = perf_counter()
    print(format('end', '*^100'))
    print('download all images cost time:{:.3f}'.format(end - start))



