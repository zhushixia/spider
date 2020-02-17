from scrapy_plus.cores.spider import Spider

# 继承框架的爬虫基类
from scrapy_plus.https.request import Request


#https://movie.douban.com/j/search_subjects?type=movie&tag=热门&page_limit=50&page_start=0


class DoubanSpider(Spider):
    name = 'doubai'
    start_urls = ['https://www.guokr.com/search/all/?page=1&wd=问答']

    def start_requests(self):
        base_url = 'https://www.guokr.com/search/all/?page={}&wd=问答'
        for i in range(1,3):
            yield Request(base_url.format(i))

    def parse(self, response):
        lis = response.xpath('//ul[@class="items"]/li')
        for li in lis[1:]:
            item = {}
            item['title'] = li.xpath('.//h2/a/text()')[0]
            item['href'] ='https://www.guokr.com/' + li.xpath('.//h2/a/@href')[0]
            yield Request(item['href'], parse='parse_detail', meta={'item': item})
    def parse_detail(self, response):
         '''解析详情页'''
         item = response.meta["item"]
         yield item