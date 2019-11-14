from selenium import webdriver
from bs4 import BeautifulSoup

class ScrapeMe():
	def __init__(self,url='https://fiind.com/',use_selenium=True):
		self.use_selenium=use_selenium
		if self.use_selenium==True:
			self.browser=webdriver.Chrome()
			self.browser.get(url)
			
	def get_page_source(self):
		if self.use_selenium:
			page_content=self.browser.page_source
			return {'page_content':page_content,'page_content_length':len(page_content)}
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
			print 'Page source collected !',person_name
		except:print 'Page source collected !'
		self.write_into_file(file_name=full_file_name,content=temp_page_source,mode='w')
		self.browser.close()
		time.sleep(1)
		# Switch back to the first tab
		self.browser.switch_to.window(self.browser.window_handles[0])
	def soup_functions(self,page_source):
		"""
		This function handles the pagesource using Beautiful Soup
		"""
		soup = BeautifulSoup(page_source, "html.parser")
		
		# removing styles and script
		if not remove_tags : remove_tags=['script','style']
		for tag in remove_tags:
			for each_tag in soup.select(tag):
				each_tag.decompose()
		each_tag=soup.find("div",{"class":"attendee-detail__info"})
		each_tag=soup.find_all("div",{"class":"attendee-detail__info"})
		header=each_element.find('h5').text.strip()

if __name__=="__main__":
	sc_obj=ScrapeMe()
	print (str(sc_obj.get_page_source()['page_content'])).encode('utf-8')
	print (sc_obj.get_page_source()['page_content_length'])
	

