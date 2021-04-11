# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FAQItem(scrapy.Item):
    # define the fields for your item here like:
    html_url = scrapy.Field(serializer=str)
    company = scrapy.Field(serializer=str)
    category = scrapy.Field(serializer=str)
    question = scrapy.Field(serializer=str)
    answer = scrapy.Field(serializer=str)



