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
from scrapy.http import JSONRequest


class LPTrackSpider(scrapy.Spider):
    name = 'lptrack'
    allowed_domains = ['laposte.fr']
    start_urls = ['https://www.laposte.fr/outils/track-a-parcel?code=LO091851994CN']
    # https://api.laposte.fr/ssu/v1/suivi-unifie/idship/LO092265094CN
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Host': 'api.laposte.fr',
        'Referer': 'https://www.laposte.fr/outils/track-a-parcel?code=',
        'Origin': 'https://www.laposte.fr',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3'
    }

    def start_requests(self):
        self.custom_headers['Referer'] += self.num
        print('>>> post request.')
        yield JSONRequest(
            url = 'https://api.laposte.fr/ssu/v1/suivi-unifie/idship/%s' % self.num,
            method='GET',
            headers = self.custom_headers,
            callback = self.after_get
        )

    def after_get(self, response):
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        print('********************** after_post. BEGIN')
        print(response.url)
        print(response.headers)
        print(bytes.decode(response.body))
        print('********************** after_post. END')

        ###############################################
        # Invoke scrapy shell to test response.
        ###############################################
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
