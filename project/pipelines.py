from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider

class BaiduPipeline(object):

    """由此来判断item是属于哪个爬虫的对象"""
    def process_item(self, item, spider):
        """处理item"""
        if isinstance(spider, BaiduSpider):
            print("这是百度爬虫管道的数据")
        return item

class DoubanPipeline(object):
    def process_item(self, item, spider):
        """处理item"""
        if isinstance(spider, DoubanSpider):
            print("这是豆瓣爬虫管道的数据")
        return item
