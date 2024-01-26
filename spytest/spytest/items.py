# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose
# from w3lib.html import remove_tags

def remove_space_and_add_tag(text):
    return 'No.' + str(text).strip()


'''''''''''''''''''''
#
#   Classes below used in spiders/info_cptrack.py
#
'''''''''''''''''''''

class TrackingInfoItem(scrapy.Item):
    # define the fields for your item here like:
    tracknum = scrapy.Field(
        input_processor = MapCompose(remove_space_and_add_tag),
        output_processor = Join()
    )
    parcelno = scrapy.Field()
    status = scrapy.Field()
    dest = scrapy.Field()
    details = scrapy.Field()
    date = scrapy.Field()
    
    def printItems(self):
        print('Tracking Number: %s' % self['tracknum'])
        print('Parcel No: %s' % self['parcelno'])
        print('Status: %s' % self['status'])
        print('Destination: %s' % self['dest'])
        print('Details: %s' % self['details'])
        print('Date: %s' % self['date'])


'''''''''''''''''''''
#
#   Classes below used in spiders/xmlsample.py
#
'''''''''''''''''''''

class XMLSampleItemGeneric(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    pubDate = scrapy.Field()
    description = scrapy.Field()


class XMLSampleItemForTechnode(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    dc_creator = scrapy.Field()
    pubDate = scrapy.Field()
    category = scrapy.Field()
    guid = scrapy.Field()
    description = scrapy.Field()
    content_encoded = scrapy.Field()


class XMLSampleItemForWilliamLong(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    pubDate = scrapy.Field()
    guid = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    comments = scrapy.Field()
    wfw_commentRss = scrapy.Field()


class XMLSampleItemForFeng(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    source = scrapy.Field()
    pubDate = scrapy.Field()
    author = scrapy.Field()
    isOrigin = scrapy.Field()


'''''''''''''''''''''
#
#   Classes below used in spiders/csvsample.py
#
'''''''''''''''''''''

class CSVSampleCountryItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    code = scrapy.Field()


class CSVSampleProvinceCityItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    code = scrapy.Field()
    cityCode = scrapy.Field()
    provinceCode = scrapy.Field()


'''''''''''''''''''''
#
#   Classes below used in spiders/sitemapsample.py
#
'''''''''''''''''''''

class SitemapSampleItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
