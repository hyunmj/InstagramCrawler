#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import  FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import  DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time
from selenium.webdriver.common.keys import Keys
import datetime as dt
import win_unicode_console
import pymongo
from pymongo import MongoClient
import csv

win_unicode_console.enable()
'''
PROXY='socks5://127.0.0.1:9151'
chrome_options=webdriver.ChromeOptions()

chrome_options.add_argument('--proxy-server=%s' % PROXY)
'''

#binary=FirefoxBinary('C:/Users/a/Desktop/Tor Browser/Browser/firefox.exe')
binary=FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')

#profile=FirefoxProfile('C:/Users/a/Desktop/Tor Browser/Browser/TorBrowser/Data/Browser/profile.default')
profile=FirefoxProfile()
#browser=webdriver.Firefox(firefox_profile=profile)
'''
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)
'''

profile.set_preference('accessibility.blockautorefresh', True)
profile.update_preferences()
browser=webdriver.Firefox(firefox_profile=profile)
list=[]
i=0

browser.get('https://instagram.com')

WebDriverWait(browser, 10).until(
EC.presence_of_element_located((By.XPATH, '/html/body/span/section/main/article/div[2]/div[2]/p/a'))
)



login_btn=browser.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[2]/p/a')
login_btn.click()

WebDriverWait(browser, 10).until(
EC.presence_of_element_located((By.XPATH, '/html/body/span/section/main/div/article/div/div[1]/div/form/span/button'))
)

## 로그인하기
email = browser.find_element_by_xpath('//*[@name="username"]')
password = browser.find_element_by_xpath('//*[@name="password"]')
btn = browser.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/span/button')

email.send_keys("hyunmj1")
password.send_keys("alswl123")
btn.click()
time.sleep(5)


f=open('2018.txt', 'r')

global html
global soup
global cur_url

while True:
	line=f.readline()


	#line=f.readline()
	if not line:
	  break

	pair = line.split('\t')

	moviename = pair[0]
	print(pair[0])
	keywordList=[]

	# :과 -는 OR로 바꿈
	tmp=pair[0].replace(',', '')
	tmp=tmp.replace(' ', '')

	t=tmp.split(':')[0]


	t=t.split('-')[0]

	# 검색어
	keyword=t

	filename=keyword+'insta.csv'
	resf=open(filename, 'a', encoding='utf-8')
	resfWriter=csv.writer(resf)



	released_date=pair[1].replace('\n','').split('-')

	# 검색할 기간 설정, untildate는 커서 역할
	dd=dt.date(year=int(released_date[0]),month=int(released_date[1]),day=int(released_date[2]))
	startdate=dd+dt.timedelta(days=-7)
	enddate=dd+dt.timedelta(days=7)
	print(dd)


	url='https://www.instagram.com/explore/tags/'+keyword

	browser.get(url)
	browser.implicitly_wait(10)
	html = browser.page_source
	soup=BeautifulSoup(html, 'html.parser')

	#button = browser.find_element_by_xpath("/html/body/span/section/main/article/div[1]/div/div/div[1]/div[2]/a/div") #--test용 인기게시글
	button = browser.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/article/div[2]/div/div[1]/div[1]/a/div")
	browser.execute_script("arguments[0].click();", button)

	articleNumber=1
	item=0

	preDate = ""
	time.sleep(3)
	cnt = 0
	while True:
		print(i)
		i=i+1
		#if i>100000:
		#   break
		WebDriverWait(browser, 3600).until(
		EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/button'))
		)
		time.sleep(0.5)

		while True:
			try:
				html = browser.page_source
				soup = BeautifulSoup(html,'html.parser')
			except Exception as e:
				print(e)
				time.sleep(0.1)
				continue
			break

		next_href=soup.find('a', {'class':'HBoOv'}).get('href')
		cur_url=browser.current_url
		cur_href=cur_url.replace('https://www.instagram.com', '')

		tmp=cur_href.split('/?')
		cur_href=tmp[0]+'/?tagged='+keyword

		"""
		# 성공적으로 로딩될 때까지 기다림
		while len(soup.find_all("li", {"class":"gElp9"})) == 0 :
		html = browser.page_source
		soup = BeautifulSoup(html, 'html.parser')
		time.sleep(0.1)
		"""

		datetime=''
		# 중복 게시글 방지 -- datetime이 같은 경우 넘어 감
		while True:
			try:
				datetime=soup.find("time", {"class":"_1o9PC"}).get("datetime")
			except:
				print(e)
				time.sleep(0.1)
				html = browser.page_source
				soup = BeautifulSoup(html,'html.parser')
				continue
			break

		datestring=datetime.split('T')
		datelist=datestring[0].split('-')
		d=dt.date(year=int(datelist[0]), month=int(datelist[1]), day=int(datelist[2]))

		next_button=''
		if enddate<d:
			while True:

				try:
					print('sleep')
					WebDriverWait(browser, 3600).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/div/div/a[2]'))
					)
					next_button=browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div/a[2]")



					print(next_href)
					print(cur_href)


					while next_href==cur_href:
						time.sleep(0.1)
						html = browser.page_source
						soup = BeautifulSoup(html,'html.parser')
						next_href=soup.find('a', {'class':'HBoOv'}).get('href')
						cur_url=browser.current_url
						cur_href=cur_url.replace('https://www.instagram.com', '')

						tmp=cur_href.split('/?')
						cur_href=tmp[0]+'/?tagged='+keyword

						print(next_href)
						print(cur_href)





					browser.execute_script("arguments[0].click();", next_button)
					print('click next')
				except Exception as e:
				   time.sleep(0.1)
				   print(e)
				   continue
				break

			print('enddate<d', d)
			continue


		elif d<startdate:

			cnt=cnt+1
			if cnt>2000:
				browser.quit()
				break

			while True:
				try:
					WebDriverWait(browser, 3600).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/div/div/a[2]'))
					)
					next_button=browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div/a[2]")


					while next_href==cur_href:
						time.sleep(0.1)
						html = browser.page_source
						soup = BeautifulSoup(html,'html.parser')
						next_href=soup.find('a', {'class':'HBoOv'}).get('href')
						cur_url=browser.current_url
						cur_href=cur_url.replace('https://www.instagram.com', '')

						tmp=cur_href.split('/?')
						cur_href=tmp[0]+'/?tagged='+keyword

						print(next_href)
						print(cur_href)


					browser.execute_script("arguments[0].click();", next_button)
					print('click next')
				except Exception as e:
					time.sleep(0.1)
					print(e)
					continue
				break

				print('enddate<d', d)
				continue

			"""
			if preDate == datetime:
			continue
			else:
			preDate = datetime
			"""

		print('startddate<d<enddate',d)
		#time.sleep(0.5)

		try :
			author = soup.find("a", {"class":"FPmhX"}).get("title")
		except :
			author = None

		fname = keyword+'_comments.csv'
		commentf=open(fname, 'a', encoding='utf-8')
		commentfWriter=csv.writer(commentf)

		#댓글 더보기 버튼

		more = soup.find("li",{"class":"LGYDV"})
		while more is not None :
			more_button = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a")
			browser.execute_script("arguments[0].click();", more_button)
			time.sleep(0.5)
			html=browser.page_source
			soup=BeautifulSoup(html,'html.parser')
			more = soup.find("li",{"class":"LGYDV"})

		text=[]
		article=''
		hash_tag_list=[]
		fav=''
		while True:
			try:
				text=soup.find_all("li", {"class":"gElp9"})
				try:
					article=text[0].find("span").getText()
					hash_tag_list=text[0].find("span").find_all("a")
				except:
				   article=''
				   hasg_tag_list=[]

				fav=soup.find("div", {"class":"HbPOm"})
			except:
				time.sleep(0.1)
				continue
			break
		dic={}
		favorites=0
		hashtag=''
		print(article)


		try:
			fav_list=fav.find_all("a")
			if len(fav_list)!=0:
				#dic['favorites']=len(fav_list)
				favorites=len(fav_list)
			else:
				#dic['favorites']=int(fav.find("span", {"class":"zV_Nj"}).find("span").getText().replace(',',''))
				favorites=int(fav.find("span", {"class":"zV_Nj"}).find("span").getText().replace(',',''))
		except:
	 		dic['favorites']=0
	 		favorites=0


		hash_tags=[]
		for h in hash_tag_list:
	 		hashtag = hashtag + " " + h.getText().replace("#", '')

		"""
		dic['author']=author
		dic['hash_tags']=hash_tags
		dic['article']=article
		dic['datetime']=datetime
		dic['moviename']=keyword
		"""

		comms=[]
		for a in range(0,len(text)):
			if a==0:
				continue
			else:
				comm={}
				comment_author=text[a].find("a", {"class":"FPmhX"}).get("title")
				comment=text[a].find("span").getText()

				comm['comment_author']=comment_author
				comm['comment']=comment
				comms.append(comm)
				commentfWriter.writerow([articleNumber, comment_author, comment])


		dic['comment']=comms
		num_of_comments=len(text)-1
		flag='instagram'
		cvsrow = [moviename, datestring[0], articleNumber, article, hashtag, favorites, num_of_comments, flag]
		resfWriter.writerow(cvsrow);
		item=item+1


		i=i+1
		articleNumber=articleNumber+1

		#다음 버튼
		while True:
			try:
				WebDriverWait(browser, 3600).until(
				EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/div/div/a[2]'))
				)
				next_button=browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div/a[2]")

				while next_href==cur_href:
					time.sleep(0.1)
					html = browser.page_source
					soup = BeautifulSoup(html,'html.parser')
					next_href=soup.find('a', {'class':'HBoOv'}).get('href')
					cur_url=browser.current_url
					cur_href=cur_url.replace('https://www.instagram.com', '')

					tmp=cur_href.split('/?')
					cur_href=tmp[0]+'/?tagged='+keyword

					print(next_href)
					print(cur_href)

				browser.execute_script("arguments[0].click();", next_button)
				print('click next')

			except:
				time.sleep(1)
				continue
			break


		time.sleep(0.01)
		print('enddate<d', d)
		continue

		time.sleep(1)


#WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div/article/header")))

#browser.find_element_by_xpath("""/html/body/div[3]/div/div[1]/div/div/a[2]""").click()

# for e in list:
#     print(e,'\n')
# print("*****lengthoflist:",len(list))
