# -*- coding: utf-8 -*-
"""
    Description: This python file have class to access BING search result
    Version    : v1.4
    History    :
                v0.1 - 07/11/2016 - Initial version. Modules are moved from CompanyWebsite to BingSearch.
                v1.0 - 07/22/2016 - Major Version
                v1.1 - 07/25/2016 - Adding search result order no as part of accuracy improvement meeting.
                v1.2 - 08/16/2016 - Removed str() from save_data_to_file as unicode conversion fails
                v1.3 - 09/01/2016 - updated _print_ function and added log_process_status variable
                v1.4 - 09/26/2016 - read from file. read once and keep it in dictionary
    Procedure to use: TBD
    Open Issues: None.
    Pending :    None.
"""
import urllib,urllib2
import json
import os
import time
from Utilities import *
class BingSearch():
    def __init__(self,BING_API_KEY,re_run_mode=False,exit_on_error=True,print_instance=None,developer_mode=False,log_process_status=True,split_search_file=False):
        self.BING_API_KEY=BING_API_KEY
        self.re_run_mode=re_run_mode
        self.re_run_mode_dictionary={}
        self.exit_on_error=exit_on_error
        self.developer_mode=developer_mode
        self.log_process_status=log_process_status
        self.search_results_file_name='bing_company_search_result'
        self.split_search_file=split_search_file
        self.initiate_print_instance(print_instance)
        self.idle_time_before_re_try=5
        if self.log_process_status:
            self._print_('__init__:\t' + ' Instance created with BING_API_KEY:' + BING_API_KEY + '\t developer_mode:' + str(self.developer_mode) + ' \t Log Process:' + str(self.log_process_status))
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='BingSearch'
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
    def initiate_print_instance(self,print_instance=None):
        self.print_instance=None
        if print_instance:
            try:
                if print_instance.check():
                    self.print_instance=print_instance
                    return True
            except:            
                return False        
        return False
    def file_name_suffix(self,input_string):
        temp_string=u''
        temp_string_1=input_string[0].lower()
        if temp_string_1 not in ['/','\\']:
            temp_string=temp_string + temp_string_1
        temp_string_1=input_string[1].lower()
        if temp_string_1 not in ['/','\\']:
            temp_string=temp_string + temp_string_1
        return temp_string
    def get_search_results(self,search_string,country_name=None,search_type='Web',no_of_result=15,azure_market_in='en-US',required_url='plain_url',try_iteration=0):
        '''
            This function will hit the azure market and fetch bing search result.
        '''
        print_prefix='get_search_results(' + str(try_iteration) + ')\t'
        if country_name:
            if country_name in ['USA','US','en-US','United States','United States of America']:
                azure_market='en-US'
            elif country_name in ['AUS','AU','Australia','AUSTRALIA','en-AU']:
                azure_market='en-AU'
            elif country_name in ['United Kingdom','UK','en-GB']:
                azure_market='en-GB'
            elif country_name in ['en-CA','Canada']:
                azure_market='en-CA'
            elif country_name in ['New Zealand','en-NZ']:
                azure_market='en-NZ'
            elif country_name in ['Finland','fi-FI']:
                azure_market='fi-FI'
            elif country_name in ['Brazil','pt-BR']:
                azure_market='pt-BR'
            elif country_name in ['Netherlands','nl-NL']:
                azure_market='nl-NL'
            elif country_name in ['Sweden','sv-SE']:
                azure_market='sv-SE'
            elif country_name in ['Norway','nb-NO']:
                azure_market='nb-NO'
            elif country_name in ['Denmark','da-DK']:
                azure_market='da-DK'
            else:
                self._print_(print_prefix + 'Country name not in list:' + country_name)
                azure_market='en-US'
        else:
            azure_market=azure_market_in
        if try_iteration >= 3: 
            if self.developer_mode:
                self._print_(print_prefix + 'Re-Try reached maximum limit(' +str(try_iteration) + ')')
            return consolidated_result
        if isinstance(search_string,list):
            if self.developer_mode:
                self._print_(print_prefix + ' Got a list for search. Code will search for each of the item in the list')
            consolidated_result=[]
            consumed_url_list=[]
            for each_item in search_string:
                if isinstance(each_item,str) or isinstance(each_item,unicode): 
                    pass
                else:
                    if self.developer_mode:
                        self._print_(print_prefix + 'item of list ' + str(each_item) + ' is of type' + str(type(each_item)))
                    continue
                temp_list=self.get_search_results(each_item,search_type=search_type,no_of_result=no_of_result,azure_market_in=azure_market)
                if temp_list:
                    for each_list_item in temp_list:
                        if each_list_item['Url'] not in consumed_url_list:
                            consolidated_result.append(each_list_item)
                            consumed_url_list.append(each_list_item['Url'])
            return consolidated_result
        search_string_modified=search_string
        if isinstance(search_string_modified,str):
            search_string_modified = urllib.quote(search_string_modified)
        elif isinstance(search_string_modified,unicode):
            search_string_modified = urllib.quote(search_string_modified.encode('utf8'))
        if self.re_run_mode:
            if self.log_process_status:
                self._print_(print_prefix + ' Rerun mode is enabled. Checking for the string in existing files')
            return self.get_data_from_file(search_string,search_string_modified)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
        auth = 'Basic %s' % (':%s' % self.BING_API_KEY).encode('base64')[:-1]
        url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+ search_type +'?Query=%27'+search_string_modified+'%27&$top=' + str(no_of_result) +'&$format=json&Market=%27' + azure_market + '%27'
        result_list=[]
        try:
            request = urllib2.Request(url)
            request.add_header('Authorization', auth)
            request.add_header('User-Agent', user_agent)
            request_opener = urllib2.build_opener()
            response = request_opener.open(request)
            response_data = response.read()
            json_result = json.loads(response_data)
            temp_result = json_result['d']['results']
            result_no=0
            for each_item in temp_result:
                if not ('Title' in each_item and 'Url' in each_item and 'DisplayUrl' in each_item): continue
                #self._print_(repr(each_item))
                result_no += 1
                temp_dict={}
                temp_dict['Url'] = each_item['Url']
                temp_dict['DisplayUrl'] = each_item['DisplayUrl']
                temp_dict['Description'] = each_item['Description']
                temp_dict['Title'] = each_item['Title']
                temp_dict['search_string'] = search_string
                temp_dict['order'] = result_no
                result_list.append(temp_dict.copy())
            if self.log_process_status:
                self._print_(print_prefix + 'No of records retrieved:' + str(len(result_list)) + ' from azure market:' + azure_market)
        except Exception as e:
            self._print_(print_prefix + 'Error :' + str(e))
            if 'http error 403' in str(e).lower():
                self._print_(print_prefix + 'BING_API_KEY:' + BING_API_KEY + ' is rejected',message_priority='FATAL')
                if self.exit_on_error: exit()
            elif 'errno 11001' in str(e).lower() and 'getaddrinfo failed' in str(e).lower():
                if try_iteration >= 2:
                    self._print_(print_prefix + 'Maximum re try limit exceeded for getaddrinfo failed',message_priority='FATAL')
                    if self.exit_on_error: exit()
                self._print_(print_prefix + 'Not able to connect over internet. Idle time to try again:' + str(self.idle_time_before_re_try),message_priority='ERROR')
                time.sleep(self.idle_time_before_re_try)
                return self.get_search_results(search_string=search_string,country_name=country_name,search_type=search_type,no_of_result=no_of_result,azure_market_in=azure_market_in,required_url=required_url,try_iteration=try_iteration+1)
        if result_list:
            self.save_data_to_file(search_string,result_list)
        if self.developer_mode:
            self._print_(print_prefix + ' Length of search result is:' + str(len(result_list)))
        return result_list

    def save_data_to_file(self,index_string,list_of_dictionary,column_order=['Title','Url','DisplayUrl','Description','search_string','order']):
        if not list_of_dictionary: return False
        if self.split_search_file:
            file_name=self.search_results_file_name + '_' + self.file_name_suffix(index_string) + '.txt'
        else:
            file_name=self.search_results_file_name + '.txt'
        w_f = open(file_name, 'ab')
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
    def get_data_from_file(self,index_string,search_string_modified=None,index_string_in_file=True,column_order=['Title','Url','DisplayUrl','Description','search_string','order']):
        print_prefix='get_data_from_file:\t'
        if isinstance(index_string,unicode):
            unicode_index_string=index_string
        else:
            unicode_index_string=get_html_to_unicode_string(index_string)
        if isinstance(search_string_modified,unicode):
            unicode_search_string_modified=search_string_modified
        else:
            unicode_search_string_modified=get_html_to_unicode_string(search_string_modified)
        if len(self.re_run_mode_dictionary)>0:
            self._print_(print_prefix + 'No of records in Master dictionary:' + str(len(self.re_run_mode_dictionary)))
            if unicode_search_string_modified in self.re_run_mode_dictionary:
                self._print_(print_prefix + 'reading the data from master dictionary')
                return self.re_run_mode_dictionary[unicode_search_string_modified]
            elif unicode_index_string in self.re_run_mode_dictionary:
                self._print_(print_prefix + 'reading the data from master dictionary')
                return self.re_run_mode_dictionary[unicode_index_string]
            return []
        #Use InputOutput Method
        self._print_(print_prefix + 'Data is not in master dictionary. proceeding to read file.')
        if not index_string or len(index_string) == 1: return False
        if not search_string_modified:
            search_string_modified = index_string
        if self.split_search_file:
            file_to_open=self.search_results_file_name + '_' + self.file_name_suffix(index_string) + '.txt'
        else:
            file_to_open=self.search_results_file_name + '.txt'
        #self._print_('READ:\tSTARTED\t:get_data_from_file')
        result_list=[]
        if not os.path.isfile(file_to_open): 
            self._print_('READ:\tFATAL\t:file does not exist:' + file_to_open)
            #self._print_('READ:\tCOMPLETED\t:get_data_from_file')
            return result_list
        r_f = open(file_to_open, 'rb')
        if index_string_in_file:
            adjust_column_order = 1
        else:
            adjust_column_order = 0
        self._print_(print_prefix + 'No of records in Master dictionary before insert:' + str(len(self.re_run_mode_dictionary)))
        record_count=0
        for each_line in r_f:
            record_count += 1
            each_line=each_line.strip()
            each_line=get_html_to_unicode_string(each_line)
            each_line_split=each_line.split('\t')
            temp_dict={}
            for i_iter in range(len(each_line_split)):
                if index_string_in_file and i_iter ==0: continue
                if (i_iter-adjust_column_order) < len(column_order):
                    #print column_order,i_iter,column_order[i_iter],':',column_order[i_iter-adjust_column_order],':',each_line_split[i_iter]
                    if column_order[i_iter-adjust_column_order] == 'order':
                        temp_dict[column_order[i_iter-adjust_column_order]]=int(each_line_split[i_iter])
                    else:
                        temp_dict[column_order[i_iter-adjust_column_order]]=each_line_split[i_iter]
            #print type(temp_dict['search_string']),type(unicode_index_string),type(unicode_search_string_modified)
            if temp_dict['search_string'] == unicode_index_string or temp_dict['search_string'] == unicode_search_string_modified:
                result_list.append(temp_dict.copy())
            if temp_dict['search_string'] not in self.re_run_mode_dictionary:
                self.re_run_mode_dictionary[temp_dict['search_string']]=[]
            self.re_run_mode_dictionary[temp_dict['search_string']].append(temp_dict.copy())
        #self._print_('READ:\tCOMPLETED\t:get_data_from_file')
        self._print_(print_prefix + 'No of records in the file:' + str(record_count))
        self._print_(print_prefix + 'No of records in Master dictionary after insert:' + str(len(self.re_run_mode_dictionary)))
        r_f.close()
        return result_list
if __name__ == '__main__':
    bs_ins=BingSearch('Am8yxHAp6Z56US6VLyXBPPn1g8w5CDgOvHRwgINyJE8',re_run_mode=True)
    bs_ins.get_search_results('ABC',country_name='India')
    for each_of in bs_ins.get_search_results([u'AXA'],no_of_result=10):##Fundação','fiind Inc','ICICI Bank
        print each_of