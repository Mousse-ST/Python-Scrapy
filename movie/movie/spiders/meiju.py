# -*- coding: utf-8 -*-
import scrapy
import os
from movie.items import Movie1Item
from movie.items import Movie2Item
from movie.items import Movie3Item

# 爬取美剧天堂最近更新的100美剧名称
class MeijuSpider1(scrapy.Spider):
    name = "meiju1"
    allowed_domains = ["meijutt.com"]
    start_urls = ['http://www.meijutt.com/new100.html']

    def parse(self, response):
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        for each_movie in movies:
            item = Movie1Item()
            item['name'] = each_movie.xpath('./h5/a/@title').extract()[0]
            print(item['name'])
            yield item

# 爬取美剧天堂最近更新的100美剧首页图
class MeijuSpider2(scrapy.Spider):
    # 爬虫名称，唯一
    name = "meiju2"
    # 允许访问的域
    allowed_domains = ["meijutt.com"]
    # 初始URL
    start_urls = ['http://www.meijutt.com/new100.html']
    # 设置一个空集合
    url_set = set()
    # 爬取首页
    def parse(self, response):
        # 获取所有首页的的地址链接
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        for each_movie in movies:
            url = each_movie.xpath('./h5/a/@href').extract()[0]
            url = 'http://www.meijutt.com' + url
            if url.startswith("http://www.meijutt.com/content/meiju"):
                if url in MeijuSpider2.url_set:
                    pass
                else:
                    MeijuSpider2.url_set.add(url)
                    yield scrapy.Request(url, callback=self.parseChild)
            else:
                pass
    # 爬取首页提供的子链接内的图片
    def parseChild(self, response):
        # 如果图片地址为指定开头，才取其名字及地址信息
        infoTitle = response.xpath('//div[@class="info-title"]')
        infoBox = response.xpath('//div[@class="info-box"]')
        if infoTitle and infoBox:
            # print(infoTitle, infoBox)
            # 分别处理每个图片，取出名称及地址
            item = Movie2Item()
            image_names = infoTitle.xpath('./h1/text()').extract()
            image_urls = infoBox.xpath('./div/div/img/@src').extract()
            item['image_names'] = image_names
            item['image_urls'] = image_urls
            # print(item['image_names'], item['image_urls'])
            # 返回爬取到的信息
            yield item

# 爬取美剧天堂最近更新的100美剧下载链接
class MeijuSpider3(scrapy.Spider):
    name = 'meiju3'
    allowed_domains = ['meijutt.com']
    start_urls = ['http://www.meijutt.com/new100.html']
    url_set = set()

    def parse(self, response):
        # 获取所有首页的的地址链接
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        for each_movie in movies:
            url = each_movie.xpath('./h5/a/@href').extract()[0]
            url = 'http://www.meijutt.com' + url
            if url.startswith("http://www.meijutt.com/content/meiju"):
                if url in MeijuSpider2.url_set:
                    pass
                else:
                    MeijuSpider2.url_set.add(url)
                    yield scrapy.Request(url, callback=self.parseChild)
            else:
                pass
    # 爬取具体子页面的链接
    def parseChild(self, response):
        # 如果图片地址为指定开头，才取其名字及地址信息
        infoTitle = response.xpath('//div[@class="info-title"]')
        downList = response.xpath('//div[@class="tabs-list current-tab"]/div[@class="down_list"]/ul/li/input')
        if infoTitle and downList:
            item = Movie3Item()
            item['movie_name'] = infoTitle.xpath('./h1/text()').extract()[0]
            item['download_titles'] = downList.xpath('@file_name').extract()
            item['download_urls'] = downList.xpath('@value').extract()

            # print(item['movie_name'],item['download_titles'],item['download_urls'])
            # 返回爬取到的信息
            yield item
