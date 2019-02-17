# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from crwalIp import items
import time
import os
import requests
import telnetlib


class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'
    # allowed_domains = ['www.kuaidaili.com/free/intr/']
    # start_urls = ['http://www.kuaidaili.com/free/intr//']
    i_endPageNum = 0

    def start_requests(self):
        # 首页进行爬取
        start_urls = [
            'https://www.kuaidaili.com/free/intr/1',
            'https://www.kuaidaili.com/free/inha/1'
        ]
        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # 提取页面数据
        # //div[@id="content"]/div[@class="con-body"]//table/tbody/tr
        print("正在解析：{}".format(response.url))
        l_tr = response.xpath(
            '//div[@id="content"]/div[@class="con-body"]//table/tbody/tr')
        for tr in l_tr:
            obj_crwalipItem = items.CrwalipItem()
            # s_ip
            s_ip = tr.xpath(
                './td[@data-title="IP"]/text()').extract_first()
            s_port = tr.xpath(
                './td[@data-title="PORT"]/text()').extract_first()
            obj_crwalipItem['s_ip'] = s_ip + ':' + s_port
            # dt_crwalTime
            obj_crwalipItem['dt_crwalTime'] = time.strftime(
                "%Y-%m-%d %H:%M:%S")

            # 测试代理ip是否有用
            try:
                self.ipProxyTest(s_ip, s_port)
                print(
                    "time:【{}】,ip【{}】----OK".format(obj_crwalipItem['dt_crwalTime'], s_ip))
            except Exception as e:
                print("time:【{}】,ip【{}】,Error:【{}】".format(
                    obj_crwalipItem['dt_crwalTime'], s_ip, e))
                continue
            yield obj_crwalipItem
        if not self.i_endPageNum:
            # 获取末尾页码
            self.i_endPageNum = int(response.xpath(
                '//div[@id="listnav"]//li[last()-1]/a/text()').extract_first())
        # 下一页的获取
        # 获取本次的页码
        i_currentPageNum = int(os.path.basename(response.url))
        if i_currentPageNum <= 10:
            # 访问下一页
            s_nextUrl = os.path.dirname(
                response.url) + '/' + str(i_currentPageNum + 1)
            yield Request(url=s_nextUrl, callback=self.parse)

    def ipProxyTest(self, s_ip, s_port):
        """
        IP是否生效检测
        """
        telnetlib.Telnet(s_ip, port=s_port, timeout=2)
