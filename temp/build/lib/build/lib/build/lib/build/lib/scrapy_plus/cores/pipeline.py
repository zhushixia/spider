"""管道的封装"""
from scrapy_plus.item import Item


class Pipeline(object):
    """负责处理数据对象"""

    def process_item(self, item, spider):
        """处理item对象"""
        print('item:', item)