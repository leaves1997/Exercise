# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GxrcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 分类名字
    Title = scrapy.Field()
    # 分类地址


#    Url = scrapy.Field()


class Infolist(scrapy.Item):

    # 职位名
    position = scrapy.Field()
    # 信息连接
    info_url = scrapy.Field()
    # 公司名
    company = scrapy.Field()
    # 薪水
    salary = scrapy.Field()
    # 工作地点
    site = scrapy.Field()
    # 学历
    education = scrapy.Field()
    # 经验
    experience = scrapy.Field()
