"""爬虫组件封装"""
from scrapy_plus import Item
from scrapy_plus.https.request import Request


class Spider(object):
    """
    1.构建请求信息，生成请求对象
    2.解析响应对象，返回数据对象或新的请求对象
    """
    start_urls = []

    def start_requests(self):
        """构建初始请求对象并返回"""
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        """解析请求并返回新的请求对象或者数据对象"""
        yield Item(response.body)