"""封装Response对象"""
import json
import re

from lxml import etree


class Response(object):
    def __init__(self, url, body, headers, status_code, meta={}):
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.meta = meta

    def xpath(self, rule):
        """提供xpath方法"""
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        """提供json解析"""
        return json.loads(self.body)

    def re_findall(self, rule, data=None):
        """封装正则的findall方法"""
        if data is None:
            data = self.body
        return re.findall(rule, data)

