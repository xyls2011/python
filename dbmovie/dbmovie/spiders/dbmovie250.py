# -*- coding: utf-8 -*-
import scrapy
from dbmovie.items import DbmovieItem


class Dbmovie250Spider(scrapy.Spider):
    name = 'dbmovie250'
    # allowed_domains = ['movie.douban.com/top250']
    start_urls = ['https://movie.douban.com/top250']
    header = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header)

    def parse(self, response):
        for quote in response.css('div.item'):
            item = DbmovieItem()
            item['title'] = quote.css('div.info div.hd a span.title::text').extract_first()
            item['rating'] = quote.css('div.info div.bd div.star span.rating_num::text').extract_first()
            item['desc'] = quote.css('div.info div.bd p.quote span.inq::text').extract_first()
            yield item

        next_url = response.css('div.paginator span.next a::attr(href)').extract()
        print(next_url)
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            print(next_url)
            yield scrapy.Request(url=next_url, headers=self.header)