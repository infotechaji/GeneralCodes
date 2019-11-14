# # -*- coding: utf-8 -*-	
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urlparse import urljoin
import os
from pathlib2 import Path
import sys
import urlparse 
import os.path
from os import path
from copy_folder import *
#self.browser.get('https://myinspire.microsoft.com/page/attendeenetworking?p1=eyJzcGVha2VyIjpbXSwidGltZXNsb3QiOltdLCJkYXkiOltdLCJyb29tIjpbXSwicGFnZW51bWJlciI6MSwiY2F0ZWdvcmllcyI6e30sImtleXdvcmQiOiIifQ%3D%3D')
#raw_input()

#oldself.password='Lailagail564!'

class MSInspire():
	def __init__(self,developer_mode=False,driver='Chrome',auto_login=False):
		if driver=='Chrome':
			self.browser=webdriver.Chrome()
		self.developer_mode=developer_mode
		self.spl_characters=[' ','/','\\','\n','\t']
		self.username='faris@fiind.com'		
		self.password='Welcome123'
		#self.url='https://myinspire.microsoft.com/'
		#self.url='https://myinspire.microsoft.com/attendees?s=%257B%2522name%2522%253A%2522A-Z%2522%252C%2522type%2522%253A1%252C%2522%2524%2524hashKey%2522%253A%2522object%253A72%2522%257D&f=%255B%257B%2522name%2522%253A%2522United%2520States%2522%252C%2522facetName%2522%253A%2522areaCountry%2522%257D%252C%257B%2522name%2522%253A%2522Partner%2522%252C%2522facetName%2522%253A%2522fieldCorp%2522%257D%255D#top-anchor'
		self.url='https://myinspire.microsoft.com/home'
		self.collected_path=os.path.join(os.getcwd(),'collected_files')
		if not os.path.exists(self.collected_path):os.makedirs(self.collected_path)
		if self.ms_login(): print 'Login Successful!!'
	def ms_login(self):
		try:
			self.browser.get(self.url)
			print ('Home page hitted ')
			time.sleep(3)
			#raw_input('Press Enter After Account Btn enabled.')
			#self.browser.find_element_by_link_text('Microsoft account').click() # first click
			
			# self.browser.find_element_by_id('MSAExchange').click()
			# print 'Ms Account Clicked'
			# #raw_input('press after mail asked')
			# time.sleep(1)
			# mail_element=self.browser.find_element_by_id('i0116')
			# mail_element.send_keys(self.username)
			# mail_element.send_keys(Keys.RETURN)
			# print 'Mail ID Entered '
			# time.sleep(1)
			# pass_element=self.browser.find_element_by_name('passwd')
			# pass_element.send_keys(self.password)
			# pass_element.send_keys(Keys.RETURN)
			# print 'Password Entered '
			# time.sleep(2)
			return True
		except Exception as e:
			print 'Exception in hitting home page  ',e
			return False
	def write_content(self,file_name,content_dict):
		if file_name=='scraped_results.txt':
			fp=open(file_name,'a')
			final_text=str(content_dict['total_accounts_count'])+'\t'
			final_text+=str(content_dict['person_name'])+'\t'+str(content_dict['person_url'])+'\t'
			final_text+=str(content_dict['linkedin_url'])+'\t'+str(content_dict['designation'])+'\t'
			final_text+=str(content_dict['company_name'])+'\t'+str(content_dict['unparsed_designation'])+'\t'
			final_text+=str(content_dict['account_count'])+'\t'+str(content_dict['page_number'])+'\t'
			final_text+='\n'
			fp.write(final_text)
			fp.close()
		elif file_name=='person_details.txt':
			fp=open(file_name,'a')
			#Headers: p_id\tperson_name\tperson_url\tcompany_website\tjobcategory\tlinkedin_url\tcustomersegment\tcompetencies\tbusinessfocus\tindustryfocus\torganization
			final_text=str(content_dict['p_id'])+'\t'
			final_text+=str(content_dict['person_name'])+'\t'+str(content_dict['person_url'])+'\t'
			final_text+=str(content_dict['company_website'])+'\t'+str(content_dict['jobcategory'])+'\t'
			final_text+=str(content_dict['linkedin_url'])+'\t'+str(','.join(content_dict['customersegment']))+'\t'
			final_text+=str(','.join(content_dict['competencies']))+'\t'+str(','.join(content_dict['businessfocus']))+'\t'
			final_text+=str(','.join(content_dict['industryfocus']))+'\t'+str(','.join(content_dict['organization']))+'\t'
			final_text+='\n'
			fp.write(final_text)
			fp.close()
	def write_into_file(self,file_name,content='',mode='a'):
		try:
			with open(file_name,mode) as fp:
				try:fp.write(content)
				except:fp.write(content.encode('utf-8'))
			return True
		except Exception as e :
			print('Exception in writing write_into_file :',e)
			return False

	def person_details_2(self):
		# soup = page_source
		# person_name =attendee-detail__info--heading
		# p_tag=get tag(c-paragraph-2 f-lean)
		# designation = span.text 
		# company_name = a_tag.text 
		pass


	def getPersonDetails(self,person_name,person_url):
		if person_url:
			time.sleep(2)
			try:
				self.browser.get(person_url)
			except Exception as e :
				print 'Exception :',e
				return False
			time.sleep(2)
			temp_file_name=str(person_name).replace(' ','').replace('.','_')
			html_file_name='person_details'+os.sep+temp_file_name
			checking_directory=Path(html_file_name)
			page_content=self.browser.page_source
			if not checking_directory.exists():
				with open(html_file_name,'a') as filewriter:
					filewriter.write(page_content.encode('utf-8'))
					filewriter.close()
				print 'File Saved  ',html_file_name
			else:
				print 'File Exists !!! ',html_file_name
				pass
			result_dict={'p_id':0,'person_name':person_name,'person_url':person_url,'company_website':'','linkedin_url':'','jobcategory':'','competencies':'','industryfocus':''
							,'businessfocus':'','customersegment':'','organization':''}
			div_tags=self.browser.find_elements_by_class_name('attendee-metadata__property')
			div_count=0
			for each_div in div_tags:
				div_count+=1
				ng_if_text=str(each_div.get_attribute('ng-if'))
				#h4_text=each_div.find_element_by_tag_name('h4')
				if 'websiteurl' in ng_if_text.lower():
					result_dict['company_website']=str(each_div.find_element_by_tag_name('a').text)
				elif 'linkedin' in  ng_if_text.lower():
					result_dict['linkedin_url']=str(each_div.find_element_by_tag_name('a').text)
				elif 'jobcategory' in  ng_if_text.lower():
					result_dict['jobcategory']=str(each_div.find_element_by_tag_name('p').text)
				elif 'competencies' in  ng_if_text.lower():
					a_tags=each_div.find_elements_by_tag_name('a')
					competencies_list=[]
					for each_a_tag in a_tags:
						a_temp_text=str(each_a_tag.text)
						if a_temp_text:
							competencies_list.append(a_temp_text)
					result_dict['competencies']=competencies_list
				elif 'industryfocus' in  ng_if_text.lower():
					a_tags=each_div.find_elements_by_tag_name('a')
					industryfocus_list=[]
					for each_a_tag in a_tags:
						a_temp_text=str(each_a_tag.text)
						if a_temp_text:
							industryfocus_list.append(a_temp_text)
					result_dict['industryfocus']=industryfocus_list
				elif 'businessfocus' in  ng_if_text.lower():
					a_tags=each_div.find_elements_by_tag_name('a')
					businessfocus_list=[]
					for each_a_tag in a_tags:
						a_temp_text=str(each_a_tag.text)
						if a_temp_text:
							businessfocus_list.append(a_temp_text)
					result_dict['businessfocus']=businessfocus_list
				elif 'customersegment' in  ng_if_text.lower():
					a_tags=each_div.find_elements_by_tag_name('a')
					customersegment_list=[]
					for each_a_tag in a_tags:
						a_temp_text=str(each_a_tag.text)
						if a_temp_text:
							customersegment_list.append(a_temp_text)
					result_dict['customersegment']=customersegment_list
				elif 'organization' in  ng_if_text.lower():
					a_tags=each_div.find_elements_by_tag_name('a')
					organization_list=[]
					for each_a_tag in a_tags:
						a_temp_text=str(each_a_tag.text)
						if a_temp_text:
							organization_list.append(a_temp_text)
					result_dict['organization']=organization_list
			return result_dict
		else:
			return False
	
	def ClickEachPage(self,directory_to_look=''):
		
		#page_source : 
		#
		#h4_tags=self.browser.find_elements_by_class_name("attendee-list-item__heading-name c-heading-4 f-lean")
		temp_page_source=self.browser.page_source
		#print 'Page source collected '
		#self.write_into_file(file_name='source_1.txt',content=temp_page_source,mode='w')
		divs=self.browser.find_elements_by_class_name("attendee-list-item__heading-name")
		user_details=[]
		combined_url=''
		count=0
		for each_tag in divs:
			#input_el = driver.find_element_by_name('A')
			#attendee-list-item__details-section - parent div class name 
			# try:
			# 	#parent_tag_selected=parent_div.find_elements_by_tag_name('attendee-list-item__details-section')
			# 	parent_div = each_tag.find_element_by_xpath('..')
			# 	spans=parent_div.find_elements_by_tag_name('attendee-list-item__details-section')
			# 	for each_span in spans:
			# 	parent_text=parent_tag_selected.text
			# 	print 'parent_text :',parent_text
			# except Exception as e :
			# 	print 'Error in getting parent tag',e
			# 	continue
				
			#print 'parent_div.text :',parent_text
			# try:
			if True:
				#print "each_tag :",str(each_tag)
				#h4=each_tag.find_element_by_tag_name('h4')
				#print 'h4 :',str(h4)
				a_tag=each_tag.find_element_by_tag_name('a')
				person_name=a_tag.text.strip()
				spans=each_tag.find_elements_by_tag_name('span')
				print "len(spans):",len(spans)
				span_text=''
				for each_span in spans:
					span_text+=each_span.text.strip()
				try:print 'span_text :',span_text
				except: print 'span_textencode(utf-8):',span_text.encode('utf-8')
#print 'a_tag :',str(a_tag)
				
				#if parent_text:
				
				temp_person_name=person_name+span_text
				print 'temp_person_name :',temp_person_name
				# else:
				# 	temp_person_name=person_name
				for each_char in self.spl_characters:
					temp_person_name=temp_person_name.replace(each_char,'_')
				temp_file_name=temp_person_name
				if directory_to_look:
					directories=directory_to_look.split(',')
					for each_directory in directories:
						temp_full_file_name =os.path.join(each_directory,temp_file_name)
						if path.exists(temp_full_file_name): 
							try:copytree(each_directory, self.collected_path,files_list=[temp_file_name])
							except:pass
							#continue
				full_file_name =os.path.join(self.collected_path,temp_file_name)
				if path.exists(full_file_name): continue
				count+=1
				href=a_tag.get_attribute("href")
				print ("count :",count,"person_name :",person_name)
				combined_url=urlparse.urljoin(self.browser.current_url, href)
				#print "combined_url :",combined_url
				if person_name and combined_url:
					temp_dict={'person_name':person_name,'combined_url' :combined_url}
					user_details.append(temp_dict)
				# opening new tab to handle the page 
				self.browser.execute_script("window.open('');")
				time.sleep(2)
				self.browser.switch_to.window(self.browser.window_handles[1])
				print 'New page Opened'
				self.browser.get(combined_url)
				time.sleep(3)
				temp_page_source=self.browser.page_source
				print 'Page source collected !'
				self.write_into_file(file_name=full_file_name,content=temp_page_source,mode='w')
				self.browser.close()
				time.sleep(1)
				# Switch back to the first tab
				self.browser.switch_to.window(self.browser.window_handles[0])
				# soup = BeautifulSoup(a_tag)
				# print 'soup :',soup
				# #for link in soup.findAll('a'):
				# href= link.get('href')
				# print 'href :',href
				# combined_url=urlparse.urljoin(self.browser.current_url, href)
				# print "combined_url :",combined_url
				# if person_name and combined_url:
				# 	temp_dict={'person_name':person_name,
				# 				'combined_url' :combined_url}
				# 	user_details.append(temp_dict)
				# print ("person_name :",person_name)
				# temp_file_name=person_name.replace(' ','_')
				# temp_content=str(person_name)+'\t'+str(temp_file_name)
				# temp_content+='\n'
				# self.write_into_file(file_name='users_log.txt',content=temp_content)
				# full_file_name =os.path.join(self.collected_path,temp_file_name)
				# if not path.exists(full_file_name):
				# 	a_tag.click()
				# 	print 'Person name clicked :',
				# 	time.sleep(3)
				# 	temp_page_source=self.browser.page_source
				# 	print 'Page source collected '
				# 	self.write_into_file(file_name=full_file_name,content=temp_page_source,mode='w')
				# 	print 'page_saved '
				# 	#self.browser.back()
				# 	#self.browser.execute_script("window.history.go(-1)")
				# 	raw_input('before hitting BACK TO ATTENDEES')
				# 	#self.browser.find_element_by_link_text('BACK TO ATTENDEES').click()
				# 	self.browser.back()
				# 	print 'Back pressed'
				# 	time.sleep(15)
				# 	temp_page_source=self.browser.page_source
				# 	print 'Page source collected '
				# 	self.write_into_file(file_name='source_2.txt',content=temp_page_source,mode='w')
				#else: print 'File already exists'
			# except Exception as e :
			# 	print 'Exception in getting Click EachPage',e
			# 	pass
			# 	time.sleep(10)
	def click_next_page(self):
		a_tags=self.browser.find_elements_by_tag_name('a')
		try_count=0
		for each_a_tag in a_tags:
			try:
				aria_label=each_a_tag.get_attribute('aria-label')
				if aria_label=="Next Page":
					each_a_tag.click()
					print 'Next page element clicked !!!'
					time.sleep(5)
					return True
			except Exception as e :
				try_count+=1
				print "Exception in click_next_page() :",e
				if try_count>=2:
					return False
				pass

	def getAttendeesList(self):
		#if self.ms_login():
		if True:
			raw_input('Presss Enter after manual Login ')
			print ('Login Successful!!')
			time.sleep(2)
			self.browser.find_element_by_id('connecting').click()
			print ('connecting clicked')
			try:
				self.browser.find_element_by_link_text(' Attendee Directory ').click()
				print ('Try : Attendee Directory clicked !!')
			except Exception as e:
				self.browser.find_element_by_partial_link_text('Attendee Directory').click()
				print ('Exception :Attendee Directory clicked !!')
			#  Filters : Us and MS Partner
			#self.browser.find_elements_by_xpath('//*[@id="content-container"]/div/div[2]/div/mwf-refiner[8]/div/div/button/text()'
			#country =self.browser.find_elements_by_xpath("//*[contains(text(), \"Country\")]")
			#print ("country found !",country)
			raw_input('After filtering Press Enter')
			page_number=76
			total_accounts_count=0
			while True:
				page_number+=1
				#save file 
				temp_file_name='Page_number'+str(page_number)
				html_file_name='htmlfiles'+os.sep+temp_file_name
				checking_directory=Path(html_file_name)
				page_content=self.browser.page_source
				if not checking_directory.exists():
					with open(html_file_name,'a') as filewriter:
						filewriter.write(page_content.encode('utf-8'))
						filewriter.close()
					print 'File Saved  ',html_file_name
				else:
					print 'File Exists !!! ',html_file_name
					pass
				accounts_div=self.browser.find_elements_by_class_name("attendee-list-item")
				print len(accounts_div)
				account_count=0
				for each_div in accounts_div:
					account_count+=1
					total_accounts_count+=1
					temp_dict={'total_accounts_count':total_accounts_count,'linkedin_url':'','person_name':'','person_url':'','designation':'','account_count':account_count,'page_number':page_number,'company_name':'','unparsed_designation':''}
					name_div =each_div.find_element_by_class_name("attendee-list-item__heading--container")
					if name_div:
						a_tags=name_div.find_elements_by_tag_name('a')
						a1_count=0
						for each_a_tag in a_tags:
							a1_count+=1
							#print 'a1_count:',a1_count
							if a1_count==1:
								try:
									temp_dict['person_name']=str(each_a_tag.text).strip(' \t\r\n')
								except Exception as e :
									try:
										temp_dict['person_name']=str(each_a_tag.text.encode('utf-8')).strip(' \t\r\n')
									except Exception as e :
										temp_dict['person_name']=''
										pass
								#print 'temp_dict[\'person_name\']:',temp_dict['person_name']
								temp_href=each_a_tag.get_attribute('href')
								temp_dict['person_url']=urljoin(self.url,temp_href)
								#print 'temp_dict[\'person_url\']:',temp_dict['person_url']
							if a1_count==2:
								temp_href=each_a_tag.get_attribute('href')
								if temp_href and 'linkedin' in temp_href:
									temp_dict['linkedin_url']=temp_href
					comp_div=each_div.find_element_by_class_name("attendee-list-item__company")
					try:
						temp_designation=str(comp_div.text).strip(' ,\t\r\n')
					except Exception as e:
						try:
							temp_designation=str(comp_div.text.encode('utf-8')).strip(' ,\t\r\n')
						except Exception as e :
							temp_designation=''
							pass
					temp_dict['unparsed_designation']=temp_designation
					splits=temp_designation.split(',')
					if len(splits)==2:
						temp_dict['designation']=splits[0]
						temp_dict['company_name']=splits[1]
					elif len(splits)==1:
						temp_dict['designation']=splits[0]
					elif len(splits)>2:
						temp_dict['designation']=splits[0]
						temp_dict['company_name']=str(','.join(splits[1:])).strip(' ,')
					print account_count,temp_dict['person_name']
					self.write_content(file_name='scraped_results.txt',content_dict=temp_dict)
				#print "loop count :2"
				#next_tags=self.browser.find_element_by_class_name("c-glyph x-hidden-focus")
				#li_tags=self.browser.find_element_by_tag_name('li')
				#print "li_tags:",len(li_tags)
				for each_a_tag in self.browser.find_elements_by_tag_name('a'):
					aria_label=each_a_tag.get_attribute('aria-label')
					#print 'aria_label:',aria_label
					if aria_label and aria_label=='Next Page':
						try:
							each_a_tag.click()
							time.sleep(4)
							break
						except Exception as e :
							print 'Exception:',e 
							pass
						#print 'Next Element Clicked!!'
				if page_number==270  or total_accounts_count>=2675: break
				#raw_input('one time executed')
				#load Next page


		# self.browser.find_element_by_id('SignInWithLogonNameExchange').click()
	# print "self.username/self.password Clicked" 
	# self.browser.find_element_by_name('login').send_keys(self.username)
	# #time.sleep(1)
	# self.browser.find_element_by_name('passwd').send_keys(self.password)
	# #time.sleep(1)
	# self.browser.find_element_by_id('cred_sign_in_button').click()
	# time.sleep(2)
	#print "Login succeed!!"
#ms_login('https://myinspire.com/page/attendeenetworking?p1=eyJzcGVha2VyIjpbXSwidGltZXNsb3QiOltdLCJkYXkiOltdLCJyb29tIjpbXSwicGFnZW51bWJlciI6MSwiY2F0ZWdvcmllcyI6e30sImtleXdvcmQiOiIifQ%3D%3D')
if __name__=='__main__':
	ms_obj=MSInspire()
	try:directory_to_look=sys.argv[1]
	except: directory_to_look=''
	target_page_count=84
	if True:
		count=0
		while True:
			count+=1
			if count==1:
				raw_input('Press enter once manual authentication is Successful')
			ms_obj.ClickEachPage(directory_to_look=directory_to_look)
			print ("processing page",count)
			if ms_obj.click_next_page()==False:
				break
			# if count>=target_page_count:
			# 	print "{} pages scraped ".format(target_page_count)
			# 	break


	if not True:
		ms_obj.getAttendeesList()
	if not True:
		input_file_name=sys.argv[1]
		file_lines=open(input_file_name,'r').readlines()
		output_file_name=input_file_name.replace('.','._output')
		write_fp=open(output_file_name,'a')
		count=0
		for each_line in file_lines:
			count+=1
			splits=each_line.strip(' \t\r\n').split('\t')
			p_id=splits[0]
			person_name=splits[1]
			person_url=splits[2]
			print count,person_name
			result_dict=ms_obj.getPersonDetails(person_name=person_name,person_url=person_url)
			result_dict['p_id']=p_id
			if result_dict:
				ms_obj.write_content(file_name="person_details.txt",content_dict=result_dict)
			time.sleep(3)
			#raw_input('one over')

	# if ms_login():
	# 	print ('Login_succeed!!')
	# else:
	# 	print ('Login Failed')
	# 	exit()