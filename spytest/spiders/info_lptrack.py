'''
    [TEST]
    
    Spider name: lptrack

    Crawl tracking information from www.laposte.fr by tracking number.

    Arguments:
        num: Tracking Number.

    Usage:
        scrapy crawl lptrack -a num=LO091851994CN -o lptrack.json
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest


class LPTrackSpider(scrapy.Spider):
    name = 'lptrack'
    allowed_domains = ['laposte.fr']
    start_urls = ['https://www.laposte.fr/outils/track-a-parcel']
    # https://api.laposte.fr/ssu/v1/suivi-unifie/idship/LO092265094CN
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Host': 'api.laposte.fr',
        'Referer': 'https://www.laposte.fr/outils/track-a-parcel',
        'Origin': 'https://www.laposte.fr',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3'
    }

    def parse(self, response):
        print('>>> repost request.')
        yield FormRequest.from_response(
            response,
            method = 'GET',
            formid = 'suiviForm',
            formdata = { 'code': self.num },
            headers = self.custom_headers,
            callback = self.after_get
        )

    def after_get(self, response):
        print('********************** After repost. BEGIN **********************')
        print(response.url)
        print(response.headers)
        print(bytes.decode(response.body))
        print('********************** After repost.   END **********************')

        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()

        ###############################################
        # Invoke scrapy shell to test response.
        ###############################################
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
