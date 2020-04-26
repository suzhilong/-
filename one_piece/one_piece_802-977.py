##################
#	python3
#	home page: https://one-piece.cn/comic/
#	802-977话
#	2020.4.25 12:33
##################
# -*- coding: utf-8 -*-	
import requests
from bs4 import BeautifulSoup
import os
import random
import time
import re

user_agent = [
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
	]

#代理
http_ip = [
		'',#不用代理
		#'112.95.20.27:8888',
		#'219.159.38.198:56210',
		]
https_ip = [
		'',
		]
'''
1、当你的Server内存充足时，KeepAlive =On还是Off对系统性能影响不大。
2、当你的Server上静态网页(Html、图片、Css、Js)居多时，建议打开KeepAlive 。
3、当你的Server多为动态请求(因为连接数据库，对文件系统访问较多)，KeepAlive 关掉，会节省一定的内存，节省的内存正好可以作为文件系统的Cache(vmstat命令中cache一列)，降低I/O压力。
PS：当KeepAlive =On时，KeepAliveTimeOut的设置其实也是一个问题，设置的过短，会导致Apache 频繁建立连接，给Cpu造成压力，设置的过长，系统中就会堆积无用的Http连接，消耗掉大量内存，具体设置多少，可以进行不断的调节，因你的网站浏览和服务器配置 而异。
'''
#请求头
headers = {
	# 'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
	# 'Accept - Encoding':'gzip, deflate',
	# 'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,ja;q=0.7',
	# 'Connection':'close',#'Keep-Alive'容易被ban IP
	# 'Host':'wx1.sinaimg.cn',
	# 'Referer':'',
	'User-Agent':random.choice(user_agent),
	}
proxies= {#该网站是https协议
	"http":random.choice(http_ip),
	"https":random.choice(https_ip)
		}


#创建页面url
def get_page_urls():
	root_url = 'https://one-piece.cn/post/10'
	page_urls = []
	for page in range(802,978):
		tmp_url = root_url+str(page)+'/'
		page_urls.append(tmp_url)
	return page_urls


#从html中提取图片url
def get_img_url(origi_url):
	req = requests.get(origi_url,headers=headers,proxies=proxies,timeout=60)
	soup = BeautifulSoup(req.text,'html.parser')
	# print(soup)
	img_urls = soup.select('p > img')
	# print(img_urls[0])
	urlStr = str(img_urls)
	pattern = re.compile(r'http://.*?jpg')
	src = pattern.findall(urlStr)
	# print(src)
	return src

#用图片url下载到对应的文件夹中
def img_downloader(img_urls,headers_page,vol):
	page = 1
	j = 0	#用来掌控请求速度
	for img_url in img_urls:
		###应该先判断文件是否存在，再请求，否则重复下载
		#req = requests.get(url,headers=headers,proxies=proxies,timeout=60)
		root = r"/Users/sousic/code/spider_one_piece/" #根目录
		#路径
		document = root + str(vol) + '/'
		path = document + str(page) + '.jpg'
		# print(path)

		if not os.path.exists(root):#判断当前根目录是否存在
			os.mkdir(root)          #创建根目录
		if not os.path.exists(document):
			os.mkdir(document)      #创建卷的文件夹
		if not os.path.exists(path):#判断文件是否存在
			#######应该放在判断文件不存在后请求
			#每请求一次页面i+1
			j += 1
			req = requests.get(img_url,headers=headers_page,proxies=proxies,timeout=60)
			############
			with open(path,'wb')as f:
				f.write(req.content)
				f.close()
				print("成功 " + " --第 %d 集" % vol + "第 %d 页" % page)# + "已完成 %.2f" % (pencent*100) + '%')
			#请求一次页面暂停一会儿
			# time.sleep(random.random() * 10)
		else:
			print("已存在 " + " --第 %d 集" % vol + "第 %d 页" % page)# + "已完成 %.2f" % (pencent*100) + '%')
		page += 1
		#每10此请求，多暂停一会儿
		# if j//10 != 0:
		# 	time.sleep(10 + random.random() * 50)

def main():
	page_urls = get_page_urls()
	# print(page_urls[0])
	img_urls =[]
	for page_url in page_urls:#先用一页测试
		print(page_url)
		img_url = get_img_url(page_url)
		img_urls.append(img_url)
	# for u in img_urls:
	# 	print(len(u))
	vol = 802
	for img_url in img_urls:
		headers_page = headers
		# headers_page['Referer'] = url
		# print(headers_page)
		img_downloader(img_url,headers_page,vol)
		vol += 1

if __name__ == '__main__':
	main()	
