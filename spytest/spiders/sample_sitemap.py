'''
    Spider name: sitemapsample

    Crawl XML sitemap from sample site.

    Arguments:
        None.

    Usage:
        $ scrapy crawl sitemapsample -o sitemapsample.csv   # Output csv file.

    Sitemap/XML Feed Sample Sites:
        - https://www.sitemaps.org/sitemap.xml
'''
# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider
from spytest.items import SitemapSampleItem


class sitemapSampleSpider(SitemapSpider):
    name = 'sitemapsample'
    allowed_domains = ['sitemaps.org']
    sitemap_urls = ['https://www.sitemaps.org/sitemap.xml']
    sitemap_rules = [('/en_GB/', 'parse_url'), ('/zh_CN/', 'parse_url')]

    def parse_url(self, response):
        item = SitemapSampleItem()
        item['title'] = response.xpath('//title/text()').get()
        item['url'] = response.url
        yield item
