'''
    Spider name: fetchimgs

   Fetch serialized images by automated sequence no from specific image website.

    Target site link examples:
        http://mtrtsy.com/
            http://img.mtrtsy.com/161213/co161213145323-0.jpg
            http://img.mtrtsy.com/170216/co1F216024225-0.jpg
            http://img.mtrtsy.com/161217/co16121F02546-0.jpg

    Arguments:
        url: Target url. ('[n]' means the variable of sequence no)
        startno: Start number. (default = 0)

    Usage:
        $ scrapy crawl --nolog fetchimgs -a url=http://img.mtrtsy.com/170216/co1F216024225-[n].jpg -a startno=0
'''  
# -*- coding: utf-8 -*-
import scrapy
import os


class FetchimgsSpider(scrapy.Spider):
    name = 'fetchimgs'
    # allowed_domains = ['.jpg', '.jpeg', '.png', '.gif']
    # start_urls = ['http://img.mtrtsy.com/161213/co161213145323-0.jpg']

    def start_requests(self):
        print('>>> Spider Started.')
        # Get argument 'startno'
        if self.startno is not None:
            sno = int(self.startno)
        else:
            sno = 0
        # Parse argument 'url'
        if self.url is not None and self.url != '':
            a = self.url.split('/')
            spath = 'imgs_' + a[-2]
            # Create Folder
            try:
                os.mkdir(spath)
            except FileExistsError as e:
                print('>>> Folder [%s] existed.' % spath)
            else:
                print('>>> Folder [%s] created.' % spath)
        else:
            a = None
        # Send request if url is available.
        if a is not None:
            return [scrapy.Request(self.url.replace('[n]', str(sno)), callback=self.fetchimage, cb_kwargs={'path': spath, 'url': self.url, 'next_no': sno + 1})]

    def fetchimage(self, response, path, url, next_no):
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
                print('>>> File [{}/{}] Save OK!'.format(path, a[-1]))
        # Send next request if url has a sub string '[n]'.
        if url.find('[n]') > 0:
            yield scrapy.Request(url.replace('[n]', str(next_no)), callback=self.fetchimage, cb_kwargs={'path': path, 'url': url, 'next_no': next_no + 1})
