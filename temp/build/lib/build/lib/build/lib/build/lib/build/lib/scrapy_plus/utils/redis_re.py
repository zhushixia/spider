import pickle
import redis
from six.moves import queue as BaseQueue
from settings import REDIS_QUEUE_NAME, REDIS_QUEUE_HOST, REDIS_QUEUE_PORT, REDIS_QUEUE_DB, REDIS_TEMP

class StringTest(object):

    def __init__(self, password=None):
        self.r = redis.StrictRedis(host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT, db=REDIS_QUEUE_DB, password=password)
        self.name = REDIS_QUEUE_NAME
        self.temp_name = REDIS_TEMP

    def put(self, request):
        ''' lpush/rpush -- 从左/右插入数据 '''
        self.r.rpush(self.name, pickle.dumps(request))

    def lrem(self, request):
        self.r.lrem(self.name, 1, pickle.dumps(request))

    def get(self, req):
        resquest = self.r.lindex(self.name, 0)
        return pickle.loads(resquest)

    def count(self):
        c = self.r.llen(self.name)
        return c

if __name__ == '__main__':
    s = StringTest()
    print(s.count())
