'''
    Spider name: feimgs_imagefap

   Fetch images by pages from website 'imagefap.com'.

    Target site link examples:
        https://www.imagefap.com/
            https://www.imagefap.com/pictures/8421455/PGF-007
            https://www.imagefap.com/pictures/8421484/PGF-008
            https://www.imagefap.com/pictures/8421503/PGF-009
            https://www.imagefap.com/pictures/8421855/g274
            https://www.imagefap.com/pictures/8423040/Shaved-Yuri-Sawashiro
            https://www.imagefap.com/pictures/8392290/Shaved-Nao-Shiraishi3

    Arguments:
        url: Target url. 

    Usage:
        $ scrapy crawl --nolog feimgs_imagefap -a url=https://www.imagefap.com/pictures/8421855/g274
'''
# -*- coding: utf-8 -*-
import scrapy
import os, re
from urllib.parse import urlparse


class FeimgsImagefapSpider(scrapy.Spider):
    name = 'feimgs_imagefap'
    allowed_domains = ['imagefap.com', 'x.imagefapusercontent.com']
    # start_urls = ['https://www.imagefap.com/pictures/8423040/Shaved-Yuri-Sawashiro']

    # Image storage path
    saved_image_path = './'
    # Saved images counter
    saved_image_count = 0

    def start_requests(self):
        print('>>> Spider [%s] Started.' % self.name)
        # Parse argument 'url'
        if self.url is not None and self.url != '':
            p, self.saved_image_path=os.path.split(self.url)
            # Create folder
            try:
                os.mkdir(self.saved_image_path)
            except FileExistsError as e:
                print('>>> Folder [%s] existed.' % self.saved_image_path)
            else:
                print('>>> Folder [%s] created.' % self.saved_image_path)
            return [scrapy.Request(self.url, callback=self.parse_firstpage)]

    # Parse first page
    def parse_firstpage(self, response):
        plink = response.xpath("//form/table/tr/td/table/tr/td/a/@href").get()
        if plink is not None and plink != '':
            u = urlparse(response.url)
            p = re.match('(.+/\?).+&(gid=.+)&page.+', plink)
            # The real content of photo list was generated by the link whose format like below:
            #   https://www.imagefap.com/photo/162731207/?gid=8423040&idx=72&partial=true
            pagelink = u.scheme + '://' + u.netloc + p[1] + p[2] + '&idx=0&partial=true'
            print('>>> Page link [%s] generated.' % pagelink)
            yield scrapy.Request(pagelink, callback=self.parse_photopage, cb_kwargs={'no':0})
        else:
            pass

    # Extract photo links from photo page
    def parse_photopage(self, response, no):
        print('>>> Fetched page [{}] at index [{}].'.format(response.url, no))
        try:
            photo_count = int(response.xpath("//div[@id='navigation']/@data-total").get())
            photo_links = response.css("ul.thumbs").xpath(".//li/a/@href").getall()
            next_no = no + len(photo_links)
            print('>>> Get {} pics on this page.'.format(len(photo_links)))
            for pitem in photo_links:
                yield scrapy.Request(pitem, callback=self.parse_image)
            if next_no < photo_count:
                next_page_link = response.url.replace('idx={}'.format(no), 'idx={}'.format(next_no))
                print('>>> Next page is [{}].'.format(next_page_link))
                yield scrapy.Request(next_page_link, callback=self.parse_photopage, cb_kwargs={'no': next_no})
            else:
                print('>>> End of photos at index [{}/{}].'.format(next_no, photo_count))
        except IOError:
            print('>>> WARNING: Error occurred on page [{}] at index [{}].'.format(
                response.url, no))
            pass

    # Fetched and save image
    def parse_image(self, response):
        print('>>> Fetched file [%s]' % response.url)
        p, a = os.path.split(response.url)
        if len(response.body) > 0:
            # Save image file to dest path
            try:
                self.saved_image_count += 1
                with open('{}/{}'.format(self.saved_image_path, a), 'wb') as fimg:
                    fimg.write(response.body)
                    fimg.close()
            except OSError as e:
                print(
                    '>>> Warning: File #{} [{}/{}] Save FAILED!'.format(self.saved_image_count, self.saved_image_path, a)
                )
            else:
                print(
                    '>>> File #{} [{}/{}] Save OK!'.format(self.saved_image_count, self.saved_image_path, a)
                )
