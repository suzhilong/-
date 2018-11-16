# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import random
import time


#从html中提取小图url
def get_thumb_url(origi_url):
	req = requests.get(origi_url)
	soup = BeautifulSoup(req.text,'html.parser')
	img_urls = soup.select('.ItemThumb img')
	urls = []
	for img_url in img_urls:
		img_url = img_url.get('src')
		urls.append(img_url)
	return urls


# 处理url，得到大图url
def get_big_url(thumb_urls):
    urls = []
    for thumb_url in thumb_urls:
        split_url = thumb_url.split('/')
        # 去掉列表中的空元素
        while '' in split_url:
            split_url.remove('')
        # 观察大图的url和小图的url的区别，把列表最后一个元素改一下
        # 以'.'分离之后把第一个.thumb去掉再用'.'连接起来
        big_url = '.'.join(split_url[-1].split('.')[1:])
        split_url = split_url[1:-1]
        split_url.append(big_url)
        url = '/'.join(split_url)
        big_url = 'http://' + url
        urls.append(big_url)
    return urls

#用大图url下载到对应的文件夹中
def img_downloader(urls):
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
	http_ip = [
			'',#不用代理
			'112.95.20.27:8888',
			'219.159.38.198:56210',
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
	headers = {
		#'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
		#'Accept - Encoding':'gzip, deflate',
		#'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
		'Connection':'Keep-Alive',#'close'
		#'Host':'',
		'User-Agent':random.choice(user_agent)
		}
	proxies= {#该网站是http协议
		"http":random.choice(http_ip),
		#"https":random.choice(https_ip)
			}

	totalurl = len(urls)
	i = 0
	for url in urls:
		i += 1
		pencent = i/totalurl
		req = requests.get(url,headers=headers,proxies=proxies,timeout=60)
		root = r"I:\dgball" #根目录
		#路径
		document = root + '\\' + url.split('/')[-2]
		path = document + '\\' + url.split('/')[-1]
		#print(path)

		if not os.path.exists(root):#判断当前根目录是否存在
			os.mkdir(root)          #创建根目录
		if not os.path.exists(document):
			os.mkdir(document)      #创建卷的文件夹
		if not os.path.exists(path):#判断文件是否存在		
			with open(path,'wb')as f:
				f.write(req.content)
				f.close()
				print("成功,已完成%.2f" % (pencent*100) + '%')
		else:
			print("已存在,已完成%.2f" % (pencent*100) + '%')
		time.sleep(random.random() * 2)
		#pause per 10 scrawl
		if i//10 != 0:
			time.sleep(5 + random.random() * 5)


def main():
	urls = []
	start_urls = [
		"http://comic.dragonballcn.com/list/gain_1.php?did=0-9-0",
		"http://comic.dragonballcn.com/list/gain_1.php?did=0-9-1",
		"http://comic.dragonballcn.com/list/gain_1.php?did=0-9-2",
		]
	for url in start_urls:
		thumb_urls = get_thumb_url(url)
		big_urls = get_big_url(thumb_urls)
		urls.extend(big_urls)
	#print(urls)
	img_downloader(urls)
		

if __name__ == '__main__':
	main()	
