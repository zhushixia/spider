"""封装request对象"""


class Request():
    def __init__(self, url, method='GET', headers=None, params=None, data=None, parse='parse', meta=None, filter=True):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.parse = parse
        self.meta = meta
        self.filter = filter
