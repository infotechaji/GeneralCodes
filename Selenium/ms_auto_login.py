from selenium import webdriver
import time
browser=webdriver.Chrome()
from bs4 import BeautifulSoup
#browser.get('https://myinspire.microsoft.com/page/attendeenetworking?p1=eyJzcGVha2VyIjpbXSwidGltZXNsb3QiOltdLCJkYXkiOltdLCJyb29tIjpbXSwicGFnZW51bWJlciI6MSwiY2F0ZWdvcmllcyI6e30sImtleXdvcmQiOiIifQ%3D%3D')
#raw_input()


def ms_login(url): 
	browser.get_element_by_class_name('ajirh kumare is ')
	browser.get(url)
	time.sleep(3)
	browser.find_element_by_link_text('Lo in to MyInspire').click()
	print "login clicked"
	#raw_input()
	time.sleep(3)
	browser.find_element_by_id('SignInWithLogonNameExchange').click()
	print "Username/Password Clicked" 
	browser.find_element_by_name('login').send_keys('faris@fiind.com')
	#time.sleep(1)
	browser.find_element_by_name('passwd').send_keys('Lailagail564!')
	#time.sleep(1)
	browser.find_element_by_id('cred_sign_in_button').click()
	time.sleep(2)
	print "Login succeed!!"
#ms_login('https://myinspire.microsoft.com/page/attendeenetworking?p1=eyJzcGVha2VyIjpbXSwidGltZXNsb3QiOltdLCJkYXkiOltdLCJyb29tIjpbXSwicGFnZW51bWJlciI6MSwiY2F0ZWdvcmllcyI6e30sImtleXdvcmQiOiIifQ%3D%3D')

'''def write_subject(subject): # function for writing contents
	browser.find_element_by_name( 'messagesubject' ).send_keys(subject) # for writing message
	
def write_message(message='some messages'): # function writes the message
	browser.find_element_by_name( 'messagebody' ).send_keys(message)

def click_send(): #  function to send the message
	#browser.find_element_by_id('attendeeCatalogSendMessageButton').click()
	pass

	
def click_cancel(): # function to click cancel
	browser.find_element_by_id('attendeeCatalogMessageCloseButton').click()
count=0
for i in browser.find_elements_by_class_name('details'):
	time.sleep(2)
	person_name=i.find_element_by_class_name('name').text # for getting person name
	try:
		i.find_element_by_link_text('Message').click() #  For clicking MESSAGE
		count+=1
		print count
		print "Message clicked for ",person_name
		time.sleep(1)
		write_subject('some subject')
		time.sleep(1)
		write_message('This is the message content')
		time.sleep(1)
		click_cancel()
	except Exception:
		print "Message button not found for ",person_name
	from selenium import webdriver
import time
browser=webdriver.Chrome()
from bs4 import BeautifulSoup
browser.get('https://myinspire.microsoft.com/page/attendeenetworking?p1=eyJzcGVha2VyIjpbXSwidGltZXNsb3QiOltdLCJkYXkiOltdLCJyb29tIjpbXSwicGFnZW51bWJlciI6MSwiY2F0ZWdvcmllcyI6eyJyZWdpc3RyYW50IHRpdGxldGhhdGRlc2NyaWJlc3lvdSI6WyI1MDdkMDc0YS01ZTI4LTRiY2EtYjNkYS1kYmIyMjIyNWQ5ZjAiXSwicmVnaXN0cmFudCBhcmVhIjpbImMwMGRhZjQzLWM5MTEtNDU1Mi04NGM1LThjNDQ1MzUzMGM4ZSJdfSwia2V5d29yZCI6IiJ9')
raw_input()

def write_subject(subject): # function for writing contents
	browser.find_element_by_name( 'messagesubject' ).send_keys(subject) # for writing message
	
def write_message(message='some messages'): # function writes the message
	browser.find_element_by_name( 'messagebody' ).send_keys(message)

def click_send(): #  function to send the message
	#browser.find_element_by_id('attendeeCatalogSendMessageButton').click()
	pass

	
def click_cancel(): # function to click cancel
	browser.find_element_by_id('attendeeCatalogMessageCloseButton').click()
count=0
'''
'''for i in browser.find_elements_by_class_name('details'):
	time.sleep(2)
	person_name=i.find_element_by_class_name('name').text # for getting person name
	try:
		i.find_element_by_link_text('Message').click() #  For clicking MESSAGE
		count+=1
		print count
		print "Message clicked for ",person_name
		time.sleep(1)
		write_subject('some subject')
		time.sleep(1)
		write_message('This is the message content')
		time.sleep(1)
		click_cancel()
	except Exception:
		print "Message button not found for ",person_name
	'''