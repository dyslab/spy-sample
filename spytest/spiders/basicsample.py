# -*- coding: utf-8 -*-
import scrapy


class BasicsampleSpider(scrapy.Spider):
    name = 'basicsample'
    allowed_domains = ['sample.com']
    start_urls = ['http://sample.com/']

    def parse(self, response):
        pass
