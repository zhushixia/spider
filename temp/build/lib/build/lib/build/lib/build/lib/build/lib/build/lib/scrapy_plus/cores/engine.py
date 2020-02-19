"""引擎组件"""
from copy import deepcopy
from datetime import datetime

import settings
# 判断使用什么异步模式，改用对应的异步池
if settings.ASYNC_TYPE == 'thread':
    from multiprocessing.dummy import Pool    # 导入线程池对象
elif settings.ASYNC_TYPE == 'coroutine':
    from scrapy_plus.async.coroutine import Pool
else:
    raise Exception("不支持的异步类型：%s, 只能是'thread'或者'coroutine'" % settings.ASYNC_TYPE)
import importlib
from scrapy_plus.utils.log import logger
from scrapy_plus.https.request import Request
from .scheduler import Scheduler
import time
from scrapy_plus.conf.settings import SPIDERS, PIPELINES, \
    SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES


from .downloader import Downloader
from scrapy_plus.utils.stats_collector import StatsCollector


class Engine(object):
    """
    1.对外提供整个的程序入口
    2.依次调用其他组件对外提供的接口，实现整个框架的运作
    """
    def __init__(self):
        self.spiders = self._auto_import_instances(SPIDERS, isspider=True)
        self.downloader = Downloader()
        self.piplines = self._auto_import_instances(PIPELINES)
        self.collector = StatsCollector(list(self.spiders.keys()))
        self.scheduler = Scheduler(self.collector)
        # self.total_request_nums = 0
        # self.total_response_nums = 0
        self.downloader_mids = self._auto_import_instances(DOWNLOADER_MIDDLEWARES)
        self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES)
        self.pool = Pool()  # 创建线程池对象

    def start(self):
        """启动整个引擎"""
        start = datetime.now()
        logger.info("开始运行时间：%s" % start)
        logger.info("运行的爬虫有：%s" % self.spiders)
        logger.info("开启的爬虫中间件有：%s" % self.spider_mids)
        logger.info("开启的下载中间件有：%s" % self.downloader_mids)
        self.running = False  # 记录是否退出程序的状态
        logger.info("启用的管道有：%s" % self.piplines)
        self._start_engine()
        stop = datetime.now()
        logger.info("结束运行时间：%s" % stop)
        logger.info("耗时：%.2f" % (stop-start).total_seconds())
        logger.info("一共获取了请求：{}个".format(self.collector.request_nums))
        logger.info("重复的请求：{}个".format(self.collector.repeat_request_nums))
        logger.info("成功的请求：{}个".format(self.collector.response_nums))
        self.collector.clear()

    def _start_request(self):
        # 1.爬虫模块发出初始请求
        print(self.spiders.items())
        for spider_name, spider in self.spiders.items():
            # def _func(spider_name, spider):
            for start_request in spider.start_requests():
                print(start_request)
            # 2.把初始请求添加给调度器
            # 利用爬虫中间件预处理对象
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)
                start_request.spider_name = spider_name
                self.collector.incr(self.collector.request_nums_key)
                self.scheduler.add_request(start_request)
            # for spider_name, spider in self.spiders.items():
            #     self.pool.apply_async(_func, args=(spider_name, spider), callback=self._callback_total_finshed_start_requests_number)

    # def _callback_total_finshed_start_requests_number(self, temp):
    #     '''记录完成的start_requests的数量'''
    #     self.collector.incr(self.collector.start_request_nums_key)


    def _execute_request_response_item(self):
        # 3.从调度器获取请求对象，交给下载器发起请求，获取响应对象
        request = self.scheduler.get_request()
        if request is None:  # 如果没有获取到请求对象，直接返回
            return
        # 利用下载器中间件预处理请求对象
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)
        # 4.利用下载器发起请求
        response = self.downloader.get_response(request)
        # if response.status_code >= 200 and response.status_code < 300:
        self.scheduler.delete_request(request)
        response.meta = request.meta
        # 5.利用爬虫解析响应的方法，处理响应，得到结果
        # 利用下载器中间件预处理响应对象
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)
        spider = self.spiders[request.spider_name]
        parse = getattr(spider, request.parse)
        for result in parse(response):
            # 6.判断结果对象
            # 6.1如果是请求对象，交给调度器
            if isinstance(result, Request):
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)
                result.spider_name = request.spider_name
                self.scheduler.add_request(result)
                self.collector.incr(self.collector.request_nums_key)
            # 6.2否则，就交给管道处理
            else:
                for pipeline in self.piplines:
                    result = pipeline.process_item(result, spider)
        # else:
        #     self.scheduler.add_lost_reqeusts()
        self.collector.incr(self.collector.response_nums_key)

    def _auto_import_instances(self, path=[], isspider=False):
        if isspider is True:
            instance = {}
        else:
            instance = []
        for p in path:
            module_name = p.rsplit('.', 1)[0] # 取出模块名称
            cls_name = p.rsplit('.', 1)[1] #取出类名称
            ret = importlib.import_module(module_name)
            cls = getattr(ret, cls_name)
            if isspider is True:
                instance[cls.name] = cls()
            else:
                instance.append(cls())
        return  instance

    def _callback(self, temp):
        '''执行新的请求的回调函数，实现循环'''
        if self.running is True:  # 如果还没满足退出条件，那么继续添加新任务，否则不继续添加，终止回调函数，达到退出循环的目的
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)

    def _error_callback(self, exception):
        '''异常回调函数'''
        try:
            raise exception  # 抛出异常后，才能被日志进行完整记录下来
        except Exception as e:
            logger.exception(e)


    def _start_engine(self):
        """
        具体实现引擎细节
        :return:
        """
        self.running = True #启动引擎，设置状态为True
        self.pool.apply_async(self._start_request, error_callback=self._error_callback) # 使用异步
        for i in range(settings.MAX_ASYNC_NUMBER):
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback, error_callback=self._error_callback)
        # # 设置循环，处理多个请求
        while True:
            time.sleep(0.0001) # 避免cpu空转，消耗性能
            if self.collector.request_nums != 0:
                if self.collector.response_nums + self.collector.repeat_request_nums >= self.collector.request_nums:
                    self.is_running = False
                    break