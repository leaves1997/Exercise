import scrapy
from bs4 import BeautifulSoup
from GXRCscrapy.items import GxrcItem


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
            Title = i.find("a").get_text(strip=True)
            info = GxrcItem()
            info['Title'] = Title

            yield scrapy.Request(
                url=industryUrl, callback=self.parse_list, meta={'info': info})

    def parse_list(self, response):
        info = response.meta['info']

        html = response.text
        page = BeautifulSoup(html, 'lxml')
        Title = info['Title']
        Title = Title.replace('/', '，')
        print('开始爬取 %s 分类下的招聘信息...' % Title)
        nextPage = page.find('a', rel='next')
        infolist = page.find_all('div', class_='rlOne')

        if nextPage:
            next_url = 'http://s.gxrc.com' + nextPage.get('href')
            yield scrapy.Request(url=next_url, callback=self.parse_list, meta={'info': info})
        
        for i in infolist:
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

            yield info

        print('信息爬取成功...')