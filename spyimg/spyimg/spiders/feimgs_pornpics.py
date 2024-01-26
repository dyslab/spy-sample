'''
    Spider name: feimgs_pornpics

    Fetch photos by gallery url from website 'https://www.pornpics.com/'. 

    Target url examples:
        https://www.pornpics.com/galleries/met-art-diana-a-nika-b-35320148/
        https://www.pornpics.com/galleries/beautiful-teen-with-small-tits-alessandra-jane-gets-railed-by-a-horny-old-man-70921958/
        https://www.pornpics.com/galleries/japanese-babe-ami-oya-takes-a-stiff-rod-deep-in-her-juicy-shaved-pussy-65124161/
        https://www.pornpics.com/galleries/asian-milf-exposing-her-shaved-creampied-pussy-in-close-up-after-shower-61453447/

    Arguments:
        url: Target url. 

    Usage:
        $ scrapy crawl --nolog feimgs_pornpics -a url=https://www.pornpics.com/galleries/met-art-diana-a-nika-b-35320148/

    Last verified date: 26 Jan, 2024
'''
# -*- coding: utf-8 -*-
import scrapy
import os
from urllib.parse import urlparse
from fake_useragent import UserAgent

class FeimgsPornpicsSpider(scrapy.Spider):
    name = 'feimgs_pornpics'
    allowed_domains = ['pornpics.com']

    # Fake user agent
    _fake_ua = UserAgent(os='linux').random
    custom_headers = {
        "User-Agent": _fake_ua
    }
    # Image storage path
    saved_image_path = './'
    # Saved images counter
    saved_image_count = 0

    def start_requests(self):
        print('Spider [%s] opened.' % self.name)
        # Parse argument 'url'
        try:
            if self.url[-1] == '/':
                self.saved_image_path = os.path.split(self.url[:-1])[-1]
            else:
                self.saved_image_path = os.path.split(self.url)[-1]
            # Create folder
            try:
                os.mkdir(self.saved_image_path)
            except FileExistsError:
                print('Local Folder [%s] existed.' % self.saved_image_path)
            else:
                print('Local Folder [%s] created.' % self.saved_image_path)
            return [scrapy.Request(self.url, callback=self.parse_photopage, headers=self.custom_headers)]
        except:
            print('Argument "url" not found or not correct.')
            return []

    # Extract photo links from photo page
    def parse_photopage(self, response):
        print('> Fetched photo page [{}]'.format(response.url))
        # Get all photo links on the page
        try:
            photo_links_on_page = response.xpath('.//a[@class="rel-link"]/@href').getall()
            photo_count_on_page = len(photo_links_on_page)
            print('- Get {} pics on this page.'.format(photo_count_on_page))
            for pitem in photo_links_on_page:
                yield scrapy.Request(pitem, callback=self.parse_image, headers=self.custom_headers)
        except IOError:
            print('- WARNING: Error occurred on photo page [{}]'.format(response.url))
            pass

    # Fetched and save image
    def parse_image(self, response):
        print('>> Fetched file [%s]' % response.url)
        # Get picture file name
        saveFileName = os.path.split(response.url)[-1]
        if len(response.body) > 0:
            # Save image file to dest path
            try:
                self.saved_image_count += 1
                with open('{}/{}'.format(self.saved_image_path, saveFileName), 'wb') as fimg:
                    fimg.write(response.body)
                    fimg.close()
            except OSError:
                print(
                    '·· Warning: File #{} [{}/{}] Save FAILED!'.format(self.saved_image_count, self.saved_image_path, saveFileName)
                )
            else:
                print(
                    '·· File #{} [{}/{}] Save OK!'.format(self.saved_image_count, self.saved_image_path, saveFileName)
                )
