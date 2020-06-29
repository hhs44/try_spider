# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class MyspiderPipeline:

    def __init__(self) -> None:
        self.client = MongoClient(host="localhost", port=27017)
        self.col = self.client["douban_movie"]
        self.top250 = self.col.top250

    def process_item(self, item, spider):
        res = dict(item)
        self.top250.insert_one(res)
        return item

    def close_spider(self, spider):
        self.client.close()
