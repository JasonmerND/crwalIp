# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from crwalIp import items
import time
import os
import requests
from fake_useragent import UserAgent
import telnetlib


class JiangxianliSpider(scrapy.Spider):
    name = 'jiangxianli'
    # allowed_domains = ['ip.jiangxianli.com/?page=1']
    start_urls = ['http://ip.jiangxianli.com/?page=1/']
    ua = UserAgent()
    header = {
        "User-Agent": ua.random,
    }

    def parse(self, response):
        """直接解析"""
        l_tr = response.xpath(
            "//table[contains(@class,'table table-hover table-bordered table-striped')]/tbody//tr")
        for tr in l_tr:
            obj_crwalipItem = items.CrwalipItem()
            s_ip = tr.xpath('./td[2]/text()').extract_first()
            s_port = tr.xpath('./td[3]/text()').extract_first()
            obj_crwalipItem['s_ip'] = s_ip + ':' + s_port
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

        # 判断下一页
        nextNode_a = response.xpath('//ul[@class="pagination"]/li[last()]/a')
        if nextNode_a:
            # 说明还没到末页
            s_nextUrl = nextNode_a[0].xpath("./@href").extract_first()
            s_nextUrl = s_nextUrl.replace(".com", ".com/")
            yield Request(url=s_nextUrl, callback=self.parse, headers=self.header)

    def ipProxyTest(self, s_ip, s_port):
        """
        IP是否生效检测
        """
        telnetlib.Telnet(s_ip, port=s_port, timeout=2)
