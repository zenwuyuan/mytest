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
    content = req.content.decode('gbk')
    selector = Selector(text=content)
    return selector

url = 'http://www.meizitu.com/a/cute_1.html'

#获取页面中的图片组名和链接
def get_one_page_dict(url):
    selector = get_content_css(url)
    for num in selector.css('div.pic a'):
        yield{
            'url':num.css('a::attr(href)').extract_first(),
            'title':num.css('a>img::attr(alt)').extract_first(),
        }
    next_page = selector.css('.next.page-numbers a::attr(href)').exreact()
    if next_page is not None:
        yield scrapy

def get_all_page_dict(url,type_page_num):
    dicts = {}
    for page_num in range(1,type_page_num + 1):
        one_page_dict = get_one_page_dict(url + str(page_num) + '.html')

        dicts =dicts + one_page_dict
    print(len(dicts))
    return(dicts)

get_all_page_dict('http://www.meizitu.com/a/cute_',2)


group_url = 'http://www.meizitu.com/a/5222.html'

#通过图片组链接获取的最大页码
def get_group_max_page_num(group_url):
    selector = get_content_css(group_url)
    group_page_num = selector.css('div#wp_page_numbers').extract()[-2]
    return(group_page_num)

#获取图片的下载链接
def get_img_download_url(image_url):
    selector = get_content_css(image_url)
    img_download_url = selector.css('.main-image img::attr(src)').extract()
    return(img_download_url)

#判断文件夹是否存在，不存在则创建
def is_dir(dir_name):
    if os.path.exists(dir_name):
        return(True)
    else:
        os.mkdir(dir_name)
        return(False)

#过滤掉特殊字符
def filter_char(str):
    r = '["*/:;?\|]|[<b>]|[</b>]'
    return(re.sub(r,'',str))

#获取当前类型的最大页码
def get_mz_type_max_page_num(url):
    selector = get_content_css(url)
    type_page_num =selector.css('').extract()[-1]
    return(type_page_num)

#保存单张图片
@timer
def save_image(dir_name,image_download_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
               'Connection': 'Keep-Alive',
               'Referer': "http://www.mzitu.com/"}
    req = requests.get(image_download_url, headers=headers)
    con = req.content()
    filename = dir_name + image_download_url.rsplit('/', 1)[-1]
    save_path = os.path.join(dir_name, filename)
    with open(save_path, 'wb') as f:
        f.write(con)

#获取最大页码
def get_page_items():
    items = []
    for num in range(1,192,1):
        selector = get_content_css('http://www.mzitu.com/page/' + str(num) +'/')
        item_urls = list(set(selector.css('#pins a::attr(href)').extract()))
        items.extend(item_urls)
    print("一共有 ",items.__len__(),' 组图片')
    return(items)

def get_something_amazing(url):
    for num in get_mz_dict(url):
        print(num['url'], ' ', num['title'])

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
    pass

@timer
def download_image(dir_name, image_url):
    pass

#if __name__ == "__main__":
#    start = perf_counter()
 #   for item in get_page_items():
 #       get_images_detail(item)
 #   end = perf_counter()
 #   print(format('end', '*^100'))
  #  print('download all images cost time:{:.3f}'.format(end - start))