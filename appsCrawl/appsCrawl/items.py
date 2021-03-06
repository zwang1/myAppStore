# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppscrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    icon = scrapy.Field()
    desc = scrapy.Field()
    appId  = scrapy.Field()

class AppListItem(scrapy.Item):
    title = scrapy.Field()
    list = scrapy.Field()
