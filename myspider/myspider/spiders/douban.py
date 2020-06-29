# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider

from myspider.items import MyspiderItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        for item in response.css('.item'):
            movie = MyspiderItem()
            movie['Staring'] = item.css('.bd p::text').extract_first()
            movie['rank'] = item.css('.pic em::text').extract_first()
            movie['title'] = item.css('.hd span.title::text').extract_first()
            movie['start'] = item.css('.star span.rating_num::text').extract_first()
            movie['quote'] = item.css('.quote span.inq::text').extract_first()
            movie['url'] = item.css('.pic a::attr("href")').extract_first()
            movie['image_url'] = item.css('.pic img::attr("src")').extract_first()
            yield movie
        next_url = response.css('span.next a::attr("href")').extract_first()
        if next_url is not None:
            url = self.start_urls[0] + next_url
            yield scrapy.Request(url=url, callback=self.parse)
