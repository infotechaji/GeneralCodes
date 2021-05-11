
# scrape-youtube-channel-videos-url.py
# _*_coding: utf-8_*_

import sys
import unittest
import time
import datetime
import urllib.request
import urllib.error
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException

# url = sys.argv[1]
# url = 'https://www.youtube.com/channel/UC-nIKQv07goKEwqxmY8sS3g' #5
url = 'https://www.youtube.com/channel/UCp9jJ4iVwdDC7pmff6Q8hRg'

channelid = url.split('/')[4]
print('channelid :', channelid)
# driver=webdriver.Firefox()
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
dt = datetime.datetime.now().strftime("%Y%m%d%H%M")
height = driver.execute_script("return document.documentElement.scrollHeight")
lastheight = 0

while True:
	if lastheight == height:
		break
	lastheight = height
	driver.execute_script("window.scrollTo(0, " + str(height) + ");")
	time.sleep(2)
	height = driver.execute_script("return document.documentElement.scrollHeight")

user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
for i in user_data:
    print(i.get_attribute('href'))
    link = (i.get_attribute('href'))
    f = open(channelid+'.txt','a')
    f.write(link + '\n')
f.close




# f = open(channelid+'-'+dt+'.list', 'a+')
    # f.write(link + '\n')
    
