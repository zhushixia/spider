import six
from six.moves.queue import Queue

from scrapy_plus.utils.log import logger
from scrapy_plus.utils.queue import Queue as RedisQueue
import w3lib.url
from hashlib import sha1
from scrapy_plus.conf.settings import SCHEDULER_PERSIST
from scrapy_plus.utils.redis_re import StringTest
from scrapy_plus.utils.set import RedisFilterContainer, NoramlFilterContainer


class Scheduler(object):
    """
    1. 缓存请求对象，并为下载器提供请求对象，实现请求的调度
    2.对请求对象进行去重判断
    """
    def __init__(self, collector):
        self.collector = collector
        self.queue =  Queue()
        if SCHEDULER_PERSIST:
            # self.queue = RedisQueue()
            self.queue = StringTest()
            self._filter_container = RedisFilterContainer()
        else:
            self.queue = Queue()
            self._filter_container = NoramlFilterContainer()
        self.repeate_request_num = 0 # 统计请求重复的数量

    def add_request(self, request):
        """添加请求对象"""
        if self._filter_request(request):
            self.queue.put(request)

    def get_request(self):
        """获取请求对象并返回"""
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            return request

    def _filter_request(self, request):
        """请求去重"""
        # 生成去重的一个指纹， 利用sha1
        request.fp = self._gen_fp(request)
        if not self._filter_container.exists(request.fp):
            self._filter_container.add_fp(request.fp)
            return True
        else:
            logger.info("发现重复的请求：<%s>" % request.url)
            self.collector.incr(self.collector.repeat_request_nums_key)
            return False

    def _gen_fp(self,request):
        """请求去重，计算指纹"""
        # url排序，借助w3lib。url模块中的canonicalize_url方法
        url = w3lib.url.canonicalize_url(request.url)
        method = request.method.upper()
        data = request.data if request.data is not None else {}
        data = sorted(data.items(), key=lambda x:x[0])

        # 利用sha1算法，计算指纹
        s1 = sha1()
        # 为了兼容py2和py3,利用_to_bytes方法, 把所有字符串转化成byte类型
        s1.update(self._to_bytes(url))
        s1.update(self._to_bytes(method))
        s1.update(self._to_bytes(str(data)))

        fp = s1.hexdigest()
        return fp

    @staticmethod
    def _to_bytes(string):
        if six.PY2:
            if isinstance(string, str):
                return string
            else:  # 如果是python2的unicode类型，转化为字节类型
                return string.encode("utf-8")
        elif six.PY3:
            if isinstance(string, str):  # 如果是python3的str类型，转化为字节类型
                return string.encode("utf-8")
            else:
                return string

