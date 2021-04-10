"""
-*- coding: utf-8 -*-

Define your item pipelines here

Don't forget to add your pipeline to the ITEM_PIPELINES setting
See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""
import pymongo
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


class MongoPipeline:
    """
    Pipeline to store extracted items
    """
    collection_name = 'collection'

    def __init__(self, mongo_uri, mongo_db, enabled):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_enabled = enabled

    @classmethod
    def from_crawler(cls, crawler):
        """
        Mongo connection params. Selects crawler settings first (in case they
        are overriding the env params) and as default uses environment
        variables
        :param crawler: crawler settings
        :return:
        """
        mongo_enabled = crawler.settings.get('MONGO_DB_ENABLED', False)
        if mongo_enabled:
            return cls(
                mongo_uri=crawler.settings.get(
                    'MONGO_DB_CONNECTION'),
                mongo_db=crawler.settings.get(
                    'MONGO_DB_NAME'),
                enabled=mongo_enabled
            )
        return cls(mongo_uri=None, mongo_db=None, enabled=False)

    def open_spider(self, spider):
        if self.mongo_enabled:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            if self.check_duplicate(spider):
                spider.logger.warning("company already exist in the DB , removing the old version")
                self.db[self.collection_name].delete_many({"company": spider.company_name})

    def close_spider(self, spider):
        if self.mongo_enabled:
            self.client.close()

    def process_item(self, item, spider):
        if self.mongo_enabled:
            self.db[self.collection_name].insert_one(dict(item))
        return item

    def check_duplicate(self, spider):
        """check if the company already exists or not"""
        companies = self.db[self.collection_name].distinct('company')
        return spider.company_name in companies
