'''
    Spider name: csvsample

    Crawl CSV content from sample link.

    Arguments:
        None.

    Usage:
        $ scrapy crawl csvsample -o csvsample.json -s FEED_EXPORT_ENCODING=utf-8 -s FEED_EXPORT_INDENT=4  # Output json file and encoding as utf-8 with indent space 4.

    CSV Feed Sample Links:
        - https://datahub.io/core/country-list/r/data.csv
        - https://datahub.io/core/s-and-p-500-companies/r/constituents.csv
        - https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/provinces.csv
        - https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/cities.csv
        - https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/areas.csv
        - https://raw.githubusercontent.com/vividvilla/csvtotable/master/sample/sample-utf8.csv
        - https://raw.githubusercontent.com/dyslab/jnb-sample/master/amz_reports/data/amz_reutrns_fba_201907.csv
'''
# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider
from spytest.items import CSVSampleCountryItem, CSVSampleProvinceCityItem


# csv sample which data from 'datahub.io'
class csvSampleSpider(CSVFeedSpider):
    name = 'csvsample'
    allowed_domains = ['.csv']
    start_urls = ['https://datahub.io/core/country-list/r/data.csv']
    headers = ['Name', 'Code']
    delimiter = ','  # '\t'
    quotechar = '"'  # "'"

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        self.logger.info('Hi, this is a row!: %r', row)
        cname = row['Name']
        # Get all counties which includes 'ch'.
        if cname.lower().find('ch') >= 0:
            i = CSVSampleCountryItem()
            i['code'] = row['Code']
            i['name'] = row['Name']
            return i


'''
# csv sample which data from 'raw.githubusercontent.com'
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
        # Get all cities information of Guangdong province.
        if pcode == '44':   # 广东省代码为44
            i = CSVSampleProvinceCityItem()
            i['code'] = row['code']
            i['name'] = row['name']
            i['cityCode'] = row['cityCode']
            i['provinceCode'] = row['provinceCode']
            return i
'''
