# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import random
import time

###########输出日志###################################################
LOG_DIRECTORY = r"I:\dgball"
class Print(object):
    @staticmethod
    def info(message):
        out_message =  Print.timeStamp() + '  ' + 'INFO: ' +str(message)
        Print.write(out_message)
        print(out_message)

    @staticmethod
    def write(message):
        log_path = os.path.join(LOG_DIRECTORY,'log.txt')
        #注意写入的编码，不然容易出错
        with open(log_path,'a+', encoding='utf-8') as f:
            f.write(message)
            f.write('\n')

    @staticmethod
    def timeStamp():
        local_time = time.localtime(time.time())
        return time.strftime("%Y_%m_%d-%H_%M_%S", local_time)

#####################################################################




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
		'203.130.46.108:9090',
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
headers_imgdownload = {#爬不同网页需要修改相应的请求头，通过浏览器查看
	'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
	'Accept - Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,ja;q=0.7',
	'Connection':'close',#'Keep-Alive'容易被ban IP
	'Host':'comic.dragonballcn.com',
	'Referer':'',
	'User-Agent':random.choice(user_agent),
	}
proxies= {#该网站是http协议
	"http":random.choice(http_ip),
	"https":random.choice(https_ip)
		}

################得到ip池############################################
import re

headers_others = {#爬不同网页需要修改相应的请求头，通过浏览器查看
		'User-Agent':random.choice(user_agent),
		}
def scraw_proxies(page_num,scraw_url="http://www.xicidaili.com/nt/"):
	#从西刺代理网站提取ip数据
	scraw_ip=list()
	available_ip=list()
	page_num = page_num + 1
	for page in range(1,page_num):
		#print("抓取第%d页代理IP" %page)
		Print.info("抓取第%d页代理IP" %page)
		url=scraw_url+str(page)
		#print(url)
		r=requests.get(url,headers=headers_others)
		r.encoding='utf-8'
		pattern = re.compile(u'<tr class=".*?">.*?'
							+u'<td class="country"><img.*?/></td>.*?'
							+u'<td>(\d+\.\d+\.\d+\.\d+)</td>.*?'
							+u'<td>(\d+)</td>.*?'
							+u'<td>.*?'
							+u'<a href=".*?">(.*?)</a>.*?'
							+u'</td>.*?'
							+u'<td class="country">(.*?)</td>.*?'
							+u'<td>([A-Z]+)</td>.*?'
							+'</tr>', re.S)
		#print(r.text)
		scraw_ip= re.findall(pattern, r.text)
		#print(scraw_ip)
		#############清洗ip#############
		scraw_ip_htt = []
		for ip in scraw_ip:
			wash_ip = ip[0] + ":" + ip[1]
			scraw_ip_htt.append(wash_ip)
		#################################
		#print(scraw_ip_htt)
		# 测试ip
		for ip in scraw_ip_htt:
			if(test_ip(ip,10)==True):
				#print('%s 通过测试，添加进可用代理列表' % ip)
				Print.info('%s 通过测试，添加进可用代理列表' % ip)
				#print('--------------此IP测试通过-------------')
				available_ip.append(ip)
			else:
				pass    
		# print("代理爬虫暂停10s")
		Print.info("代理爬虫暂停10s")
		time.sleep(10)
		# print("爬虫重启")
		Print.info("爬虫重启")
	# print('抓取结束')
	Print.info('抓取结束')
	#返回测试通过的ip
	return available_ip

#测试ip网站，前面年需要更新，改为当前年
def test_ip(ip,time_out,test_url='http://2018.ip138.com/ic.asp'):
	proxies_ip_test = {'http': ip}
	#print(proxies_ip_test)
	try_ip = ip
	try:
		Print.info("测试ip：" + try_ip)
		r=requests.get(test_url,headers=headers_others,proxies=proxies_ip_test,timeout=time_out)
		#print(r.status_code)
		if r.status_code==200:
			#提取出当前ip
			r.encoding='gbk'
			result=re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',r.text)
			result=result.group()
			#比较两个测试ip和请求得到ip
			if result[:9]==try_ip[:9]:
				#print(r.text)
				#print('--------------此IP测试通过-------------')
				return True
			else:
				#print('%s 携带代理失败,使用了本地IP' % ip)
				Print.info('%s 携带代理失败,使用了本地IP' % ip)
				return False    
		else:
			#print('%s 请求码不是200,是%s' %(ip,str(r.status_code)))
			Print.info('%s 请求码不是200,是%s' %(ip,str(r.status_code)))
			return False
	except:
		#print('%s 请求过程错误' % ip )
		Print.info('%s 请求过程错误' % ip)
		return False

###################################################################



#从html中提取小图url
def get_thumb_url(origi_url,ip_pool):
	proxies_thumb_download= {#该网站是http协议
						"http":random.choice(ip_pool),
						#"https":random.choice(https_ip)
							}
	try:
		Print.info('代理：' + proxies_thumb_download['http'])
		req = requests.get(origi_url,headers=headers_others,proxies=proxies_thumb_download,timeout=30)
	except:
		Print.info(origi_url + '！！！！！整体网页请求失败，暂停一下！！！！！')
		time.sleep(10 + random.random() * 60)
		thumb_urls = get_thumb_url(origi_url,ip_pool)
	else:
		Print.info("整体网页请求码：" + str(req.status_code))
		req.encoding='utf-8'
		soup = BeautifulSoup(req.text,'html.parser')
		Print.info(soup.prettify())
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
def img_downloader(urls,headers_page,ip_pool,vol):
	totalurl = len(urls)
	i = 0	#用来算完成度
	j = 0	#用来掌控请求速度
	flag = 0 #判断是否已经全部下载完毕
	for url in urls:
		i += 1
		pencent = i/totalurl
		###应该先判断文件是否存在，再请求，否则重复下载
		#req = requests.get(url,headers=headers,proxies=proxies,timeout=60)
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
			#只要有一次请求，flag就不等于0
			flag += 1
			#######应该放在判断文件不存在后请求
			#每请求一次页面i+1
			j += 1
			try:
				# 每次都重新选择代理
				proxies_download= {#该网站是http协议
						"http":random.choice(ip_pool),
						#"https":random.choice(https_ip)
							}
				#print('------------------\n代理：' + proxies_download['http'])
				Print.info('请求图片------------------\n代理：' + proxies_download['http'])
				req = requests.get(url,headers=headers_page,proxies=proxies_download,timeout=60)
				Print.info('请求码：' + req.status_code)
			except:
				#failure = url.split('/')[-1]
				#print("%s 请求失败" % url)
				Print.info("%s 请求失败" % url)
				continue

			with open(path,'wb')as f:
				f.write(req.content)
				f.close()
				#print("成功 " + " --第 %d 卷" % vol + "已完成 %.2f" % (pencent*100) + '%')
				Print.info("成功 " + " --第 %d 卷" % vol + "已完成 %.2f" % (pencent*100) + '%')
			#请求一次页面暂停一会儿
			time.sleep(random.random() * 10)
		else:
			#print("已存在 " + " --第 %d 卷" % vol + "已完成 %.2f" % (pencent*100) + '%')
			Print.info("已存在 " + " --第 %d 卷" % vol + "已完成 %.2f" % (pencent*100) + '%')
		#每10此请求，多暂停一会儿
		if j//10 != 0:
			time.sleep(10 + random.random() * 50)
	return flag

def main(ip_pool):
	urls = []
	flag = 0
	start_urls = [
		"http://comic.dragonballcn.com/list/gain_1.php?did=0-9-0",
		"http://comic.dragonballcn.com/list/gain_1.php?did=0-9-1",
		"http://comic.dragonballcn.com/list/gain_1.php?did=0-9-2",
		]
	for url in start_urls:
		fragment = url.split('-')
		page = int(fragment[-1]) + 1
		thumb_urls = get_thumb_url(url,ip_pool)
		big_urls = get_big_url(thumb_urls)
		#print('第 %d 卷链接获取完毕，开始下载图片：' % page)
		Print.info('第 %d 卷链接获取完毕，开始下载图片：' % page)
		headers_page = headers_imgdownload
		headers_page['Referer'] = url
		#print(headers_page)
		flag += img_downloader(big_urls,headers_page,ip_pool,page)
	return flag

if __name__ == '__main__':
	flag = 1
	while flag != 0:
		#修改需要爬取的页数
		available_ip=scraw_proxies(10)
		#print(available_ip)
		#print('=================================')
		#加入代理池
		ip_pool = http_ip
		ip_pool.extend(available_ip)
		#print(ip_pool)
		Print.info(ip_pool)
		#print('代理爬取完毕\n==================================\n开始爬取漫画：')
		Print.info('代理爬取完毕\n==================================\n开始爬取漫画：')
		flag = main(ip_pool)
		Print.info('\n*************完成一轮：共下载 %d 张图片 暂停10分钟左右******************\n')
		time.sleep(300 + random.random() * 300)
	#分割不同次运行的日志
	Print.info('**********************\n*\n*********   爬取结束  \n*\n*\n********************')