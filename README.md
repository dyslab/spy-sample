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

    - 🕷 cptrack

        ```shell
        $ scrapy crawl --nolog cptrack -a num=FX000090696630220
        ```

    - 🕷 tttrack

        ```shell
        $ scrapy crawl --nolog tttrack -a num=MHE827061910013817 -o tttrack.csv
        ```

    - 🕷 uspstrack

        ```shell
        $ scrapy crawl uspstrack --nolog -o uspstrack.csv -a num=9274890983116178146826
        ```

    - 🕷 xmlsample

        ```shell
        $ scrapy crawl --nolog xmlsample -o xmlsample.csv
        ```

    - 🕷 csvsample

        ```shell
        $ scrapy crawl csvsample -o csvsample.json -s FEED_EXPORT_ENCODING=utf-8 -s FEED_EXPORT_INDENT=4
        ```

    - 🕷 sitemapsample

        ```shell
        $ scrapy crawl sitemapsample -o sitemapsample.csv
        ```


- **spyimg**

    - 🕷 fetchimgs

        ```shell
        $ scrapy crawl --nolog fetchimgs -a url=http://img.mtrtsy.com/170216/co1F216024225-[n].jpg -a startno=0
        ```

    - 🕷 feimgs_kkrtys

        ```shell
        $ scrapy crawl --nolog feimgs_kkrtys -a url=http://kkrtys.com/guomo/2018/0523/381.html
        ```

    - 🕷 feimgs_ojbk

        ```shell
        $ scrapy crawl --nolog feimgs_ojbk -a url=http://www.ojbk.cc/metcn/6904.html
        ```


---


Packages list: See [pip_list.txt](pip_list.txt)


Document information:

- *Last Modified on 31 October 2019*

- *Created on 12 October 2019*
