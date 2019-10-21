'''
    [TEST]
    
    Spider name: tttrack

    Crawl tracking information from http://www.ttsucha.com/ by tracking number.

    Arguments:
        ! num: Tracking Number.

    Usage:
        scrapy crawl --nolog tttrack -o tttrack.csv
        ! scrapy crawl tttrack -a num=MHE827061910013817 -o tttrack.json
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from spytest.items import TrackingInfoItem


class TTTrackSpider(scrapy.Spider):
    name = 'tttrack'
    allowed_domains = ['ttsucha.com']
    # start_urls = ['http://www.ttsucha.com/']
    # formData: {'TrackingNo': 'MHE827061910013817'}
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Host': 'ttsucha.com',
        'Referer': 'http://www.ttsucha.com/',
        'TE': 'Trailers',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3'
    }

    def start_requests(self):
        print('>>> post request.')
        return [FormRequest(
            url = "http://www.ttsucha.com/",
            method='POST',
            headers = self.custom_headers,
            formdata = {
                #'__VIEWSTATE': '/wEPDwULLTE4ODQwNzE0NjQPZBYCAgEPZBYCAgEPFgIeCWlubmVyaHRtbAUSTUhFODI3MDYxOTEwMDEzODE3ZGR8BgFdAanB1zaZf3mQlc2CNbOsoWhIFrDodqKCFwKN0A==',
                #'__VIEWSTATEGENERATOR': '6A15E89B',
                #'__EVENTVALIDATION': '/wEdAAPFGCYzQrtKNCkQosxArgW/6QLmfmzsA3xixpakJO1yl0j93FC3MjAsSJrDkFJF8PNnkrWMfkEhqGjv1dblHohhCAyZQt8ve5TxjCiDuDM4XQ==',
                
                '__VIEWSTATE': '/wEPDwULLTE4ODQwNzE0NjQPZBYCAgEPZBYEAgEPFgIeCWlubmVyaHRtbAUSTUhFODI3MDYxOTEwMDEzODE3ZAIFDxYCHwAFlg88ZGl2IGNsYXNzPSJiZWxsb3dzX19pdGVtIj48ZGl2IGNsYXNzPSJiZWxsb3dzX19oZWFkZXIiPjx1bD48bGk+MTwvbGk+PGxpPjwvbGk+PGxpPjxzcGFuPk1IRSoqKioqMTkxMDAxMzgxNzwvc3Bhbj48YnI+5o+Q6LSn5pe26Ze077yaMjAxOS8xMC8xNyAxNDo0MTowMzwvbGk+PGxpPjxpbWcgc3JjPSJ0dHNjL2ltYWdlcy9qZHQucG5nIj7ovazov5DkuK08L2xpPjxsaT48c3BhbiBjbGFzcz0ndXBkYXRlZGF5cyc+MTwvc3Bhbj7lpKk8L2xpPjxsaT48YSBocmVmPSIjIj48c3Bhbj7or6bnu4bkv6Hmga88aW1nIHNyYz0idHRzYy9pbWFnZXMvYXNjLnBuZyIgd2lkdGg9IjE2IiBoZWlnaHQ9IjIwIj48L3NwYW4+PC9hPjwvbGk+PC91bD48L2Rpdj48ZGl2IGNsYXNzPSJiZWxsb3dzX19jb250ZW50Ij48dWw+PGxpPiZuYnNwOzwvbGk+PGxpPiZuYnNwOzwvbGk+PGxpPiZuYnNwOzwvbGk+PGxpPjIwMTktMTAtMTcgMTQ6NDI8L2xpPjxsaT5HVUFOR1pIT1UtQ0hJTkEv5bm/5beeLeS4reWbvQk8L2xpPjxsaT7lv6vku7blt7LliLDlub/lt57ku5PlupMgVGhlIGdvb2RzIGhhdmUgYmVlbiBhcnJpdmFsIEd1YW5nemhvdSB3aG91c2U8L2xpPjwvdWw+PHVsPjxsaT4mbmJzcDs8L2xpPjxsaT4mbmJzcDs8L2xpPjxsaT4mbmJzcDs8L2xpPjxsaT4yMDE5LTEwLTE4IDAwOjU1OjQzPC9saT48bGk+R1VBTkdaSE9VLUNISU5BL+W5v+W3ni3kuK3lm708L2xpPjxsaT7lv6vku7blt7Loo4Xmn5ws5bCG5a6J5o6S5oql5YWzIFRoZSBnb29kcyBoYXZlIGJlZW4gbG9hZGluZyBhbmQgcmVhZHkgdG8gY3VzdG9tcyBkZWNsYXJlLjwvbGk+PC91bD48dWw+PGxpPiZuYnNwOzwvbGk+PGxpPiZuYnNwOzwvbGk+PGxpPiZuYnNwOzwvbGk+PGxpPjIwMTktMTAtMTggMjM6NTY6MzQ8L2xpPjxsaT5TSEVOWkhFTi1DSElOQS/mt7HlnLMt5Lit5Zu9PC9saT48bGk+5rW35YWz54q25oCB5pu05pawIEN1c3RvbXMgc3RhdHVzIHVwZGF0ZWQuPC9saT48L3VsPjx1bD48bGk+Jm5ic3A7PC9saT48bGk+Jm5ic3A7PC9saT48bGk+Jm5ic3A7PC9saT48bGk+MjAxOS0xMC0xOSAwMDo1NjozNDwvbGk+PGxpPlNIRU5aSEVOLUNISU5BL+a3seWcsy3kuK3lm708L2xpPjxsaT7lv6vku7blt7LlrozmiJDmiqXlhbPmiYvnu63lubbku47mtbflhbPmlL7ooYwuIENsZWFyYW5jZSBwcm9jZXNzaW5nIGNvbXBsZXRlZC48L2xpPjwvdWw+PHVsPjxsaT4mbmJzcDs8L2xpPjxsaT4mbmJzcDs8L2xpPjxsaT4mbmJzcDs8L2xpPjxsaT4yMDE5LTEwLTE5IDA5OjU3PC9saT48bGk+U0hFTlpIRU4tQ0hJTkEv5rex5ZyzLeS4reWbvTwvbGk+PGxpPuiIueWQjeiIquasoSBFVkVSIFNVUEVSQiAxMTExLTA3OUUuPC9saT48L3VsPjx1bD48bGk+Jm5ic3A7PC9saT48bGk+Jm5ic3A7PC9saT48bGk+Jm5ic3A7PC9saT48bGk+MjAxOS0xMC0xOSAxMDo1ODwvbGk+PGxpPlNIRU5aSEVOLUNISU5BL+a3seWcsy3kuK3lm708L2xpPjxsaT7lv6vku7blsIbkuo4xMOaciDIw5pel5byA6Ii5VGhlIGV4cHJlc3Mgd2lsbCBsZWF2ZSBvbiAxMC4yMDwvbGk+PC91bD48dWw+PGxpPiZuYnNwOzwvbGk+PGxpPiZuYnNwOzwvbGk+PGxpPiZuYnNwOzwvbGk+PGxpPjIwMTktMTAtMjAgMjI6Mzc6MjI8L2xpPjxsaT5TSEVOWkhFTi1DSElOQS/mt7HlnLMt5Lit5Zu9PC9saT48bGk+5b+r5Lu256a75byA5riv5Y+jLkRlcGFydGVkIFBvcnQgaW4gU0hFTlpIRU4tQ0hJTkEsIFBFT1BMRVMgUkVQVUJMSUMuPC9saT48L3VsPjx1bD48bGk+Jm5ic3A7PC9saT48bGk+Jm5ic3A7PC9saT48bGk+Jm5ic3A7PC9saT48bGk+MjAxOS0xMC0yMSAwOTozNzoyMjwvbGk+PGxpPlNIRU5aSEVOLUNISU5BL+a3seWcsy3kuK3lm708L2xpPjxsaT7lv6vku7bpooTorqExMeaciDPml6XmirXovr7muK/lj6NFeHByZXNzIGlzIGV4cGVjdGVkIHRvIGFycml2ZSBhdCBwb3J0IDExLjM8L2xpPjwvdWw+PC9kaXY+PC9kaXY+ZGS1R/J9kjEG7Y6cOWqexjAk8zCX2exe87EdZoZTq2F7GQ==',
                '__VIEWSTATEGENERATOR': '6A15E89B',
                '__EVENTVALIDATION': '/wEdAAN/+cWHwHuF6+tha+Pjgzko6QLmfmzsA3xixpakJO1yl0j93FC3MjAsSJrDkFJF8PP8epjBacooIVh4XrsYamdFPlZ6wo+p2+QsBtKD26lTnQ==',
                
                'TrackingNo': 'MHE827061910013817'
            },
            callback = self.after_post
        )]

    def after_post(self, response):
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        print('********************** after_post. BEGIN')
        print(response.url)
        print(response.xpath('//input[@id="__VIEWSTATE"]/@value').get())
        print(response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').get())
        print(response.xpath('//input[@id="__EVENTVALIDATION"]/@value').get())

        for item in response.css('div.bellows__content').xpath('.//ul').getall():
            sel = scrapy.selector.Selector(text=item)
            print('{} , {}, {}'.format(
                sel.xpath('//li[4]/text()').get(),
                sel.xpath('//li[5]/text()').get(),
                sel.xpath('//li[6]/text()').get()
            ))
            titem = TrackingInfoItem()
            titem['status'] = sel.xpath('//li[4]/text()').get()
            titem['dest'] = sel.xpath('//li[5]/text()').get()
            titem['details'] = sel.xpath('//li[6]/text()').get()
            yield titem

        print('********************** after_post. END')
