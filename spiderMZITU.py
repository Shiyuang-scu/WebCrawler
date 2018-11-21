import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os
def makeFile(title):
	path = str(title).strip()
	os.makedirs(os.path.join('/Users/seunoboru/Desktop/mzitu/', path))
	os.chdir('/Users/seunoboru/Desktop/mzitu/'+path)

count = 0
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'http://www.mzitu.com/all'  ##开始的URL地址
start_html = requests.get(all_url,  headers=headers)  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
Soup = BeautifulSoup(start_html.text, 'lxml') ##使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）
all_a = Soup.find('div', class_='all').find_all('a') ##意思是先查找 class为 all 的div标签，然后查找所有的<a>标签。
for a in all_a[1:]:
	if count<=1:
		title = a.get_text() #取出a标签的文本
		makeFile(title)
		href = a['href'] #取出a标签的href 属性
		html = requests.get(href, headers=headers) ##上面说过了
		html_Soup = BeautifulSoup(html.text, 'lxml') ##上面说过了
		max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text() ##查找所有的<span>标签获取第十个的<span>标签中的文本也就是最后一个页面了。
		for page in range(1, int(max_span)+1): ##不知道为什么这么用的小哥儿去看看基础教程吧
			page_url = href + '/' + str(page) ##同上
			page_html = requests.get(page_url, headers=headers)
			page_html_soup = BeautifulSoup(page_html.text, 'lxml')
			pic_url = page_html_soup.find('div', class_='main-image').find('img')['src']
			pic_name = pic_url[-9:-4]
			img = requests.get(pic_url, headers=headers)
			file = open(pic_name+'.jpg', 'wb')
			file.write(img.content)
			file.close()
	count = count + 1