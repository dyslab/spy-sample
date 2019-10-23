# spy-sample

Scrapy Learning Program.


## Python version (venv mode):  Python 3.7.3

```shell
$ . bin/activate
```


## Spiders:

- 🕷 cptrack   (Usage: scrapy crawl --nolog cptrack -a num=FX000090696630220)

- 🕷 tttrack   (Usage: scrapy crawl --nolog tttrack -a num=MHE827061910013817 -o tttrack.csv)

- 🕷 uspstrack   (Usage: scrapy crawl uspstrack --nolog -o uspstrack.csv -a num=9274890983116178146826)

- 🕷 xmlsample   (Usage: scrapy crawl --nolog xmlsample -o xmlsample.csv)

- 🕷 csvsample   (Usage: scrapy crawl csvsample -o csvsample.json -s FEED_EXPORT_ENCODING=utf-8 -s FEED_EXPORT_INDENT=4)

- 🕷 sitemapsample   (Usage: scrapy crawl sitemapsample -o sitemapsample.csv)


---


Document information:

- *Last Modified on 23 October 2019*

- *Created on 12 October 2019*
