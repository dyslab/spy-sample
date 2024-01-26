'''
    Spider name: feimgs_imagefap2

    Fetch entire photo gallery by url '/pictures/' or '/gallery/' from website 'https://www.imagefap.com/'. 

    Target url examples:
        https://www.imagefap.com/gallery/11922185
        https://www.imagefap.com/gallery/11933775
        https://www.imagefap.com/pictures/11925535/Ellis%20Lesbian%20Fun

    Arguments:
        url: Target url. 

    Usage:
        $ scrapy crawl --nolog feimgs_imagefap2 -a url=https://www.imagefap.com/gallery/11922185

    Last verified date: 26 Jan, 2024
'''
# -*- coding: utf-8 -*-
import scrapy
import os, math
from urllib.parse import urlparse
from fake_useragent import UserAgent

class FeimgsImagefapSpider(scrapy.Spider):
    name = 'feimgs_imagefap2'
    allowed_domains = ['imagefap.com', 'x.imagefapusercontent.com']

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
            self.saved_image_path=os.path.split(self.url)[-1]
            # Create folder
            try:
                os.mkdir(self.saved_image_path)
            except FileExistsError:
                print('Local Folder [%s] existed.' % self.saved_image_path)
            else:
                print('Local Folder [%s] created.' % self.saved_image_path)
            return [scrapy.Request(self.url, callback=self.parse_photolistpage, headers=self.custom_headers, cb_kwargs={'page': 0})]
        except:
            print('Argument "url" not found or not correct.')
            return []

    # Parse first photo list page
    def parse_photolistpage(self, response, page):
        print('> Fetched photo list page #{} [{}]'.format(page, response.url))
        try:
            u = urlparse(response.url)
            first_photopage_link = response.xpath("//form/table/tr/td/table/tr/td/a/@href").get()
            purl =  u.scheme + '://' + u.netloc + first_photopage_link
            if page == 0:
                yield scrapy.Request(purl, callback=self.parse_photopage, headers=self.custom_headers, cb_kwargs={'digflag': True})
            else:
                yield scrapy.Request(purl, callback=self.parse_photopage, headers=self.custom_headers, cb_kwargs={'digflag': False})
        except:
            pass

    # Extract photo links from photo page
    def parse_photopage(self, response, digflag):
        print('>> Fetched photo page [{}]'.format(response.url))
        # Get all photo links on the page
        try:
            photo_links_on_a_page = response.css("ul.thumbs").xpath(".//li/a/@href").getall()
            photo_count_on_a_page = len(photo_links_on_a_page)
            print('-- Get {} pics on this page.'.format(photo_count_on_a_page))
            for pitem in photo_links_on_a_page:
                yield scrapy.Request(pitem, callback=self.parse_image, headers=self.custom_headers)
        except IOError:
            print('-- WARNING: Error occurred on photo page [{}]'.format(response.url))
            pass
        # Get total_photos and calculate how many photo list pages should be generated while digflag is true
        if digflag:
            try:
                print('-- Digging on page [{}]'.format(response.url))
                str_total_photos = response.xpath('//*[@id="_navi_cavi"]/@data-total').get()
                total_photos = int(str_total_photos)
                if photo_count_on_a_page > 0:
                    generate_photo_list_pages = math.ceil(total_photos / photo_count_on_a_page)
                else:
                    generate_photo_list_pages = 0
                for pageno in range(1,generate_photo_list_pages):
                    # Galeery url patter example:
                    #   https://www.imagefap.com/gallery/11933775
                    # Photo list page url patter example:
                    #   https://www.imagefap.com/gallery/11933775?page=1&view=0
                    # Photo page url patter example:
                    #   https://www.imagefap.com/photo/629476762/?pgid=&gid=11933775&page=1
                    #
                    # Generate photo list page links and send request
                    pageurl = self.url + '?page=' + str(pageno) + '&view=0'
                    yield scrapy.Request(pageurl, callback=self.parse_photolistpage, headers=self.custom_headers, cb_kwargs={'page': pageno})
            except ValueError:
                print('-- Warning: Did NOT get the number of total photos!')
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
