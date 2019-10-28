'''
    Spider name: cptrack

    Crawl tracking information from www.colisprive.com by tracking number.

    Arguments:
        num: Tracking Number.

    Usage:
        $ scrapy crawl --nolog cptrack -a num=FX000110077668320
        $ scrapy crawl cptrack -o cptrack.csv -a num=FX000090696630220   # Output csv file.
        $ scrapy crawl cptrack -o cptrack.json -s FEED_EXPORT_ENCODING=utf-8 -a num=FX000113628526320   # Output json file and encoding as utf-8.
'''
# -*- coding: utf-8 -*-
import scrapy
from spytest.items import TrackingInfoItem


class CPTrackSpider(scrapy.Spider):
    name = 'cptrack'
    allowed_domains = ['colisprive.com']
    # start_urls = ['http://sample.com/']
    # custom_settings = {
    # }

    def start_requests(self):
        yield scrapy.Request('https://www.colisprive.com/moncolis/pages/detailColis.aspx?numColis=%s' % self.num)

    def parse(self, response):
        # print(response.css('div.divColis div.tdText::text').get())
        # print(response.css('div.divStatut div.tdText::text').get())
        # print(response.css('div.divDesti div.tdText::text').get())
        titem = TrackingInfoItem()
        titem['tracknum'] = self.num
        titem['parcelno'] = response.css('div.divColis div.tdText::text').get()
        titem['status'] = response.css('div.divStatut div.tdText::text').get()
        titem['dest'] = response.css('div.divDesti div.tdText::text').get()
        titem['details'] = response.css('tr.bandeauText td.tdText::text').getall()
        titem.printItems()

        yield titem
