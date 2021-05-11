"""
Functionlaity : Script to handle Rtrack
Version       : v1.0
History       :
                v1.0 - 17/11/2020 - initial version
                

Input:

Process      :
Output       :

Test Cases taken   :
Test Cases passed  :
Test Cases need
to be handled      :

Pending   items :
                    




Open issues :
Comments :

"""
import time,argparse,re
import urllib.parse,sys
sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')
from selenium import webdriver
from bs4 import BeautifulSoup
from Rtrack_config import *
from Help_print import *
from CustomisedFileOperation import *
from Datastructure_help import *
from CompareAndUpdate import *

from selenium.webdriver.common.keys import Keys


class Rtrack():
	def __init__(self,url ,use_selenium = True,developer_mode = False,login = True):
		self.use_selenium = use_selenium
		self.developer_mode = developer_mode
		if not url:
			url = 'https://advisor.morganstanley.com/search?profile=16347&;q=Miami%2C+FL%2C+USA&r=5'
		if self.use_selenium == True:
			self.browser = webdriver.Chrome()
			self.browser.set_page_load_timeout(600)
			self.browser2 = webdriver.Firefox()
			# self.browser2.set_page_load_timeout(500)
			# self.browser = webdriver.Firefox()
			developer_print('Browser started...')

			self.browser.get(url)

			time.sleep(15)
			# input('Enter after the page loads')
			write_into_file(file_name='temp_soup.html', contents=str(self.browser.page_source), mode='w')


			# if login:
			# 	self.login()
			# 	time.sleep(5)


	def click_show_more(self,developer_mode= False):
		status = False
		comments = ''
		try:
			show_more_elem = self.browser.find_element_by_link_text("See More")
			if show_more_elem:
				if developer_mode:
					developer_print('Show more element is found ')
				show_more_elem.click()
				if developer_mode:
					developer_print('Show more element is clicked ')
				time.sleep(5)
				status = True
		except Exception as e:
			developer_print('Error while clicking show more :',e)
			comments = str(e)

		return  {
			'status': status
			,'comments': comments
		}




	def get_indivijual_profile(self,page_source ='',developer_mode = False):
		headers = '''Total_count\tPage_count\tData_count\tLink\t
					Name\tTitle\tPhoto\tComplex\tAddress\t
					Direct\tBranch\tCertifications\tAreas of Focus\tLanguage\t
					Email\tOur Story\tServices Include\tView my Bio\tLinkedin_link\tTwitter_link\tFacebook\n'''

		write_into_file(file_name='Morgon_results.txt', contents=headers, mode='w')
		processed_list = []
		page_count = 0
		total_count = 0
		while True:
			if not page_source:
				page_source = self.browser.page_source
			soup = BeautifulSoup(page_source, "html.parser")
			page_count+=1
			result_list = soup.find_all("li", {"class":"ResultList-item"})
			result_set_to_return = []
			data_count = 0
			for each_item in result_list:
				data_count +=1
				name = ''
				name_link = ''
				print('Processing .. Total count: {0} Loop count:{1} profile count : {2}  '.format(total_count,page_count,data_count))
				try:
					name_elem = each_item.find("a", {"class": "Teaser-titleLink Link Link--primaryPlain"})
					name  = str(name_elem.get_text()).strip()
					name_link  = name_elem['href']
					if developer_mode:
						developer_print('Name is extracted :', name)
				except Exception as e:
					if developer_mode:
						developer_print('Error in getting name :', e)
				key_elem = name+name_link
				if key_elem not in processed_list:
					processed_list.append(key_elem)
				else:
					developer_print('Skipping the already processed list :',name)
					continue
				total_count+=1
				complex_data = ''
				complex_link = ''
				try:
					complex_data  = str(each_item.find("a", {"class": "Teaser-groupLink Teaser-link"}).get_text()).strip()
					complex_link = str(each_item.find("a", {"class": "Teaser-groupLink Teaser-link"})['href'])
					if developer_mode:
						developer_print('complex data is extracted :', complex_data)
						developer_print('complex link is extracted :', complex_link)
				except Exception as e:
					if developer_mode:
						developer_print('Error in getting complex :', e)


				title = ''
				try:
					title  = str(each_item.find("div", {"class": "Teaser-titles"}).get_text()).strip()
					if complex_data:
						title = title.replace(complex_data,'')
					if developer_mode:
						developer_print('Title is extracted :', title)
				except Exception as e:
					if developer_mode:
						developer_print('Error in getting title :', e)

				address = ''
				try:
					address  = str(each_item.find("div", {"class": "Teaser-address Teaser-link"}).get_text()).strip()
					if developer_mode:
						developer_print('Address is extracted :',address)
				except Exception as e:
					if developer_mode:
						developer_print('Error in getting address :',e)


				direct_phone = ''
				branch_phone = ''
				try:
					phones = each_item.find_all("div", {"class": "c-phone c-phone-main"})#.get_text().strip()
					for each_phone in phones:
						temp_str = str(each_phone.get_text()).strip().replace(' ','')

						temp_phone  = str(each_phone.find("span", {"id": "telephone"}).get_text()).strip()
						if developer_mode:
							developer_print('Temp phone :', temp_phone)
							developer_print('temp_str :', temp_str)
						if 'direct' in temp_str.lower():
							direct_phone = temp_phone
							if developer_mode:
								developer_print('direct phone is found based on keyword :', direct_phone)
						elif 'branch' in temp_str.lower():
							branch_phone = temp_phone
							if developer_mode:
								developer_print('branch phone is found based on keyword :', branch_phone)
						else:
							developer_print('phone cannot be classified , hence adding to the direct phone')
							direct_phone = temp_phone
				except Exception as e:
					if developer_mode:
						developer_print('Error in getting phones :',e)

				certification = ''
				try:
					cert_elem = each_item.find("div", {"class": "Teaser-list Teaser-list--starburst"})

					if cert_elem:
						if developer_mode:
							developer_print('Certification element is found ')
						certification = str(cert_elem.find("div", {"class": "Teaser-listItems"}).get_text()).strip()
					if developer_mode:
						developer_print('Certification is extracted :', certification)
				except Exception as e:
					if developer_mode:
						developer_print('Error in getting certification :', e)

				area_of_focus = ''
				try:
					area_elem = each_item.find("div", {"class": "Teaser-list Teaser-list--clipboard"})
					if area_elem:
						if developer_mode:
							developer_print('Area of focus element is found ')
						area_of_focus = str(area_elem.find("div", {"class": "Teaser-listItems"}).get_text()).strip()
					if developer_mode:
						developer_print('Area of focus extracted :', area_of_focus)
				except Exception as e:
					if developer_mode:
						developer_print('Error in getting area_of_focus :', e)
				languages = ''
				try:
					lang_elem = each_item.find("div", {"class": "Teaser-list Teaser-list--language"})
					if lang_elem:
						if developer_mode:
							developer_print('Language  element is found ')
						languages = lang_elem.find("div", {"class": "Teaser-listItems"}).get_text().strip()
					if developer_mode:
						developer_print('Languages extracted :', languages)
				except Exception as e:
					if developer_mode:
						developer_print('Error in getting languages :', e)
					pass
				image_link = ''
				try:
					img_elem = each_item.find("img", {"class": "ProfilePhoto ProfilePhoto--teaser js-lazy loaded"})
					if img_elem:
						if developer_mode:
							developer_print('Image element is found ')
						image_link = img_elem['src'].strip()
					if developer_mode:
						developer_print('image link extracted :', image_link)

				except Exception as e:
					if developer_mode:
						developer_print('Error in getting image link  :', e)

				# switching windows here
				our_story = ''
				services = ''
				bio = ''
				email = ''
				linkedin_link = ''
				twitter_link = ''
				facebook_link = ''
				if not complex_link:
					complex_link = name_link
				if complex_link:
					# if developer_mode:
					# 	developer_print('Opening another tab....')
					# self.browser.execute_script("window.open('');")
					# self.browser.switch_to.window(self.browser.window_handles[1])
					# if developer_mode:
					# 	developer_print('Hitting link for bio/email:', complex_link)
					# self.browser.get(complex_link)
					# time.sleep(5)
					# temp_page_source = self.browser.page_source
					if developer_mode:
						developer_print('Hitting link in another driver ...',complex_link)
					self.browser2.get(complex_link)
					time.sleep(8)
					temp_page_source = self.browser2.page_source
					if developer_mode:
						developer_print('Page source :', len(str(temp_page_source)))
					each_item2 = BeautifulSoup(temp_page_source, "html.parser")
					write_into_file(file_name='temp_soup2.txt', contents=str(each_item2), mode='w')
					if developer_mode:
						developer_print('Soup length :', len(each_item2))
					try:
						our_story = str(each_item2.find("div", {"class": "Tabs-description"}).get_text()).strip()
						if developer_mode:
							developer_print('our_story extracted  :',our_story)
					except Exception as e:
						if developer_mode:
							developer_print('Error in getting our_story  :', e)


					try:
						service_elem_ul = each_item2.find("ul", {"class": "Tabs-list"})
						temp_li_list = []
						service_elem_li = []
						if service_elem_ul:
							if developer_mode:
								developer_print('Services ul element found   :')
							service_elem_li = service_elem_ul.find_all("li", {"class": "Tabs-listItem"})
						if service_elem_li:
							if developer_mode:
								developer_print('Services list elements are found   :', len(service_elem_li))
							for each_li in service_elem_li:
								temp_text = str(each_li.get_text()).strip()
								if developer_mode:
									developer_print('Extracted service :')
								if temp_text not in temp_li_list:
									if developer_mode:
										developer_print('text added is the list "temp_li_list" :')
									temp_li_list.append(temp_text)
						services = str(','.join(temp_li_list)).strip(',')
						if developer_mode:
							developer_print('extracted services ( final)  :', services)
					except Exception as e:
						if developer_mode:
							developer_print('Error in getting our_story  :', e)


					try:
						# total_bio_team = self.browser2.find_elements_by_css_selector('article."Bio Bio--team"')
						total_bio_team = self.browser2.find_elements_by_class_name('Bio Bio--team')
						if developer_mode:
							developer_print('Total bio profiles found   :', len(total_bio_team))
						for bio_index, each_bio_elem in enumerate(total_bio_team):
							bio_name = str(each_bio_elem.find_element_by_class_name("Bio-nameText").text).strip()
							if developer_mode:
								developer_print('Extracted bio name (suspect) :', bio_name)
							# developer_print('Processing bio {0}/{1}, looping name : {2}, we looking for {3}:'.format(bio_index,len(total_bio_team),bio_name,name))
							if name.lower() in bio_name.lower():
								if developer_mode:
									developer_print('Confirmed bio profile  :', bio_name)
								try:
									bio_click_elem  = each_bio_elem.find_element_by_link_text('View My Bio')
									if bio_click_elem:
										if developer_mode:
											developer_print('Bio element is found :', bio_name)
										bio_click_elem.click()
										if developer_mode:
											developer_print('Bio element is clicked :', bio_name)
										time.sleep(3)
										bio = str(each_bio_elem.find_element_by_class_name("BioAbout-row BioAbout-row--main").text).strip()
								except Exception as bio_e:
									if developer_mode:
										developer_print('Bio is not extracted due to error :', bio_e)
								each_bio = BeautifulSoup(each_bio_elem, "html.parser")
								all_as = each_bio.find_all("a", href=True)
								if developer_mode:
									developer_print('Total a_tags found in bio ', len(all_as))
								temp_href = ''
								for each_a in all_as:

									try:
										if each_a['itemprop'] == "email":
											if developer_mode:
												developer_print('item property is found as email :', each_a['itemprop'])

											span_text = str(each_a.find("span", {"class": "sr-only"}).get_text()).strip()
											if developer_mode:
												developer_print('Span text before replacing :', span_text)
											span_text = str(span_text.lower().replace('email ')).strip()
											if developer_mode:
												developer_print('Span text after replacing :', span_text)
											if span_text:
												email = span_text + email_suffix
											if developer_mode:
												developer_print('Developed email (final):', email)
									except Exception as e_em:
										if developer_mode:
											developer_print('Error in getting email id  :', e_em)
									try:
										temp_href = each_a['href']
										if developer_mode:
											developer_print('each href :', temp_href)
									except Exception as href_e:
										developer_print('Error while getting href element :', href_e)
									if not temp_href: continue
									if 'linkedin' in temp_href:
										linkedin_link = temp_href
										if developer_mode:
											developer_print('linkedin link is extracted :', linkedin_link)
									elif 'twitter' in temp_href:
										twitter_link = temp_href
										if developer_mode:
											developer_print('twitter_link is extracted :', twitter_link)
									elif 'facebook' in temp_href:
										facebook_link = temp_href
										if developer_mode:
											developer_print('facebook_link is extracted :', facebook_link)
					except Exception as e:
						if developer_mode:
							developer_print('Error in getting Bio sections  :', e)
						pass





					#
					# try:
					# 	email_suffix = '@morganstanley.com'
					# 	total_bio_team = each_item2.find_all("article", {"class": "Bio Bio--team"})
					# 	if developer_mode:
					# 		developer_print('Total bio profiles found   :', len(total_bio_team))
					# 	# bio_sections = each_item.find_all("div", {"class": "Bio-section Bio-section--heading"})
					# 	for bio_index,each_bio in enumerate(total_bio_team):
					# 		bio_name = str(each_bio.find("span", {"class": "Bio-nameText"}).get_text()).strip()
					# 		if developer_mode:
					# 			developer_print('Extracted bio name (suspect) :',bio_name)
					# 			# developer_print('Processing bio {0}/{1}, looping name : {2}, we looking for {3}:'.format(bio_index,len(total_bio_team),bio_name,name))
					# 		if name.lower() in bio_name.lower():
					# 			if developer_mode:
					# 				developer_print('Confirmed bio profile  :', bio_name)
					# 			try:
					# 				bio = str(each_bio.find("div", {"class": "BioAbout-row BioAbout-row--main"}).get_text()).strip()
					# 			except Exception as bio_e:
					# 				if developer_mode:
					# 					developer_print('Bio is not extracted due to error :',bio_e)
					# 					# 'View My Bio' click this button correctly and
					#
					# 			if developer_mode:
					# 				developer_print('extracted bio :', bio)
					# 			all_as = each_bio.find_all("a", href=True)
					# 			if developer_mode:
					# 				developer_print('Total a_tags found in bio ', len(all_as))
					# 			temp_href = ''
					# 			for each_a in all_as:
					#
					# 				try:
					# 					if each_a['itemprop']=="email":
					# 						if developer_mode:
					# 							developer_print('item property is found as email :',each_a['itemprop'])
					#
					# 						span_text = str(each_a.find("span", {"class": "sr-only"}).get_text()).strip()
					# 						if developer_mode:
					# 							developer_print('Span text before replacing :', span_text)
					# 						span_text = str(span_text.lower().replace('email ')).strip()
					# 						if developer_mode:
					# 							developer_print('Span text after replacing :', span_text)
					# 						if span_text:
					# 							email = span_text+email_suffix
					# 						if developer_mode:
					# 							developer_print('Developed email (final):', email)
					# 				except Exception as e_em:
					# 					if developer_mode:
					# 						developer_print('Error in getting email id  :', e_em)
					# 				try:
					# 					temp_href = each_a['href']
					# 					if developer_mode:
					# 						developer_print('each href :', temp_href)
					# 				except Exception as href_e:
					# 					developer_print('Error while getting href element :',href_e)
					# 				if not temp_href: continue
					# 				if 'linkedin' in temp_href:
					# 					linkedin_link  = temp_href
					# 					if developer_mode:
					# 						developer_print('linkedin link is extracted :', linkedin_link)
					# 				elif 'twitter' in temp_href:
					# 					twitter_link = temp_href
					# 					if developer_mode:
					# 						developer_print('twitter_link is extracted :', twitter_link)
					# 				elif 'facebook' in temp_href:
					# 					facebook_link = temp_href
					# 					if developer_mode:
					# 						developer_print('facebook_link is extracted :', facebook_link)
					# 			#
					# 			# try:
					# 			# 	a_tag = each_bio.find("a", {"itemprop": "email"})
					# 			# 	span_text = a_tag.find("span", {"class": "sr-only"}).get_text().strip()
					# 			#
					# 			# 	if developer_mode:
					# 			# 		developer_print('Span text before replacing :', span_text)
					# 			# 	span_text = span_text.lower().replace('email ')
					# 			# 	if developer_mode:
					# 			# 		developer_print('Span text after replacing :', span_text)
					# 			# 	if span_text:
					# 			# 		email = span_text
					# 			# 	break
					# 			# except Exception as e_em:
					# 			# 	if developer_mode:
					# 			# 		developer_print('Error in getting email id  :', e_em)
					#
					#
					#
					# except Exception as e:
					# 	if developer_mode:
					# 		developer_print('Error in getting Bio sections  :', e)
					# 	pass


					# self.browser.close()
					# if developer_mode:
					# 	developer_print('Closing the new tab')
					# self.browser.switch_to.window(self.browser.window_handles[0])
					# if developer_mode:
					# 	developer_print('Switching back to the first tab')



				res = {		'name':name
						,'complex_data':complex_data
						,'complex_link':complex_link
						,'title':title
						,'address':address
						,'direct_phone':direct_phone
						,'branch_phone':branch_phone
						,'certification':certification
						,'area_of_focus':area_of_focus
						,'languages':languages
						,'image_link':image_link
						,'our_story':our_story
						,'services':services
						,'bio':bio
						,'email':email
						,'linkedin_link':linkedin_link
						,'twitter_link':twitter_link
						,'facebook_link':facebook_link
						,'page_count':page_count
						,'data_count':data_count
						,'total_count':total_count
				   }


				final_text = [res['total_count'],res['page_count'],res['data_count'],res['complex_link'],
							  res['name'],res['title'],res['image_link'],res['complex_data'],res['address']
							,res['direct_phone'],res['branch_phone'],res['certification'],res['area_of_focus'], res['languages']
						  ,res['email'], res['our_story'], res['services'], res['bio'],res['linkedin_link'],res['twitter_link'],res['facebook_link']
						  ]
				text_to_write = '\t'.join(apply_to_list(final_text,make_string = True))+'\n'
				write_into_file(file_name='SCRAPED_RESULTS_LOG.txt', contents=add_timestamp(text_to_write), mode='a')
				result_set_to_return.append(res)
			if self.click_show_more()['status']:
				print('Looping next set of elements ')
				page_source = ''
			else:
				print('No new elements are found \n Skipping the loop ')
				break
			for res in result_set_to_return:

				final_text_out = [res['total_count'],res['page_count'],res['data_count'],res['complex_link'],
							  res['name'],res['title'],res['image_link'],res['complex_data'],res['address']
							,res['direct_phone'],res['branch_phone'],res['certification'],res['area_of_focus'], res['languages']
						  ,res['email'], res['our_story'], res['services'], res['bio'],res['linkedin_link'],res['twitter_link'],res['facebook_link']
						  ]
				text_to_write_out = '\t'.join(apply_to_list(final_text_out, make_string=True)) + '\n'
				write_into_file(file_name='Morgon_results.txt', contents=text_to_write_out, mode='a')


		return  {
			'results':result_set_to_return
				}













		# removing styles and script
		if not remove_tags: remove_tags = ['script', 'style']
		for tag in remove_tags:
			for each_tag in soup.select(tag):
				each_tag.decompose()
		each_tag = soup.find("div", {"class": "attendee-detail__info"})
		each_tag = soup.find_all("div", {"class": "attendee-detail__info"})
		header = each_element.find('h5').text.strip()
		return {}
	def login(self):
		user_name = USERNAME
		password = PASSWORD
		try:
			print('Logging in with username {} ..............'.format(USERNAME))
			time.sleep(1)
			self.browser.find_element_by_id('login-form-username').send_keys(USERNAME)
			time.sleep(1)
			password_elem = self.browser.find_element_by_id('login-form-password')
			password_elem.send_keys(PASSWORD)
			time.sleep(1)
			password_elem.send_keys(Keys.ENTER)

			print('Login success ! ')
		except Exception as e:
			print('Error while loggin in ..',e)
			return False
		return True

	def raise_merge_request(self,epe_id ,ut_branch_name):
		print('Sleeping 5 seconds.......')
		time.sleep(5)
		# if self.developer_mode:
		# 	print('RamcoGIT:\t raise_merge_request:\t Given ID :{0}\n Branch name :{1}'.format(epe_id,ut_branch_name))
		#
		# # clicking "Merge Requests" on the home page
		# try:
		# 	# self.browser.find_element_by_class_name('shortcuts - merge_requests').click() # clicking merge requests on left side
		# 	self.browser.find_element_by_class_name('shortcuts - merge_requests').click() # clicking merge requests on left side
		# 	merge_url = 'https://ops.ramcouat.com/gitlab/ramco-logistics/lgt/blgt/merge_requests'
		# 	self.browser.get(url)
		# 	print('RamcoGIT:\t raise_merge_request:\t Clicked Merge requests :')
		# except Exception as e:
		# 	print('Error while clicking "merge requests" :',e)
		# 	return False
		# time.sleep(2)
		# try:
		# 	self.browser.find_element_by_link_text('New merge request').click() # clicking merge requests on left side
		# 	print('RamcoGIT:\t raise_merge_request:\t Clicked "New merge request"')
		# except Exception as e:
		# 	print('Error in clicking "New merge request" :',e)
		# 	return False
		# time.sleep(2)
		# // *[ @ id = "new_merge_request"] / div[2] / div[1] / div / div[2] / div[2] / button / span
		# driver.find_element_by_xpath("//div[@id='a']//a[@class='click']")
		# selecting source EPE- ID
		try:
			# source_click_elem = self.browser.find_element_by_xpath('//[ @ id = "new_merge_request"]// div[2] // div[1] // div // div[2] // div[2] // button // span [text() = "Select source branch"]').click()
			# try:
			# 	source_click_elem = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div/form/div[2]/div[2]/div/div[2]/div[2]/button/span').click()
			# 	print('source element is found and clicked - attempt1 ')
			# except Exception as e:
			# 	developer_print ('First attempt missing ')
			# 	pass
			try:
				source_click_elem = self.browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[3]/div/form/div[2]/div[2]/div/div[2]/div[2]/button/span')
				print('source element is found - attempt2')
				print('Total search elements found :', len(source_click_elem))
				try:
					print('text from the span :',source_click_elem.text())
				except:
					print('TExt cannot be extracted')
				source_click_elem.click()
				print('element is clicked')

				# yes slighty tought to do this
				# self.browser.find_element_by_id('merge_request_source_branch')
				# self.browser.find
				#
				# id merge_request_target_branch
				# data-field-name = merge_request[target_branch]


			except Exception as e:
				print('Second attempt  missing ')
				pass
			input('')
			time.sleep(1)

			# source_search = self.browser.find_element_by_xpath('//*[@id="new_merge_request"]//div[2]//div[1]//div//div[2]//div[2]//div//div[2]//input').send_keys(epe_id)
			print('EPE ID is typed in source search ')
			# time.sleep(1)

			# source_search.send_keys(Keys.ENTER)
			print('Enter is pressed and the source id is be selected')
		except Exception as e:
			print('Error in selecting source EPE-ID :', e)
			return False

		# selecting destination branch
		# // *[ @ id = "new_merge_request"] / div[2] / div[2] / div / div[2] / div[2] / button # dest name
		# // *[ @ id = "new_merge_request"] / div[2] / div[2] / div / div[2] / div[2] / div / div[2] / input # dest search
		destination_click_elem = self.browser.find_element_by_xpath('//[ @ id = "new_merge_request"] // div[2] // div[2] // div // div[2] // div[2] // button').click()
		try:
			print('destination  element is found and clicked')
			time.sleep(1)

			destination_search = self.browser.find_element_by_xpath('// *[ @ id = "new_merge_request"] // div[2] // div[2] // div // div[2] // div[2] // div // div[2] // input').send_keys(ut_branch_name)
			print('UT branch name is is typed in destination search ')
			time.sleep(1)

			destination_search.send_keys(Keys.ENTER)
			print('Enter is pressed and the source id is be selected')
		except Exception as e:
			print('Error in selecting Destination branch :', e)
			return False

		try:
			self.browser.find_element_by_name('commit').click() # clicking "Compare branches and continue" after selecting two branches
		except Exception as e:
			print('Error in clicking "Compare branches and continue" ', e)
			return False
		time.sleep(2)

		try:
			self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		except Exception as e:
			print('Error in scrolling down ', e)
			return False
		time.sleep(1)

		try:
			# value of the click button "Submit merge request"
			self.browser.find_element_by_name('commit').click() # clicking "Compare branches and continue" after selecting two branches
		except Exception as e:
			print('Error in clicking "Submit merge request" ', e)
			return False
		time.sleep(2)


		# # // span[text() = "No"]
		# // span[text() = "Select source branch"]
		# Select source branch

		self.browser.find_element_by_class_name('shortcuts - merge_requests').click() # clicking merge requests on left side

		# click_merge_requests()
		# search_two_id


	def get_page_source(self):
		if self.use_selenium:
			page_content=self.browser.page_source
			return {'page_content':page_content,'page_content_length':len(page_content)}
	def click_next_page(self):
		module_name=_class_name+'click_next_page\t'
		print_statement=module_name
		try:
			click_next_button()
			'Next ›'
			print()
		except Exception as e:
			print('Next page not available !')
			return  False
		return True

	def fiind_elements():
		# div_tags=self.browser.find_elements_by_class_name('attendee-metadata__property')
			# div_tags=self.browser.find_element_by_class_name('attendee-metadata__property')
			# div_tags=self.browser.find_element_by_class_name('attendee-metadata__property')
			# 					find_element_by_id
			# 					find_element_by_name
			# 					find_element_by_xpath
			# 					find_element_by_link_text
			# 					find_element_by_partial_link_text
			# 					find_element_by_tag_name
			# 					find_element_by_class_name
			# 					find_element_by_css_selector
		pass
	def switch_browser_window():
		"""
		which switch to new tab and gets the page source and then roll backs to the start page !!!
		"""
		self.browser.execute_script("window.open('');")
		time.sleep(1)
		self.browser.switch_to.window(self.browser.window_handles[1])
		#print 'New page Opened'
		self.browser.get(combined_url)
		time.sleep(2)
		temp_page_source=self.browser.page_source
		try:
			print ('Page source collected !',person_name)
		except:print ('Page source collected !')
		write_into_file(file_name=full_file_name,content=temp_page_source,mode='w')
		self.browser.close()
		time.sleep(1)
		# Switch back to the first tab
		self.browser.switch_to.window(self.browser.window_handles[0])
	def soup_functions(self,page_source):
		"""
		This function handles the pagesource using Beautiful Soup
		"""
		# self.browser.page_source
		soup = BeautifulSoup(page_source, "html.parser")
		
		# removing styles and script
		if not remove_tags : remove_tags=['script','style']
		for tag in remove_tags:
			for each_tag in soup.select(tag):
				each_tag.decompose()
		each_tag=soup.find("div",{"class":"attendee-detail__info"})
		each_tag=soup.find_all("div",{"class":"attendee-detail__info"})
		header=each_element.find('h5').text.strip()

	def get_rtrack_defect_link(self,defect_id,rtrack_defect_link = 'https://rtrackconnect.ramco.com/browse/',developer_mode = False):
		rtrack_link_temp = ''
		if defect_id:
			defect_id = str(defect_id).strip().upper()
			if developer_mode:
				developer_print('prepared rtrack link :',rtrack_link_temp)
			rtrack_link_temp  =  urllib.parse.urljoin(rtrack_defect_link, defect_id)
		return {
			'rtrack_link':rtrack_link_temp
			,'defect_id':defect_id
				}
	def get_defect_details(self,defect_id = '', rtrack_link = '',developer_mode = False):
		temp_defect_link = ''
		defect_id = defect_id.strip()
		defect_id = defect_id.replace(' ','').upper()
		total_dependencies = []
		comments = ''

		if rtrack_link:
			temp_defect_link = rtrack_link
		elif defect_id:
			temp_defect_link = self.get_rtrack_defect_link(defect_id=defect_id,developer_mode = developer_mode)['rtrack_link']
		else:
			developer_print('Please provide either defect id or rtrack link !')
			return {}
		if temp_defect_link:
			if developer_mode:
				developer_print('Hitting link ...:',temp_defect_link)
			self.browser.get(temp_defect_link)
			time.sleep(3)
			temp_soup = BeautifulSoup(self.browser.page_source, "html.parser")
			if developer_mode:
				developer_print('Soup extracted from page source  ...:',len(temp_soup))
				write_into_file(file_name ='temp_soup.txt', contents =str(temp_soup), mode='w')

			if temp_soup:
				status_of_defect = str((temp_soup.find("span", {"id": "status-val"})).get_text()).strip()
				assignee = str((temp_soup.find("span", {"id": "assignee-val"})).get_text()).strip()
				if developer_mode:
					developer_print('status_of_defect is extracted :',status_of_defect)
				# dependencies
				links_list = temp_soup.find("dl", {"class": "links-list"})
				if developer_mode:
					developer_print(' Links list is found  :',len(links_list))
				try:
					total_dependencies = links_list.find_all('dd', id=re.compile('^internal-'))
				except Exception as e:
					if developer_mode:
						developer_print('Error in finding dependencies :',e)
						comments = 'Dependecies not found '



				dependency_list = []
				if total_dependencies:
					if developer_mode:
						developer_print('Total link defects (extracted) :',len(total_dependencies))

					for inde,each_elem in enumerate(total_dependencies):
						write_into_file(file_name='temp_dependency_list.txt', contents=str(each_elem), mode='a')
						defect_desc_temp = ''
						defect_id_temp = ''
						priority_temp = ''
						status_temp = ''
						try:

							try:
								defect_id_temp = (each_elem.find('a', {"class": "issue-link link-title"})).get_text().strip()
							except:
								# developer_print('Defect_id is extracted from second case ')
								defect_id_temp = (each_elem.find('a', {"class": "issue-link link-title resolution"})).get_text().strip()

							defect_desc_temp = (each_elem.find('span', {"class": "link-summary"})).get_text().strip()
							status_temp = (each_elem.find('li', {"class": "status"})).get_text().strip()
							if developer_mode:
								developer_print(' defect_id_temp:', defect_id_temp)
								developer_print(' defect_desc_temp:', defect_desc_temp)
								developer_print(' status_temp:', status_temp)

							temp_dict = {'status':status_temp,'priority':priority_temp,'defect_id':defect_id_temp,'defect_desc':defect_desc_temp,}
							dependency_list.append(temp_dict)
						except Exception as e:
							developer_print('Error in getting dependencies !',e)
							comments = str(e)
		res_dict = {
				'defect_status':status_of_defect
				,'assignee':assignee
				,'defect_id':defect_id
				,'dependency_list':dependency_list
				,'comments':comments
				}
		if developer_mode:
			developer_print('res_dict:',res_dict)
		
		final_text = [len(res_dict['dependency_list'])]
		final_text.append(res_dict['defect_id'])
		final_text.append(res_dict['defect_status'])
		final_text.append(res_dict['assignee'])
		final_text.append(res_dict['comments'])
		for dep_index,each_item in enumerate(res_dict['dependency_list']):
			final_text.append(each_item['defect_id'])
			final_text.append(each_item['status'])
		
		temp_str = str('\t'.join(apply_to_list(final_text,make_string=True))).strip()+'\n'
		write_into_file(file_name=RTRACK_LOG_FILE, contents=add_timestamp(str(temp_str)), mode='a')

		return  res_dict









if __name__ == "__main__":
	start = time.time()

	arg = argparse.ArgumentParser('Program to handle Rtrack details !!', add_help=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	# arg.add_argument('--sp_name', help='single sp file', required=False)
	arg.add_argument('-i', '--input_file', help='File contains list of procedures', required=False)
	# arg.add_argument('-dir', '--directory', help='Directory to save the file.', required=False)
	arg.add_argument('-dev_mode', '--developer_mode',help='This will enable the developer mode which helps the developer', nargs='?', const=True,default=False, required=False)
	# arg.add_argument('--validate_sp', help='This option helps you to verify the fixes present in procedure  ',nargs='?', const=True, default=False, required=False)
	# arg.add_argument('--check_missing_defects',help='This option helps to find the missing defects between different version', nargs='?',const=True, default=False, required=False)
	# arg.add_argument('--save_files', help='This option helps to save the sps for future refereces', nargs='?',const=True, default=False, required=False)
	# arg.add_argument('--use_local_files', help='This option helps to ignore the extraction of sps from SERVER',nargs='?', const=True, default=False, required=False)

	args = arg.parse_args()
	print('Input arguments :', args)
	input("Enter to proceed ?")
	input_file = args.input_file
	developer_mode = args.developer_mode

	ramco_obj = Rtrack(url='')
	# while True:
	ramco_obj.get_indivijual_profile(developer_mode = developer_mode)
		# if ramco_obj.click_show_more()['status'] in (False,'Error'):
		# 	print('Next page element is not found')
		# 	break



	# input_data = get_input_excel(input_file, developer_mode=developer_mode)['excel_data']
	# # print ('input_data[0] :',input_data[0])
	# if input_file:
	# 	t_dic = handle_extension(input_file)
	# 	temp_file_name = str(t_dic['no_extension']) + '_Rtrack_results.txt'
	# 	DIRECTORY = t_dic['directory']
	# 	if not DIRECTORY:
	# 		DIRECTORY = os.getcwd()
	# 	output_file_name = os.path.join(DIRECTORY,temp_file_name)
	# 	write_into_file(file_name=output_file_name, contents=RTRACK_HEADERS, mode='w')
	# for index,each_line in enumerate(input_data):
	# 	if index==0:
	# 		print('Skipping headers :',each_line)
	# 		continue
	# 	defect_id = each_line[0][0].strip()
	# 	# formalizing to LME-123_12 to LME-123
	# 	# print ('Defect ID before formalization : ',defect_id)
	# 	defect_id = get_all_fix_id(file_content = str(defect_id),extract_from_header = False,developer_mode=developer_mode,get_rtrack_id = True)['valid_fixes'][0]
	# 	# print ('Defect ID after formalization : ',defect_id)
	# 	if index ==0:
	# 		print('Ignoring index :',defect_id)
	# 		continue
	# 	print('Processing line : {0}/{1} , Defect id : {2}'.format(index,len(input_data),defect_id))
	# 	res_dict = ramco_obj.get_defect_details(defect_id = defect_id,developer_mode = developer_mode)
	# 	#print('Results :',res_dict)
	#
	# 	# res_dict ={'defect_status': '\nFix Sent ',
	# 	# 		   'defect_id': 'LLE-930',
	# 	# 		   'dependency_list':
	# 	# 			   	[
	# 	# 					{'status': 'Sent For Review',
	# 	# 					 'priority': '',
	# 	# 					 'defect_id': 'EPE-25625',
	# 	# 					 'defect_desc': 'LBC FIX object  movement to UT'
	# 	# 					 }
	# 	# 				]
	# 	# 		   }
	# 	# input('Proceed ?')
	# 	if res_dict:
	#
	# 		final_text = [len(res_dict['dependency_list'])]
	# 		final_text.append(res_dict['defect_id'])
	# 		final_text.append(res_dict['defect_status'])
	# 		final_text.append(res_dict['assignee'])
	# 		final_text.append(res_dict['comments'])
	# 		for dep_index,each_item in enumerate(res_dict['dependency_list']):
	# 			final_text.append(each_item['defect_id'])
	# 			final_text.append(each_item['status'])
	#
	# 		temp_str = str('\t'.join(apply_to_list(final_text,make_string=True))).strip()+'\n'
	# 		write_into_file(file_name=output_file_name, contents=str(temp_str), mode='a')
	# 		write_into_file(file_name=RTRACK_LOG_FILE, contents=add_timestamp(str(temp_str)), mode='a')
	# print('Results are written in :',output_file_name)
	#
	end = time.time()

	print()
	print('Total Time taken in seconds : {:.1f}'.format(end - start))
	print('Total Time taken in Minutes : {:.2f}'.format((end - start) / 60))

	#
