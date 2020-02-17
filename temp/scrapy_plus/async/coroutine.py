'''
由于gevent的Pool的没有close方法，也没有异常回调参数
引出需要对gevent的Pool进行一些处理，实现与线程池一样接口，实现线程和协程的无缝转换
'''
import gevent.monkey
gevent.monkey.patch_all()    # 打补丁，替换内置的模块

from gevent.pool import Pool as BasePool


class Pool(BasePool):
    '''协程池
    使得具有close方法
    使得apply_async方法具有和线程池一样的接口
    '''
    def apply_async(self, func, args=None, kwds=None, callback=None, error_callback=None):
        return super().apply_async(func, args=args, kwds=kwds, callback=callback)

    def close(self):
        '''什么都不需要执行'''
        pass