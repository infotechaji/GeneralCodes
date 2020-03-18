"""

"""
from selenium import webdriver
import time
import sys,os

class Youtube():
	def __init__(self,source_url='',use_driver='chrome',hit_home_page=True,developer_mode=False,time_mins=2):
		self.source_url=source_url
		self.developer_mode=developer_mode
		self.browser_opened=False
		self.use_driver=use_driver.lower()
		# self.open_browser()
		self.open_yt_link(source_url,time_mins)
	def open_yt_link(self,link,timing_mins):
		self.browser = webdriver.Chrome()
		self.browser.get(link)
		time.sleep(int(timing_mins*60))
		self.browser.close()

		

	# def open_browser(self):
	# 	if self.use_driver.lower()=='chrome':
	# 		try:
	# 			self.browser = webdriver.Chrome()
	# 			self.browser_opened=True
	# 			return True
	# 		except:
	# 			print('Please download the chrome driver from  "https://chromedriver.chromium.org/downloads"/  ')
	# 			return False



	# def open_youtube(self,link_dict,no_of_views,sleep_time_mins)
	# 	while True:
	# 		if self.browser_opened==True:
	# 			self.browser.get(link_dict['link'])
	# 			self.browser.implicitly_wait(5)
	# 			# time.sleep(int(float(link_dict['sleep_time']*60)))
	# def get_browser_control(self):
if __name__=="__main__":
	main_list=[
				{'https://www.youtube.com/watch?v=_EKvQBpfWKg':1},
				{'https://www.youtube.com/watch?v=zJcmFqspTMc':3}
			   ]
	for link_dict in main_list:
		for each_link in link_dict:	
			print ('processing link :',each_link)
			ob=Youtube(source_url=each_link,time_mins=link_dict[each_link],developer_mode=False)

	