# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrwalipItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    s_ip = scrapy.Field()
    dt_crwalTime = scrapy.Field()

    def get_insert_sql(self):
        # 书写insert语句
        s_insertSql = """
        insert into ipProxyPool(IP, crawl_time)
            VALUES (%s, %s)
        """
        params = (self['s_ip'], self['dt_crwalTime'])

        return s_insertSql, params

    def get_select_sql(self):
        # 书写查询语句
        s_selectSql = """
        select id from ipProxyPool
        where IP = %s
        """
        params = (self['s_ip'], )
        return s_selectSql, params
