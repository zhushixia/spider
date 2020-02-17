# 修改默认日志文件名称
DEFAULT_LOG_FILENAME = '日志.log'    # 默认日志文件名称

# 增加以下信息：
# 启用的爬虫类
SPIDERS = [
    'spiders.baidu.BaiduSpider',
    'spiders.douban.DoubanSpider',
    # 'spiders.sina.SinaGunDong'
]

# 启用的管道类
PIPELINES = [
    # 'pipelines.BaiduPipeline',
    # 'pipelines.DoubanPipeline'
]
MAX_ASYNC_NUMBER = 5
# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = []

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = []

# 异步方式  thread、coroutine
ASYNC_TYPE = 'thread' # coroutine/thread

SCHEDULER_PERSIST = True

# redis队列默认配置
REDIS_QUEUE_NAME = 'request_queue'
REDIS_QUEUE_HOST = '192.168.80.157'
REDIS_QUEUE_PORT = 6379
REDIS_QUEUE_DB = 0

# REDIS集合配置
REDIS_SET_NAME = "filter_set"
REDIS_SET_HOST = '192.168.80.157'
REDIS_SET_PORT = 6379
REDIS_SET_DB = 0