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
    dazhunzhu = scrapy.Field()
    dazhunpan = scrapy.Field()
    dazhunke = scrapy.Field()

    company = scrapy.Field()
    yachuzhu = scrapy.Field()
    yachupan = scrapy.Field()
    yachuke = scrapy.Field()
    yazhunzhu = scrapy.Field()
    yazhunpan = scrapy.Field()
    yazhunke = scrapy.Field()
