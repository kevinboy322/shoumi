# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import urllib
import pymysql

class ProxyMiddleware(object):
    def __init__(self):
        self.client = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',  #使用自己的用户名
            passwd='root',  # 使用自己的密码
            db='ceshi',  # 数据库名
            charset='utf8'
        )
        self.cur = self.client.cursor()

    # 接口获取代理IP
    def get_get_ip(self):
        APIurl = "http://dev.kdlapi.com/api/getproxy/?orderid=973500483852076&num=100&area=%E5%9B%BD%E5%86%85&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&sp2=1&sep=1"
        res = urllib.request.urlopen(APIurl).read().decode("utf-8")
        IPs = res.split("\n")
        # 入库
        for a in IPs:
            try:
                proxy_handler = urllib.request.ProxyHandler({"http": a})
                opener = urllib.request.build_opener(proxy_handler)
                urllib.request.install_opener(opener)
                html = urllib.request.urlopen('http://live.titan007.com/', timeout=1)
                if (html.status == 200):
                    sql = 'insert into ips(ip) VALUES (%s)'
                    lis = (a)
                    self.cur.execute(sql, lis)
                    self.client.commit()
                else:
                    continue
            except:
                continue



    def get_random_ip(self):
        try:
            sql = 'select * from ips'
            self.cur.execute(sql)
            result = self.cur.fetchone()
            if result:
                pass
            else:
                self.get_get_ip()
            # 删除该条
            del_sql = 'delete from ips where id=%s'
            val = (result[0])
            self.cur.execute(del_sql,val)
            self.client.commit()
            return 'http://' + result[1]
        except:
            return ''

    def process_request(self, request, spider):
        ip = self.get_random_ip()
        request.meta['proxy'] = ip

    # 爬取可用代理ip
    def getIp(self):
        Ips = []
        # num = random.randint(1, 2)
        xiciUrl = 'http://www.xicidaili.com/nn/1'
        # kuaidailiUrl = 'https://www.kuaidaili.com/free/inha/1'
        header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        headers = {'User-agent': header}
        request = urllib.request.Request(xiciUrl, headers=headers)
        content = urllib.request.urlopen(request).read()
        bs = BeautifulSoup(content, "html.parser")
        res = bs.find_all('tr')
        for item in res:
            try:
                tds = item.find_all('td')
                ip = tds[1].text
                port = tds[2].text
                server = ip + ":" + str(port)
                proxy_handler = urllib.request.ProxyHandler({"http": server})
                opener = urllib.request.build_opener(proxy_handler)
                urllib.request.install_opener(opener)
                html = urllib.request.urlopen('http://live.titan007.com/')
                if (html.status == 200):
                    Ips.append(server)
                    return Ips
            except:
                pass
        return Ips

class FootballSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FootballDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
