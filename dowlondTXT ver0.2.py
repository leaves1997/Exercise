# -*- coding: utf-8 -*-
# 自学爬虫的产物
# 成功学会怎样利用cookie模拟登陆
# 还重写了获取文章连接的部分方便顺利爬下VIP部分的文
# 只能爬已经购买的VIP的文

import requests
from bs4 import BeautifulSoup
import time
import re


# 网页获得和处理
def getHTMLText(url, params):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    }
    cookies = "timeOffset_o=585.5; UM_distinctid=16bb81d391d449-0c189ac9bf21568-14397440-100200-16bb81d39204c9; token=Mzc4Mjc4NzF8NThhZWExODQyNTMzODhiZGMyNzVjOTQ4NmIzY2NjN2N8fHx8MjU5MjAwMHwxfHx85qyi6L%2BO5oKo77yM5pmL5rGf55So5oi3fDB8bW9iaWxl; testcookie=yes; JJEVER=%7B%22ispayuser%22%3A%2237827871-1%22%2C%22foreverreader%22%3A%2237827871%22%2C%22sms_total%22%3A1%7D; JJSESS=%7B%22nicknameAndsign%22%3A%22undefined%7E%29%2524%22%2C%22clicktype%22%3A%22%22%7D; CNZZDATA30075907=cnzz_eid%3D1770875631-1561097691-http%253A%252F%252Fwww.jjwxc.net%252F%26ntime%3D1562496720; Hm_lvt_bc3b748c21fe5cf393d26c12b2c38d99=1562214146,1562215697,1562400517,1562501154; Hm_lpvt_bc3b748c21fe5cf393d26c12b2c38d99=1562501832"
    cookies1 = dict(map(lambda x: x.split('='), cookies.split(';')))
    try:
        r = requests.get(
            url, headers=headers, params=params, timeout=30, cookies=cookies1)
        r.raise_for_status()
        r.encoding = 'gbk'
        r = r.text
        r = BeautifulSoup(r, 'lxml', from_encoding='gbk')
        return r
    except Exception as e:
        print(e)
        print('页面获取错误')


def getText(novelpage):
    pagehtml = getHTMLText(novelpage, params).find(class_='noveltext')
    novelpage = pagehtml.find('h2').get_text(strip=True)
    novelpage = novelpage.strip()
    print('%s 开始下载。' % novelpage)
    [s.extract() for s in pagehtml('div')]
    [s.extract() for s in pagehtml('script')]
    novelTXT = pagehtml.get_text('\n', strip=True)
    novelTXT = novelTXT.strip()
    novelTXT = novelTXT.replace('@无限好文，尽在晋江文学城', '')
    if not novelTXT:
        print('该章节无法下载')
    try:
        with open(TXTName, 'a+', encoding='utf-8') as f:
            f.write('\n')
            f.write(novelpage)
            f.write('\n\n')
            f.write(novelTXT)
            f.write('\n')
            print('%s 已下载完成。' % novelpage)
    except Exception as e:
        print(e)
        print('下载出现错误，跳过此章节')
    time.sleep(0.5)


# 获得书籍信息
bookid = input('输入想要下载的书籍ID：')
bookurl = 'http://www.jjwxc.net/onebook.php'
payload = {'novelid': bookid}

bookhtml = getHTMLText(bookurl, payload)

info1 = bookhtml.find('title').get_text().split('_')[0]
info2 = bookhtml.find(id='novelintro').get_text('\n', strip=True)
info3 = bookhtml.find(class_='bluetext').get_text(strip=True)

# 创建文件
TXTName = info1 + '.txt'
with open(TXTName, 'a+', encoding='utf-8') as f:
    f.write(info2)
    f.write('\n')
    f.write(info3)
    f.write('\n')
print('文件 %s 已创建' % TXTName)

# 开始爬文
params = {}
bookpage = bookhtml.find_all(itemprop='url')
for i in bookpage:
    if i.get('rel') is None:
        novelpage = i.get('href')
        getText(novelpage)
    else:
        novelpage = i.get('rel')
        for s in novelpage:
            if re.match(r'http://my.jjwxc.net/onebook_vip.php*', s):
                getText(s)

print('%s 已下载完成' % info1)
