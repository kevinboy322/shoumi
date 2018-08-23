# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
from football.items import FootballItem
import urllib
import time

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
                site = response.body
                bs = BeautifulSoup(site, "html.parser")
                trs = bs.select("tr[id*='tr1_']")
                matchId = [tr.get("id")[4:] for tr in trs]
                for id in matchId:
                    item = FootballItem()
                    item['matchId'] = id
                    yaUrl = "http://vip.win007.com/AsianOdds_n.aspx?id=" + id
                    dxUrl = "http://live.titan007.com/jsData/" + id[:2] + "/" + id[2:4] + "/" + id + ".js?"
                    item = self.parse_detail(dxUrl,item)
                    time.sleep(0.5)
                    item = self.parse_ya(yaUrl,item)
                    time.sleep(0.5)
                    yield item
            except:
                pass
    def parse_detail(self,url,item):
        header = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        headers = {'User-agent': header}
        try:
            re = urllib.request.Request(url, headers=headers)
            content = urllib.request.urlopen(re).read()
            bs = BeautifulSoup(content, "html.parser",from_encoding='gb18030')
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
                item['dazhunzhu'] = str(ret[24])
                item['dazhunpan'] = str(ret[25])
                item['dazhunke'] = str(ret[26])
        except:
            pass
        return item

    def parse_ya(self,url,item):
        header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        headers = {'User-agent': header}
        try:
            re = urllib.request.Request(url, headers=headers)
            content = urllib.request.urlopen(re).read()
            bs = BeautifulSoup(content, "html.parser",from_encoding='gb18030')
            trs = bs.select("#odds tr")
            tds = []
            for a in trs:
                if 'Bet365' in a:
                    tds = a.find_all('td')
                    break
            if tds:
                item['company'] = tds[0].text
                item['yachuzhu'] = tds[2].text
                item['yachupan'] = tds[3].text
                item['yachuke'] = tds[4].text
                item['yazhunzhu'] = tds[5].text
                item['yazhunpan'] = tds[6].text
                item['yazhunke'] = tds[7].text
        except:
            pass
        return item


