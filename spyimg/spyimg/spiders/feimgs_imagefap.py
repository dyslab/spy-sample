'''
    Spider name: feimgs_imagefap

    Fetch up to 10-page photos by url '/pictures/' or '/gallery/' from website 'https://www.imagefap.com/'.

    Target url examples:
        https://www.imagefap.com/gallery/11933803
        https://www.imagefap.com/gallery/11933785
        https://www.imagefap.com/pictures/8421503/PGF-009
        https://www.imagefap.com/pictures/11922724/les1506

    Arguments:
        url: Target url. 

    Usage:
        $ scrapy crawl --nolog feimgs_imagefap -a url=https://www.imagefap.com/pictures/11922724/les1506

    Last verified date: 26 Jan, 2024
'''
# -*- coding: utf-8 -*-
import scrapy
import os
from urllib.parse import urlparse
from fake_useragent import UserAgent


class FeimgsImagefapSpider(scrapy.Spider):
    name = 'feimgs_imagefap'
    allowed_domains = ['imagefap.com', 'x.imagefapusercontent.com']
    # start_urls = ['https://www.imagefap.com/pictures/8423040/Shaved-Yuri-Sawashiro']

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
        try:
            # Parse argument 'url'
            self.saved_image_path=os.path.split(self.url)[-1]
            # Create folder
            try:
                os.mkdir(self.saved_image_path)
            except FileExistsError:
                print('Local Folder [%s] existed.' % self.saved_image_path)
            else:
                print('Local Folder [%s] created.' % self.saved_image_path)
            return [scrapy.Request(self.url, callback=self.parse_first_photolistpage, headers=self.custom_headers)]
        except:
            print('Argument "url" not found or not correct.')
            return []

    # Parse first photo list page
    # Photo list page url patter examples:
    #   https://www.imagefap.com/gallery/11933803?gid=11933803&page=1&view=0
    def parse_first_photolistpage(self, response):
        try:
            photo_list_page_links = response.xpath("//div[@id='gallery']/font/span/a/@href").getall()
            photo_list_page_links = list(dict.fromkeys(photo_list_page_links)) # Remove duplicated items from list
            photo_list_page_links.insert(0, '?page=0') # Insert this first photo list page to photo list page links
            photo_list_page_count = len(photo_list_page_links)
            print('- Total {} pages found on page [{}].'.format(photo_list_page_count,response.url))

            '''
            # Since up to 10 photo list page links can be showed on the first photo list page, the following
            # procedure may not get accurate total photo list page links once the photo list pages are more than 10.
            '''
            if photo_list_page_count >= 10:
                print('- CAUTION: This spider can only fetch 10 pages'' photo at most. ')

            plid = 0
            for plitem in photo_list_page_links:
                plid += 1
                plurl =  response.url.split('?')[0] + plitem
                yield scrapy.Request(plurl, callback=self.get_photopage_link_from_photolistpage, headers=self.custom_headers, cb_kwargs={'pageno':plid})
        except IOError:
            pass

    # Get photo page link from photo list page 
    def get_photopage_link_from_photolistpage(self, response, pageno):
        print('> Getting photo page link from photo list page #{}: [{}]'.format(pageno, response.url))
        try:
            u = urlparse(response.url)
            first_photopage_link = response.xpath("//form/table/tr/td/table/tr/td/a/@href").get()
            purl =  u.scheme + '://' + u.netloc + first_photopage_link
            yield scrapy.Request(purl, callback=self.parse_photopage, headers=self.custom_headers)
            '''
            # Since we can get all image links on next photo page. It's unnecessary to traverse all nodes on this page.
            photopage_links = response.xpath("//form/table/tr/td/table/tr/td/a/@href").getall()
            photo_count = len(photopage_links)
            print('- Total {} photos found on page [{}].'.format(photo_count,response.url))
            pid = 0
            for pitem in photopage_links:
                pid += 1
                purl =  u.scheme + '://' + u.netloc + pitem
                yield scrapy.Request(purl, callback=self.parse_photopage, headers=self.custom_headers, cb_kwargs={'no':pid})
            '''
        except IOError:    
            print('-- WARNING: Error occurred on photo list page [{}]'.format(response.url))
            pass

    # Extract photo links from photo page
    # Photo page url patter examples:
    #   https://www.imagefap.com/photo/793946831/?pgid=&gid=11932767&page=0
    def parse_photopage(self, response):
        print('>> Fetched photo page [{}]'.format(response.url))
        try:
            photo_links = response.css("ul.thumbs").xpath(".//li/a/@href").getall()
            photo_count = len(photo_links)
            print('-- Get {} pics on this page.'.format(photo_count))
            for pitem in photo_links:
                yield scrapy.Request(pitem, callback=self.parse_image, headers=self.custom_headers)
        except IOError:
            print('-- WARNING: Error occurred on photo page [{}]'.format(response.url))
            pass

    # Fetched and save image
    def parse_image(self, response):
        print('>>> Fetched file [%s]' % response.url)
        # Get picture file name
        fn = os.path.split(response.url)[-1]
        questionMarkPos = fn.find('?')
        if questionMarkPos > 0:
            saveFileName = fn[0:questionMarkPos]
        else:
            saveFileName = fn
        if len(response.body) > 0:
            # Save image file to dest path
            try:
                self.saved_image_count += 1
                with open('{}/{}'.format(self.saved_image_path, saveFileName), 'wb') as fimg:
                    fimg.write(response.body)
                    fimg.close()
            except OSError:
                print(
                    '··· Warning: File #{} [{}/{}] Save FAILED!'.format(self.saved_image_count, self.saved_image_path, saveFileName)
                )
            else:
                print(
                    '··· File #{} [{}/{}] Save OK!'.format(self.saved_image_count, self.saved_image_path, saveFileName)
                )
