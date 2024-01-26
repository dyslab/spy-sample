'''
    Spider name: csvsample

    Crawl CSV content from sample link.

    Arguments: None.

    Usage:
    $ scrapy crawl csvsample -o csvsample.json  # Output json file

    CSV Feed Sample Links:
    - https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/provinces.csv
    - https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/cities.csv
    - https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/areas.csv
    - https://raw.githubusercontent.com/vividvilla/csvtotable/master/sample/sample-utf8.csv

    Last verified date: 22 Jan, 2024
'''
# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider
from spytest.items import CSVSampleCountryItem, CSVSampleProvinceCityItem


# csv sample which data from 'datahub.io'
class csvSampleSpider(CSVFeedSpider):
    name = 'csvsample'
    allowed_domains = ['.csv']
    start_urls = ['https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/provinces.csv']
    headers = ['code', 'name']   # Change it accordingly by the column names of .csv sourcefile
    delimiter = ','  # '\t'
    quotechar = '"'  # "'"

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        self.logger.info('Hi, this row content: %r', row)
        item = CSVSampleCountryItem()
        item['code'] = row['code']
        item['name'] = row['name']
        return item


'''
# csv sample snippet corresponding to 'https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/areas.csv'
class csvSampleSpider(CSVFeedSpider):
    name = 'csvsample'
    allowed_domains = ['.csv']
    start_urls = ['https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/areas.csv']
    headers = ['code', 'name', 'cityCode', 'provinceCode']
    delimiter = ',' # '\t'
    quotechar = '"' # "'"

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        self.logger.info('Hi, this is a row!: %r', row)
        pcode = row['provinceCode']
        # Fetch all cities information of Guangdong province.
        if pcode == '44':   # The provice code of Guangdong is 44
            i = CSVSampleProvinceCityItem()
            i['code'] = row['code']
            i['name'] = row['name']
            i['cityCode'] = row['cityCode']
            i['provinceCode'] = row['provinceCode']
            return i
'''
