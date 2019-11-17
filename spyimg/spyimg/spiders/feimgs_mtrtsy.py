'''
    Spider name: feimgs_mtrtsy

   Fetch serialized images by automated sequence no from specific image website.

    Target site link examples:
        http://mtrtsy.com/
            http://img.mtrtsy.com/161213/co161213145323-0.jpg
            http://img.mtrtsy.com/170216/co1F216024225-0.jpg
            http://img.mtrtsy.com/161217/co16121F02546-0.jpg
            http://img.mtrtsy.com/170216/co1F216023328-0.jpg

    Arguments:
        url: Target url. ('[n]' means the variable of sequence no)
        startno: Start number. (default = 0)
        threads: Amount threads, equal to amount quantity of fetched images at each time. (default = 1)

    Usage:
        $ scrapy crawl --nolog feimgs_mtrtsy -a threads=5 -a url=http://img.mtrtsy.com/170907/co1FZF23R5-[n].jpg -a startno=0
'''  
# -*- coding: utf-8 -*-
import scrapy
import os, re


class FeimgsMtrtsySpider(scrapy.Spider):
    name = 'feimgs_mtrtsy'
    # allowed_domains = ['mtrtsy.com']
    # start_urls = ['http://img.mtrtsy.com/161213/co161213145323-0.jpg']

    # Custom variable
    download_file_count = 0
    threads_count = 1

    def start_requests(self):
        print('>>> Spider [%s] Started.' % self.name)
        # Get argument 'startno'
        if self.startno is not None:
            sno = int(self.startno)
        else:
            sno = 0
        # Get argument 'threads'
        if self.threads is not None:
            self.threads_count = int(self.threads)
        # Parse argument 'url'
        if self.url is not None and self.url != '':
            a = re.match('.+/(.+)\[n\]', self.url)
            spath = a.group(1)
            # Create folder
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
            return [scrapy.Request(self.url.replace('[n]', str(sno)), callback=self.fetch_image, cb_kwargs={'path': spath, 'url': self.url, 'next_no': sno + 1})]

    def fetch_image(self, response, path, url, next_no):
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
        # Send next request if url has a sub string '[n]'.
        if url.find('[n]') > 0:
            for id in range(self.threads_count):
                yield scrapy.Request(
                    url.replace('[n]', str(next_no + id)),
                    callback=self.fetch_image, 
                    cb_kwargs = {
                        'path': path,
                        'url': url,
                        'next_no': next_no + self.threads_count + id
                    }
                )
