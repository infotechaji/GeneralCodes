# -*- coding: utf-8 -*-
"""
    Description: This python file have class to get company details from wikipedia page.
    Version    : v1.3
    History    :
                v1.0 - initial version 
                v1.1 - 08/16/2016 - Added fix to return data only from company pages
                v1.2 - 09/01/2016 - updated _print_ function
                v1.3 - 28/09/2016 - Added fixes for IndexErrors and for newlines in data
    Open Issues: None.
    Pending :    None.
"""


import urllib
import urllib2
import re
from bs4 import BeautifulSoup
from Utilities import *

class Wikipedia:
    ''' 
    Class to get the company's Wikipedia Page as input and returns a
    dictionary containing the company's details.
    '''
        
    def __init__(self,developer_mode=False,print_instance=None,log_process_status=True):
        self.developer_mode=developer_mode
        self.log_process_status=log_process_status
        self.initiate_print_instance(instance_instance=print_instance)

    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='Wikipedia'
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
    def set_url(self,page_url):
        self.wiki_url = page_url
        self.summary_list = []
        self.ticker_temp_list = []
        self.products_list = []
        self.services_list = []
        self.parent_list = []
        self.subsidiaries_list = []
        self.industry_list = []
        self.website_list = []
        self.type_list = []
        self.wiki_result_dict = {"company_name" : "",
                                "type" : "",
                                "industry" : "",
                                "website" : "",
                                "headquarters" : "",
                                "ticker_data" : "",
                                "traded_as" : "",
                                "employee_count" : "",
                                "products" : "",
                                "services" : "",
                                "parent_company" : "",
                                "subsidiaries_list" : "",
                                "revenue" : "",
                                "revenue_year" : "",
                                "operating_income" : "",
                                "operating_income_year" : "",
                                "net_income" : "",
                                "net_income_year" : "",
                                "total_assets" : "",
                                "total_equity" : "",
                                "slogan" : "",
                                "summary" : "",
                                "founded_year":""}
        
                
    def get_wiki_details(self,wiki_url):    
        self.set_url(wiki_url)
        soup = BeautifulSoup(urllib.urlopen(self.wiki_url).read())
        for h in soup.findAll("h1", {"class": "firstHeading"}):
            self.wiki_result_dict['company_name'] = h.text
        for table in soup.findAll("table", {"class": "infobox vcard"}):
            for tr in table.findAll('tr'):
                try:
                    if 'Type' in tr.text:
                        data_td = tr.findAll('td')[0]
                        for a in data_td.findAll('a'):
                            self.type_list.append(a.text)
                        if len(self.type_list) > 1: 
                            self.wiki_result_dict['type'] = self.type_list
                        else:
                            self.wiki_result_dict['type'] = tr.text.split('Type')[1]
                except IndexError:
                        next_tr = tr.find_next_sibling('tr')
                        data_td = next_tr.findAll('td')[0]
                        for a in data_td.findAll('a'):
                            self.type_list.append(a.text)
                        if len(self.type_list) == 1:
                            self.wiki_result_dict['type'] = next_tr.text.strip("\n ")
                        else:
                            self.wiki_result_dict['type'] = self.type_list
                if 'Industry' in tr.text:
                    data_td = tr.findAll('td')[0]
                    for a in data_td.findAll('a'):
                        self.industry_list.append(a.text)
                    if len(self.industry_list) == 1:
                        self.wiki_result_dict['industry'] = tr.text.split('Industry')[1]
                    else:
                        self.wiki_result_dict['industry'] = self.industry_list
                if 'Website' in tr.text:
                    try:
                        data_td = tr.findAll('td')[0]
                        for a in data_td.findAll('a'):
                            self.website_list.append(a['href'])
                        if len(self.website_list) == 1:
                            self.wiki_result_dict['website'] = self.website_list[0]
                        else:
                            self.wiki_result_dict['website'] = self.website_list
                    except IndexError:
                        next_tr = tr.find_next_sibling('tr')
                        data_td = next_tr.findAll('td')[0]
                        for a in data_td.findAll('a'):
                            self.website_list.append(a.text)
                        if len(self.website_list) == 1:
                            self.wiki_result_dict['website'] = next_tr.text.strip("\n ")
                        else:
                            self.wiki_result_dict['website'] = self.website_list
                if 'Headquarters' in tr.text:
                    self.wiki_result_dict['headquarters'] = tr.text.split('Headquarters')[1]
                if 'Traded' in tr.text:
                    tr1 = str(tr).replace('&#160;', ' ').replace('&amp;', '&')
                    data_td = BeautifulSoup(tr1).findAll('td')[0]
                    if '<ul>' in  str(data_td):
                        for li in data_td.findAll('li'):
                            self.ticker_temp_list.append(li.text)
                    else:
                        for a in data_td.findAll('a'):
                            self.ticker_temp_list.append(a.text)
                    temp_stock_list = []
                    if str(tr).count(':') > 1:
                        if self.ticker_temp_list and ':' in self.ticker_temp_list[0]:
                            temp_stock_dict = {}
                            temp_stock_dict['stock_exchange'] = self.ticker_temp_list[0].split(":")[0]
                            temp_stock_dict['stock_symbol'] = self.ticker_temp_list[0].split(":")[1]
                            temp_stock_list.append(temp_stock_dict.copy())
                        if len(self.ticker_temp_list) > 1 and ':' in self.ticker_temp_list[1]:
                            temp_stock_dict = {}
                            temp_stock_dict['stock_exchange'] = self.ticker_temp_list[1].split(":")[0]
                            temp_stock_dict['stock_symbol'] = self.ticker_temp_list[1].split(":")[1]
                            temp_stock_list.append(temp_stock_dict.copy())
                        elif len(self.ticker_temp_list) > 1:
                            temp_stock_dict = {}
                            temp_stock_dict['stock_exchange'] = self.ticker_temp_list[0]
                            temp_stock_dict['stock_symbol'] = self.ticker_temp_list[1]
                            temp_stock_list.append(temp_stock_dict.copy())
                        self.wiki_result_dict['ticker_data'] = temp_stock_list
                    elif ':' in self.ticker_temp_list[0]:
                        temp_stock_dict = {}
                        temp_stock_dict['stock_symbol'] = self.ticker_temp_list[0].split(":")[1]
                        temp_stock_dict['stock_exchange'] = self.ticker_temp_list[0].split(":")[0]
                        temp_stock_list.append(temp_stock_dict.copy())
                    elif ':' in str(tr):
                        temp_stock_dict = {}
                        temp_stock_dict['stock_symbol'] = self.ticker_temp_list[1]
                        temp_stock_dict['stock_exchange'] = self.ticker_temp_list[0]
                        temp_stock_list.append(temp_stock_dict.copy())
                    self.wiki_result_dict['ticker_data'] = temp_stock_list
                    self.wiki_result_dict['traded_as'] = self.ticker_temp_list                
                if 'Founded' in tr.text:
                    year = re.findall('\d\d\d\d', tr.text.split('Founded')[1])
                    if year:
                        self.wiki_result_dict['founded_year'] = year[0]
                    else:
                        self.wiki_result_dict['founded_year'] = ""
                if 'Number of employees' in tr.text:
                    self.wiki_result_dict['employee_count'] = tr.text.split('Number of employees')[1].split("(")[0].replace(",","")
                if 'Products' in tr.text:
                    data_td = tr.findAll('td')[0]
                    for a in data_td.findAll('a'):
                        if 'see ' not in a.text.lower() and 'more..' not in a.text and 'list ' not in a.text.lower() :
                            self.products_list.append(a.text)
                    self.wiki_result_dict['products'] = self.products_list
                if 'Services' in tr.text:
                    data_td = tr.findAll('td')
                    if data_td:
                        data_td1 = data_td[0]
                        for a in data_td1.findAll('a'):
                            self.services_list.append(a.text)
                    self.wiki_result_dict['services'] = self.services_list
                if 'Parent' in tr.text:
                    data_td = tr.findAll('td')[0]
                    for a in data_td.findAll('a'):
                        self.parent_list.append(a.text)
                    self.wiki_result_dict['parent_company'] = self.parent_list
                    if not self.parent_list:
                        self.wiki_result_dict['parent_company'] = tr.text.split('Parent')[1]
                if 'Subsidiaries' in tr.text:
                    data_td = tr.findAll('td')[0]
                    for a in data_td.findAll('a'):
                        if 'list ' not in a.text.lower() and '[' not in a.text:
                            self.subsidiaries_list.append(a.text)
                    self.wiki_result_dict['subsidiaries_list'] = self.subsidiaries_list
                if 'Revenue' in tr.text:
                    self.wiki_result_dict['revenue'] = tr.text.split('Revenue')[1].split(" (")[0]
                    if "(" in tr.text:
                        self.wiki_result_dict['revenue_year'] = tr.text.split("(")[1].split(")")[0]
                if 'Operating income' in tr.text:
                    self.wiki_result_dict['operating_income'] = tr.text.split('Operating income')[1].split(" (")[0]
                    if "(" in tr.text:
                        self.wiki_result_dict['operating_income_year'] = tr.text.split("(")[1].split(")")[0]
                if 'Net income' in tr.text:
                    self.wiki_result_dict['net_income'] = tr.text.split('Net income')[1].split(" (")[0]
                    if "(" in tr.text:
                        self.wiki_result_dict['net_income_year'] = tr.text.split("(")[1].split(")")[0]
                if 'Total assets' in tr.text:
                    self.wiki_result_dict['total_assets'] = tr.text.split('Total assets')[1].split(" (")[0]
                if 'Total equity' in tr.text:
                    self.wiki_result_dict['total_equity'] = tr.text.split('Total equity')[1].split(" (")[0]
                    
                if 'Slogan' in tr.text:
                    self.wiki_result_dict['slogan'] = tr.text.split('Slogan')[1]
        for div in soup.findAll("div", {"id": "mw-content-text"}):
            for elem in soup.findAll(['table']):
                elem.extract()
            for span in soup.findAll("span", {'class':'IPA nopopups'}):
                span.decompose()
            for p in div.findAll('p'):
                p = str(p).replace('<a', '#<a')
                p = str(p).replace('<b', '#<b')
                p = str(p).replace('/b>', '#/b>')
                p = str(p).replace('/a>', '#/a>')
                self.summary_list.append(BeautifulSoup(p).text)
        if self.summary_list:
            summary_text = get_printable_string(self.summary_list[0]).replace('<# /a>','').replace('<#/a>','').replace('<# /b>','').replace('<#/b>','').replace('#','')
            summary_text = re.sub('\[\d{1,2}]', '', summary_text)
            summary_text = re.sub(r'\.(?! |$)', '. ', summary_text)
            self.wiki_result_dict['summary'] = summary_text
              
        if isinstance(self.wiki_result_dict['type'],list):
            self.wiki_result_dict['type'] = ", ".join(self.wiki_result_dict['type']).strip("\n ")
        if isinstance(self.wiki_result_dict['industry'],list):
            self.wiki_result_dict['industry'] = ", ".join(self.wiki_result_dict['industry']).strip("\n ")
        if isinstance(self.wiki_result_dict['website'],list):
            self.wiki_result_dict['website'] = ", ".join(self.wiki_result_dict['website']).strip("\n ")
        if isinstance(self.wiki_result_dict['ticker_data'],list):
            temp_ticker_list = []
            for each in self.wiki_result_dict['ticker_data']:
                temp_str = each['stock_exchange'] + ":"+ each['stock_symbol']
                temp_ticker_list.append(temp_str)
            self.wiki_result_dict['ticker_data'] = ", ".join(temp_ticker_list).strip("\n ")
        if isinstance(self.wiki_result_dict['products'],list):
            self.wiki_result_dict['products'] = ", ".join(self.wiki_result_dict['products']).strip("\n ")
        if isinstance(self.wiki_result_dict['services'],list):
            self.wiki_result_dict['services'] = ", ".join(self.wiki_result_dict['services']).strip("\n ")
        if isinstance(self.wiki_result_dict['parent_company'],list):
            self.wiki_result_dict['parent_company'] = ", ".join(self.wiki_result_dict['parent_company']).strip("\n ")
        if isinstance(self.wiki_result_dict['subsidiaries_list'],list):
            self.wiki_result_dict['subsidiaries_list'] = ", ".join(self.wiki_result_dict['subsidiaries_list']).strip("\n ")
        if isinstance(self.wiki_result_dict['traded_as'],list):
            self.wiki_result_dict['traded_as'] = ", ".join(self.wiki_result_dict['traded_as']).strip("\n ")
            
        self.wiki_result_dict['type'] = self.wiki_result_dict['type'].strip()
        self.wiki_result_dict['industry'] = self.wiki_result_dict['industry'].strip()
        self.wiki_result_dict['website'] = self.wiki_result_dict['website'].strip()
        self.wiki_result_dict['headquarters'] = self.wiki_result_dict['headquarters'].strip().replace("\n",", ")
        self.wiki_result_dict['ticker_data'] = self.wiki_result_dict['ticker_data'].strip()
        self.wiki_result_dict['traded_as'] = self.wiki_result_dict['traded_as'].strip()
        self.wiki_result_dict['founded_year'] = self.wiki_result_dict['founded_year'].strip()
        self.wiki_result_dict['employee_count'] = self.wiki_result_dict['employee_count'].strip()
        self.wiki_result_dict['products'] = self.wiki_result_dict['products'].strip()
        self.wiki_result_dict['services'] = self.wiki_result_dict['services'].strip()
        self.wiki_result_dict['parent_company'] = self.wiki_result_dict['parent_company'].strip()
        self.wiki_result_dict['subsidiaries_list'] = self.wiki_result_dict['subsidiaries_list'].strip()
        self.wiki_result_dict['revenue'] = self.wiki_result_dict['revenue'].strip()
        self.wiki_result_dict['operating_income'] = self.wiki_result_dict['operating_income'].strip()
        self.wiki_result_dict['operating_income_year'] = self.wiki_result_dict['operating_income_year'].strip()
        self.wiki_result_dict['net_income'] = self.wiki_result_dict['net_income'].strip()
        self.wiki_result_dict['net_income_year'] = self.wiki_result_dict['net_income_year'].strip()
        self.wiki_result_dict['total_assets'] = self.wiki_result_dict['total_assets'].strip()
        self.wiki_result_dict['total_equity'] = self.wiki_result_dict['total_equity'].strip()
        self.wiki_result_dict['slogan'] = self.wiki_result_dict['slogan'].strip()
        self.wiki_result_dict['summary'] = self.wiki_result_dict['summary'].strip()
        # returns result only if either employee_count/trade_symbol/industry is found in page    
        if self.wiki_result_dict['employee_count'] or self.wiki_result_dict['traded_as'] or self.wiki_result_dict['industry']:
            return self.wiki_result_dict
        return {}

if __name__ == '__main__':
    wiki_obj = Wikipedia()
    # result_data = wiki_obj.get_wiki_details('https://en.wikipedia.org/wiki/intel')
    # result_data = wiki_obj.get_wiki_details('https://en.wikipedia.org/wiki/Culpepper_Island')
    result_data = wiki_obj.get_wiki_details('https://en.wikipedia.org/wiki/Eric_Schmidt')
    if 'company_name' in result_data and 'website' in result_data:
        print 'Both company_name(' + result_data['company_name'] + ') and website(' + result_data['website'] + ') are available'
    for each in result_data:
        print each," :"
        print result_data[each]
        print
