# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GxrcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    position = scrapy.Field()
    info_url = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    site = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    date = scrapy.Field()
