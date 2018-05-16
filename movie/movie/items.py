# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Movie1Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()

class Movie2Item(scrapy.Item):
    # define the fields for your item here like:
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_names = scrapy.Field()

class Movie3Item(scrapy.Item):
    # define the fields for your item here like:
    movie_name = scrapy.Field()
    download_urls = scrapy.Field()
    download_titles = scrapy.Field()

