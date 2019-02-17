# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from crwalIp import items
import time
import os
import requests
import telnetlib
import fake_useragent


class XsdailiSpider(scrapy.Spider):
    name = 'xsdaili'
    # allowed_domains = ['www.xsdaili.com/dayProxy/2019/1/2.html']
    # start_urls = ['http://www.xsdaili.com/dayProxy/2019/1/2.html/']
    ua = fake_useragent.UserAgent()
    headers = {
        "useragent": ua.random,
    }

    def start_requests(self):
        """
        起点，采集两个月内的ip
        """
        i_year = int(time.strftime("%Y"))
        i_month = int(time.strftime("%m"))
        if i_month == 1:
            i_oldyear = i_year - 1
            i_oldmonth = 12
        else:
            i_oldmonth = i_month - 1
            i_oldyear = i_year
        s_nowtime = str(i_year) + '/'+str(i_month)
        s_oldtime = str(i_oldyear) + '/' + str(i_oldmonth)
        l_url = [
            'http://www.xsdaili.com/dayProxy/{}/1.html'.format(s_nowtime),
            'http://www.xsdaili.com/dayProxy/{}/1.html'.format(s_oldtime),
        ]
        for s_url in l_url:
            yield Request(url=s_url, callback=self.ListDetail, headers=self.headers)

    def ListDetail(self, response):
        """
        解析列表，进行请求详情页
        """
        l_pageUrl = response.xpath(
            '//div[@class="panel-body"]//div[@class="title"]//a/@href').extract()
        for url in l_pageUrl:
            yield Request(url=response.urljoin(url), callback=self.parse, headers=self.headers)

        # 判断是否还有下一页
        l_nextUrl = response.xpath(
            '//div[@class="page"]//a[last()-1 and text()="下一页"]').extract()
        if l_nextUrl:
            yield Request(url=response.urljoin(l_nextUrl[0]), callback=self.ListDetail, headers=self.headers)

    def parse(self, response):
        """
        明细解析
        """
        l_ipXpath = response.xpath("//div[@class='cont']/text()")
        l_ip = l_ipXpath.extract()
        for ip in l_ip:
            obj_crwalipItem = items.CrwalipItem()
            try:
                obj_crwalipItem['s_ip'] = ip.strip().split("@")[0]
            except Exception as e:
                continue
            obj_crwalipItem['dt_crwalTime'] = time.strftime(
                "%Y-%m-%d %H:%M:%S")

            # 测试代理ip是否有用
            s_ip, s_port = obj_crwalipItem['s_ip'].split(":")
            try:
                self.ipProxyTest(s_ip, s_port)
                print(
                    "time:【{}】,ip【{}】----OK".format(obj_crwalipItem['dt_crwalTime'], s_ip))
            except Exception as e:
                print("time:【{}】,ip【{}】,Error:【{}】".format(
                    obj_crwalipItem['dt_crwalTime'], s_ip, e))
                continue
            yield obj_crwalipItem

    def ipProxyTest(self, s_ip, s_port):
        """
        IP是否生效检测
        """
        telnetlib.Telnet(s_ip, port=s_port, timeout=2)
