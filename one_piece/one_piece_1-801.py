##################
#	python3
#	home page: https://manhua.fzdm.com/2/
#	1-801话
#	2020.4.25 
##################
# -*- coding: utf-8 -*-	
import requests
from bs4 import BeautifulSoup
import os
import random
import time
import re

user_agent = [
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",#1
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",#1
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",#1
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",#1
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",#1
	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",#1
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",#1
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
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
	'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
	'Accept - Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,ja;q=0.7',
	'Connection':'close',#'Keep-Alive'容易被ban IP
	# 'Host':'p2.manhuapan.com',
	'Referer':'',
	#'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
	'User-Agent':random.choice(user_agent),
	}
proxies= {#该网站是https协议
	"http":random.choice(http_ip),
	"https":random.choice(https_ip)
		}


#创建 每集 页面url
def get_page_urls():
	root_url = 'https://manhua.fzdm.com/2/'
	page_urls = []
	for page in range(1,36):#前面是按卷
		if page<10:
			tmp = '0' + str(page)
		else:
			tmp = str(page)
		tmp_url = root_url + 'Vol_0' + tmp +'/'
		page_urls.append(tmp_url)
	for page in range(337,802):#之后是集不是卷
		tmp_url = root_url + str(page) + '/'
		page_urls.append(tmp_url)
	return page_urls

#从html中提取每页url
def get_idx_url(origi_url):
	# print(origi_url)
	
	idxUrl = origi_url + 'index_0.html'
	
	idx_url_list = []
	idx_url_list.append(idxUrl)

	img_url_list = []

	hasNextPage = 1
	while hasNextPage==1:
		print('\ncurrent url: ',idxUrl)
		req = requests.get(idxUrl,headers=headers,proxies=proxies,timeout=120)
		soup = BeautifulSoup(req.text,'html.parser')
		# print(soup)
		
	# get img url
		imgFilter = soup.select('script')
		# print('script: ',imgFilter)
		imgStr = str(imgFilter)
		patternImgUrl = re.compile(r'var mhurl1="(.*?)"')
		imgurlRear = patternImgUrl.findall(imgStr)
		# print("length of rearlist: ",len(imgurlRear))
		rootUrl = 'http://p2.manhuapan.com/'
		if len(imgurlRear)!=0:			
			imgUrl = rootUrl + imgurlRear[0]
			img_url_list.append(imgUrl)
			print("img url: ",imgUrl)

	# find next page url
		idxFilter = soup.select('.navigation')
		idxStr = str(idxFilter)
		# print("\nidxStr: ",idxStr)
		patternNextP = re.compile(r'下一页')
		nextPage = patternNextP.findall(idxStr)
		# print('\nnextPage: ',nextPage)
		hasNextPage = len(nextPage)
		# print(hasNextPage)

		if hasNextPage!=0:
			idxPattren = re.compile(r'"pure-button pure-button-primary" href="(.*?)">')
			href = idxPattren.findall(idxStr)
			if(len(href)==1):
				idx = str(href[0])
			else:
				idx = str(href[1])
			# print("\nidx: ",idx)
			# print("\nidx: ",idx)
			idxUrl = origi_url + idx
			print("next url: ",idxUrl)
			idx_url_list.append(idxUrl)

	return  img_url_list#, idx_url_list

#用图片url下载到对应的文件夹中
def img_downloader(img_urls,headers_page,vol):
	page = 1
	j = 0	#用来掌控请求速度
	for img_url in img_urls:
		###应该先判断文件是否存在，再请求，否则重复下载
		#req = requests.get(url,headers=headers,proxies=proxies,timeout=60)
		root = r"/Users/sousic/code/spider_one_piece/onepiece/" #根目录
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
			req = requests.get(img_url,headers=headers_page,proxies=proxies,timeout=120)
			############
			with open(path,'wb')as f:
				f.write(req.content)
				f.close()
				print("成功 " + " --第 %d 集" % vol + "第 %d 页" % page)# + "已完成 %.2f" % (pencent*100) + '%')
			#请求一次页面暂停一会儿
			time.sleep(random.random() * 20)
		else:
			print("已存在 " + " --第 %d 集" % vol + "第 %d 页" % page)# + "已完成 %.2f" % (pencent*100) + '%')
		page += 1
		#每10此请求，多暂停一会儿
		if j//10 != 0:
			time.sleep(10 + random.random() * 50)

#按规律生成url  更快
def getLastPageNum(page_url,vol):
	print('find max page...')

	if vol<36:
		idxNot404 = 20
		idx404 = 200
	else:
		idxNot404 = 10
		idx404 = 50
	while idx404!=idxNot404+1:
		idx = (idxNot404+idx404)//2
		idxUrl = page_url + 'index_' + str(idx) + '.html'
		curHeader = {'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
					'Accept - Encoding':'gzip, deflate',
					'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,ja;q=0.7',
					'Connection':'close',#'Keep-Alive'容易被ban IP
					'Referer':'',
					'User-Agent':random.choice(user_agent),}
		print(str(curHeader)[203:-2])
		req = requests.get(idxUrl,headers=curHeader,proxies=proxies,timeout=120)
		soup = BeautifulSoup(req.text,'html.parser')
		if str(soup)=='404!':
			idx404 = idx
		else:
			idxNot404 = idx
		print('idx404:',idx404,'idxNot404:',idxNot404)
		#请求一次页面暂停一会儿
		time.sleep(random.random() * 10)
	print('max page is: ',idxNot404)

	#保存每一集的lastPage
	path = r"/Users/sousic/code/spider_one_piece/lastPage.txt"
	with open(path,'a')as f:
			f.write('vol'+str(vol)+':'+str(idxNot404)+',')
			f.close()
			print("last page保存成功")

	return idxNot404

def generateImgUrl(maxPage,rootUrl,vol):
	print('generate img url...')
	startNum = 1
	alpTab1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
	alpTab2 = ['a','c','e','g','i','k','m','o','q','s','u','w','y']
	img_urls = []
	for i in range(0,maxPage+1):
		curNum = startNum + i
		alp1 = alpTab1[i // 13]
		alp2 = alpTab2[i % 13]
		if curNum<10:
			numStr = '00'+str(curNum)
		elif curNum>=10 and curNum<100:
			numStr = '0'+str(curNum)
		else:
			numStr = str(curNum)
		tmp_url = rootUrl + numStr + alp1 + alp2 + '.jpg'
		# print(tmp_url)
		img_urls.append(tmp_url)

	# print(str(img_urls))
	#保存urls
	root = r"/Users/sousic/code/spider_one_piece/img_url/"
	path = root + str(vol) + '.txt'
	if not os.path.exists(path):#判断文件是否存在
		with open(path,'w')as f:
			f.write(str(img_urls))
			f.close()
			print("url保存成功 " + " --第 %d 集" % vol)

	return img_urls

def getUrlAndDownload():
	page_urls = get_page_urls()
	# print(page_urls[0], page_urls[35])
	img_urls = []
	
	# 总结规律生产url链接
	vol = 1
	for page_url in page_urls:#注意改vol
		print('\n----page url: ',page_url,'------------------------------------')
		maxPage = getLastPageNum(page_url,vol)
		urlRear = page_url.split('/')[-2]
		rootUrl = 'http://p2.manhuapan.com/2/'+urlRear+'/'
		
		if vol ==36:
			vol = 337
		img_url = generateImgUrl(maxPage,rootUrl,vol)
		vol += 1

		img_urls.append(img_url)

	# 从html里找url链接
	# for page_url in page_urls[0:1]:#先用一页测试
	# 	print('\n----page url: ',page_url,'------------------------------------')
	# 	img_url = get_idx_url(page_url)
	# 	img_urls.append(img_url)

	vol = 1
	for img_url in img_urls:
		headers_page = headers
		# headers_page['Referer'] = url
		# print(headers_page)
		if vol ==36:
			vol = 337
		img_downloader(img_url,headers_page,vol)
		vol += 1

def downloadUseImgUrl(urlList,vol,root):
	print('\n---- download %d vol ----------' % vol)
	path = root + 'onepiece/'
	document = path + str(vol) + '/'
	totalUrl = len(urlList)
	for n in range(0,totalUrl):
		page = n+1
		pic = document + str(page) + '.jpg'
		if not os.path.exists(document):
			os.mkdir(document)      #创建卷的文件夹
		if not os.path.exists(pic):#判断文件是否存在
			try:
				curHeader = {'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
						'Accept - Encoding':'gzip, deflate',
						'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,ja;q=0.7',
						'Connection':'close',#'Keep-Alive'容易被ban IP
						'Referer':'',
						'User-Agent':random.choice(user_agent),}
				print(str(curHeader)[203:-2])
				print('get url: ',urlList[n])
				req = requests.get(urlList[n],headers=curHeader,proxies=proxies,timeout=60)
			except:
				print('!!!!!!!!!! 第 %d 集  第 %d 页 下载失败 !!!!!!!!!!!!!!!!!!!!!' %(vol,page))
				continue

			with open(pic,'wb')as f:
				f.write(req.content)
				f.close()
				print("成功 " + " --第 %d 集" % vol + " --第 %d 页" % page)# + "已完成 %.2f" % (pencent*100) + '%')
			#请求一次页面暂停一会儿
			# time.sleep(random.random() * 10)
		
		else:
			print("已存在 " + " --第 %d 集" % vol + " --第 %d 页" % page)

def getUrlFromTxt(document):
	with open(document,'r')as f:
		urlStr = f.read()
		f.close()
	urlList = urlStr[1:-1].split(',') #去括号 分割开
	url_list = []
	for url in urlList:
		tmpUrl = url.lstrip().rstrip()[1:-1]#去引号
		url_list.append(tmpUrl)
	# print(len(url_list))
	return url_list

def main():
	# getUrlAndDownload()
	root = r"/Users/sousic/code/spider_one_piece/"
	for vol in range(1,36):
		document = root + 'img_url/' + str(vol) + '.txt'
		urlList = getUrlFromTxt(document)
		downloadUseImgUrl(urlList,vol,root)
	for vol in range(337,802):
		document = root + 'img_url/' + str(vol) + '.txt'
		urlList = getUrlFromTxt(document)
		downloadUseImgUrl(urlList,vol,root)

if __name__ == '__main__':
	main()

