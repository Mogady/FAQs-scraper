"""
Configuration package for scrapy project
"""
import json
import os

# -*- coding: utf-8 -*-

# Scrapy settings for FAQ project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'FAQ'

LOG_LEVEL = 'DEBUG'

SPIDER_MODULES = ['FAQ.spiders']
NEWSPIDER_MODULE = 'FAQ.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 20

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2

# Disable cookies (enabled by default)
COOKIES_ENABLED = False


# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'FAQ.middlewares.RandomUserAgentMiddleware': 400,
    'FAQ.middlewares.LoadingMiddleware': 500,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'FAQ.pipelines.DropPipeline': 200,
    'FAQ.pipelines.JsonWriterPipeline': 300,
}

# # Custom settings for FAQ DB
MONGO_DB_ENABLED = True
MONGO_DB_CONNECTION = 'address'
MONGO_DB_NAME = 'db_name'

USER_AGENT_LIST = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.91 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/63.0.3239.108 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (Macintosh; '
     'Intel Mac OS X 10_15_1) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/81.0.4044.138 Safari/537.36'),
    ('Mozilla/5.0 (Macintosh; '
     'Intel Mac OS X 10_15_1) '
     'AppleWebKit/537.36 '
     '(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')
]
