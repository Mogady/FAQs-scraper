"""
Middlewares for scrapy projects
"""
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random


class RandomUserAgentMiddleware(UserAgentMiddleware):
    """
    Middleware to use random user agent to avoid banning
    """

    def __init__(self, settings, user_agent='Scrapy'):
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent
        user_agent_list_file = settings.get('USER_AGENT_LIST')
        if not user_agent_list_file:
            # If USER_AGENT_LIST_FILE settings is not set,
            # Use the default USER_AGENT or whatever was
            # passed to the middleware.
            ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/81.0.4044.138 Safari/537.36 '
            self.user_agent_list = [ua]
        else:
            self.user_agent_list = user_agent_list_file

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened,
                                signal=signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)


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
