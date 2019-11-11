# -*- coding: utf-8 -*-
"""
    Description: This python file have functions and classes to handle company website related functionalities.
    Version    : v1.2
    History    :
                v1.0 - 08/08/2016 - Initial version
                v1.1 - 09/01/2016 - updated _print_ function and added log_process_status variable
                v1.2 - 09/22/2016 - variable to suppress output from PatternScraping
    Open Issues: None.
    Pending :    None.
                1. Pending: https://www.google.com/finance?cid=682495624520475 - Website is not fully visible
                2. Pending : Not fetching comp name for http://www.bloomberg.com/research/stocks/private/snapshot.asp?privcapId=275605035
                3. Yahoo: https://au.finance.yahoo.com/q?s=AXP.AX to https://au.finance.yahoo.com/q/pr?s=AXP.AX . Implement
"""


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import requests
import sys
from PatternScraping import *

class WebsitePick():
    def __init__(self,browser_instance=None,developer_mode=False,print_instance=None,log_process_status=True,write_output=True):
        self.developer_mode=developer_mode
        self.ins_browser=browser_instance
        self.initiate_print_instance(instance_instance=print_instance)
        self.write_output=write_output
        self.ins_pattern_scraping=PatternScraping(developer_mode=self.developer_mode,print_instance=self.print_instance,browser_instance=self.ins_browser,write_output=self.write_output)
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='WebsitePick'
        input_string=input_string_in
        if isinstance(input_string,str):
            input_string = get_html_to_unicode_string(input_string)
        if self.print_instance:
            self.print_instance.customPrint(input_string,skip_timestamp=skip_timestamp,add_leading_space=add_leading_space,module_name=module_name,message_priority=message_priority)
        else:
            print_string=u'' + module_name + '\t' + message_priority + '\t' + input_string
            if not skip_timestamp:
                print_string = log_time_stamp() + print_string
            print get_printable_string(print_string)
    def initiate_print_instance(self,instance_instance=None):
        self.print_instance=None
        if instance_instance:
            try:
                if instance_instance.check():
                    self.print_instance=instance_instance
                    return True
            except:            
                return False        
        return False
    def get_data(self,url_page):
        if not self.ins_pattern_scraping:
            self.ins_pattern_scraping=PatternScraping(developer_mode=self.developer_mode,print_instance=self.print_instance,browser_instance=self.ins_browser,write_output=self.write_output)
        input_commands=[]
        input_commands.append(['GO',url_page])
        input_commands.append(['SLEEP','2'])
        if 'www.google.com/finance' in url_page:
            input_commands.append(['GET_VALUE','XPATH','//*[@id="fs-chome"]','website_link'])
            input_commands.append(['GET_VALUE','XPATH','//*[@id="appbar"]/div/div[2]/div[1]/span','company_name'])
        elif 'bloomberg.com/quote/' in url_page:
            #Why didnt we check class="profile__detail__website_link"
            input_commands.append(['GET_VALUE','XPATH','//*[@id="content"]/div/div/div[19]/div[2]/div/div[3]/div[3]/a','website_link'])
            input_commands.append(['GET_VALUE','XPATH','//*[@id="content"]/div/div/div[1]/div/h1','company_name'])
        elif 'bloomberg.com/' in url_page and '/stocks/private' in url_page:
            #input_commands.append(['GET_VALUE','XPATH','//*[@id="detailsContainer"]/div[2]/div/p/a','website_link']) #This is also working.
            input_commands.append(['GET_VALUE','XPATH','//*[@id="columnLeft"]/div/div[2]/h1/span','company_name'])
            input_commands.append(['GET_LINKS','ID','detailsContainer','website_link'])
        elif 'bloomberg.com/' in url_page and '/profiles/companies/' in url_page:
            input_commands.append(['GET_VALUE','XPATH','/html/body/div[1]/div[1]/div[3]/div/div[2]/div[4]/div/div[5]/a','website_link'])
            input_commands.append(['GET_VALUE','XPATH','/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/h1','company_name'])
        else:
            return {}
        self.ins_pattern_scraping.feed_input(input_commands)
        self.ins_pattern_scraping.run()
        current_data=self.ins_pattern_scraping.get_data_dictionary()
        if 'website_link' in current_data:
            if isinstance(current_data['website_link'],list):
                current_data['website_link']=current_data['website_link'][0]
        return self.ins_pattern_scraping.get_data_dictionary()
    def close(self):
        if self.ins_pattern_scraping:
            if not self.ins_browser:
                self.ins_pattern_scraping.close()
            self.ins_pattern_scraping=None
if __name__ == '__main__':
    if not True:
        ins=WebsitePick()
        #print ins.get_data('http://www.bloomberg.com/profiles/companies/DCRN:US-diacrin-inc')
        #print ins.get_data('http://www.bloomberg.com/research/stocks/private/snapshot.asp?privcapId=91774')
        #print ins.get_data('http://www.bloomberg.com/Research/stocks/private/snapshot.asp?privcapId=34215182')
        #print ins.get_data('http://www.bloomberg.com/research/stocks/private/snapshot.asp?privcapId=126889641')
        print ins.get_data('http://www.bloomberg.com/research/stocks/private/snapshot.asp?privcapId=33173184')
        print ins.get_data('http://www.bloomberg.com/profiles/companies/NNW:AU-99-wuxian-ltd')
        print ins.get_data('http://www.bloomberg.com/profiles/companies/AEV:AU-avenira-ltd')
        print ins.get_data('http://www.bloomberg.com/profiles/companies/ATA:AU-atc-alloys-ltd')
        print ins.get_data('http://www.bloomberg.com/profiles/companies/AHX:AU-apiam-animal-health-ltd')
        ins.close()
    elif True:
        ins=WebsitePick()
        print ins.get_data('https://www.google.com/finance?cid=3047186')
    elif not True:
        input_filename = 'input.txt'
        output_filename = 'output.txt'
        obj = Selenium_test(False)
        obj.write_file('https://www.google.com/finance?cid=22144')
        obj.setUp(input_filename, output_filename)
        obj.run()