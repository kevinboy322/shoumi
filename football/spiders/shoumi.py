# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
import urllib.request
import requests
import urllib.parse
import random

class ShoumiSpider(scrapy.Spider):
    name = 'shoumi'
    # allowed_domains = ['live.titan007.com']
    # start_urls = ['http://live.titan007.com/']
    start_urls = ['http://op1.win007.com/oddslist/1496804.htm']

    # request需要封装成SplashRequest
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,self.parse_oupan,args={'wait': '0.5'})
            # yield SplashRequest(url, self.parse_oupan, endpoint='execute', args={'lua_source': self.script, 'wait': '0.5'})
            # arr = self.getIp()
            # yield scrapy.Request(url)

    def parse(self, response):
        if response.status == 200:
            num = 1
            site = Selector(response)
            trList = site.xpath('//table[@id="table_live"]/tr')
            for sel in trList:
                if num == 1:
                    num += 1
                    continue
                else:
                    gameId = sel.xpath('td[5]/@onclick').re('(?<=\()(.+?)(?=\))')
    def parse_oupan(self,response):
        if response.status == 200:
            site = response.body
            bs = BeautifulSoup(site, "html.parser")
            trs = bs.select('#oddsList_tab > tbody > tr')
            print(trs)

    # 爬取可用代理ip
    def getIp(self):
        Ips = []
        num = random.randint(1,3366)
        url = 'http://www.xicidaili.com/nn/'+str(num)
        header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        headers = {'User-agent': header}
        request = urllib.request.Request(url, headers=headers)
        content = urllib.request.urlopen(request).read()
        bs = BeautifulSoup(content,"html.parser")
        res = bs.find_all('tr')
        for item in res:
            try:
                tds = item.find_all('td')
                ip = tds[1].text
                port = tds[2].text
                server = ip+ ":" + str(port)
                proxy_handler = urllib.request.ProxyHandler({"http": server})
                opener = urllib.request.build_opener(proxy_handler)
                urllib.request.install_opener(opener)
                html = urllib.request.urlopen('https://www.baidu.com/')
                if(html.status==200):
                    Ips.append(server)
            except:
                pass
        return Ips
