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
        self.ws.append(['matchId','yapan','dachuzhu','dachupan','dachuke'])
    def process_item(self, item, spider):
        line = [item['matchId'],item['yapan'],item['dachuzhu'],item['dachupan'],item['dachuke']]
        self.ws.append(line)
        self.wb.save('data.xlsx')
        return item
