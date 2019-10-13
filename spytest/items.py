# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrackingInfoItem(scrapy.Item):
    # define the fields for your item here like:
    parcelno = scrapy.Field()
    state = scrapy.Field()
    dest = scrapy.Field()
    details = scrapy.Field()
    
    def printItems(self):
        print('Parcel No: %s' % self['parcelno'])
        print('State: %s' % self['state'])
        print('Destination: %s' % self['dest'])
        print('Details: %s' % self['details'])
    