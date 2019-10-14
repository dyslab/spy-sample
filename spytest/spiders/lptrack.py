'''
    Spider name: lptrack

    Crawl tracking information from www.laposte.fr by tracking number.

    Arguments:
        num: Tracking Number.

    Usage:
        scrapy crawl lptrack -a num=LO091851994CN -o t.json
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LPTrackSpider(CrawlSpider):
    name = 'lptrack'
    allowed_domains = ['laposte.fr']
    # start_urls = ['https://www.laposte.fr/outils/track-a-parcel?code=LO091851994CN']
    # https://api.laposte.fr/ssu/v1/suivi-unifie/idship/LO092265094CN
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Host': 'api.laposte.fr',
        'Referer': 'https://www.laposte.fr/outils/track-a-parcel?code=',
        'Origin': 'https://www.laposte.fr',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3'
    }

    rules = (
        Rule(LinkExtractor(allow=r'suivi-unifie/idship/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        self.custom_headers['Referer'] += self.num
        yield scrapy.Request(
            'https://api.laposte.fr/ssu/v1/suivi-unifie/idship/%s' % self.num, 
            headers=self.custom_headers
        )

    def parse_item(self, response):
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return response
