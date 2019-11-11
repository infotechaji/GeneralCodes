# -*- coding: utf-8 -*-
"""
    Content Type: Company Website
    Description: This python file have functions and classes to handle company website related functionalities.
    Version    : v2.7
    History    :
                v1.0 - 07/08/2016 - Initial version
                v1.1 - 07/11/2016 - commented functions are removed.
                                  - Moved get_top_occurence from CompanyWebsite to Utilities
                                  - Removed unused function get_ticker_url_file from CompanyWebsite. It is a duplicate. Bingsearch works for the function.
                v2.0 - 08/08/2016 - The logic is re-written to identify a company website
                v2.1 - 08/19/2016 - DuckDuckGo and Google is integrated
                v2.2 - 08/23/2016 - Listing directory names from file(ListingDirectories.txt).
                v2.3 - 08/30/2016 - Three search instances method are unified i.e., same function name used. Add log_process_status.
                v2.4 - 08/31/2016 - Provision to consider/ignore financial website in the process.
                v2.5 - 09/01/2016 - Method quick_make_string to be enhanced and moved to Utilities.
                                    Added self.run_type_flag for usage of use_deeper_analysis flag.
                v2.6 - 09/26/2016 - Logic changed to assign weightage for each check abbreviation , title, domain, country
                v2.7 - 06/05/2017 - Check for ListingDirectories in current directory(for batch run) else in the common folder
    Procedure to use: TBD
    Open Issues: None.
    Pending :    Unicode to ascii name conversion for name in domain and title check
        http://symbolcodes.tlt.psu.edu/web/codehtml.html

        Const AccChars= "ŠŽšžŸÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïðñòóôõöùúûüýÿ"
        Const RegChars= "SZszYAAAAAACEEEEIIIIDNOOOOOUUUUYaaaaaaceeeeiiiidnooooouuuuyy"


        import sys 
        reload(sys) 
        sys.setdefaultencoding("utf-8")
        import csv
        import unicodedata

        def remove_accents(input_str):
            nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
            return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

        with open('test.txt') as f:
            read = csv.reader(f)
            for row in read:
                for element in row:
                    print remove_accents(element)
"""
import urllib
import urllib2
import json
#from fuzzywuzzy import fuzz
#from unidecode import unidecode
from BingSearch import *
from GoogleSearch import *
from DuckDuckGOSearch import *
# from get_new_urls import *
from Utilities import *
#from WebRedirect import *
from DomainSupport import *
from BeautifulSoup import BeautifulSoup
from WebsiteCodesSupport import *
from Bloomberg import * #get_data
from Wikipedia import * #get_wiki_details
from InputOutput import * #To write stats
#temp module to write long dictionary to file
def quick_make_string(first_item,*argv):
    temp_string=u''
    if isinstance(first_item,unicode):
        current_string=first_item
    elif isinstance(first_item,str):
        current_string=get_html_to_unicode_string(first_item)
    else:
        current_string=repr(first_item)
    temp_string=temp_string + current_string
    for each_item in argv:
        if isinstance(each_item,unicode):
            current_string=first_item
        elif isinstance(each_item,str):
            current_string=get_html_to_unicode_string(each_item)
        else:
            current_string=repr(each_item)
        temp_string=temp_string + current_string
    return temp_string
def write_delimited_file(file_name,list_of_dictionary,column_separator='\t'):
    fw=open(file_name,"ab")
    header_is=''
    list_of_keys=[]
    for each_dict in list_of_dictionary:
        for each_pair in each_dict:
            if each_pair not in list_of_keys:
                list_of_keys.append(each_pair)
    for column_name in list_of_keys:
        header_is=header_is + column_separator + str(column_name)
    fw.write(header_is.strip(column_separator) + "\n")
    for each_dict in list_of_dictionary:
        temp_string=u''
        first_word=True
        for value in list_of_keys:
            if isinstance(each_dict[value],str) or isinstance(each_dict[value],unicode):
                current_data=each_dict[value]
            else:
                current_data=str(each_dict[value])
            if not first_word:
                if value in each_dict:
                    if isinstance(current_data,unicode):
                        pass
                    else:
                        current_data=current_data.decode('utf-8')
                    temp_string=temp_string + column_separator + current_data
                else:
                    temp_string=temp_string + column_separator + u''
            else:
                if value in each_dict:
                    temp_string=current_data
                else:
                    temp_string=u''
                first_word=False
        fw.write(temp_string.encode('utf-8') + "\n")
    fw.close()
# from tld import get_tld
class CompanyWebsiteSearch():
    def __init__(self,re_run_mode=False,developer_mode=False,print_instance=None,use_deeper_analysis=True,search_method='DuckDuckGo',browser_instance=None,log_process_status=True,financial_domains_to_check=['bloomberg','google','wikipedia']):
        #self.domains_to_filtered_out=['bloomberg.com','hoovers.com','privco.com','wikipedia.org','google.com','yahoo.com','facebook.com','twitter.com','marketwatch.com','nasdaq.com','reuters.com','indiatimes.com','stockhouse.com','wsj.com','asx.com.au','londonstockexchange.com','seekingalpha.com','thestreet.com','dailyfinance.com','advfn.com','cnbc.com','fool.com','barrons.com','morningstar.com','investorroom.com','newsroom.com','nzx.com','whitepages.com','whitepages.com.au','asx.com.au']
        self.search_method=search_method
        self.developer_mode=developer_mode
        self.ins_browser=browser_instance
        self.log_process_status=log_process_status
        self.financial_domains_to_check=financial_domains_to_check
        self.initiate_print_instance(print_instance)
        if self.search_method == 'Bing':
            self.ins_search=BingSearch('Am8yxHAp6Z56US6VLyXBPPn1g8w5CDgOvHRwgINyJE8',re_run_mode=re_run_mode,developer_mode=self.developer_mode,log_process_status=self.log_process_status)
        elif self.search_method == 'DuckDuckGo':
            self.ins_search=DuckDuckGoSearch(browser_instance=self.ins_browser,developer_mode=self.developer_mode,log_process_status=self.log_process_status,use_selenium=True)
        elif self.search_method == 'Google':
            self.ins_search=GoogleSearch(browser_instance=self.ins_browser,developer_mode=self.developer_mode,log_process_status=self.log_process_status)
        self.url_parse_ins=WebURLParse('www.test.com')
        self.use_deeper_analysis=use_deeper_analysis
        if self.use_deeper_analysis:
            self.run_type_flag='D:' #without using deep analysis
        else:
            self.run_type_flag='N:' #without using deep analysis
        if self.developer_mode and (not self.use_deeper_analysis):
            self._print_('INFO:\tuse_deeper_analysis indicator is off')
        self.ins_wiki=Wikipedia() #get_wiki_details
        self.domains_to_filtered_out=[]
        ld_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'ListingDirectories.txt')
        if os.path.isfile(ld_dir):
            self.listing_directory_file_name=ld_dir
        else:
            self.listing_directory_file_name='..\\common\\ListingDirectories.txt'
        self.get_listing_directories()
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='CompanyWebsiteSearch'
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
    def get_listing_directories(self):
        write_ins=InputOutput('Read')
        write_ins.open(self.listing_directory_file_name)
        self.domains_to_filtered_out=write_ins.read(output_format='list')
        write_ins.close()
    def analyse_links(self):
        print_prefix='analyse_links\t'
        self.search_result_details=[]
        self.search_result_details[:]=[]
        self.indirect_website_indicator=False
        if not self.company_search_result: return []
        self.ins_websitepick=WebsitePick(browser_instance=self.ins_browser,developer_mode=self.developer_mode,log_process_status=self.log_process_status,write_output=False) #get_data
        self.domain_name_list=[]
        self.domain_name_list[:]=[]
        self.non_listing_domain_at=100
        consumed_urls=[]
        for search_result in self.company_search_result:
            if not ('Title' in search_result and 'Url' in search_result and 'DisplayUrl' in search_result and 'order' in search_result): 
                continue
            if search_result['Url'] in consumed_urls: continue
            consumed_urls.append(search_result['Url'])
            temp_dict={}
            temp_dict['Url']=search_result['Url']
            temp_dict['DisplayUrl']=search_result['DisplayUrl']
            temp_dict['Title']=search_result['Title']
            temp_dict['Order']=search_result['order']
            temp_dict['Description']=search_result['Description']
            temp_dict['company_name']=self.company_name
            self.url_parse_ins.set_url(search_result['Url'],title=temp_dict['Title'],description=temp_dict['Description'])
            domain_details_is=self.url_parse_ins.get_domain_details()
            temp_dict['country']=domain_details_is['country']
            temp_dict['has_ticker']=domain_details_is['has_ticker']
            temp_dict['ticker']=domain_details_is['ticker']
            temp_dict['ticker_country']=domain_details_is['ticker_country']
            temp_dict['ticker_exchange']=domain_details_is['ticker_exchange']
            temp_dict['ticker_source']=domain_details_is['ticker_source']
            temp_dict['suffix']=domain_details_is['suffix']
            temp_dict['domain_name']=domain_details_is['domain_name']
            temp_dict['domain_alone']=domain_details_is['domain_alone']
            temp_dict['abbreviation']=check_all_combination_abbreviation(self.company_name,temp_dict['domain_alone'],check_half_name_match=True)
            #The Miller Group(millergroup),The Travel Corp(ttc) with or without stopwords
            temp_dict['sub_domain']=domain_details_is['sub_domain']
            temp_dict['parent_domain']=temp_dict['domain_alone'].lower() + '.' + temp_dict['suffix']
            temp_dict['parent']=temp_dict['domain_alone'].lower()
            temp_dict['path']=domain_details_is['path']
            temp_dict['param']=domain_details_is['param']
            temp_dict['www']=domain_details_is['www_type']
            temp_dict['schema']=domain_details_is['schema']
            temp_dict['company_base_name']=get_company_name_without_common_words(temp_dict['company_name'])
            temp_dict['company_in_domain']=string_list_in_statement_sequential(temp_dict['domain_alone'],temp_dict['company_base_name'])
            temp_dict['company_in_title']=string_list_in_statement_sequential(temp_dict['Title'],temp_dict['company_base_name'])
            temp_dict['company_in_path']=string_list_in_statement_sequential(temp_dict['path'],temp_dict['company_base_name'])
            temp_dict['link_type']=get_html_link_type(link_url=temp_dict['Url'])
            temp_dict['indicative_website']=''
            if 'reuters.com' in temp_dict['parent_domain']:
                temp_dict['indicative_website']='reuters'
            elif 'bloomberg.com' in temp_dict['parent_domain']:
                temp_dict['indicative_website']='bloomberg'
            elif 'marketwatch.com' in temp_dict['parent_domain']:
                temp_dict['indicative_website']='marketwatch'
            elif 'finance.yahoo.com' in temp_dict['Url'].lower():
                temp_dict['indicative_website']='yahoo'
            elif 'google.com/finance' in temp_dict['Url'].lower():
                temp_dict['indicative_website']='google'
            elif 'nasdaq.com/symbol' in temp_dict['Url'].lower():
                temp_dict['indicative_website']='nasdaq'
            elif 'facebook.com' in temp_dict['parent_domain']:
                temp_dict['indicative_website']='facebook'
            elif 'twitter.com' in temp_dict['parent_domain']:
                temp_dict['indicative_website']='twitter'
            elif 'linkedin.com' in temp_dict['parent_domain']:
                temp_dict['indicative_website']='linkedin'
            elif 'wikipedia' in temp_dict['parent_domain']:
                temp_dict['indicative_website']='wikipedia'
            if temp_dict['parent'] in self.domains_to_filtered_out:
                temp_dict['listing_directory']=True
            else:
                temp_dict['listing_directory']=False
                if (temp_dict['Order']-1) < self.non_listing_domain_at:
                    self.non_listing_domain_at=temp_dict['Order']-1
                self.domain_name_list.append(temp_dict['parent_domain'])
            temp_dict['indirect_company_name']=''
            temp_dict['indirect_company_website']=''
            temp_dict['indirect_website_suffix']=''
            temp_dict['indirect_website_parent']=''
            temp_dict['indirect_website_country']=''
            if self.use_deeper_analysis and temp_dict['indicative_website'] in ['google','bloomberg'] and temp_dict['indicative_website'] in self.financial_domains_to_check:
                if self.log_process_status:
                    self._print_(print_prefix + 'Before opening ' + get_printable_string(temp_dict['Url']))
                temp_result=self.ins_websitepick.get_data(temp_dict['Url'])
                if self.log_process_status:
                    self._print_(print_prefix + 'Completed getting data from ' + get_printable_string(temp_dict['Url']))
                if self.developer_mode:
                    self._print_(print_prefix + 'Indicative Website:G/B' + str(temp_result))
                if temp_result:
                    if 'company_name' in temp_result and 'website_link' in temp_result:
                        temp_dict['indirect_company_name']=temp_result['company_name']
                        temp_dict['indirect_company_website']=temp_result['website_link']
                        self.indirect_website_indicator=True
            if self.use_deeper_analysis and temp_dict['indicative_website'] == 'wikipedia' and temp_dict['indicative_website'] in self.financial_domains_to_check:
                if self.log_process_status:
                    self._print_(print_prefix + 'Before opening ' + get_printable_string(temp_dict['Url']))
                try:
                    temp_result=self.ins_wiki.get_wiki_details(temp_dict['Url'])
                except:
                    temp_result={}
                if self.log_process_status:
                    self._print_(print_prefix + 'Completed getting data from ' + get_printable_string(temp_dict['Url']))
                if self.developer_mode:
                    self._print_(print_prefix + 'Indicative Website:W' + str(temp_result))
                # print temp_result
                # raw_input()
                # if 'company_name' in temp_result and 'website' in temp_result:
                if 'company_name' in temp_result and 'website' in temp_result and temp_result['company_name'] and temp_result['website'] in temp_result:
                        temp_dict['indirect_company_name']=temp_result['company_name']
                        temp_dict['indirect_company_website']=temp_result['website']
                        self.indirect_website_indicator=True
            if len(temp_dict['indirect_company_website']) > 4:
                self.url_parse_ins.set_url(temp_dict['indirect_company_website'],title='',description='')
                domain_details_is=self.url_parse_ins.get_domain_details()
                temp_dict['indirect_website_suffix']=domain_details_is['suffix']
                temp_dict['indirect_website_parent']=domain_details_is['domain_alone']
                temp_dict['indirect_website_country']=domain_details_is['country']
            if self.developer_mode:
                self._print_(print_prefix + 'Temp Dictionary:\t' + str(temp_dict))
            self.search_result_details.append(temp_dict.copy())
        top_domain_occurence_temp=get_top_occurrence(self.domain_name_list)
        self.top_domain_occurence=''
        self.top_domain_occurence_weightage=0
        self.domain_occurence_details=[]
        if top_domain_occurence_temp:
            if top_domain_occurence_temp[1]>1:#it is already taken care by get_top_occurence
                self.top_domain_occurence=top_domain_occurence_temp[0]
                self.top_domain_occurence_weightage=top_domain_occurence_temp[1]
                self.domain_occurence_details=top_domain_occurence_temp[2]
                self.top_domain_occurences_all=top_domain_occurence_temp[3]
        self.ins_websitepick.close()
        return True
    def get_company_website(self,company_name,company_id=000000,country_name='USA',record_identifier=None,additional_attributes={},ignore_record_on_different_country=False):
        #WHAT IF no country is provided. Just find the website case.
        #ADD weightage for top occurence
        #WHEN THERE IS NOT COUNTRY whom to give preference aia.com.au vs aia.com
        print_prefix='get_company_website\t'
        self.company_name=company_name
        self.company_id=company_id
        self.record_identifier=record_identifier
        record_identifier=None
        if self.log_process_status:
            self._print_(print_prefix + 'Got request to search for company :' + get_printable_string(self.company_name))
        #should consider all possibilities - Absolute Equity Performance Fund www.aepfund.com.au
        #The right method will be sending the company name and check the abbreviation is in the domain instead of finding the abbreviation and check the same in there
        self.company_name_abbr=abbreviate_name(company_name,upper_case_indicator=False)
        if self.log_process_status:
            self._print_(print_prefix + 'Before Getting search result for ' + get_printable_string(self.company_name))
        if self.search_method == 'Bing':
            self.company_search_result = self.ins_search.get_search_results(self.company_name,country_name=country_name)
        elif self.search_method == 'Google':
            self.company_search_result=[]
            self.company_search_result=self.ins_search.get_search_results(self.company_name)
            #google_temp=self.google_ins.get_search_results(self.company_name)
            #if 'search_result' in google_temp:
            #    self.company_search_result=google_temp['search_result']
        elif self.search_method == 'DuckDuckGo':
            self.company_search_result=self.ins_search.get_search_results(self.company_name)
        else:
            self.company_search_result=[]
        if self.log_process_status:
            self._print_(print_prefix + 'Completed search for ' + get_printable_string(self.company_name))
        if (not self.company_search_result) or len(self.company_search_result) == 0:
            write_string=u'' + self.run_type_flag +'\t' + country_name + '\t'
            if record_identifier:
                write_string + write_string + str(record_identifier) + '\t'
            write_string = write_string + str(self.record_identifier) + '\t' + self.company_name + '\t' + str(len(self.company_search_result)) + '\t' + 'No Search Result' + '\t' + 'NA'
            write_string = write_string + '\t' + '' + '\t' + '' + '\t' 
            if additional_attributes:
                for each_key in sorted(additional_attributes.keys()):
                    write_string = write_string + str(additional_attributes[each_key]) + '\t'
            write_string=write_string +'\t'+'\n'
            write_ins=InputOutput('Write')
            write_ins.open('CompanyWebsites.stat.txt')
            write_ins.write(write_string)
            write_ins.close()
            return False
        if self.developer_mode:
            for each_record in self.company_search_result:
                self._print_(print_prefix + repr(each_record['Url']) + '\t' + repr(each_record['order']) + '\t' + repr(each_record['DisplayUrl']) + '\t' + repr(each_record['Title']))
        self.analyse_links()
        if True:#self.developer_mode:
            write_delimited_file('temp.result.txt',self.search_result_details)
            with open('search_result_details.txt','w') as target:
                target.write(str(self.search_result_details))
            
        if self.developer_mode:
            self._print_(print_prefix + 'Top Domain Occurence(s):\t' + str(self.top_domain_occurences_all) + ' with occurence count=' + str(self.top_domain_occurence_weightage))
            self._print_(print_prefix + 'Top occurence details:\t' + str(self.domain_occurence_details))
            if self.non_listing_domain_at < len(self.company_search_result):
                self._print_(print_prefix + 'First non listing domain at ' + str(self.non_listing_domain_at)  + '\t' + str(self.company_search_result[self.non_listing_domain_at]))
            self._print_(print_prefix + 'indirect_website_indicator:\t' + str(self.indirect_website_indicator))
        indirect_websites={}
        country_mathes=False
        for each_record in self.search_result_details:
            if (not each_record['listing_directory']) and len(each_record['country']) > 2:
                if each_record['country'] == country_name:
                    country_mathes=True
            if self.indirect_website_indicator and len(each_record['indirect_company_website']) > 3:
                if each_record['indirect_website_parent'] not in indirect_websites:
                    indirect_websites[each_record['indirect_website_parent']]={'company_name':each_record['indirect_company_name'],'website':each_record['indirect_company_website'],'suffix':each_record['indirect_website_suffix'],'country':each_record['indirect_website_country'],'count':1}
                else:
                    indirect_websites[each_record['indirect_website_parent']]['count'] = indirect_websites[each_record['indirect_website_parent']]['count'] + 1
        additional_message=''
        domain_listed=''
        #Use temp_dict['link_type']
        print self.indirect_website_indicator,self.use_deeper_analysis
        # raw_input()
        if self.indirect_website_indicator and self.use_deeper_analysis: # there is link one of the financial website like Bloomberg, Google, Reuters, Yahoo.
            indirect_top_occurence=False
            for each_key in indirect_websites:
                for each_top_record in self.domain_occurence_details:
                    if each_key in each_top_record[0]:
                        indirect_top_occurence=True
                        break
                if indirect_top_occurence:
                    break
            website_domain_selected=''
            financial_site_multiple_suffix_yield=False#When there is a site with .com and .co.in
            if indirect_top_occurence:
                #There is a match between indirect website and top occurence domain
                #commented comment ## There is only one match. It can be the correct website. This is the common scenario.

                # Possible scenarios. 
                #    1. Two domain smell like the same company. #telstra telstraglobal
                #    2. More than one result from financial websites
                #    3. Same domain confirmed by multiple financial websites and appears in search result.
                if len(indirect_websites) > 1:
                    if self.developer_mode: self._print_(print_prefix + 'Financial websites produced more than one company website. A rare scenario yet to find and test.' + str(indirect_websites))
                    #Current logic consider any one from them
                current_selected_search_result=-1
                identification_method=''
                current_selected_country_matches=False
                previous_selected_country_matches=False
                current_selected_suffix_matches=False
                previous_selected_suffix_matches=False
                current_selected_sub_domain=False
                previous_selected_sub_domain=False
                for i_iter in range(len(self.search_result_details)):
                    if not self.search_result_details[i_iter]['listing_directory']:
                        for each_fin_website in indirect_websites:
                            identification_string=''
                            if each_fin_website == self.search_result_details[i_iter]['domain_alone']: 
                                #There can be multiple matches only when financial websites yield more than one result(may same domain or different)
                                #ALTO METALS LIMITED has http://enterpriseuranium.com.au/ (google) from altometals.com.au(B)
                                identification_string = identification_string + ':DOMAIN'
                                if indirect_websites[each_fin_website]['suffix'] == self.search_result_details[i_iter]['suffix']: #This plays a role when the website is not specific to country.
                                    current_selected_suffix_matches=True
                                    identification_string = identification_string + '-SFX-Y'
                                else:
                                    current_selected_suffix_matches=False
                                    identification_string = identification_string + '-SFX-N'
                                if len(indirect_websites[each_fin_website]['country'])>1 and indirect_websites[each_fin_website]['country'] == self.search_result_details[i_iter]['country']:
                                    current_selected_country_matches=True
                                    identification_string = identification_string + '-CNTR-Y'
                                else:
                                    current_selected_country_matches=False
                                    identification_string = identification_string + '-CNTR-N'
                                if current_selected_search_result == -1:
                                    current_selected_search_result = i_iter
                                    identification_method='FINSITE:' + 'FIRST:' + identification_string 
                                    #There is no previous selected record. Hence current record considered as sacred for next iteration
                                    previous_selected_suffix_matches=current_selected_suffix_matches
                                    previous_selected_country_matches=current_selected_country_matches
                                    if self.developer_mode:
                                        self._print_(print_prefix + 'Having Financial Website: Current record selected:' + str(self.search_result_details[current_selected_search_result]))
                                else:
                                    pass
                                    temp_selection_indicator=False
                                    #Logic to handle if a website is already selected.
                                    temp_string=':'
                                    if (not previous_selected_country_matches) and current_selected_country_matches:
                                        temp_selection_indicator=True
                                        temp_string=':LATEST CNTR-Y'
                                    if (not previous_selected_country_matches) and (not previous_selected_suffix_matches) and current_selected_suffix_matches:
                                        temp_selection_indicator=True
                                        temp_string=':LATEST SFX-Y'
                                    if temp_selection_indicator:
                                        #Allow only when current record is better than previous record.
                                        current_selected_search_result = i_iter
                                        identification_method='FINSITE:' + 'REPLACE:' + identification_string + temp_string
                                        previous_selected_suffix_matches=current_selected_suffix_matches
                                        previous_selected_country_matches=current_selected_country_matches
                                        if self.developer_mode:
                                            self._print_(print_prefix + 'Having Financial Website: Current record selected changed to:' + str(self.search_result_details[current_selected_search_result]))
                                break #If website from search result is matching with any of the financial yielded website then it is qualified to next level. So Break the financial website iteration.
                #A website record should have been based on current data. There should be more data validation not to select any website
                if current_selected_search_result == -1:
                    if self.developer_mode:
                        self._print_(print_prefix + ' Something went wrong to reach - No selection though top occurence and indicative_website are there')
                    additional_message=additional_message + 'Something went wrong to reach - No selection though top occurence and indicative_website are there'
                    #write_string=u'' + self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + 'None' + '\t' + 'Something went wrong to reach - No selection though top occurence and indicative_website are there'
                    #write_string = write_string + '\t' + '' + '\t' + '' + '\t' + '\n'
                    #write_ins=InputOutput('Write')
                    #write_ins.open('CompanyWebsites.stat.txt')
                    #write_ins.write(write_string)
                    #write_ins.close()
                    #custom_exit()
                    #Logic to handle all rejection case
                elif current_selected_search_result >= 0:
                    if self.developer_mode:
                        self._print_(print_prefix + 'Current record selected:' + str(self.search_result_details[current_selected_search_result]))
                    write_string=u'' + self.run_type_flag +'\t' + country_name + '\t'
                    if record_identifier:
                        write_string + write_string + str(record_identifier) + '\t'
                    write_string = write_string  + str(self.record_identifier) + '\t' +  self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + self.search_result_details[current_selected_search_result]['Url'] + '\t' + identification_method
                    write_string = write_string + '\t' + str(current_selected_search_result) + '\t' + '' + '\t'  
                    if additional_attributes:
                        for each_key in sorted(additional_attributes.keys()):
                            write_string = write_string + str(additional_attributes[each_key]) + '\t'
                    write_string=write_string + additional_message + '\t' + domain_listed.strip(',') + '\n'
                    write_ins=InputOutput('Write')
                    write_ins.open('CompanyWebsites.stat.txt')
                    write_ins.write(write_string)
                    write_ins.close()
                    return (self.search_result_details[current_selected_search_result]['Url'],current_selected_search_result,0,identification_method,'')
            else:
                #how come this scenario happens. The financial website yield the a website but not in the top occurence. To be checked.
                #Bloomber says http://www.acuvax.com.au/[Inactive] for ACTIVISTIC LIMITED. But the actual is 
                additional_message=additional_message + 'No top occurence matche when there is indirect website clue from financial websites'
                if self.developer_mode:
                    self._print_(print_prefix + 'No top occurence matche when there is indirect website clue from financial websites')
                #write_string=u'' + self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + 'None' + '\t' + 'No top occurence matche when there is indirect website clue from financial websites'
                #write_string = write_string + '\t' + '' + '\t' + '' + '\t' + '\n'
                #write_ins=InputOutput('Write')
                #write_ins.open('CompanyWebsites.stat.txt')
                #write_ins.write(write_string)
                #write_ins.close()
                #custom_exit()
        #STARTING NO FINSITE Website
        #country,parent_domain,sub_domain,suffix,company_in_title,company_in_path,abbreviation,company_in_domain
        selected_indexes=[]
        current_index=-1
        current_weightage=0
        country_match_found=False
        identification_method=''
        for i_iter in range(len(self.search_result_details)):
            if (not self.search_result_details[i_iter]['listing_directory']) and (not self.search_result_details[i_iter]['indicative_website']):
                identification_string=''
                record_order_no=self.search_result_details[i_iter]['Order']
                if record_order_no > 5: continue#Dont consider the second half and higher
                if self.developer_mode:
                    self._print_(print_prefix + 'No Financial Path: Processing record:' + str(self.search_result_details[i_iter]['Order']) + ' having url:' + self.search_result_details[i_iter]['Url'])
                current_comp_base_name=self.search_result_details[i_iter]['company_base_name']
                current_country=self.search_result_details[i_iter]['country']
                current_parent_domain=self.search_result_details[i_iter]['domain_alone']
                if current_parent_domain not in domain_listed:
                    domain_listed = domain_listed + ',' + current_parent_domain
                current_sub_domain=self.search_result_details[i_iter]['sub_domain']
                current_suffix=self.search_result_details[i_iter]['suffix']
                current_comp_in_title=' '.join(self.search_result_details[i_iter]['company_in_title'])
                current_comp_in_path=' '.join(self.search_result_details[i_iter]['company_in_path'])
                current_comp_in_domain=' '.join(self.search_result_details[i_iter]['company_in_domain'])
                current_abbreviation=self.search_result_details[i_iter]['abbreviation']
                if self.developer_mode:
                    temp_string=str(i_iter) + '\t' + current_comp_base_name + '\t' + current_country + '\t' + current_parent_domain + '\t' + current_sub_domain + '\t' + current_suffix
                    temp_string = quick_make_string(temp_string) + quick_make_string('\t',current_comp_in_domain ,'\t' , current_comp_in_path, '\t' , current_comp_in_title , '\t' , current_abbreviation)
                    #temp_string=temp_string + '\t' + str(current_comp_in_domain) + '\t' + str(current_comp_in_path) + '\t' + str(current_comp_in_title) + '\t' + str(current_abbreviation)
                    self._print_(print_prefix + 'No Financial Website: current_record:\t' + temp_string)
                #CA - (10,0,2), ND(Name = domain)[country +-](8,0,7) , NID(NameInDomain)[country +-](4,0,3),NIDT (NameInDomainAndTitle)[country +-](6,0,5),?
                temp_weightage=0
                if current_abbreviation:# full match vs partial match..check for title as well
                    temp_weightage = temp_weightage + 4
                    identification_string=identification_string + ':ABBR(' + str(4) + ')'
                    if self.developer_mode:
                        self._print_(print_prefix + 'No Financial Website: Added weightage 4 for abbreviation match. current weightage:' + str(temp_weightage))
                if current_parent_domain == current_comp_in_domain: #full match vs partial match
                    #THING ON current_comp_in_domain != current_comp_base_name ABERDEEN LEADERS LIMITED(aberdeen) aberdeenasset(parent)
                    #domain matches with company base name
                    temp_weightage = temp_weightage + 2.5
                    identification_string=identification_string + ':EXACTDOMAIN(' + str(2.5) + ')'
                    if self.developer_mode:
                        self._print_(print_prefix + 'No Financial Website: Added weightage 2.5 for domain name exactly matches with company name in domain. current weightage:' + str(temp_weightage))
                    if len(current_comp_in_title)>1 and current_comp_in_title.startswith(current_comp_in_domain):
                        temp_weightage = temp_weightage + 1
                        identification_string=identification_string + ':TITLE(' + str(1) + ')'
                        if self.developer_mode:
                            self._print_(print_prefix + 'No Financial Website: Added weightage 1 for having company name in title. current weightage:' + str(temp_weightage))
                elif len(current_comp_in_domain)>1 and len(current_comp_in_title)>1 and current_comp_in_title.startswith(current_comp_in_domain): #WHAT if one part is in domain and full part is in title
                    #Scenario - ABERDEEN LEADERS LIMITED(aberdeen) aberdeenasset(parent)
                    temp_weightage = temp_weightage + 2.5
                    identification_string=identification_string + ':DOMAINTITLE(' + str(2.5) + ')'
                    #domain has company base name #Do we need to check for length
                    if self.developer_mode:
                        self._print_(print_prefix + 'No Financial Website: Added weightage 2.5 for domain having company name and title has company name. current weightage:' + str(temp_weightage))
                #perform only when any one of the leading clue is set - abbreviation, domain
                if temp_weightage > 0:
                    if len(current_country) > 1 and current_country == country_name:
                        temp_weightage = temp_weightage + 2
                        identification_string=identification_string + '-CNTR-Y(' + str(2) + ')'
                        if self.developer_mode:
                            self._print_(print_prefix + 'No Financial Website: Added weightage 2 for country match. current weightage:' + str(temp_weightage))
                    elif len(current_country) > 1:
                        if ignore_record_on_different_country:
                            if self.developer_mode:
                                self._print_(print_prefix + 'No Financial Website: ignore_record_on_different_country is set and ignoring the record for having country(' + current_country + ') while looking for country:' + country_name)
                            continue
                        else:
                            temp_weightage = temp_weightage - 2
                            identification_string=identification_string + '-CNTR-N(' + str(-2) + ')'
                            if self.developer_mode:
                                self._print_(print_prefix + 'No Financial Website: Reduced weightage 2 for having different country(' + current_country + '). current weightage:' + str(temp_weightage))
                        #Do Nothing- May be this logic need to be changed . Case when we check for australia and the parent website is in UK.
                    else:
                        identification_string=identification_string + '-CNTR-NA(' + str(0) + ')'

                    if len(current_sub_domain) == 0:
                        temp_weightage = temp_weightage + 0.5
                        identification_string=identification_string + ':SUBDOMAIN-N(' + str(0.5) + ')'
                        if self.developer_mode:
                            self._print_(print_prefix + 'No Financial Website: Added weightage 0.5 for not having sub domain. current weightage:' + str(temp_weightage))
                    if len(current_comp_in_path) > 0:
                        temp_weightage = temp_weightage - 0.5 #Reduce the weightage if company is appear in the url other than domain
                        identification_string=identification_string + ':INPATH-Y(' + str(-0.5) + ')'
                        if self.developer_mode:
                            self._print_(print_prefix + 'No Financial Website: Reduced weightage 0.5 for having company name url path. current weightage:' + str(temp_weightage))
                    #if self.top_domain_occurence_weightage > 0  and self.top_domain_occurence == current_parent_domain + '.' + current_suffix: #i.e domain is a top occurence domain
                    if self.top_domain_occurence_weightage > 0  and current_parent_domain + '.' + current_suffix in self.top_domain_occurences_all: #i.e domain is a top occurence domain
                        #if we have multiple top domains? [u'leagle.com', 2], [u'justia.com', 2], [u'stewart.com', 2]
                        incremental_weight_factor=1 + round((self.top_domain_occurence_weightage)/(1.0 * len(self.search_result_details)),2) #Maximum weight 3 is added when all links have same domain
                        identification_string=identification_string + ':TOPOCCUR(*' + str(incremental_weight_factor) + ')'
                        temp_weightage = temp_weightage * incremental_weight_factor
                        if self.developer_mode:
                            self._print_(print_prefix + 'No Financial Website: Multiple by ' + str(incremental_weight_factor) + ' for top occurence weightage.current weightage:' + str(temp_weightage))

                    #This line is to give more weightage when the result appears in the top
                    #This logic can be changed. If we want to consider the first result(based on other condition) always
                    order_weightage_to_reduce=round((record_order_no * (1/6.0)),2)
                    temp_weightage = temp_weightage - order_weightage_to_reduce
                    identification_string=identification_string + ':ORDER(' + str(-1*order_weightage_to_reduce) + ')'
                    if self.developer_mode:
                        self._print_(print_prefix + 'No Financial Website: Reduced weightage ' + str(order_weightage_to_reduce) + ' based on the record place in search result. current weightage:' + str(temp_weightage))
                if temp_weightage > 0:#do we get -ve weightage for valid companies?
                    selected_indexes.append((i_iter,temp_weightage,record_order_no,identification_string,self.search_result_details[i_iter]['Url']))
                    if temp_weightage > current_weightage:
                        if self.developer_mode:
                            self._print_(print_prefix + 'No Financial Website: Index ' + str(i_iter) + ' is selected over ' + str(current_index) + ' since current weightage (' + str(temp_weightage) + ') is greater than previous(' + str(current_weightage) + ').' )
                        current_index=i_iter
                        current_weightage=temp_weightage
                        identification_method=identification_string
                #name in domain and not in path 
                #company name occurence in listed company -- additional confident--how
            elif self.developer_mode:
                self._print_(print_prefix + 'Current record ignored:' + self.search_result_details[i_iter]['Url'] + '\t because listing_directory=' + str(self.search_result_details[i_iter]['listing_directory']) + '\t indicative_website:' + str(self.search_result_details[i_iter]['indicative_website']))
        if current_index > -1:
            if self.developer_mode:
                self._print_(print_prefix + 'Selected Index:' + str(current_index) + ' Collected Indexes:\t' + str(selected_indexes))
            write_string=u''  + self.run_type_flag +'\t' + country_name + '\t'
            if record_identifier:
                write_string + write_string + str(record_identifier) + '\t'
            write_string = write_string  + str(self.record_identifier) + '\t' +  self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + self.search_result_details[current_index]['Url'] + '\t' + identification_method
            write_string = write_string + '\t' + str(current_index) + '\t' + str(current_weightage) + '\t' + str(selected_indexes)   
            if additional_attributes:
                for each_key in sorted(additional_attributes.keys()):
                    write_string = write_string + str(additional_attributes[each_key]) + '\t'
            write_string=write_string + additional_message + '\t' + domain_listed.strip(',') + '\n'
            write_ins=InputOutput('Write')
            write_ins.open('CompanyWebsites.stat.txt')
            write_ins.write(write_string)
            write_ins.close()
            return (self.search_result_details[current_index]['Url'],current_index,current_weightage,identification_method,'')
        elif self.developer_mode:
            self._print_(print_prefix + 'Not able to decide the website.')
        write_string=u''  + self.run_type_flag +'\t' + country_name + '\t'
        if record_identifier:
            write_string + write_string + str(record_identifier) + '\t'
        write_string = write_string  + str(self.record_identifier) + '\t' +  self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + 'None' + '\t' + 'NA'
        write_string = write_string + '\t' + '' + '\t' + '' + '\t'   
        if additional_attributes:
            for each_key in sorted(additional_attributes.keys()):
                write_string = write_string + str(additional_attributes[each_key]) + '\t'
        write_string=write_string + additional_message + '\t' + domain_listed.strip(',') + '\n'
        write_ins=InputOutput('Write')
        write_ins.open('CompanyWebsites.stat.txt')
        write_ins.write(write_string)
        write_ins.close()
        return False
        
    # def get_company_website_old(self,company_name,country_name='USA',record_identifier=None,additional_attributes={}):
        # #WHAT IF no country is provided. Just find the website case.
        # #ADD weightage for top occurence
        # #WHEN THERE IS NOT COUNTRY whom to give preference aia.com.au vs aia.com
        # print_prefix='get_company_website\t'
        # self.company_name=company_name
        # if self.log_process_status:
            # self._print_(print_prefix + 'Got request to search for company :' + get_printable_string(self.company_name))
        # #should consider all possibilities - Absolute Equity Performance Fund www.aepfund.com.au
        # #The right method will be sending the company name and check the abbreviation is in the domain instead of finding the abbreviation and check the same in there
        # self.company_name_abbr=abbreviate_name(company_name,upper_case_indicator=False)
        # if self.log_process_status:
            # self._print_(print_prefix + 'Before Getting search result for ' + get_printable_string(self.company_name))
        # if self.search_method == 'Bing':
            # self.company_search_result = self.ins_search.get_search_results(self.company_name,country_name=country_name)
        # elif self.search_method == 'Google':
            # self.company_search_result=[]
            # self.company_search_result=self.ins_search.get_search_results(self.company_name)
            # #google_temp=self.google_ins.get_search_results(self.company_name)
            # #if 'search_result' in google_temp:
            # #    self.company_search_result=google_temp['search_result']
        # elif self.search_method == 'DuckDuckGo':
            # self.company_search_result=self.ins_search.get_search_results(self.company_name)
        # else:
            # self.company_search_result=[]
        # if self.log_process_status:
            # self._print_(print_prefix + 'Completed search for ' + get_printable_string(self.company_name))
        # if (not self.company_search_result) or len(self.company_search_result) == 0:
            # write_string=u'' + self.run_type_flag +'\t' + country_name + '\t'
            # if record_identifier:
                # write_string + write_string + str(record_identifier)
            # write_string = write_string  + str(self.record_identifier) + '\t' +  self.company_name + '\t' + str(len(self.company_search_result)) + '\t' + 'No Search Result' + '\t' + 'NA'
            # write_string = write_string + '\t' + '' + '\t' + '' + '\t' 
            # if additional_attributes:
                # for each_key in sorted(additional_attributes.keys()):
                    # write_string = write_string + str(additional_attributes[each_key]) + '\t'
            # write_string=write_string + '\n'
            # write_ins=InputOutput('Write')
            # write_ins.open('CompanyWebsites.stat.txt')
            # write_ins.write(write_string)
            # write_ins.close()
            # return False
        # if self.developer_mode:
            # for each_record in self.company_search_result:
                # self._print_(print_prefix + repr(each_record['Url']) + '\t' + repr(each_record['order']) + '\t' + repr(each_record['DisplayUrl']) + '\t' + repr(each_record['Title']))
        # self.analyse_links()
        # if self.developer_mode:
            # write_delimited_file('temp.result.txt',self.search_result_details)
        # if self.developer_mode:
            # self._print_(print_prefix + 'Top Domain Occurence:\t' + str(self.top_domain_occurence))
            # self._print_(print_prefix + 'Top occurence details:\t' + str(self.domain_occurence_details))
            # if self.non_listing_domain_at < len(self.company_search_result):
                # self._print_(print_prefix + 'First non listing domain at ' + str(self.non_listing_domain_at)  + '\t' + str(self.company_search_result[self.non_listing_domain_at]))
            # self._print_(print_prefix + 'indirect_website_indicator:\t' + str(self.indirect_website_indicator))
        # indirect_websites={}
        # country_mathes=False
        # for each_record in self.search_result_details:
            # if (not each_record['listing_directory']) and len(each_record['country']) > 2:
                # if each_record['country'] == country_name:
                    # country_mathes=True
            # if self.indirect_website_indicator and len(each_record['indirect_company_website']) > 3:
                # if each_record['indirect_website_parent'] not in indirect_websites:
                    # indirect_websites[each_record['indirect_website_parent']]={'company_name':each_record['indirect_company_name'],'website':each_record['indirect_company_website'],'suffix':each_record['indirect_website_suffix'],'country':each_record['indirect_website_country'],'count':1}
                # else:
                    # indirect_websites[each_record['indirect_website_parent']]['count'] = indirect_websites[each_record['indirect_website_parent']]['count'] + 1
        # additional_message=''
        # domain_listed=''
        # #Use temp_dict['link_type']
        # if self.indirect_website_indicator and self.use_deeper_analysis: # there is link one of the financial website like Bloomberg, Google, Reuters, Yahoo.
            # indirect_top_occurence=False
            # for each_key in indirect_websites:
                # for each_top_record in self.domain_occurence_details:
                    # if each_key in each_top_record[0]:
                        # indirect_top_occurence=True
                        # break
                # if indirect_top_occurence:
                    # break
            # website_domain_selected=''
            # financial_site_multiple_suffix_yield=False#When there is a site with .com and .co.in
            # if indirect_top_occurence:
                # #There is a match between indirect website and top occurence domain
                # #commented comment ## There is only one match. It can be the correct website. This is the common scenario.

                # # Possible scenarios. 
                # #    1. Two domain smell like the same company. #telstra telstraglobal
                # #    2. More than one result from financial websites
                # #    3. Same domain confirmed by multiple financial websites and appears in search result.
                # if len(indirect_websites) > 1:
                    # if self.developer_mode: self._print_(print_prefix + 'Financial websites produced more than one company website. A rare scenario yet to find and test.' + str(indirect_websites))
                    # #Current logic consider any one from them
                # current_selected_search_result=-1
                # identification_method=''
                # current_selected_country_matches=False
                # previous_selected_country_matches=False
                # current_selected_suffix_matches=False
                # previous_selected_suffix_matches=False
                # current_selected_sub_domain=False
                # previous_selected_sub_domain=False
                # for i_iter in range(len(self.search_result_details)):
                    # if not self.search_result_details[i_iter]['listing_directory']:
                        # for each_fin_website in indirect_websites:
                            # identification_string=''
                            # if each_fin_website == self.search_result_details[i_iter]['domain_alone']: 
                                # #There can be multiple matches only when financial websites yield more than one result(may same domain or different)
                                # #ALTO METALS LIMITED has http://enterpriseuranium.com.au/ (google) from altometals.com.au(B)
                                # identification_string = identification_string + ':DOMAIN'
                                # if indirect_websites[each_fin_website]['suffix'] == self.search_result_details[i_iter]['suffix']: #This plays a role when the website is not specific to country.
                                    # current_selected_suffix_matches=True
                                    # identification_string = identification_string + '-SFX-Y'
                                # else:
                                    # current_selected_suffix_matches=False
                                    # identification_string = identification_string + '-SFX-N'
                                # if len(indirect_websites[each_fin_website]['country'])>1 and indirect_websites[each_fin_website]['country'] == self.search_result_details[i_iter]['country']:
                                    # current_selected_country_matches=True
                                    # identification_string = identification_string + '-CNTR-Y'
                                # else:
                                    # current_selected_country_matches=False
                                    # identification_string = identification_string + '-CNTR-N'
                                # if current_selected_search_result == -1:
                                    # current_selected_search_result = i_iter
                                    # identification_method='FINSITE:' + 'FIRST:' + identification_string 
                                    # #There is no previous selected record. Hence current record considered as sacred for next iteration
                                    # previous_selected_suffix_matches=current_selected_suffix_matches
                                    # previous_selected_country_matches=current_selected_country_matches
                                    # if self.developer_mode:
                                        # self._print_(print_prefix + 'Having Financial Website: Current record selected:' + str(self.search_result_details[current_selected_search_result]))
                                # else:
                                    # pass
                                    # temp_selection_indicator=False
                                    # #Logic to handle if a website is already selected.
                                    # temp_string=':'
                                    # if (not previous_selected_country_matches) and current_selected_country_matches:
                                        # temp_selection_indicator=True
                                        # temp_string=':LATEST CNTR-Y'
                                    # if (not previous_selected_country_matches) and (not previous_selected_suffix_matches) and current_selected_suffix_matches:
                                        # temp_selection_indicator=True
                                        # temp_string=':LATEST SFX-Y'
                                    # if temp_selection_indicator:
                                        # #Allow only when current record is better than previous record.
                                        # current_selected_search_result = i_iter
                                        # identification_method='FINSITE:' + 'REPLACE:' + identification_string + temp_string
                                        # previous_selected_suffix_matches=current_selected_suffix_matches
                                        # previous_selected_country_matches=current_selected_country_matches
                                        # if self.developer_mode:
                                            # self._print_(print_prefix + 'Having Financial Website: Current record selected changed to:' + str(self.search_result_details[current_selected_search_result]))
                                # break #If website from search result is matching with any of the financial yielded website then it is qualified to next level. So Break the financial website iteration.
                # #A website record should have been based on current data. There should be more data validation not to select any website
                # if current_selected_search_result == -1:
                    # if self.developer_mode:
                        # self._print_(print_prefix + ' Something went wrong to reach - No selection though top occurence and indicative_website are there')
                    # additional_message=additional_message + 'Something went wrong to reach - No selection though top occurence and indicative_website are there'
                    # #write_string=u'' + self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + 'None' + '\t' + 'Something went wrong to reach - No selection though top occurence and indicative_website are there'
                    # #write_string = write_string + '\t' + '' + '\t' + '' + '\t' + '\n'
                    # #write_ins=InputOutput('Write')
                    # #write_ins.open('CompanyWebsites.stat.txt')
                    # #write_ins.write(write_string)
                    # #write_ins.close()
                    # #custom_exit()
                    # #Logic to handle all rejection case
                # elif current_selected_search_result >= 0:
                    # if self.developer_mode:
                        # self._print_(print_prefix + 'Current record selected:' + str(self.search_result_details[current_selected_search_result]))
                    # write_string=u'' + self.run_type_flag +'\t' + country_name + '\t'
                    # if record_identifier:
                        # write_string + write_string + str(record_identifier)
                    # write_string = write_string  + str(self.record_identifier) + '\t' +  self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + self.search_result_details[current_selected_search_result]['Url'] + '\t' + identification_method
                    # write_string = write_string + '\t' + str(current_selected_search_result) + '\t' + '' + '\t'  
                    # if additional_attributes:
                        # for each_key in sorted(additional_attributes.keys()):
                            # write_string = write_string + str(additional_attributes[each_key]) + '\t'
                    # write_string=write_string + additional_message + '\t' + domain_listed.strip(',') + '\n'
                    # write_ins=InputOutput('Write')
                    # write_ins.open('CompanyWebsites.stat.txt')
                    # write_ins.write(write_string)
                    # write_ins.close()
                    # return (self.search_result_details[current_selected_search_result]['Url'],current_selected_search_result,0,identification_method,'')
            # else:
                # #how come this scenario happens. The financial website yield the a website but not in the top occurence. To be checked.
                # #Bloomber says http://www.acuvax.com.au/[Inactive] for ACTIVISTIC LIMITED. But the actual is 
                # additional_message=additional_message + 'No top occurence matche when there is indirect website clue from financial websites'
                # if self.developer_mode:
                    # self._print_(print_prefix + 'No top occurence matche when there is indirect website clue from financial websites')
                # #write_string=u'' + self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + 'None' + '\t' + 'No top occurence matche when there is indirect website clue from financial websites'
                # #write_string = write_string + '\t' + '' + '\t' + '' + '\t' + '\n'
                # #write_ins=InputOutput('Write')
                # #write_ins.open('CompanyWebsites.stat.txt')
                # #write_ins.write(write_string)
                # #write_ins.close()
                # #custom_exit()
        # #STARTING NO FINSITE Website
        # #country,parent_domain,sub_domain,suffix,company_in_title,company_in_path,abbreviation,company_in_domain
        # selected_indexes=[]
        # current_index=-1
        # current_weightage=0
        # country_match_found=False
        # identification_method=''
        # for i_iter in range(len(self.search_result_details)):
            # if (not self.search_result_details[i_iter]['listing_directory']) and (not self.search_result_details[i_iter]['indicative_website']):
                # identification_string=''
                # record_order_no=self.search_result_details[i_iter]['Order']
                # if record_order_no > 5: continue#Dont consider the second half and higher
                # if self.developer_mode:
                    # self._print_(print_prefix + 'No Financial Path: Processing record:' + str(self.search_result_details[i_iter]['Order']) + ' having url:' + self.search_result_details[i_iter]['Url'])
                # current_comp_base_name=self.search_result_details[i_iter]['company_base_name']
                # current_country=self.search_result_details[i_iter]['country']
                # current_parent_domain=self.search_result_details[i_iter]['domain_alone']
                # if current_parent_domain not in domain_listed:
                    # domain_listed = domain_listed + ',' + current_parent_domain
                # current_sub_domain=self.search_result_details[i_iter]['sub_domain']
                # current_suffix=self.search_result_details[i_iter]['suffix']
                # current_comp_in_title=' '.join(self.search_result_details[i_iter]['company_in_title'])
                # current_comp_in_path=' '.join(self.search_result_details[i_iter]['company_in_path'])
                # current_comp_in_domain=' '.join(self.search_result_details[i_iter]['company_in_domain'])
                # current_abbreviation=self.search_result_details[i_iter]['abbreviation']
                # if self.developer_mode:
                    # temp_string=str(i_iter) + '\t' + current_comp_base_name + '\t' + current_country + '\t' + current_parent_domain + '\t' + current_sub_domain + '\t' + current_suffix
                    # temp_string = quick_make_string(temp_string) + quick_make_string('\t',current_comp_in_domain ,'\t' , current_comp_in_path, '\t' , current_comp_in_title , '\t' , current_abbreviation)
                    # #temp_string=temp_string + '\t' + str(current_comp_in_domain) + '\t' + str(current_comp_in_path) + '\t' + str(current_comp_in_title) + '\t' + str(current_abbreviation)
                    # self._print_(print_prefix + 'No Financial Website: current_record:\t' + temp_string)
                # #CA - (10,0,2), ND(Name = domain)[country +-](8,0,7) , NID(NameInDomain)[country +-](4,0,3),NIDT (NameInDomainAndTitle)[country +-](6,0,5),?
                # temp_index=-1
                # temp_weightage=0
                # if current_abbreviation:#
                    # identification_string=identification_string + ':ABBR'
                    # #country matches and company name abbreviation matches with domain name
                    # if len(current_country) > 1 and current_country == country_name:
                        # temp_index=i_iter
                        # temp_weightage=10
                        # identification_string=identification_string + '-CNTR-Y'
                    # elif len(current_country) > 1:
                        # pass
                        # identification_string=identification_string + '-CNTR-N'
                        # #Do Nothing- May be this logic need to be changed . Case when we check for australia and the parent website is in UK.
                    # else:
                        # identification_string=identification_string + '-CNTR-NA'
                        # temp_index=i_iter
                        # temp_weightage=2
                    # if self.developer_mode:
                        # self._print_(print_prefix + 'No Financial Website: Selected(Weightage:' + str(temp_weightage)+ ') based on abbreviation(' + self.company_name_abbr + ') is equal to domain(' + current_parent_domain + ')')
                # elif current_parent_domain == current_comp_in_domain:
                    # #THING ON current_comp_in_domain != current_comp_base_name ABERDEEN LEADERS LIMITED(aberdeen) aberdeenasset(parent)
                    # #domain matches with company base name
                    # identification_string=identification_string + ':EXACTDOMAIN'
                    # if len(current_country) > 1 and current_country == country_name:
                        # temp_index=i_iter
                        # temp_weightage=8
                        # identification_string=identification_string + '-CNTR-Y'
                    # elif len(current_country) > 1:
                        # pass
                        # identification_string=identification_string + '-CNTR-N'
                        # #Do Nothing- May be this logic need to be changed . Case when we check for australia and the parent website is in UK.
                    # else:
                        # temp_index=i_iter
                        # temp_weightage=7
                        # identification_string=identification_string + '-CNTR-NA'
                    # if self.developer_mode:
                        # self._print_(print_prefix + 'No Financial Website: Selected(Weightage:' + str(temp_weightage)+ ') based on domain(' + current_parent_domain + ') exactly matches with company base name (' + current_comp_in_domain + ').')
                # elif len(current_comp_in_domain)>1 and len(current_comp_in_title)>1 and current_comp_in_title.startswith(current_comp_in_domain): #WHAT if one part is in domain and full part is in title
                    # #Scenario - ABERDEEN LEADERS LIMITED(aberdeen) aberdeenasset(parent)
                    # identification_string=identification_string + ':DOMAINTITLE'
                    # #domain has company base name #Do we need to check for length
                    # if len(current_country) > 1 and current_country == country_name:
                        # temp_index=i_iter
                        # temp_weightage=6
                        # identification_string=identification_string + '-CNTR-Y'
                    # elif len(current_country) > 1:
                        # pass
                        # identification_string=identification_string + '-CNTR-N'
                        # #Do Nothing- May be this logic need to be changed . Case when we check for australia and the parent website is in UK.
                    # else:
                        # temp_index=i_iter
                        # temp_weightage=5
                        # identification_string=identification_string + '-CNTR-NA'
                    # if self.developer_mode:
                        # self._print_(print_prefix + 'No Financial Website: Selected(Weightage:' + str(temp_weightage)+ ') based on base name(' + current_comp_base_name + ') in domain(' + current_comp_in_domain + ') and title(' + current_comp_in_title + ')')
                # if temp_index > -1:
                    # if len(current_sub_domain) == 0:
                        # temp_weightage = temp_weightage + 0.5
                        # identification_string=identification_string + ':SUBDOMAIN-N'
                        # if self.developer_mode:
                            # self._print_(print_prefix + 'No Financial Website: 0.5 added since for not having sub domain:(Weightage:' + str(temp_weightage)+ ')')
                    # if len(current_comp_in_path) > 0:
                        # temp_weightage = temp_weightage - 0.5 #Reduce the weightage if company is appear in the url other than domain
                        # identification_string=identification_string + ':INPATH-Y'
                        # if self.developer_mode:
                            # self._print_(print_prefix + 'No Financial Website: reduced 0.5 for having base name in url path:(Weightage:' + str(temp_weightage)+ ')')
                    # #This line is to give more weightage when the result appears in the top
                    # #This logic can be changed. If we want to consider the first result(based on other condition) always
                    # temp_weightage = temp_weightage - round((record_order_no * (1/6.0)),2)
                    # identification_string=identification_string + ':ORDER'
                    # selected_indexes.append((temp_index,temp_weightage,record_order_no,identification_string,self.search_result_details[i_iter]['Url']))
                    # if temp_weightage > current_weightage:
                        # if self.developer_mode:
                            # self._print_(print_prefix + 'No Financial Website: Index ' + str(temp_index) + ' is selected over ' + str(current_index) + ' since current weightage (' + str(temp_weightage) + ') is greater than previous(' + str(current_weightage) + ').' )
                        # current_index=temp_index
                        # current_weightage=temp_weightage
                        # identification_method=identification_string
                # #name in domain and not in path 
                # #company name occurence in listed company -- additional confident
        # if current_index > -1:
            # if self.developer_mode:
                # self._print_(print_prefix + 'Selected Index:' + str(current_index) + ' Collected Indexes:\t' + str(selected_indexes))
            # write_string=u''  + self.run_type_flag +'\t' + country_name + '\t'
            # if record_identifier:
                # write_string + write_string + str(record_identifier)
            # write_string = write_string  + str(self.record_identifier) + '\t' +  self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + self.search_result_details[current_index]['Url'] + '\t' + identification_method
            # write_string = write_string + '\t' + str(current_index) + '\t' + str(current_weightage) + '\t' + str(selected_indexes)   
            # if additional_attributes:
                # for each_key in sorted(additional_attributes.keys()):
                    # write_string = write_string + str(additional_attributes[each_key]) + '\t'
            # write_string=write_string + additional_message + '\t' + domain_listed.strip(',') + '\n'
            # write_ins=InputOutput('Write')
            # write_ins.open('CompanyWebsites.stat.txt')
            # write_ins.write(write_string)
            # write_ins.close()
            # return (self.search_result_details[current_index]['Url'],current_index,current_weightage,identification_method,'')
        # elif self.developer_mode:
            # self._print_(print_prefix + 'Not able to decide the website.')
        # write_string=u''  + self.run_type_flag +'\t' + country_name + '\t'
        # if record_identifier:
            # write_string + write_string + str(record_identifier)
        # write_string = write_string  + str(self.record_identifier) + '\t' +  self.company_name + '\t' + str(len(self.search_result_details)) + '\t' + 'None' + '\t' + 'NA'
        # write_string = write_string + '\t' + '' + '\t' + '' + '\t'   
        # if additional_attributes:
            # for each_key in sorted(additional_attributes.keys()):
                # write_string = write_string + str(additional_attributes[each_key]) + '\t'
        # write_string=write_string + additional_message + '\t' + domain_listed.strip(',') + '\n'
        # write_ins=InputOutput('Write')
        # write_ins.open('CompanyWebsites.stat.txt')
        # write_ins.write(write_string)
        # write_ins.close()
        # return False

if __name__ == '__main__':
    if not True:
        print get_ticker_url('hp')
        custom_exit()
    if not True:
        print 'http://www.colliersparrish.com/html/en/us/index.asp?ptype=1',get_domain_details('http://www.colliersparrish.com/html/en/us/index.asp?ptype=1')
        ##print 'http://www.macraesbluebook.com/search/company.cfm?company=867549',get_domain_details('http://www.macraesbluebook.com/search/company.cfm?company=867549')
        custom_exit()
   # if True:
        ##for each in ['hp','Allovus Design','Bidpal Network','Colliers International','Heinz','Johnson Controls','Lojas Renner','The Herjavec Group','Velux','Microsoft Corporation','FMC Corporation','Eagle Materials Inc','Amphenol Corporation','PPG Industries, Inc.','Benchmark Electronics, Inc.','CenturyLink, Inc.','MediaCorp Pte Ltd','Mondelez International, Inc.','Flextronics Holding USA, Inc.','Lockheed Martin Corporation','Under Armour, Inc.','Coles Supermarkets','gloStream','MetLife','Walsh Group','Alcatel-Lucent USA, Inc.','National-Oilwell Varco, Inc.','Wells Fargo & Company','Kimball International','Kyocera International, Inc.','CH2M Hill Ltd.','Biogen Inc','Methode Electronics Inc.','Lalitha Jewellery Mart Pvt Ltd','BBVA Compass','Cytec Industries Inc','Amgen, Inc.','Fastenal co','flash entertainment','Hallmark Cards','AQR CAPITAL MANAGEMENT LLC']:#get_company_names_from_campaign():
            #print each,get_company_website(each)
        ##exit()
    if True:
        ins=CompanyWebsiteSearch(search_method='Google')
        print ins.get_company_website('Lowe\'s Companies')
        custom_exit()
#