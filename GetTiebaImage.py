# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os


def getHTMLText(url):
    try:
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
        }
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return "出现异常"


def getImgUrlList(Number):
    First_Page = getHTMLText('https://tieba.baidu.com/p/' + Number)
    Title = BeautifulSoup(First_Page, "html.parser").find('h3').string

    urlList = []
    p = 1

    while True:
        url = 'https://tieba.baidu.com/p/' + Number + '?pn=' + str(p)
        html = getHTMLText(url)
        soup = BeautifulSoup(html, "html.parser")

        Next = soup.find_all('a', text='下一页')

        if Next:
            i = soup.find_all(
                'img',
                class_="BDE_Image",
                src=re.compile(r'https://imgsa.baidu.com/forum/*'))
            urlList.extend(i)
            p += 1
        else:
            i = soup.find_all(
                'img',
                class_="BDE_Image",
                src=re.compile(r'https://imgsa.baidu.com/forum/*'))
            urlList.extend(i)
            break

    return Title, urlList


def DowlandImage(Title, urlList):
    os.mkdir(Title)
    os.chdir(os.path.join(os.getcwd(), Title))

    t = 1
    for i in urlList:
        try:
            ImgURLs = i.get('src')
            Img = requests.get(ImgURLs, timeout=50)
            ImgName = str(t) + '.jpg'
            with open(ImgName, 'wb') as f:
                f.write(Img.content)
            print('下载第 %s 张图片完成' % t)
            t += 1
        except:
            print('下载第 %s 张图片错误，跳过该图片' % t)
            continue
    print('全部图片已下载完成')


def Main():
    Number = input('帖子编号：')
    Tielist = getImgUrlList(Number)
    Title = Tielist[0]
    urlList = Tielist[1]
    DowlandImage(Title, urlList)


if __name__ == "__main__":
    Main()
