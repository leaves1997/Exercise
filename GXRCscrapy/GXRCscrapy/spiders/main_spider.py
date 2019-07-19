import scrapy
from bs4 import BeautifulSoup
import csv
import os


class GCRCscrapy(scrapy.Spider):
    name = 'GXRC'

    def start_requests(self):
        url = 'http://s.gxrc.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('开始获取分类信息...')
        html = response.text
        industinfo = BeautifulSoup(html, 'lxml').find_all('div', class_='tit')
        for i in industinfo:
            industryUrl = 'http://s.gxrc.com' + i.find("a").get('href')

            yield scrapy.Request(url=industryUrl, callback=self.parse_list)

    def parse_list(self, response):
        html = response.text
        page = BeautifulSoup(html, 'lxml')
        Title = page.find(
            'div', id='changeIndustry').find('h3').get_text(strip=True)
        Title = Title.replace('/', '，')
        print('开始爬取 %s 分类下的招聘信息...' % Title)
        nextPage = page.find('a', rel='next')
        infolist = page.find_all('div', class_='rlOne')
        for i in infolist:
            info = {}
            info['position'] = i.find(
                "a", class_='posName').get_text(strip=True)
            info['info_url'] = i.find("a", class_='posName').get('href')
            info['company'] = i.find(
                "a", class_='entName').get_text(strip=True)
            info['salary'] = i.find('li', class_='w3').get_text(strip=True)
            info['site'] = i.find("li", class_='w4').get_text(strip=True)
            info['education'] = i.find(
                'ul', class_='qitaUL').find_all('li')[1].find('span').get_text(
                    strip=True)
            info['experience'] = i.find(
                'ul', class_='qitaUL').find_all('li')[2].find('span').get_text(
                    strip=True)
            info['date'] = i.find("li", class_='w5').get_text(strip=True)

            f = open(Title + '.csv', 'a+', newline='')
            writer = csv.writer(f, dialect='excel')
            if os.path.getsize(Title + '.csv') == 0:
                writer.writerow(
                    ['职位', '链接', '公司', '薪水', '地址', '学历', '经验', '更新日期'])
            writer.writerow(
                (info['position'], info['info_url'], info['company'],
                 info['salary'], info['site'], info['education'],
                 info['experience'], info['date']))

        print('保存信息完成...')

        if nextPage:
            next_url = 'http://s.gxrc.com' + nextPage.get('href')
            return scrapy.Request(url=next_url, callback=self.parse_list)
