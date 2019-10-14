# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrackingInfoItem(scrapy.Item):
    # define the fields for your item here like:
    tracknum = scrapy.Field()
    parcelno = scrapy.Field()
    status = scrapy.Field()
    dest = scrapy.Field()
    details = scrapy.Field()
    
    def printItems(self):
        print('Tracking Number: %s' % self['tracknum'])
        print('Parcel No: %s' % self['parcelno'])
        print('Status: %s' % self['status'])
        print('Destination: %s' % self['dest'])
        print('Details: %s' % self['details'])


class XMLSampleItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()


class CSVSampleItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    code = scrapy.Field()
    cityCode = scrapy.Field()
    provinceCode = scrapy.Field()


class SitemapSampleItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
