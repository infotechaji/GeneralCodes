# -*- coding: utf-8 -*-
"""
    Module Name: DuckDuckGo selenium search.
    Discription: The module will fetch link,title and discription of the search results from DuckDuckGo.
    Version: 1.3
    History:
            v1.0 - 08/19/2016 - Initial Version
            v1.1 - 08/20/2016 - used html.parser instead of lxml as it thrown error. Need to check and fix.
            v1.2 - 09/01/2016 - updated _print_ function and added log_process_status variable
            v1.3 - 09/05/2016 - added logic to fetch page content using requests package
    Input Values: A 'search string' for which the search need to be carried out.
    Output Values: List of dictionaries, that contains the link,title and discription of the search results.
    Assumptions: phantomJS.exe is present in the current folder (if using phantomJS search engine).
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from pyparsing import htmlComment
#from unidecode import unidecode
import re
import os
import urllib
import requests
import datetime
from Utilities import *
from InputOutput import *
# used to write the result in the output file
#from HTMLParser import HTMLParser
#h = HTMLParser()

class DuckDuckGoSearch():
    def __init__(self,web_driver='Phantom',browser_instance=None,developer_mode=False,print_instance=None,limit_result=15,log_process_status=True,use_selenium=True):
        self.developer_mode=developer_mode
        self.company_url=''
        self.webpage_content=''
        self.search_string=''
        self.time_to_sleep_before_scrap=3
        self.use_selenium=use_selenium
        self.limit_result=limit_result
        self.web_driver=web_driver
        self.log_process_status=log_process_status
        self.ins_browser=browser_instance
        self.search_results_file_name='ddg_company_search_result'
        self.ddg_result=[]
        self.initiate_print_instance(instance_instance=print_instance)
        if self.log_process_status:
            self._print_('__init__:\t' + ' Instance created with web driver:' + web_driver + '\t developer_mode:' + str(self.developer_mode) + ' \t Log Process:' + str(self.log_process_status))
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='DuckDuckGoSearch'
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
    # method to extract web page content
    def extract_webpage_content(self,company_name):
        print_prefix='extract_webpage_content:\t'
        webpage_content=''
        if self.use_selenium:
            base_url="https://duckduckgo.com/?"
            if self.ins_browser:
                browser=self.ins_browser
            else:
                if self.web_driver == 'Chrome':
                    browser=webdriver.Chrome()
                elif self.web_driver == 'Phantom':
                    browser=webdriver.PhantomJS()
                elif self.web_driver == 'Firefox':
                    browser=webdriver.Firefox()
                else:
                    browser=web_driver.Chrome()
            # self.modified_company_name=company_name.replace(" ",'+')
            self.modified_company_name = urllib.urlencode({'q': str(company_name.encode('utf-8'))})
            base_url=base_url+self.modified_company_name
            if self.developer_mode: 
                self._print_(print_prefix + base_url)
            try:
                browser.get(base_url)
                time.sleep(self.time_to_sleep_before_scrap)
                html_element=browser.find_element_by_tag_name('html')
                webpage_content=html_element.get_attribute('outerHTML')
            except Exception as e:
                self._print_(print_prefix + 'Encountered error while processing. Error:' + str(e))
                if not self.ins_browser:
                    browser.quit()
            if not self.ins_browser:
                browser.quit()
        else:
            start_time=datetime.datetime.now()
            url = 'https://duckduckgo.com/html/'
            params = {
            'q': company_name,
            's': '0',
            }
            # html_directory=os.path.join(os.getcwd(),'html_files',get_filename_from_url(url+params['q']))
            html_directory=''
            if os.path.isfile(html_directory):
                print 'into this'
                webpage_content=open(html_directory).read()
            else:
                res = requests.post(url, data=params)
                webpage_content = res.text.encode('utf-8')
                # with open(html_directory,'a') as html_file:
                    # html_file.write(webpage_content)
            end_time=datetime.datetime.now()
            total_time=end_time-start_time
            timer_record=company_name+'\t'+str(start_time)+'\t'+str(end_time)+'\t'+str(total_time)+'\n'
            with open('html_timer.txt','a') as htmlt:
                htmlt.write(timer_record.encode('utf-8'))
        if webpage_content:
            return self.content_modification(webpage_content)

    # method to remove comments and newline
    def content_modification(self,webpage_content):
        for comment in htmlComment.searchString(webpage_content):
            for string in comment:
                webpage_content=webpage_content.replace(string,"")
        webpage_content=webpage_content.replace("\n",'')
        webpage_content=webpage_content.replace('_x000D_','')
        webpage_content=re.sub("( +)"," ",webpage_content)
        return webpage_content
   
    # method to remove unwanted tags
    def soup_modification(self,soup):
        unwanted_tags=['script','g-img','.rg_meta','image-viewer-group','kno-share-button','style']
        text_tags=[]
        for tag in unwanted_tags:
            for each_tag in soup.findAll(tag):
                each_tag.decompose()
        for tag in text_tags:
            for each_tag in soup.findAll(tag):
                each_tag.replaceWithChildren()
        return soup
    
    # method to get the url and the title
    def ddg_get_url(self,div_tag):
        h_tag=div_tag.h2
        if h_tag:
            a_tag=h_tag.a
            if a_tag:
                url=a_tag['href']
                return (url, a_tag.text)
        return ('','')
    # method to get the description           
    def get_url_description(self,div_tag):
        url_desc=''
        for result_snippet in div_tag.select('div[class="result__snippet"]'):
            url_desc=result_snippet.text
        return url_desc
        
    # method to get the attribute value 'data-domain'   
    def get_tag_parent_domain(self,div_tag):
        domain=''
        try:
            url_domain_name=div_tag.parent["data-domain"]
        except KeyError:
            return ''
        return url_domain_name
        
    # method to initiate data processing functions and store processed resuls   
    def ddg_url_with_highlights(self,soup):
        result_count=0
        for div_tag in soup.select('div[class="result_body"]'):
            result_dict={}
            url_text=self.ddg_get_url(div_tag)
            description=self.get_url_description(div_tag)
            domain=self.get_tag_parent_domain(div_tag)
            result_count+=1
            result_dict['search_string']=self.search_string    
            result_dict['Url']=url_text[0]
            result_dict['DisplayUrl']=url_text[0]
            result_dict['Title']=url_text[1]          
            result_dict['Description']=description           
            result_dict['Url_domain']=domain
            result_dict['order']=result_count
            self.ddg_result.append(result_dict.copy())
            if self.limit_result >0 and self.limit_result <= result_count:
                break
    # method to initiialize webpage extraction and data extraction              
    def ddg_results(self,company_results):
        print_prefix='ddg_result:\t'
        self.webpage_content=self.extract_webpage_content(company_results)
        webpage_content=self.webpage_content
        if not webpage_content: 
            if self.developer_mode:
                self._print_(print_prefix + 'No Webpage Content')
            return
        webpage_content=webpage_content.replace("<br>"," ")
        webpage_content=webpage_content.replace("<br/>"," ")
        if 'class="result__body links_main links_deep"' in webpage_content:
           webpage_content=webpage_content.replace('class="result__body links_main links_deep"','class="result_body"')
        elif 'class="links_main links_deep result__body"' in webpage_content:
           webpage_content=webpage_content.replace('class="links_main links_deep result__body"','class="result_body"')
        # webpage_content=webpage_content.replace('class="result__body links_main links_deep"','class="result_body"')
        # web_soup=BeautifulSoup(webpage_content,'html.parser')#"lxml")
        web_soup=BeautifulSoup(webpage_content,'lxml')#"lxml")
        soup=self.soup_modification(web_soup)
        self.ddg_url_with_highlights(soup)
        return self.ddg_result   
    
    # method to store the search string and initiate the search process    
    def get_ddg_scrap_list(self,company_name,limit_result=None):
        if limit_result:
            self.limit_result=limit_result
        self.ddg_result=[]
        self.search_string=company_name
        result_dict=self.ddg_results(company_name)
        if result_dict:
            self.save_data_to_file(self.search_string,result_dict)
        return result_dict
    def save_data_to_file(self,index_string,list_of_dictionary,column_order=['Title','Url','DisplayUrl','Description','search_string','order']):
        if not list_of_dictionary: return False
        l_index=0
        for each_dict in list_of_dictionary:
            each_dict['index_string']=index_string
            l_index += 1
        rw_ins=InputOutput('Write')
        rw_ins.open(self.search_results_file_name+'.txt')
        rw_ins.write(list_of_dictionary,column_structure=['index_string','Title','Url','DisplayUrl','Description','search_string','order'])
        rw_ins.close()
        return True
        #Delete the blow sectioin after check-in
        w_f = open(self.search_results_file_name+'.txt', 'ab')
        #self._print_('WRITE:\tSTARTED\t:save_data_to_file')
        for each_dict in list_of_dictionary:
            current_string=u'' + index_string 
            for each_column in column_order:
                if each_column in each_dict:
                    if each_column == 'order':
                        current_string = current_string + '\t' + str(each_dict[each_column])
                    else:
                        current_string = current_string + '\t' + each_dict[each_column]
                else:
                    current_string = current_string + '\t'
            current_string = current_string + '\n'
            current_string=current_string.encode('utf8')
            w_f.write(current_string)
            #self._print_('WRITE:\t' + current_string)
        w_f.close()
    def get_search_results(self,company_name,company_id=000000,limit_result=None):
        if limit_result:
            self.limit_result=limit_result
        return self.get_ddg_scrap_list(company_name)
    
if __name__ == '__main__':
    browser=webdriver.Chrome()
    search_handle=DuckDuckGoSearch(browser_instance=browser)
    enterprise_companies = [each_company.strip('\r\n\t ') for each_company in open('E:\\_data\\becloud\\glassdoorinput.txt')]
    for each in enterprise_companies:
        print 'Processing {}'.format(each)
        try:
            output=search_handle.get_ddg_scrap_list(each.split('\t')[0])
        except:
            print 'Error'
    # for each_record in output:
        # print repr(each_record)
    browser.close()