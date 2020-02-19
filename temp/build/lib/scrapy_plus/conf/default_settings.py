import logging

# 默认的日志配置
DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s[line:%(lineno)d] \
                  %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'log.log'    # 默认日志文件名称

MAX_ASYNC_NUMBER = 5

# 异步方式  thread、coroutine
ASYNC_TYPE = 'coroutine' # coroutine/thread

# 如果是False, 不会说那个redis队列，会使用python的set存储指纹和请求
SCHEDULER_PERSIST = False
# redis队列默认配置
REDIS_QUEUE_NAME = 'request_queue'
REDIS_QUEUE_HOST = '192.168.80.157'
REDIS_QUEUE_PORT = 6379
REDIS_QUEUE_DB = 0

# REDIS集合配置
REDIS_SET_NAME = 'filter_set'
REDIS_SET_HOST = '192.168.80.157'
REDIS_SET_PORT = 6379
REDIS_SET_DB = 0
#默认重试次数
MAX_RETRY_TIMES = 3

REDIS_BACKUP_NAME = "back_request"
REDIS_BACKUP_HOST = "192.168.80.157"
REDIS_BACKUP_PORT = 6379
REDIS_BACKUP_DB = 0