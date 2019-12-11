'''
    Spider name: tttrack

    Crawl tracking information from http://www.ttsucha.com/ by tracking number.

    Arguments:
        num: Tracking Number. eg. MHE827061910013817, MHE827061911021187

    Usage:
        scrapy crawl --nolog tttrack -a num=MHE827061911021187 -o tttrack.csv
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import JsonRequest
from spytest.items import TrackingInfoItem
import json


##########################################################################
#
#   WORKFLOW NOTE:
#       
#   Update on 2019/12/12, Obtain tracking info via the following steps:
#   
#       1. Get tokenvalue form http://www.ttsucha.com/   
#
#       2. Get parameter 'd_id' from json data via:
#           http://www.ttsucha.com/api/ttscapi/noTosearch
#
#       3. Get details info from json data via:
#           http://www.ttsucha.com/api/ttscapi/tomaindetail
#           http://www.ttsucha.com/api/ttscapi/todetail
#
#       4. Print and save items.
#   
##########################################################################
class TTTrackSpider(scrapy.Spider):
    name = 'tttrack'
    allowed_domains = ['ttsucha.com']
    start_urls = ['http://www.ttsucha.com/']

    # Custom variables
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Host': 'ttsucha.com',
        'Referer': 'http://www.ttsucha.com/',
        'TE': 'Trailers',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3'
    }
    trackno = ''
    token = ''

    def parse(self, response):
        print('\n>>> Get html from URL: %s' % response.url)
        # print(response.text)
        self.token = response.xpath('//input[@id="tokenvalue"]/@value').get()
        print('token: %s' % self.token)
        return [JsonRequest(
            url='http://www.ttsucha.com/api/ttscapi/noTosearch',
            method = 'POST',
            headers = self.custom_headers,
            data = { 'trackingNo': self.num, 'token': self.token },
            callback = self.parse_trackinginfo
        )]

    def parse_trackinginfo(self, response):
        print('\n>>> Get json data from URL: %s' % response.url)
        # print(response.text)
        returnJsonString = json.loads(response.text)
        returnJsonData= json.loads(returnJsonString)
        print(returnJsonData)
        for item in returnJsonData['items']:
            print('did: %s' % item['d_id'])
            print('token: %s' % self.token)
            # get d_id from json data
            # redirect to: ../../Home/detail.html?did=${d_id}&snum=87675
            yield JsonRequest(
                url='http://www.ttsucha.com/api/ttscapi/tomaindetail', # '/todetail',
                method = 'POST',
                headers = self.custom_headers,
                data = { 'did': item['d_id'], 'token': self.token },
                callback = self.parse_trackingdetails
            )

    def parse_trackingdetails(self, response):
        print('\n>>> Get json data from URL: %s' % response.url)
        returnJsonString = json.loads(response.text)
        returnJsonData= json.loads(returnJsonString)
        print(returnJsonData)
        print('\n>>> Parsing json data and Save to items...')
        print('>>> Tracking number is: %s' % self.num)
        for item in returnJsonData['newinfo']:
            print('>>> Parsing item: %s' % item['date'])
            titem = TrackingInfoItem()
            titem['tracknum'] = self.num
            titem['parcelno'] = ''
            titem['status'] = item['status']
            titem['dest'] = item['place']
            titem['details'] = item['info']
            titem['date'] = item['date']
            yield titem
        print('\n>>> Items saved OK!')
