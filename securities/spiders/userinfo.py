# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from bs4.element import Tag
from securities.spiders.savecsv import save_csv
from securities.items import BookItem


class UserinfoSpider(scrapy.Spider):
    name = 'userinfo'
    allowed_domains = ['www.gutenberg.org']
    home_url = 'https://www.gutenberg.org'
    start_urls = [home_url + '/browse/scores/top#books-last1m']

    def parse(self, response, **args):
        soup = BeautifulSoup(response.text)
        urls = []
        suffix = '.txt.utf-8'
        for menu in soup.select("ol"):
            for child in menu.contents:
                if isinstance(child, Tag):
                    url = child.contents[0]['href']
                    if 'ebooks' in url:
                        urls.append(url + suffix)
        for url in urls:
            yield scrapy.Request(url=self.home_url + url, callback=self.get_info)

    def get_info(self, response):
        item = BookItem()
        item['title'] = re.findall("Title:(.*)", response.text)[0]
        item['author'] = re.findall("Author:(.*)", response.text)[0]
        item['content'] = response.text
        yield item


