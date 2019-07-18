# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class GxrcscrapyPipeline(object):
    def process_item(self, item, spider):
        f = open('info.csv', 'a+', newline='')
        if item['position']:
            writer = csv.writer(f, dialect='excel')
            writer.writerow((item['position'], item['info_url'],
                             item['company'], item['salary'], item['site'],
                             item['education'], item['experience']))

        return item
