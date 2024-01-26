# Demos of the spider 'feimgs_svgrepo'

```bash
# Fetch 'wechat' SVG files and save to the sub-directory './wechat/'
scrapy crawl --nolog feimgs_svgrepo -a cat=wechat

# Fetch 'git' SVG files and save to the sub-directory './git/'
scrapy crawl --nolog feimgs_svgrepo -a cat=git

# Fetch 'github' SVG files and save to the sub-directory './github/'
scrapy crawl --nolog feimgs_svgrepo -a cat=github

# # Fetch 'anti-virus' SVG files and save to the sub-directory './anti-virus/'
scrapy crawl --nolog feimgs_svgrepo -a cat=anti-virus

# # Fetch 'windows' SVG files and save to the sub-directory './windows/'
scrapy crawl --nolog feimgs_svgrepo -a cat=windows
```
