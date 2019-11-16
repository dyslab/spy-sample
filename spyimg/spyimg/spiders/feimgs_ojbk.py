'''
    Spider name: feimgs_ojbk

   Fetch images by pages from website 'ojbk.cc'.

    Target site link examples:
        http://www.ojbk.cc/metcn/
            http://www.ojbk.cc/metcn/6902.html
            http://www.ojbk.cc/metcn/6900.html
            http://www.ojbk.cc/metcn/6904.html
            http://www.ojbk.cc/metcn/6906.html
            http://www.ojbk.cc/metcn/6898.html

    Arguments:
        url: Target url. 

    Usage:
        $ scrapy crawl --nolog feimgs_ojbk -a url=http://www.ojbk.cc/metcn/6890.html
'''
# -*- coding: utf-8 -*-
import scrapy
import os


class FeimgsOjbkSpider(scrapy.Spider):
    name = 'feimgs_ojbk'
    # allowed_domains = ['ojbk.cc']
    # start_urls = ['http://www.ojbk.cc/metcn/6902.html']

    # Custom variable
    page_links = []
    download_file_count = 0

    def start_requests(self):
        print('>>> Spider [%s] Started.' % self.name)
        # Parse argument 'url'
        if self.url is not None and self.url != '':
            p, a = os.path.split(self.url)
            self.page_links.append(a)
            spath = os.path.splitext(a)[0]
            # Create folder
            try:
                os.mkdir(spath)
            except FileExistsError as e:
                print('>>> Folder [%s] existed.' % spath)
            else:
                print('>>> Folder [%s] created.' % spath)
            return [scrapy.Request(self.url, callback=self.parse_page, cb_kwargs={'path': spath})]

    # Check whether page link is in same series or not.
    def is_same_series(self, pagelink):
        if len(self.page_links) > 0:
            s = self.page_links[0].split('.')[0].split('_')[0]
            if pagelink.find(s) == 0:
                return True
        return False

    def parse_page(self, response, path):
        # Get image urls
        for imgurl in response.xpath('//img[@id="bigimg"]/@src').getall():
            print('>>> Get image url [%s]' % imgurl)
            yield scrapy.Request(imgurl, callback=self.fetch_image, cb_kwargs={'path': path})
        # Get other page links
        for pagelink in response.css('div.content-page').xpath('a/@href').getall():
            if pagelink.lower().find('.htm') > 0:
                if (pagelink not in self.page_links) and self.is_same_series(pagelink):
                    self.page_links.append(pagelink)
                    # Reconstruct page link
                    p = os.path.split(response.url)[0]
                    plink = p + '/' + pagelink
                    print('>>> Get page link [%s]' % plink)
                    yield scrapy.Request(plink, callback=self.parse_page, cb_kwargs={'path': path})

    def fetch_image(self, response, path):
        print('>>> Fetched file [%s]' % response.url)
        p, a = os.path.split(response.url)
        if len(response.body) > 0:
            # Save image file to dest path.
            try:
                with open('{}/{}'.format(path,a), 'wb') as fimg:
                    fimg.write(response.body)
                    fimg.close()
            except OSError as e:
                print('>>> Warning: File [{}/{}] Save FAILED!' .format(path, a))
            else:
                self.download_file_count += 1
                print('>>> #{} File [{}/{}] Save OK!'.format(self.download_file_count, path, a))
