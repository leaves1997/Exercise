import scrapy
from GXRCscrapy.items import GxrcItem
from GXRCscrapy.items import Infolist
from bs4 import BeautifulSoup


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
            industryTitle = i.find("a").get_text(strip=True)
            industryUrl = 'http://s.gxrc.com' + i.find("a").get('href')

            info = GxrcItem()
            info['Title'] = industryTitle

            yield scrapy.Request(url=industryUrl, callback=self.parse_list)

    def parse_list(self, response):
        print(response.url)
        print('开始爬取简历信息...')
        html = response.text
        page = BeautifulSoup(html, 'lxml')
        nextPage = page.find('a', rel='next')
        infolist = page.find_all('div', class_='rlOne')

        for i in infolist:
            info = Infolist()
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
            yield info

        if nextPage:
            next_url = 'http://s.gxrc.com' + nextPage.get('href')
            print(next_url)
            return scrapy.Request(url=next_url, callback=self.parse_list)


                
