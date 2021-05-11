import sys,os
sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')
from selenium import webdriver
from bs4 import BeautifulSoup
from Rtrack_config import *
from Help_print import *
from CustomisedFileOperation import *
from Datastructure_help import *
from CompareAndUpdate import *

import requests

# Search GitHub's repositories for requests
if __name__ == '__main__':
    # response = requests.get('https://advisor.morganstanley.com/the-lee-group')
    # print(response.text)
    # json_response = response.json()
    # print(json_response)
    # write_into_file(file_name='response_text.txt', contents=str(response.text), mode='w')
    # write_into_file(file_name='response_json.txt', contents=str(json_response), mode='w')
    url = 'https://advisor.morganstanley.com/the-lee-group'
    browser = webdriver.Chrome()
    browser.get(url)

