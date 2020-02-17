import importlib

SPIDERS = [
    'spiders.baidu.BaiduSpider',
    'spiders.douban.DoubanSpider'
]
def test(SPIDERS=[]):
    for path in SPIDERS:
        module_name = path.rsplit(".", 1)[0]  # 取出模块名称
        cls_name = path.rsplit(".", 1)[1]  # 取出类名称
        ret = importlib.import_module(module_name)  # 动态导入爬虫模块
        cls = getattr(ret, cls_name)
        print(cls)
        de = getattr(cls(), "start_requests") # start_requests是cls类中实现的一个方法
        print(de)

test(SPIDERS)
