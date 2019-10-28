'''
    Spider name: uspstrack

    Crawl tracking information from usps.com by tracking number.

    Arguments:
        num: Tracking Number.

    Usage:
        $ scrapy crawl uspstrack --nolog -a num=9274890983116178146826
        $ scrapy crawl uspstrack --nolog -o uspstrack.csv -a num=9261290983116176669147   # Output csv file.
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from spytest.items import TrackingInfoItem


class InfoUspstrackSpider(CrawlSpider):
    name = 'uspstrack'
    allowed_domains = ['tools.usps.com']
    # start_urls = ['https://tools.usps.com/go/TrackConfirmAction?tLabels=9274890983116178146826']

    # rules = (
    #     Rule(LinkExtractor(allow=r'go/TrackConfirmAction'), callback='parse_item', follow=True),
    # )

    def start_requests(self):
        return [scrapy.Request('https://tools.usps.com/go/TrackConfirmAction?tLabels=%s' % self.num)]

    def parse(self, response):
        print(response.xpath('//span[@class="tracking-number"]/text()').get())
        print(response.xpath('//div[@class="delivery_status"]/h2/strong/text()').get())
        print(response.xpath('//div[@class="expected_delivery"]/p/text()').get())
        
        iloader = ItemLoader(item=TrackingInfoItem(), response=response)
        # iloader.add_css('tracknum', 'span.tracking-number::text')
        iloader.add_xpath('tracknum', '//span[@class="tracking-number"]/text()')
        iloader.add_xpath('status', '//div[@class="delivery_status"]/h2/strong/text()')
        iloader.add_xpath('dest', '//div[@class="expected_delivery"]/p/text()')
        xdetails_list = response.xpath('//div[@id="trackingHistory_1"]/div/div/div/span')
        # Get details of tracking history.
        str_details = ''
        for ditem in xdetails_list:
            print(ditem)
            str_details += ditem.xpath('string(.)').get()
        iloader.add_value('details', str_details)
        
        return iloader.load_item()
        
