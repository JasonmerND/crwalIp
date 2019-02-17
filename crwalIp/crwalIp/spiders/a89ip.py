# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from crwalIp import items
import time
import os
import requests
import telnetlib


class A89ipSpider(scrapy.Spider):
    name = '89ip'
    # allowed_domains = ['www.89ip.com']
    start_urls = [
        'http://www.89ip.cn/tqdl.html?num=9999&address=&kill_address=&port=&kill_port=&isp=']

    def parse(self, response):
        # 只有一页，直接写解析
        l_ipXpath = response.xpath("//div[@class='fly-panel']/div/text()")
        l_ip = l_ipXpath.extract()
        for ip in l_ip:
            obj_crwalipItem = items.CrwalipItem()
            obj_crwalipItem['s_ip'] = ip.strip()
            obj_crwalipItem['dt_crwalTime'] = time.strftime(
                "%Y-%m-%d %H:%M:%S")

            # 测试代理ip是否有用
            s_ip, s_port = ip.split(":")
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
