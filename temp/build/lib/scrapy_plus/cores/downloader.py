"""下载器组件"""
import requests

from scrapy_plus.https.response import Response
from scrapy_plus.utils.log import logger


class Downloader(object):
    """根据请求对象，发起http请求， 获取响应"""

    def get_response(self,request):
        """发起请求获取响应"""
        if request.method.upper() == 'GET':
            resp = requests.get(request.url, headers=request.headers, params=request.params)
        elif request.method.upper() == 'POST':
            resp = request.post(request.url, headers=request.headers, params=request.params, data=request.data)
        else:
            raise Exception('不支持的请求方法')
        logger.info("<{} {}>".format(resp.status_code, resp.url))
        return Response(resp.url, resp.content, resp.headers, resp.status_code)