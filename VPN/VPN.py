"""
Description :	Script to auto connect VPN
Version     :	v1.0
History     :	
				v1.0 - 04/01/2019 - intial version
Open Issues :
Pending     :
				Options to disconnect ( which involves clicking alert button)
				Wifi Network detection
				Auto monitor/connect VPN 
				Status Intimation via popup incase of Connection/Disconnection through the code 

"""

from selenium import webdriver
from Credentials import *
import time
import sys,os
# sys.path.append(os.path.abspath('G:\\Ajith\\OtherFiles\\Encryption'))
from Cryptography import *

class Selenium():
	def __init__(self,source_url='',use_driver='IE',hit_home_page=True,developer_mode=False):
		self.source_url=source_url
		self.developer_mode=developer_mode
		if use_driver.lower()=='ie':
			self.browser = webdriver.Ie()
		elif use_driver.lower()=='chrome':
			self.browser = webdriver.Chrome()
		elif use_driver.lower()=='firefox':
			self.browser = webdriver.Chrome()
		else:
			self.browser = webdriver.Chrome()
		if hit_home_page==True :
			if len(self.source_url)>2:
				self.browser.get(self.source_url)
				self.browser.implicitly_wait(10)
				time.sleep(10)
				# self.browser.maximize_window()
				# print ('title:',self.browser.title)
				print ('Home page is hitted....',self.source_url)
			else:
				print('Please provide a valid input link')
				exit()
		
	def get_browser_control(self):
		"""
		This function returns the browser object.
		and the object can be accessed for getting page source 
		"""
		return self.browser
	def current_page_source(self):
		return self.browser.page_source

	def connect_vpn(self):
		"""
		Do the Login using username and passowordn(predefined)
		"""
		try_count=2
		loop_count=0
		while True:
			try:
				user_name=self.browser.find_element_by_name('uname')
				user_name.send_keys(USERNAME)
				break
			except Exception as e: 
				print ('Error while typing username :',e)
				loop_count+=1
				if loop_count>=try_count:break
				time.sleep(2)
			

		try:
			# pwd=Decrypt(PWD)
			# print ('pwd :',pwd)
			password=self.browser.find_element_by_name('pwd').send_keys(Decrypt(PWD))
		except Exception as e: print ('Error while typing password :',e)
		if developer_mode: print('Credentials entered')
		# # Click Sign In 
		try:
			sign_in=self.browser.find_element_by_name('submitbutton').click()
			# print ('sign in element :',sign_in)
			if developer_mode: print ('Sign in clicked!!')
			time.sleep(8)
			print ('Sleeping for 20 Seconds')
		except Exception as e:
			print ('Error while clicking Signin  :',e)
		
		return self.check_connection_status(change_connection='connect')
	def check_connection_status(self,change_connection='connect'):
		"""
		Function which clicks connect/disconnect the vpn button
		"""
		status='Not_traced'
		comments=''
		updated_status=''
		try:
			connect_element=self.browser.find_element_by_id('btnConnect')
			connect_txt=connect_element.get_attribute('value').strip('\r\n\t ')
			print ('connect_txt :',connect_txt)
			if connect_txt.lower()=='Disconnect'.lower():
				status='Connected'
			elif connect_txt.lower()=='Connect'.lower():
				status='Disconnected'
			if len(change_connection)>1:
				if connect_txt.lower()==change_connection.lower().strip():
					print ('Element is clicked ')
					connect_element.click()
					time.sleep(15)
					updated_status=self.check_connection_status(change_connection='')['previous_conn_status']
			print ('Connection status: ',status)
		except Exception as e:
			print ('Exception while checking status of the connection :',e)
			updated_status='Error'
			comments=str(e)
		return {'previous_conn_status':status,
				'current_conn_status':updated_status,
				'comments':comments}


		



if __name__=="__main__":
	# vpn_link='https://securevpn.ramco.com/'
	vpn_link='https://securevpn.ramco.com/prx/000/http/localhost/login'
	developer_mode=False
	ob=Selenium(source_url=vpn_link,developer_mode=developer_mode)
	if True: # for auto connecting VPN 
		ob.connect_vpn()
	if not True:
		limit=3
		try_count=0
		wait_time_mins=1
		while True:
			# ob.connect_vpn()
			bro=ob.get_browser_control()
			print ('Browser control :',bro)
			print ('Based on Browser control :',len(bro.page_source))
			#time.sleep(wait_time_mins*60)
			try_count+=1
			if try_count>=limit:break
			# test