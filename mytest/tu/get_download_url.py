#!/usr/bin/env python3

# _*_coding: utf-8_*_
import os
import asyncio
from functools import wraps
from time import perf_counter
import aiohttp
import aiofiles
from scrapy import Selector


def timer(func):
    """
    :param func: remeber_time
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        cls_name = func.__name__
        print('{cls_name} spend time: {time:.5f}'.format(cls_name=cls_name, time=end_time - start_time))
        return result
    return wrapper

class MeiZiTuDownload:
    def __init__(self, *, genre: str='cute', start_page_num: int=1, end_page_num: int=5, step: int=1):
        self.base_url = 'http://www.meizitu.com/a/{genre}_{page_num}.html'
        self.start_num = start_page_num
        self.end_num = end_page_num
        self.step = step
        self.genre = genre
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    async def get_html_content(self, url: str):
        """
        :param url: page_url
        :return:    page_html
        """
        req = await aiohttp.request('GET', url, headers=self.headers)
        content = await req.read()
        content = content.decode('gbk')
        return content

    async def get_page_item(self, page_num: int):
        """
        :param page_num: get_page_url
        :return:
        """
        item_url = self.base_url.format(genre=self.genre, page_num=page_num)
        content = await self.get_html_content(item_url)
        selector = Selector(text=content)
        urls = list(set(selector.css('#maincontent a::attr(href)').extract()))
        page_items = (url for url in urls if url.startswith('http://www.meizitu.com/a/'))
        for item in page_items:
            await self.get_item(item)

    async def get_item(self, item: str):
        """
        :param item:
        :return:
        """
        item_content = await self.get_html_content(item)
        selector = Selector(text=item_content)
        dir_name = selector.css('#maincontent div.metaRight h2 a::text').extract_first()
        image_urls = selector.css('#picture p img::attr(src)').extract()
        'ok' if os.path.exists(dir_name) else os.mkdir(dir_name)
        for image_url in image_urls:
            image_name = image_url.rsplit('/', 1)[-1]
            save_path = os.path.join(dir_name, image_name)
            await self.download_images(save_path, image_url)

    async def download_images(self, save_path: str, image_url: str):
        """
        :param save_path:
        :param image_url:
        :return:
        """
        req = await aiohttp.ClientSession.get(image_url, headers=self.headers)
        #req = await aiohttp.request('GET', image_url, headers=self.headers)
        image = await req.read()
        fp = await aiofiles.open(save_path, 'wb')
        await fp.write(image)

    async def __call__(self, page_num: int):
        await self.get_page_item(page_num)

    def __repr__(self):
        cls_name = type(self).__name__
        return '{cls_name}{args}'.format(cls_name=cls_name, args=(self.genre, self.start_num, self.end_num, self.step))


if __name__ == "__main__":
    start = perf_counter()
    download = MeiZiTuDownload(genre='cute')
    loop = asyncio.get_event_loop()
    to_do = [download(num) for num in range(1, 4)]
    wait_future = asyncio.wait(to_do)
    resp, _ = loop.run_until_complete(wait_future)
    loop.close()
    end = perf_counter()
    func_name = download.__class__.__name__
    spend_time = end - start
    print(format('end', '*^100'))
    print('{func_name} spend time: {time:.5f}'.format(func_name=func_name, time=spend_time))