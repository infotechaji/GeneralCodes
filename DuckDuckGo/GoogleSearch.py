# -*- coding: utf-8 -*-
"""
    Description: This Testing python module have class to fetch result from Google search using Selenium tool.
    Version    : v1.1
    History    :
                v1.0 - 08/01/2016 - nitial version.
                v1.1 - 09/01/2016 - Maintain the order of the search result.
                                    updated _print_ function and added log_process_status variable
    Open Issues: None.
    Pending :    Unicode Handling.
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pyparsing import htmlComment
import unicodedata
#from unidecode import unidecode
import re
from Utilities import *
from InputOutput import *
class GoogleSearch():
    def __init__(self,web_driver='Phantom',browser_instance=None,developer_mode=False,print_instance=None,log_process_status=True):
        self.developer_mode=developer_mode
        self.ins_browser=browser_instance
        self.web_driver=web_driver
        self.log_process_status=log_process_status
        self.search_results_file_name='google_company_search_result'
        self.needed_text=['wikipedia','facebook','linkedin','twitter','instagram','pininterest','youtube','google+']
        self.company_url=''
        self.webpage_content=''
        self.result={
            'url_with_hightlight_words':{}
        }
        self.final_dict={
            'company_name':'',
            'site_block':'',
            'url':'',
            'highlighted_words':'',
            'desc':''
        }
        self.initiate_print_instance(instance_instance=print_instance)
        if self.log_process_status:
            self._print_('__init__:\t' + ' Instance created with web driver:' + web_driver + '\t developer_mode:' + str(self.developer_mode) + ' \t Log Process:' + str(self.log_process_status))
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='GoogleSearch'
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
        
    def extract_webpage_content(self,company_name):
        print_prefix='extract_webpage_content:\t'
        webpage_content=''
        base_url="https://www.google.co.in/#q="
        if not self.ins_browser:
            if self.web_driver == 'Chrome':
                browser=webdriver.Chrome()
            elif self.web_driver == 'Phantom':
                browser=webdriver.PhantomJS()
            elif self.web_driver == 'Firefox':
                browser=webdriver.Firefox()
            else:
                browser=web_driver.Chrome()
        else:
            browser=self.ins_browser
        self.modified_company_name=company_name.replace(" ",'+')
        base_url=base_url+self.modified_company_name
        if self.developer_mode: 
            self._print_(print_prefix + 'Base URL:' + base_url)
        try:
            browser.get(base_url)
            time.sleep(5)
            html_element=browser.find_element_by_tag_name('html')
            webpage_content=html_element.get_attribute('outerHTML')
            webpage_content=unicodedata.normalize('NFKD',webpage_content).encode('ascii','ignore')
            # webpage_content=webpage_content.encode("utf-8")
        except Exception as e:
            if self.log_process_status:
                self._print_(print_prefix + 'Page:' + base_url + '\tError while processing:' + str(e))
            if not self.ins_browser:
                browser.quit()
        if not self.ins_browser:
            browser.quit()
        if webpage_content:
            return self.content_modification(webpage_content)
           
    def content_modification(self,webpage_content):
        for comment in htmlComment.searchString(webpage_content):
            for string in comment:
                webpage_content=webpage_content.replace(string,"")
        webpage_content=webpage_content.replace("\n",'')
        webpage_content=webpage_content.replace('_x000D_','')
        # for i in range(0,5):
            # webpage_content=webpage_content.replace("  "," ")
            # if "  " not in webpage_content: break
        webpage_content=re.sub("( +)"," ",webpage_content)
        return webpage_content
        
    def soup_modification_rhs(self,soup):
        print_prefix='soup_modification_rhs:\t'
        self.company_url=''
        unwanted_tags=['script','g-img','.rg_meta','image-viewer-group','kno-share-button','g-bubble']
        text_tags=['span','a'] 
        # url_identity=['.com','.org','.net','.edu']
        for tag in unwanted_tags:
            for each_tag in soup.findAll(tag):
                each_tag.decompose()
        for tag in text_tags:
            for each_tag in soup.findAll(tag):
                if tag=='a':
                    tag_text=each_tag.text.lower().strip()
                    if tag_text in self.needed_text:
                        if "Subsidiar" not in each_tag.parent.text:  #To handle Subsidiaries: YouTube, Nik Software, AdMob, ITA Software, more
                            continue
                    if tag_text=='website':
                        if each_tag.has_attr('href'): self.company_url=each_tag['href']
                        if self.developer_mode: 
                            self._print_(print_prefix + 'company url=' + self.company_url)
                    elif " " not in tag_text and tag_text in each_tag['href'] and each_tag.find('svg'): #any(word in tag_text for word in url_identity):
                        self.company_url=each_tag['href']
                        if self.developer_mode: 
                            self._print_(print_prefix + 'company url=' + self.company_url)
                each_tag.replaceWithChildren()
        return soup
        
    
    def google_results(self,company_name):
        print_prefix='google_results:\t'
        attr_dict={}
        unwanted_list=['Hours','AM','PM']
        self.webpage_content=self.extract_webpage_content(company_name)
        webpage_content=self.webpage_content
        if not webpage_content: 
            if self.log_process_status:
                self._print_(print_prefix + 'Page:\t' + self.company_url + ' \tNo Webpage Content')
            return
        web_soup=BeautifulSoup(webpage_content,"html.parser")
        rhs_soup=web_soup.select("#rhs_block")
        if not rhs_soup:
            if self.log_process_status:
                self._print_(print_prefix + 'Page:\t' + self.company_url + ' \tNo RHS Block')
            return
        soup=self.soup_modification_rhs(rhs_soup[0])
        new_content=soup.encode('utf-8')
        new_soup=BeautifulSoup(new_content,"html.parser")
        if self.developer_mode:
            with open("html_content.txt",'w') as fopen:
                fopen.write(new_soup.prettify().encode('utf-8'))
        if self.company_url:
            attr_dict.setdefault('Website',self.company_url)
        for text in new_soup.stripped_strings:
            if self.developer_mode: 
                self._print_(print_prefix + 'Text=' + get_html_to_unicode_string(text))
            text_lower=text.lower()
            if text_lower=="see results about" and not attr_dict:
                attr_dict={}
                break
            if ":" in text and not any(word in text for word in unwanted_list):
                colon_index = text.index(":")
                key=text[:colon_index].strip()
                value=text[colon_index+1:].strip()
                attr_dict.setdefault(key,value)
            elif text_lower in self.needed_text:
                for a_tag in new_soup.select('a'):
                    a_tag_text=a_tag.text.lower().strip()
                    if a_tag_text==text_lower and a_tag.has_attr('href'):
                        attr_dict.setdefault(text_lower.title(),a_tag['href'])
            elif len(text)>120: attr_dict.setdefault('Description',text)
        return attr_dict
            
    #New Code Begins
    def soup_modification(self,soup):
        unwanted_tags=['script','g-img','.rg_meta','image-viewer-group','kno-share-button','style']
        text_tags=[]#'a','span'
        for tag in unwanted_tags:
            for each_tag in soup.findAll(tag):
                each_tag.decompose()
        for tag in text_tags:
            for each_tag in soup.findAll(tag):
                each_tag.replaceWithChildren()
        return soup
        
    def google_table_results(self,div_tag):
        print_prefix='google_table_results:\t'
        for table_tag in div_tag.select('table'):
            if table_tag.has_attr('class'):
                if table_tag['class'][0]=='nrgt':
                    if self.developer_mode: 
                        self._print_(print_prefix + get_html_to_unicode_string(str(table_tag)))
                    return "Yes"
        return "No"

        
    def get_matched_text(self,div_tag):
        desc=''
        for span_tag in div_tag.select('span[class="st"]'):
            desc=span_tag.text
        match_text=[]
        for em_tag in div_tag.select('em'):
            match_text.append(em_tag.text)
        return [desc,match_text]
        
    def get_url(self,div_tag):
        print_prefix='get_url:\t'
        h_tag=div_tag.h3
        if h_tag:
            a_tag=h_tag.a
            if a_tag:
                url=a_tag['href']
                if '/url?q=' in url:
                    url_split=url.split('/url?q=')
                    if len(url_split)>1:
                        url=url_split[1]
                if '&' in url:
                    url=url.split('&')[0]
                if self.developer_mode:
                    self._print_(print_prefix + ' URL identified:' + url)
                return (url, a_tag.text)
        
    def url_with_hightlights(self,soup):
        print_prefix=u'url_with_hightlights:\t'
        index = 0 
        for div_tag in soup.select('div[class="g"]'):
            url=''
            #matched_text=[]
            url_text=self.get_url(div_tag)
            if url_text:
                index += 1
                url, text = url_text[0], url_text[1]
                matched_text_with_desc=self.get_matched_text(div_tag)
                is_table_block=self.google_table_results(div_tag)
                if self.developer_mode: 
                    self._print_(print_prefix + url + '\t' + get_html_to_unicode_string(str(matched_text_with_desc)))
                self.result['url_with_hightlight_words'].setdefault(url,(matched_text_with_desc, text, is_table_block,index))
            
    
    def google_center_block_results(self,company_name):
        print_prefix=u'google_center_block_results:\t'
        if self.developer_mode: 
            self._print_(print_prefix + 'Company Name=' + get_html_to_unicode_string(company_name))
        self.result['url_with_hightlight_words']={}
        webpage_content=self.webpage_content
        if not webpage_content: return
        webpage_content=webpage_content.replace("<br>"," ")
        webpage_content=webpage_content.replace("<br/>"," ")
        web_soup=BeautifulSoup(webpage_content,"html.parser")
        soup=self.soup_modification(web_soup)
        self.url_with_hightlights(soup)
        return self.result
        
    def return_dict_list(self,company_name,result_dict):
        url_list=[]
        if result_dict['url_with_hightlight_words']:
            #result_no=0
            for key,value in result_dict['url_with_hightlight_words'].items():
                #result_no += 1
                self.final_dict=dict.fromkeys(self.final_dict,'')
                self.final_dict['search_string']=company_name
                self.final_dict['site_block']=value[2]
                self.final_dict['Url']=key
                self.final_dict['DisplayUrl']=key
                self.final_dict['Title']=value[1]
                self.final_dict['highlighted_words']=" , ".join(value[0][1])
                self.final_dict['Description']=value[0][0].strip()
                # self.final_dict['order'] = result_no
                self.final_dict['order'] = value[3]
                if self.final_dict not in url_list:
                    url_list.append(self.final_dict.copy())
        url_list = sorted(url_list, key=lambda k: k['order'])
        return url_list
    
    def print_list(self,url_list):
        print_prefix=u'print_list:\t'
        for result in url_list:
            if self.developer_mode:
                self._print_(print_prefix + '')
            for key,value in result.items():
                self._print_(print_prefix + str(key) + '\t' + get_html_to_unicode_string(value))
                
    def get_google_scrap_dict(self,company_name):
        google_scrap_dict={}
        result_dict= self.google_results(company_name)#RightSideBox
        if result_dict: 
            google_scrap_dict.setdefault("right_side_block",result_dict.copy())
        else:
            google_scrap_dict.setdefault("right_side_block",[])
        result_dict=self.google_center_block_results(company_name)#1 Page Result
        url_list=self.return_dict_list(company_name,result_dict)#check for sitemap and others
        if url_list: 
            google_scrap_dict.setdefault("search_result",url_list)
        else:
            google_scrap_dict.setdefault("search_result",[])
        return google_scrap_dict
    def get_search_results(self,company_name):
        current_result=self.get_google_scrap_dict(company_name)
        if 'search_result' in current_result:
            if current_result['search_result']:
                self.save_data_to_file(company_name,current_result['search_result'])
            return current_result['search_result']
        return []
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
if __name__=='__main__':
    company_name='Lowe\'s Companies'
    result_obj=GoogleSearch()
    google_scrap_dict=result_obj.get_google_scrap_dict(company_name)
    print "\n\n",google_scrap_dict
