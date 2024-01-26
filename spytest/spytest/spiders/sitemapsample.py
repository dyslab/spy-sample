'''
    Spider name: sitemapsample

    Crawl XML sitemap from sample site.

    Arguments: None.

    Usage:
    $ scrapy crawl sitemapsample -o sitemapsample.csv   # Output csv file.
    $ scrapy crawl sitemapsample -o sitemapsample.json  # Output json file.

    Sitemap/XML Feed Sample Sites:
    - https://www.sitemaps.org/sitemap.xml

    Last verified date: 22 Jan, 2024
'''
# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider
from spytest.items import SitemapSampleItem


class sitemapSampleSpider(SitemapSpider):
    name = 'sitemapsample'
    allowed_domains = ['sitemaps.org']
    sitemap_urls = ['https://www.sitemaps.org/sitemap.xml']
    sitemap_rules = [
        ('/zh_CN/', 'parse_url'),
        ('/zh_HK/', 'parse_url'),
        ('/en_GB/', 'parse_url'),
    ]   # Fetch pages based on the language code paths of 'sitemap.xml'

    def parse_url(self, response):
        item = SitemapSampleItem()
        self.logger.info(response.text)
        item['title'] = response.xpath('//title/text()').get()
        item['url'] = response.url
        item['content'] = response.text
        yield item
