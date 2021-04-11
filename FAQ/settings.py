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
COOKIES_ENABLED = True


# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'FAQ.middlewares.LoadingMiddleware': 500,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'FAQ.pipelines.DropPipeline': 200,
    'FAQ.pipelines.JsonWriterPipeline': 300,
}
USER_AGENT = "Scrapy/VERSION (+https://scrapy.org)"
