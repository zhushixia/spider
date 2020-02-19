import six
from six.moves.queue import Queue

from scrapy_plus.utils.log import logger
# from scrapy_plus.utils.queue import Queue as RedisQueue
import w3lib.url
from hashlib import sha1
from scrapy_plus.conf.settings import SCHEDULER_PERSIST, MAX_RETRY_TIMES
from scrapy_plus.utils.set import RedisFilterContainer, NoramlFilterContainer
from scrapy_plus.utils.queue import Queue as RedisQueue
from scrapy_plus.utils.redis_hash import RedisBackupRequest


class Scheduler(object):
    """
    1. 缓存请求对象，并为下载器提供请求对象，实现请求的调度
    2.对请求对象进行去重判断
    """
    def __init__(self, collector):
        self._backup_request = RedisBackupRequest()
        self.collector = collector
        if SCHEDULER_PERSIST:
            self.queue = RedisQueue()
            # self.queue = StringTest()
            self._filter_container = RedisFilterContainer()
        else:
            self.queue = Queue()
            self._filter_container = NoramlFilterContainer()
        self.repeate_request_num = 0 # 统计请求重复的数量

    def add_request(self, request):
        """添加请求对象"""
        if request.filter is False:
            self.queue.put(request)
        else:
            if self._filter_request(request):
                self.queue.put(request)
        self._backup_request.save_request(request.fp, request)

    def get_request(self):
        """获取请求对象并返回"""
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            # if request.filter is True:  # 先判断 是否需要进行去重
            #     # 判断重试次数是否超过规定
            #     fp = self._gen_fp(request)
            #     if request.retry_time >= MAX_RETRY_TIMES:
            #         self._backup_request.delete_request(fp)  # 如果超过，那么直接删除
            #         logger.warnning("出现异常请求，且超过最大尝试的次数：[%s]%s" % (request.method, request.url))
            #         return None
            #     request.retry_time += 1  # 重试次数+1
            #
            #     self._backup_request.update_request(fp, request)  # 并更新到备份中
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

    def delete_request(self, request):
        '''根据请求从备份删除对应的请求对象'''
        fp = self._gen_fp(request)
        self._backup_request.delete_request(fp)

    def add_lost_reqeusts(self):
        '''将丢失的请求对象再添加到队列中'''
        # 从备份容器取出来，放到队列中
        for request in self._backup_request.get_requests():
            self.queue.put(request)




