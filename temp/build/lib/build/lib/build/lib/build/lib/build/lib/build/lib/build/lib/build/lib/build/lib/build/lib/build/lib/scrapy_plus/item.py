"""item对象"""
class Item(object):
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        """
        对外提供data访问，一定程度达到保护作用，实现data参数无法进行重新赋值
        :return:
        """
        return self._data