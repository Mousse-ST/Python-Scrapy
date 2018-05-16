# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib
import scrapy
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline


class MoviePipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'meiju1':
            with open("my_meiju.txt", 'w', encoding="utf8") as fp:
                fp.write(item['name'] + '\n')
        elif spider.name == 'meiju2':
            print(11)
            pass
        elif spider.name == 'meiju3':
            if not os.path.exists("MovieList"):
                os.mkdir("MovieList")
            with open('MovieList/' + item['movie_name'], 'a', encoding="utf8") as fp:
                #fp.writelines(item['download_urls'])
                for each in item['download_urls']:
                    fp.write(each + '\n')
        return item


class MyImagesPipeline(ImagesPipeline):
    # 图片重命名
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print(1, image_url)
            yield Request(image_url)

    def item_completed(self, results, item, info):
        print(results)
        image_paths = [x['path'] for ok, x in results if ok]
        print(2, image_paths)
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
