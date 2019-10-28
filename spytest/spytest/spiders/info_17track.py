'''
    [TEST]
    
    Spider name: 17track

    Crawl tracking information from www.17track.net by tracking number.

    Arguments:
        ! num: Tracking Number.

    Usage:
        scrapy crawl --nolog 17track -a num=LO091851994CN
        ! scrapy crawl 17track -a num=LO091851994CN -o 17track.json
'''
# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import JSONRequest


class Test17TrackSpider(scrapy.Spider):
    name = '17track'
    allowed_domains = ['17track.net']
    # start_urls = ['https://t.17track.net/restapi/track']
    # formData: {"data":[{"num":"LO091851994CN","fc":0,"sc":0}],"guid":"","timeZoneOffset":-480}
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Host': 't.17track.net',
        'Referer': 'https://t.17track.net/en',
        'TE': 'Trailers',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3'
    }

    def start_requests(self):
        print('>>> post request.')
        return [JSONRequest(
            url = "https://t.17track.net/restapi/track",
            method='POST',
            headers = self.custom_headers,
            data = {'data': [{'num': self.num, 'fc': 0, 'sc': 0}], 'guid': '', 'timeZoneOffset': -480},
            callback = self.after_post
        )]

    def after_post(self, response):
        print('********************** after_post. BEGIN')
        print(response.url)
        print(response.headers)
        # print(bytes.decode(response.body))  #  as same as the line below
        print(response.text)
        res = json.loads(response.text, encoding = 'utf-8')
        print('ret: {}, msg: {}'.format(res['ret'], res['msg']))

        # Write to a json file by binary mode.
        with open('17track.json', 'wb') as fbjson:
            fbjson.write(b'------------ header part ------------\t\n')
            for item in dict(response.headers):
                print('{}: {}'.format(bytes.decode(item), bytes.decode(response.headers[item])))
                fbjson.write(item)
                fbjson.write(b': ')
                fbjson.write(response.headers[item])
                fbjson.write(b'\t\n')

            fbjson.write(b'\t\n------------- body part -------------\t\n')
            fbjson.write(response.body)
            fbjson.close()
        
        print('********************** after_post. END')
