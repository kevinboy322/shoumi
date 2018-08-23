# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook

class FootballPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['matchId','company','yachuzhu','yachupan','yachuke','yazhunzhu','yazhunpan','yazhunke','dachuzhu','dachupan','dachuke','dazhunzhu','dazhunpan','dazhunke'])
    def process_item(self, item, spider):
        line = [item['matchId'],item['company'],item['yachuzhu'],item['yachupan'],item['yachuke'],item['yazhunzhu'],item['yazhunpan'],item['yazhunke'],item['dachuzhu'],item['dachupan'],item['dachuke'],item['dazhunzhu'],item['dazhunpan'],item['dazhunke']]
        self.ws.append(line)
        self.wb.save('d://shoumi.xlsx')
        return item
