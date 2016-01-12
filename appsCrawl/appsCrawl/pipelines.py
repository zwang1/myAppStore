# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log


class AppscrawlPipeline(object):

    def __init__(self):
        print "===========begin"
        client = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DB']]
        print str(db)
        print "connection to db"
        self.collection = db[settings['MONGODB_COLLECTION']]
       # print "get collection" + self.collection

    def process_item(self, item, spider):
        valid = True
        print "processing item"
        for data in item:
            # here we only check if the data is not null
            # but we could do any crazy validation we want
            if not data:
                valid = False
                raise DropItem("Missing %s of APP from %s" % (data, item['url']))
        if valid:
            print "before insert"
            self.collection.insert(dict(item))
            print " after insert"
            log.msg("Item wrote to MongoDB database %s/%s" %
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider)
        return item


class AppListPipeline(object):

    def __init__(self):
        print "===========begin"
        client = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DB']]
        print str(db)
        print "connection to db"
        self.collection = db[settings['MONGODB_COLLECTION2']]
       # print "get collection" + self.collection

    def process_item(self, item, spider):
        valid = True
        print "processing item"
        for data in item:
            # here we only check if the data is not null
            # but we could do any crazy validation we want
            if not data:
                valid = False
                raise DropItem("Missing %s of APP from %s" % (data, item['url']))
        if valid:
            print "before insert"
            self.collection.insert(dict(item))
            print " after insert"
            log.msg("Item wrote to MongoDB database %s/%s" %
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION2']),
                    level=log.DEBUG, spider=spider)
        return item

