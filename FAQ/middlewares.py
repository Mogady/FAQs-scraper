"""
Middlewares for scrapy projects
"""
from scrapy import signals

class LoadingMiddleware:
    """
    Middleware used to wait for JS to load
    """

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls()

    def process_request(self, request, spider):
        try:
            res = spider.process_request(request)
            return res
        except Exception as e:
            spider.logger.warning(e)
            return None
