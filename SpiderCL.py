
from bs4 import BeautifulSoup
import re
# headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
# all_url = 'https://www.t66y.com/thread0806.php?fid=16&search=&page=1' 

# # for i in range(1,50):
# page_html = requests.get(all_url, headers = headers)
# soup = BeautifulSoup(page_html.text, 'lxml')
# page_list = soup.find_all('h3')
# for list in page_list:
#     print(list.find_all('a').get_text())
from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
import urllib
import socket

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path='/Library/Frameworks/Python.framework/Versions/3.6/chromedriver')


def makeFile():
	os.makedirs('/Users/seunoboru/Desktop/pic/')
	os.chdir('/Users/seunoboru/Desktop/pic/')

#Get the url which contains the content that I select
def getConcretePage(start_url,title,href):
    for i in range(1,3):
        html = start_url+str(i)
        browser.get(html)
        ele = browser.find_elements_by_xpath("//a[contains(text(), '臀')]")
        for list in ele:
            tit = list.text
            hre = list.get_attribute('href')
            print(tit)
            title.append(tit)
            href.append(hre)


#Get the picture
def GetPic(img_url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=img_url, headers=headers)  
    data = urllib.request.urlopen(req).read() 
    return data


#Get the picture URL
def getPicURL(concrete_html, picURL):
    for page in concrete_html:
        browser.get(page)
        ele = browser.find_elements_by_tag_name("input")
        for list in ele:
            src = list.get_attribute('src')
            src = re.compile('^https:.*').match(src)
            if src:
                picURL.append(src.group(0))


if __name__ == '__main__':
    start_url = 'https://www.t66y.com/thread0806.php?fid=16&search=&page='
    title = []
    href = []
    picURL = []

    getConcretePage(start_url, title, href)
    getPicURL(href, picURL)
    makeFile()
    for i in range(len(picURL)):
        data = GetPic(picURL[i])
        print('正在获取图片'+str(i))
        file = open(str(i)+'.jpg', 'wb')
        file.write(data)
        file.close()







    # test = ['https://www.touimg.com/u/20181126/23154767.jpg','https://www.touimg.com/u/20181126/23154926.jpg','https://www.touimg.com/u/20181126/23155116.jpg','   ']
    # for src in test:
    #     src = re.compile('^https:.*').match(src)
    #     if src:
    #         print(src.group(0))