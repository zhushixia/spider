from scrapy_plus.utils.stats_collector import StatsCollector

s = StatsCollector(spider_names=['a', 'b'], host='192.168.80.157', port='6379', db=0)
s.start_request_nums
