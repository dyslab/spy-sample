'''
    Spider name: feimgs_svgrepo

    Fetch SVG images by category from website 'https://www.svgrepo.com/'. 
    --- ONLY FOR TEST! --- 
    This spider only fetches SVG files on first return page. 

    Target site link examples:
        https://www.svgrepo.com/vectors/wechat/
        https://www.svgrepo.com/vectors/windows/

    Arguments:
        cat: Category name. 

    Usage:
        $ scrapy crawl --nolog feimgs_svgrepo -a cat=wechat
        $ scrapy crawl --nolog feimgs_svgrepo -a cat=windows

    Last verified date: 25 Jan, 2024
'''
# -*- coding: utf-8 -*-
import scrapy
import os

class FeimgsSvgrepoSpider(scrapy.Spider):
    name = 'feimgs_svgrepo'
    allowed_domains = ['svgrepo.com']
    start_urls = ['https://svgrepo.com/vectors/']

    # Image storage path
    saved_image_path = './'
    # Saved images counter
    saved_image_count = 0

    def start_requests(self):
        print('· Spider [%s] Opened.' % self.name)
        # Parse argument 'cat'
        try:
            self.saved_image_path = self.cat.strip().lower()
            start_url = self.start_urls[0] + self.saved_image_path + '/'
            try:
                os.mkdir(self.saved_image_path)
            except FileExistsError:
                print('· Folder [%s] existed.' % self.saved_image_path)
            else:
                print('· Folder [%s] created.' % self.saved_image_path)
            return [scrapy.Request(start_url, callback=self.parse_page)]
        except:
            print('· Argument "cat" not found.')
            return []

    def parse_page(self, response):
        # Following xpath got from Chrome
        svg_images = response.xpath('//*[@id="__next"]/div/div/div/div/div/a/img/@src').getall()
        svg_images=list(dict.fromkeys(svg_images))  # Remove duplicated items from list
        svg_images_count = len(svg_images)
        print('·· Got {} SVG images on this page.'.format(svg_images_count))
        for sitem in svg_images:
            yield scrapy.Request(sitem, callback=self.parse_image)

    # Fetched and save image
    def parse_image(self, response):
        print('··· Fetched file [%s]' % response.url)
        # Get SVG file name
        url_filename = os.path.split(response.url)
        saveFileName = url_filename[0].split('/')[-1] + '_' + url_filename[-1]
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
