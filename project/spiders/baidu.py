# project_dir/spiders/baidu.py
from scrapy_plus.cores.spider import Spider

# 继承框架的爬虫基类
class BaiduSpider(Spider):
    name = 'baidu'
    start_urls = ['http://www.baidu.com']*3    # 设置初始请求url