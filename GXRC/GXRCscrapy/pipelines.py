# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class GxrcscrapyPipeline(object):
    def __init__(self):
        self.f = open('info.csv', 'a+', newline='')
        self.write = csv.writer(self.f)
        self.write.writerow(
            ['分类', '职位', '链接', '公司', '薪水', '地址', '学历', '经验', '更新时间'])

    def process_item(self, item, spider):
        info = [
            item['Title'], item['position'], item['info_url'], item['company'],
            item['salary'], item['site'], item['education'],
            item['experience'], item['date']
        ]
        self.write.writerow(info)
        print('信息保存成功...')
        return item
