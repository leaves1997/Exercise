# -*- coding: utf-8 -*-
# 最近沉迷在晋江看小说所以写了用来爬晋江的文放手机里看的
# 目前只能爬免费的文
# 因为我还不会怎么弄模拟登陆
# 第二个自己搞定的爬虫 来自一个刚会写爬虫的小菜鸟

import requests
from bs4 import BeautifulSoup
import time


def getHTMLText(url, params):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/67.0',
    }

    r = requests.get(url, timeout=30, headers=headers, params=params)
    r.raise_for_status()
    r.encoding = 'gb2312'
    r = r.text
    r = BeautifulSoup(r, 'lxml', from_encoding='gbk')
    return r


# 获得书籍信息
bookid = input('输入想要下载的书籍ID：')
bookurl = 'http://www.jjwxc.net/onebook.php'
payload = {'novelid': bookid, 'chapterid': ''}

bookhtml = getHTMLText(bookurl, payload)

i = 1
a = int(input('输出下载的章节数：'))

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

while i <= a:
    page = {'novelid': bookid, 'chapterid': i}
    pagehtml = getHTMLText(bookurl, page).find(class_='noveltext')
    novelpage = pagehtml.contents[3].get_text()
    novelpage = novelpage.strip()
    print('%s 开始下载。' % novelpage)
    [s.extract() for s in pagehtml('div')]
    novelTXT = pagehtml.get_text('\n', strip=True)
    novelTXT = novelTXT.strip()
    if not novelTXT:
        print('该章节无法下载')
        i += 1
        continue
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
    i += 1

print('%s 已下载完成' % info1)