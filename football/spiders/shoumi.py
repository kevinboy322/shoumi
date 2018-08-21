# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
from football.items import FootballItem
from bs4 import UnicodeDammit

class ShoumiSpider(scrapy.Spider):
    name = 'shoumi'
    # allowed_domains = ['live.titan007.com']
    start_urls = ['http://live.titan007.com/']

    # request需要封装成SplashRequest
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': '0.5'})

    def parse(self, response):
        if response.status == 200:
            try:
                item = FootballItem()
                site = response.body
                bs = BeautifulSoup(site, "html.parser")
                trs = bs.select("tr[id*='tr1_']")
                matchId = [tr.get("id")[4:] for tr in trs]
                for id in matchId:
                    item['matchId'] = id
                    dxUrl = "http://live.titan007.com/jsData/"+id[:2]+"/"+id[2:4]+"/"+id+".js?"
                    yield scrapy.Request(dxUrl,meta={'item':item},callback=self.parse_detail, dont_filter=True)
            except:
                pass
    def parse_detail(self,response):
        item = response.meta['item']
        if response.status == 200:
            try:
                site = response.body
                bs = BeautifulSoup(site, "html.parser")
                data = bs.text.strip('var sOdds=').strip('[[').strip(']]').split('],[')
                ret = []
                for a in data:
                    if '未开场' in a:
                        ret = a.split(',')
                        break
                if ret:
                    item['dachuzhu'] = str(ret[21])
                    item['dachupan'] = str(ret[22])
                    item['dachuke'] = str(ret[23])
            except:
                pass
        yaUrl = "http://vip.win007.com/AsianOdds_n.aspx?id="+item['matchId']
        yield scrapy.Request(yaUrl,meta={'item':item},callback=self.parse_ya, dont_filter=True)

    def parse_ya(self,response):
        item = response.meta['item']
        if response.status == 200:
            try:
                site = response.body
                bs = BeautifulSoup(site, "html.parser", from_encoding="gb18030")
                trs = bs.select("#odds tr")[2:][:-2]
                item['yapan'] = trs[2].find_all('td')[3].text
            except:
                pass
        yield item

