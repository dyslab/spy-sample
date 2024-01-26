'''
    Spider name: xmlsample

    Crawl XML content from sample site.

    Arguments:
        target: [Optional] The target site url you want to fetch data. You could input sitename or part of the site url, and it will automatically pont to first matched item of the below list 'avaliable_sites'.

    Usage:
    $ scrapy crawl xmlsample                                        # Standard output for debug
    $ scrapy crawl --nolog xmlsample -o xmlsample.csv               # Output to a csv file.
    $ scrapy crawl xmlsample -o xmlsample.json -s FEED_EXPORT_ENCODING=utf-8 -s FEED_EXPORT_INDENT=3    # Output to a json file with set encoding to 'utf-8' and indent '3' spaces.
    $ scrapy crawl xmlsample -a target=feng.com -o xmlsample.json   # Fetch data and output to a json file from 'https://www.feng.com/rss.xml' according to the below list 'avaliable_sites'
    $ scrapy crawl xmlsample -a target=tmtpost -o xmlsample.csv     # Fetch data and output to a csv file from 'https://www.tmtpost.com/rss.xml' according to the below list 'avaliable_sites'

    Last verified date: 25 Jan, 2024
'''
# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from scrapy.http import Request
from spytest.items import XMLSampleItemGeneric, XMLSampleItemForTechnode, XMLSampleItemForWilliamLong, XMLSampleItemForFeng


class xmlSampleSpider(XMLFeedSpider):
    name = 'xmlsample'
    iterator = 'iternodes' # Optional value: 'iternodes', 'html' or 'xml'
    # allowed_domains = []  # Disable 'allowed_domains' to allow all request

    # Available RSS/XML Feed Sample Sites: 
    # Test Passed on 01/22/2024
    avaliable_sites = [
        { 'url': 'https://cn.technode.com/feed/', 'itertag': 'item' },
        { 'url': 'https://www.williamlong.info/rss.xml', 'itertag': 'item' },
        { 'url': 'https://www.feng.com/rss.xml', 'itertag': 'item' },
        { 'url': 'https://36kr.com/feed', 'itertag': 'item' },
        { 'url': 'http://www.techweb.com.cn/rss/allnews.xml', 'itertag': 'item' },
        { 'url': 'https://www.tmtpost.com/rss.xml', 'itertag': 'item' },
        { 'url': 'https://www.meihua.info/feed', 'itertag': 'item' },
        { 'url': 'https://www.leiphone.com/feed', 'itertag': 'item' },
        { 'url': 'http://www.geekpark.net/rss', 'itertag': 'item' },
        { 'url': 'https://hk.news.yahoo.com/rss/hong-kong', 'itertag': 'item' },
        { 'url': 'https://www.ithome.com/rss/', 'itertag': 'item' },
        { 'url': 'https://rss.yesky.com/index.xml', 'itertag': 'item' },
        { 'url': 'https://rthk.hk/rthk/news/rss/c_expressnews_cinternational.xml', 'itertag': 'item' },
        { 'url': 'https://news.google.com/rss?pz=1&cf=all&hl=zh-HK&gl=HK&ceid=HK:zh-Hant', 'itertag': 'item' },
    ]
    # Default target site to fetch! Value 'id' range from 0 to 13, Corresponding to the index of above sites list
    target_site_id = 1
    
    # The overridden method 'start_requests' will be called before emitting first request
    def start_requests(self):
        try:
            self.logger.info('Argument "target" got value "%s"',self.target)
            for id in range(len(self.avaliable_sites)):
                if self.avaliable_sites[id]['url'].find(self.target) >= 0:
                    self.target_site_id = id
                    break
        except:
            pass

        self.start_urls = [self.avaliable_sites[self.target_site_id]['url']]
        self.itertag = self.avaliable_sites[self.target_site_id]['itertag']
        for url in self.start_urls:
            yield Request(url, dont_filter=True)
    
    '''
    # The method 'adapt_response' will be called first before the method 'parse_node'
    def adapt_response(self, response):
        print(response.url)

        return response
    '''

    def parse_node(self, response, node):
        if self.target_site_id == 0:    # Refer to 'https://cn.technode.com/feed/'
            item = XMLSampleItemForTechnode()
            item['title'] = node.xpath('//item/title/text()').get()
            item['link'] = node.xpath('//item/link/text()').get()
            item['dc_creator'] = node.xpath('//item/dc:creator/text()', namespaces={'dc': 'http://purl.org/dc/elements/1.1/'}).get()
            item['pubDate'] = node.xpath('//item/pubDate/text()').get()
            item['category'] = node.xpath('//item/category/text()').getall()
            item['guid'] = node.xpath('//item/guid/text()').get()
            item['description'] = node.xpath('//item/description/text()').get()
            item['content_encoded'] = node.xpath('//item/content:encoded/text()', namespaces={'content': 'http://purl.org/rss/1.0/modules/content/'}).get()
        elif self.target_site_id == 1:    # Refer to 'https://www.williamlong.info/rss.xml'
            item = XMLSampleItemForWilliamLong()
            item['title'] = node.xpath('//item/title/text()').get()
            item['author'] = node.xpath('//item/author/text()').get()
            item['link'] = node.xpath('//item/link/text()').get()
            item['pubDate'] = node.xpath('//item/pubDate/text()').get()
            item['guid'] = node.xpath('//item/guid/text()').get()
            item['description'] = node.xpath('//item/description/text()').get()
            item['category'] = node.xpath('//item/category/text()').get()
            item['comments'] = node.xpath('//item/comments/text()').get()
            item['wfw_commentRss'] = node.xpath('//item/wfw:commentRss/text()', namespaces={'wfw': 'http://wellformedweb.org/CommentAPI/'}).get()
        elif self.target_site_id == 2:    # Refer to 'https://www.feng.com/rss.xml'
            item = XMLSampleItemForFeng()
            item['id'] = node.xpath('//item/id/text()').get()
            item['title'] = node.xpath('//item/title/text()').get()
            item['link'] = node.xpath('//item/link/text()').get()
            item['category'] = node.xpath('//item/category/text()').get()
            item['description'] = node.xpath('//item/description/text()').get()
            item['source'] = node.xpath('//item/source/text()').get()
            item['pubDate'] = node.xpath('//item/pubDate/text()').get()
            item['author'] = node.xpath('//item/author/text()').get()
            item['isOrigin'] = node.xpath('//item/isOrigin/text()').get()
        else:    # Refer to majority news feed sites
            item = XMLSampleItemGeneric()
            item['title'] = node.xpath('//item/title/text()').get()
            item['link'] = node.xpath('//item/link/text()').get()
            item['pubDate'] = node.xpath('//item/pubDate/text()').get()
            item['description'] = node.xpath('//item/description/text()').get()

        return item
