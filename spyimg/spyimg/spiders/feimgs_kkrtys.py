'''
    Spider name: feimgs_kkrtys

   Fetch images by pages from website 'kkrtys.com'.

    Target site link examples:
        http://kkrtys.com/guomo/
            http://kkrtys.com/guomo/2018/0523/382.html
            http://kkrtys.com/guomo/2018/0523/381.html
            http://kkrtys.com/guomo/2018/0523/380.html
            http://kkrtys.com/guomo/2018/0523/379.html

    Arguments:
        url: Target url. 

    Usage:
        $ scrapy crawl --nolog feimgs_kkrtys -a url=http://kkrtys.com/guomo/2018/0523/379.html
'''
# -*- coding: utf-8 -*-
import scrapy
import os, re


class FeimgsKkrtysSpider(scrapy.Spider):
    name = 'feimgs_kkrtys'
    allowed_domains = ['kkrtys.com']
    # start_urls = ['http://kkrtys.com/guomo/2018/0523/382.html']

    # Custom variable
    page_links = []
    download_file_count = 0

    def start_requests(self):
        print('>>> Spider [%s] Started.' % self.name)
        # Parse argument 'url'
        if self.url is not None and self.url != '':
            self.page_links.append(os.path.split(self.url)[1])
            a = re.match('.*/([0-9]+/+[0-9]+).*', self.url)
            spath = a.group(1).replace('/', '_')
            # Create folder
            try:
                os.mkdir(spath)
            except FileExistsError as e:
                print('>>> Folder [%s] existed.' % spath)
            else:
                print('>>> Folder [%s] created.' % spath)
            return [scrapy.Request(self.url, callback=self.parse_page, cb_kwargs={'path': spath})]

    def parse_page(self, response, path):
        # Get image urls
        for imgurl in response.xpath('//img[@border=0]/@src').getall():
            print('>>> Get image url [%s]' % imgurl)
            yield scrapy.Request(imgurl, callback=self.fetch_image, cb_kwargs={'path': path})
        # Get other page links
        for pagelink in response.css('div.page').xpath('.//li/a/@href').getall():
            if pagelink.lower().find('.htm') > 0:
                if (pagelink not in self.page_links) and self.is_same_series(pagelink):
                    self.page_links.append(pagelink)
                    # Reconstruct page link
                    plink = os.path.join(os.path.split(self.url)[0], pagelink)
                    print('>>> Get page link [%s]' % plink)
                    yield scrapy.Request(plink, callback=self.parse_page, cb_kwargs={'path': path})

    # Check whether page link is in same series or not.
    def is_same_series(self, pagelink):
        if len(self.page_links) > 0:
            s = self.page_links[0].split('.')
            if pagelink.find(s[0]) == 0:
                return True
        return False

    def fetch_image(self, response, path):
        print('>>> Fetched file [%s]' % response.url)
        a = response.url.split('/')
        if len(response.body) > 0:
            # Save image file to dest path.
            try:
                with open('{}/{}'.format(path,a[-1]), 'wb') as fimg:
                    fimg.write(response.body)
                    fimg.close()
            except OSError as e:
                print('>>> Warning: File [{}/{}] Save FAILED!' .format(path, a[-1]))
            else:
                self.download_file_count += 1
                print('>>> #{} File [{}/{}] Save OK!'.format(self.download_file_count, path, a[-1]))
