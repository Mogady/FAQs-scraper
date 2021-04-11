"""
-*- coding: utf-8 -*-

Define your item pipelines here

Don't forget to add your pipeline to the ITEM_PIPELINES setting
See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""
import json
import os
from scrapy.exceptions import DropItem
from FAQ.validation import validate_doc
from itemadapter import ItemAdapter


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class DropPipeline:
    def __init__(self):
        self.seen_faq = set()

    def process_item(self, item, spider):
        if item['answer']:
            if isinstance(item['answer'], list):
                item['answer'] = '\n'.join(item['answer']).strip()
            else:
                item['answer'] = item['answer'].strip()
        try:
            schema_check = validate_doc(dict(item), spider.company_name, spider.logger)
        except AttributeError as e:
            raise DropItem("Dropped: spider Company name is not provided")
        if not schema_check:
            raise DropItem("Dropped: Error in FAQ Json Schema: %s" % item)

        item['question'] = item['question'].strip()

        if item['question'] in self.seen_faq:
            raise DropItem("Dropped: Duplicate item found: %s" % item)
        self.seen_faq.add(item['question'])

        return item


class JsonWriterPipeline:
    def __init__(self, settings):
        self.company = settings['name']
        self.items = []
        os.makedirs(os.path.join(ROOT_DIR, self.company), exist_ok=True)
        self.file = open(os.path.join(ROOT_DIR, self.company, 'FAQs.json'), 'w')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
