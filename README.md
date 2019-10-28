# spy-sample

Scrapy Learning Program.


## Python version:  Python 3.7 or above

Install virtual enviroment:

```shell
$ python3 -m venv venv
```

Activate venv:

```shell
$ . venv/bin/activate
$ cd [project_dir]
$ scrapy [command ...]
```

## Sample Projects:


- **spytest**

    - 🕷 cptrack   (Usage: scrapy crawl --nolog cptrack -a num=FX000090696630220)

    - 🕷 tttrack   (Usage: scrapy crawl --nolog tttrack -a num=MHE827061910013817 -o tttrack.csv)

    - 🕷 uspstrack   (Usage: scrapy crawl uspstrack --nolog -o uspstrack.csv -a num=9274890983116178146826)

    - 🕷 xmlsample   (Usage: scrapy crawl --nolog xmlsample -o xmlsample.csv)

    - 🕷 csvsample   (Usage: scrapy crawl csvsample -o csvsample.json -s FEED_EXPORT_ENCODING=utf-8 -s FEED_EXPORT_INDENT=4)

    - 🕷 sitemapsample   (Usage: scrapy crawl sitemapsample -o sitemapsample.csv)


- **spyimg**

    - 🕷 fetchimgs   (Usage: scrapy crawl --nolog fetchimgs -a url=http://img.mtrtsy.com/170216/co1F216024225-[n].jpg -a startno=0)


---


Packages list: See [pip_list.txt](pip_list.txt)


Document information:

- *Last Modified on 29 October 2019*

- *Created on 12 October 2019*
