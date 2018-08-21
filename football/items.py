# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FootballItem(scrapy.Item):
    matchId = scrapy.Field()
    dachuzhu = scrapy.Field()
    dachupan = scrapy.Field()
    dachuke = scrapy.Field()
    yapan = scrapy.Field()
