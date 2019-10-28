'''
    Spider name: xmlsample

    Crawl XML content from sample site.

    Arguments:
        None.

    Usage:
        $ scrapy crawl --nolog xmlsample -o xmlsample.csv   # Output csv file.
        $ scrapy crawl xmlsample -o xmlsample.json -s FEED_EXPORT_ENCODING=utf-8 -s FEED_EXPORT_INDENT=4   # Output json file and encoding as utf-8.

    RSS/XML Feed Sample Sites:
        - http://www.36kr.com/feed/
        - https://www.williamlong.info/rss.xml
        - https://www.huxiu.com/rss/0.xml
        - https://www.feng.com/rss.xml
        - https://cn.technode.com/feed/
        - http://www.techweb.com.cn/rss/allnews.xml
        - https://www.tmtpost.com/rss.xml
        - https://www.pingwest.com/feed
        - https://www.meihua.info/feed
        - https://www.leiphone.com/feed
        - http://www.geekpark.net/rss
        - http://news.163.com/special/00011K6L/rss_newsattitude.xml
        - https://cn.engadget.com/rss.xml
        - http://rss.sina.com.cn/tech/rollnews.xml
        - https://www.iyiou.com/feed
        - https://www.lieyunwang.com/newrss/feed.xml
        - https://www.ithome.com/rss/
        - http://rss.yesky.com/index.xml
'''
# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from spytest.items import XMLSampleItem


class xmlSampleSpider(XMLFeedSpider):
    name = 'xmlsample'
    allowed_domains = ['36kr.com']
    start_urls = ['http://www.36kr.com/feed/']
    iterator = 'iternodes' # Optional value: 'iternodes', 'html' or 'xml'.
    itertag = 'item' # change it accordingly

    def parse_node(self, response, node):
        item = XMLSampleItem()
        item['author'] = node.xpath('//item/author/text()').get()
        item['title'] = node.xpath('//item/title/text()').get()
        item['category'] = node.xpath('//item/category/text()').get()
        item['link'] = node.xpath('//item/link/text()').get()
        item['description'] = node.xpath('//item/description/text()').get()
        return item
