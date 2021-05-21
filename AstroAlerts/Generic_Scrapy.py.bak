"""
Description : script to scrape tracemy Ip domains 
Version : v1.2

History :
		  v1.0 - 04/23/2019 - initial version 
		  v1.1 - 04/23/2019 - added logic  
		  v1.2 - 05/20/2019 - added a Function GetPageSource is added 

"""

import requests, zipfile, io
from selenium import webdriver
from urllib2 import quote
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import sys,time
#from urllib.parse import urljoin
from urlparse import urljoin
import os
import os.path
from os import path
from MasterGmail import * 
from TechProcessSupport import * 
import datetime 


class MasterScrape():
	def __init__(self,source_count=0):
		self.source_count=source_count
		self.source_url="https://tools.tracemyip.org/search--domain/500-01.shtml:-v-:&gTr=<index>&gNr=50"
		self.output_file_name='default_output.txt'
		#driver_location=os.path.join(os.getcwd(), "chromedriver.exe")
		self.collected_path='collected_files'
		self.browser_opened=False
		self.suspect_limit=0
		self.universal_count=0
		if not os.path.exists(self.collected_path): os.makedirs(self.collected_path)
	
	def GetPageSoure(self,link,use_request=True,check_files=True,use_selenium=False,close_browser=True,save_file=True):
		try:
			page_source=''
			if check_files==True:
				file_presence=self.check_file_presence(link)
				if file_presence['status']:
					print 'Page source from File !'
					page_source=file_presence['file_content']
			if len(page_source)<=2 and use_request==True:
				page_source = requests.get(link).text
			elif len(page_source)<=2 and use_selenium==True:
				if self.browser_opened==False:
					self.browser = webdriver.Chrome() # testing 
					self.browser_opened=True
					suspect_limit=0
				self.browser.get(link) # tesing 
				time.sleep(10)
				page_source=self.browser.page_source
				if close_browser==True:
					self.browser.quit()
					self.browser_opened=False
			if page_source and save_file==True:self.save_file(page_source)
		except Exception as e:
			print 'Exception in getting page source ',e
			return ''
		return page_source

	def get_page_source(self,browser_current_url,use_selenium=True,close_browser=False,extract=True):
			if not browser_current_url:browser_current_url=self.browser.current_url
			print 'scraping url :',browser_current_url
			#file_presence=self.check_file_presence(browser_current_url)
			if check_files==True:
				file_presence=self.check_file_presence(browser_current_url+str(self.universal_count))
				retry_count=0
				if file_presence['status']:
					print 'Page source from File !'
					page_source=file_presence['file_content']
					if len(page_source)==237:
						page_source=self.browser.get(browser_current_url)
					else:	
						self.send_error_mail(exception='Page source from File !',url=browser_current_url)
						print 'Quitting code....'
						exit()
					page_source=file_presence['file_content']
			else:
				#if not self.browser_opened or self.suspect_limit>=30:
				if not self.browser_opened:
					self.browser = webdriver.Chrome() # testing 
					self.browser_opened=True
					suspect_limit=0
				self.browser.get(browser_current_url) # tesing 
				time.sleep(10)
				page_source=self.browser.page_source
				print 'page_source :',len(page_source)
				for i in range(0,3):
					if len(page_source)==237 and retry_count<=3:
						retry_count+=1
						time.sleep(10)
						print 'Retrying count :',retry_count
						self.browser.get(browser_current_url)
						time.sleep(10)
						page_source=self.browser.page_source
					else:break
				if page_source:
					self.save_file(page_source)
				browser_current_url=self.browser.current_url
			print 'browser_current_url :',browser_current_url
			if extract:
				soup=self.soup_modification(page_source)
			if close_browser:
				self.browser.quit()
			return soup
	def close_browser(self):
		try:
			self.browser.quit()
			return True
		except Exception as e:
			print 'Exception in closing browser !' ,e
			return False
	def get_text_from_tag(self,selected_tag):
		temp_text=selected_tag.text.strip(' ')
		temp_text=temp_text.strip('\n')
		temp_text=temp_text.replace('  ',' ')
		return temp_text

	def get_table_data(self,soup):
		temp_data=''
		table_element=soup.find_all("table")
		#print 'table_element :',table_element
		if not table_element: 
			print 'table table_element  missing !'
			table_element=soup
		#print 'table_element :',table_element
		tbody=table_element.find('tbody')
		#print 'tbody :',tbody
		count=0
		if tbody:
			tr_elements=table_element.find_all('tr')
			print 'Total Rows :',len(tr_elements)
			tr_count=0
			if tr_elements:
				for each_tr in tr_elements:
					tr_count+=1
					sys.stdout.write('Page : '+str(self.universal_count)+' , Processing row :'+str(tr_count)+'  \r')
					tds=each_tr.find_all('td')
					#print 'tds :',len(tds)
					for each_td in tds:
						temp_text=self.get_text_from_tag(each_td)
						#print 'temp_text :',temp_text
						temp_data+=temp_text+'\t'
					#print 'td over :'
					temp_data=temp_data.strip('\t')
					temp_data+='\n'
					if count>=10:
						self.write_content(file_content=temp_data)
						count=0
						temp_data=''
						#print 'temp_data is null '
						#raw_input('ssdf')
					else:count+=1
		if count>0 and count<10 and temp_data:
			temp_data=temp_data.strip('\n')
			self.write_content(file_content=temp_data)
		#print 'temp_data :',temp_data
		return True
	def get_nextpage_url(self):
		self.source_count+=50
		print "self.source_url :",self.source_url
		normalised_url=(self.source_url).replace('<index>',str(self.source_count))
		print 'next page url  : ',normalised_url
		#raw_input('raw_input : ')
		return normalised_url
		#self.browser.get(normalised_url)
	def click_next_page(self,next_page_element='',use_numbers=False):
		#if next_page_element:
		if use_numbers:
			return self.get_nextpage_url()
			# self.page_index+=50
			# normalised_url=self.source_url.replace('<index>',self.page_index)
			# self.browser.get(normalised_url)
		try:
			self.browser.find_element_by_id('sbmButton2').click()
			#self.browser.find_element_by_partial_link_text('Next')
			print 'Next page button clicked !!'
			return True
		except: print 'Exception in gettiing next page.'
		return False
	def write_content(self,file_name='',file_content='',mode='a'):
		if not file_name:file_name=self.output_file_name
		with open(file_name,mode) as fp:
			try:
				fp.write(file_content)
			except Exception as e:
				fp.write(str(file_content.encode('utf-8')))

	def get_file_name(self,url,replace_by='_'):
		spl_characters=['/','\\',':','-']
		temp_name=url
		for i in spl_characters:
			temp_name=temp_name.replace(i,replace_by)
		return temp_name
	def __del__(object):
		print "MasterScrape Object Deleted !!"
	def check_file_presence(self,browser_current_url):
		self.file_name=self.get_file_name(browser_current_url+str(self.universal_count))
		self.full_file_path=os.path.join(self.collected_path,self.file_name)
		file_content=''
		if path.isfile(self.full_file_path):
			file_content=open(self.full_file_path).read()
			return {'status':True,'file_content':file_content}
		else:
			return {'status':False,'file_content':file_content}
	def save_file(self,page_source):
		with open(self.full_file_path,'w') as fp:
			try:
				fp.write(str(page_source))
			except:
				fp.write(str(page_source.encode('utf-8')))
				pass
	def soup_modification(self,page_source,remove_tags=[]):
		try:
			soup = BeautifulSoup(page_source, "html.parser")
		except Exception as e:
			#print 'except :',e
			soup=page_source
			pass
		if not remove_tags : remove_tags=['script','style']
		for tag in remove_tags:
			for each_tag in soup.select(tag):
				each_tag.decompose()
		#soup = BeautifulSoup(soup, "html.parser")
		return soup
	def unicode_data(self, data):
		if not data: 
			return u''
		if type(data) in [int, float, long]:
			data = unicode(data)
		if not isinstance(data, unicode):
			data = data.decode('utf-8')
		return data
	
	def send_error_mail(self,exception,url):
		host_dict=get_host_details()
		ip_address=host_dict['ip_address']
		host_name=host_dict['host_name']
		user_name=host_dict['user_name']
		gm_obj=Gmail()
		#gm_obj.read_email_from_gmail()
		receivers='ajith@fiind.com'
		input_dict={}
		input_dict['subject']='Error In Script execution !! with IP : '+str(ip_address)+' host name : '+str(host_name)+' User name :'+str(user_name)
		input_dict['body']={
							'greetings':'Hi All ,',
							'content':'Error while scraping the link : '+str(url)+'\n\n'+str(exception),
							'bottom_content':'',
							'table_input':{
											'headers':{'Title':'Value'},
											'table_content':[
															{'ip_address':ip_address},
															{'host_name':host_name},
															{'user_name':user_name},
															{'time_stamp':datetime.datetime.now()}
															]
											}
							}
		input_dict['attachment']=[]
		# {'file_name':'Dummy_textFile.txt',
									# 'full_file_path':'D:\\Ajith\\_code\\GeneralCodes\\Mail\\Dummy_textFile.txt'}
		
		gm_obj.send_mail(input_dict=input_dict,receivers=receivers)
	def custom_scrape(self,url,use_selenium,close_browser,waiting_time_mins=5):
		url=self.get_nextpage_url()
		try_count=0
		while True:
			try:
				page_soup =self.get_page_source(url,use_selenium=use_selenium,close_browser=close_browser)
				#print page_soup
				table_element =page_soup.find('table',{"id":"tlzRDTIDom"})
				#print 'table_element',table_element
				if table_element:
					print self.get_table_data(table_element)
					#if self.click_next_page():
					temp_url=self.get_nextpage_url()
					self.universal_count+=1
					self.suspect_limit+=1
					if temp_url==url and try_count>3:
						raise Exception('Same URL Matched !!')
						break
					elif temp_url==url and try_count<=3:
						try_count+=1
						url=temp_url
						continue
					else:
						url=temp_url
						print 'Sleeping for '+str(waiting_time_mins)+' minutes  !!'
						for i in range(int(waiting_time_mins)*60,0,-1):
							sys.stdout.write('Code is under sleep.. Seconds remaining  :'+str(i)+'  \r')
							time.sleep(1)
			except Exception as e:
				print 'Got Exception :',e
				self.send_error_mail(exception=e,url=url)
				print 'Quitting script !'
				break


if __name__=="__main__":
	url="https://tools.tracemyip.org/search--domain/500-01.shtml"
	url="https://tools.tracemyip.org/search--domain/500-01.shtml:-v-:&gTr=1501&gNr=50"
	url="https://tools.tracemyip.org/search--domain/500-01.shtml:-v-:&gTr=1651&gNr=50"
	url="https://tools.tracemyip.org/search--domain/500-01.shtml:-v-:&gTr=6301&gNr=50"
	use_selenium=True
	close_browser=False
	# source_count=8051
	# source_count=15351
	# source_count=17951
	# source_count=18651
	source_count=56551
	ms_obj=MasterScrape(source_count)
	ms_obj.custom_scrape(url,use_selenium=use_selenium,close_browser=close_browser,waiting_time_mins=15)
	