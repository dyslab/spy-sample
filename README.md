# spy-sample: Python Scrapy Learning Program

[![Powered by Scrapy](./assets/powered-by-scrapy.svg)](https://scrapy.org/) &nbsp;&nbsp;[![Github license](./assets/license-MIT.svg)](./LICENSE)

***NOTE: The project is ONLY FOR LEARNING, TEST and EDUCATIONAL PURPOSE. It is NOT dedicated to be used as a practised part for certain specific purpose.***

## Development framework: 

- Python version: v3.7

- Scrapy version: v1.8 (Check out [HERE](https://docs.scrapy.org/en/1.8/topics/commands.html) for details about Scrapy v1.8)

### Install virtual enviroment:

```bash
python3 -m venv venv
```

### Activate venv and run:

```bash
# Activate venv mode
source venv/bin/activate

# Install packages before first run. This is a one time action
pip install -r requirements.txt

# Jump to work directory and run python script
cd [project_dir] # './spytest' or './spyimg'
scrapy [command ...] # See below content

# Deactivate venv mode
deactivate
```

### Packages info

Install packages by **pip** in virtual enviroment. All packages listed in [requirements.txt](requirements.txt). 

```bash
# Check out `requirements.txt`
cat requirements.txt

# Export packages list to `requirements.txt` in virtual enviroment
pip freeze > requirements.txt
```

## Sample Scripts CLIs

```bash
# Jump into the project directory './spytest' or './spyimg'
cd ./spytest    # or, cd ./spyimg

# List all spiders belong to the project
scrapy list
```

- **spytest**

    - 🕷 [xmlsample](./spytest/spytest/spiders/xmlsample.py)

    ```bash
    # Fetch data from default url.
    scrapy crawl --nolog xmlsample -o xmlsample.csv

    # Fetch data and output to a json file from 'https://www.feng.com/rss.xml' according to the list 'avaliable_sites' in 'xmlsample.py'
    scrapy crawl xmlsample -a target=feng.com -o xmlsample.json
    ```

    - 🕷 [csvsample](./spytest/spytest/spiders/csvsample.py)

    ```bash
    scrapy crawl csvsample -o csvsample.json
    ```

    - 🕷 [sitemapsample](./spytest/spytest/spiders/sitemapsample.py)

    ```bash
    scrapy crawl sitemapsample -o sitemapsample.csv
    ```

    - _Deprecated spiders 🕷: ~~cptrack, tttrack, uspstrack~~_


- **spyimg**

    - 🕷 feimgs_svgrepo (See demos on _[./spyimg/feimgs_svgrepo_demos/README.md](./spyimg/feimgs_svgrepo_demos/README.md)_ )

    ```bash
    scrapy crawl --nolog feimgs_svgrepo -a cat=wechat
    ```

    - 🕷 feimgs_pornpics

    ```bash
    scrapy crawl --nolog feimgs_pornpics -a url=https://www.pornpics.com/galleries/met-art-diana-a-nika-b-35320148/
    ```

    - 🕷 feimgs_imagefap (Fit for the gallery which contains less than 10-page photos)

    ```bash
    scrapy crawl --nolog feimgs_imagefap -a url=https://www.imagefap.com/pictures/11922724/les1506
    ```

    - 🕷 feimgs_imagefap2 (Fit for all galleries)

    ```bash
    scrapy crawl --nolog feimgs_imagefap2 -a url=https://www.imagefap.com/gallery/11922185
    ```

    - _Deprecated spiders 🕷: ~~feimgs_mtrtsy, feimgs_kkrtys, feimgs_ojbk~~_

---

*··· Last Modified on 26 January 2024 ···*

*··· Created on 12 October 2019 ···*
