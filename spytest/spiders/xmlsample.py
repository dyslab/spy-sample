# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider


class XmlsampleSpider(XMLFeedSpider):
    name = 'xmlsample'
    allowed_domains = ['sample.com']
    start_urls = ['http://sample.com/feed.xml']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        item = {}
        #item['url'] = selector.select('url').get()
        #item['name'] = selector.select('name').get()
        #item['description'] = selector.select('description').get()
        return item
