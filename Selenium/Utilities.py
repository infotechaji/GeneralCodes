# # -*- coding: utf-8 -*-
"""
    Content Type: Utilities
    Description: This python file has common scripts used across the application
    Version    : v2.21
    History    :
                v1.0 - 01/01/2015 - Initial version
                v1.1 - 05/14/2015 - Added function has_list_word_in_statement_tuple
                v1.2 - 05/18/2015 - Added list week_days_long and calender_all_keywords
                v1.3 - 05/19/2015 - Added variable REGEX_URL_PATTERN , REGEX_HASHTAG and master_keyword_set_removable
                v1.4 - 05/21/2015 - remove - from statement_has_string_sequential
                v1.5 - 05/22/2015 - Added tuple functionality in keyword sequential search
                v1.6 - 05/27/2015 - Updated stopwords_generic to include arent in addition to aren't
                v1.7 - 06/01/2015 - Added variable stock_keywords
                v1.8 - 06/17/2015 - Added data_identifier_extraction and data_detail_extraction for data_detail and data_feed_identifier fields in post_feed
                v1.9 - 06/23/2015 - Added has_dict_pattern_in_statement
                v1.10 - 07/10/2015 - Imported stem module from nltk.Updated remove_list_word_in_statement and data_feed_identifier_extraction. Add stem_the_statement and get_statement_without_bracket
                v1.11 - 07/10/2015 - Added new function fetch_dict_pattern_matching_statement_from_article
                v1.12 - 10/04/2015 - Added function is_link_to_news
                v1.13 - 10/19/2015 - Added log_time_stamp function
                v1.14 - 10/20/2015 - Updated logic for get_news_must_match and moved common_company_words to global variables
                v1.15 - 10/29/2015 - Moved COMP_EXTENSIONS from ControlConfig to Utilities
                v1.16 - 11/03/2015 - Updated statement_has_string_sequential to handle |
                v1.17 - 11/05/2015 - Added module chardet to detect encoding of the string and added guess_language to update is_english 
                v1.18 - 11/13/2015 - Added get_directory_name to get the base directory of a file if the path is absolute
                v1.19 - 11/13/2015 - replaced has_list_word_in_statement with content from Job Utilities which has pattern_to_replace and upper case comparison logic
                v1.20 - 11/17/2015 - Added comp keyword pty for proprietary
                v1.21 - 12/05/2015 - Updated statement_has_string_sequential. Added no of words threshold to restrict incorrect pattern like statements
                v1.22 - 12/11/2015 - Added argument source_directory to move_processed_file
                v1.23 - 12/16/2015 - Logic pattern_to_replace added in statement_has_string_sequential
                v1.24 - 12/21/2015 - Added function get_file_age to get the time elapsed since a file is modified/changed(metadata)
                v1.25 - 12/23/2015 - Added remove_unhealthy_html_tags
                v1.26 - 01/05/2016 - removed stock_keywords check get_news_must_match and added 'of' and 'and' as removables.
                v1.27 - 01/06/2016 - Updated select_statement and using the function in ArticleHandling
                v1.28 - 01/20/2015 - Added article in news_link_like_keywords for is_a_press_release_link
                v1.29 - 01/28/2016 - Added norm_keywords and company_name_normalizer for company name normalization and fuzzy_compare for comparing names/words using fuzzy logic
                v1.30 - 02/05/2016 - Increased the number of the trail end characters to 1000 in is_html_doc to check for </html> and </body>
                v1.31 - 02/05/2016 - Function count list of words in statement is added
                v1.32 - 02/25/2016 - There was two functions with name count_list_word_in_statement. Commented the old one. Improved the function.
                v1.33 - 03/10/2016 - Added logic to check !doctype and html & head in the first n characters in is_html_doc function to detect html document.
                v1.34 - 03/14/2016 - count_list_word_in_statement: argument 2 (list_of_words_in) can be either list of words or a string to be split by space.
                v1.35 - 03/30/2016 - creating custom exit function custom_exit() and exit_custom(). All exis changed to custom_exit
                v1.36 - 06/02/2016 - Change in is_html_doc. the closing > brackets are removed from document , head, html check.
                v1.37 - 07/11/2016 - Moved get_top_occurrence from CompanyWebsite to Utilities
                v1.38 - 07/14/2016 - allowed urls containing pdfs
                v1.39 - 07/14/2016 - restricted urls containing social media links and added keyword jpeg to image url list to restrict them
                v1.40 - 07/19/2016 - Added variable english_articles and added function get_html_to_unicode_string
                v2.00 - 07/20/2016 - Combined version check-in to common repository
                v2.01 - 07/25/2016 - Updated get_top_occurrence to output occurrence_details[all domain and their count] as the 3rd param for output
                v2.02 - 08/02/2016 - added guess_statement_language function
                v2.03 - 08/03/2016 - Updated get_html_to_unicode_string for encoding type.
                v2.04 - 08/09/2016 - Added function check_all_combination_abbreviation to check whether a string is related to an abbrevation
                v2.05 - 08/16/2016 - get_company_name_without_common_words -changed argument name from company_id to company_name
                                   - string_list_in_statement_sequential and statement_has_just_string_sequential - Removed str()
                v2.06 - 09/01/2016 - Exit when other str or unicode is received as input for get_html_to_unicode_string
                v2.07 - 09/02/2016 - Added a section in get_smell_like_date_from_text(word_length>4) for Press Release 
                v2.08 - 09/22/2016 - Added functions make_company_name_comparable and string_fits_one_in_another
                v2.09 - 09/26/2016 - with and without stopwords check in check_all_combination_abbreviation and return all top matching domain in get_top_occurrence
                v2.10 - 09/29/2016 - youtube.com added in social list
                v2.11 - 10/06/2016 - write_content_to_file - Do not save file if length of the filename is greater than 256
                v2.12 - 10/07/2016 - Added perfect_fit for string_fits_one_in_another i.e., compare word to word
                v2.13 - 10/14/2016 - Try & Except for unichr error in get_html_to_unicode_string
                v2.14 - 10/20/2016 - get_html_to_unicode_string: performance improvement. Concatenate postponed to final step
                v2.15 - 10/27/2016 - treat tel: mailto: as schema URI in get_html_link_type. Refer : http://stackoverflow.com/questions/1737575/are-colons-allowed-in-urls
                v2.16 - 11/25/2016 - get_html_link_type - handle ? and schemas tel, mailto and others.
                v2.17 - 05/09/2017 - has_list_word_in_statement - changed for unicode handling.
                v2.18 - 05/12/2017 - Display error message for write_content_to_file when developer_mode is on
                v2.19 - 05/18/2017 - Copied get_absolute_path from HTMLHandling. The function is a common function.
                v2.20 - 07/27/2017 - Added function guess_name_for_domain
                v2.21 - 08/07/2017 - Rename file to milliseconds if flag is True
    Procedure to use: Import this config file into all python scripts where database operation is performed
    Open Issues: None.
    Pending :    None.
"""
import re
import datetime
import time
import dateutil.parser
import os.path
from urlparse import urlparse,urljoin
from os import walk ##required for get_all_files
import fnmatch ##required for get_all_files
from fuzzywuzzy import fuzz
#from ControlConfig import *
from nltk import stem #for version v1.10 - data_detail_extraction,stem_the_statement
import chardet #get_encoding,is_english
from guess_language import guessLanguage #is_english
import sys,traceback

stopwords_generic=[
        "a","about","above","after","again","against","all","am","an","and","any","are","aren't","arent","as","at"
        ,"be","because","been","before","being","below","between","both","but","by"
        ,"can't","cant","cannot","could","couldn't","couldnt"
        ,"did","didn't","didnt","do","does","doesn't","doesnt","doing","don't","down","during"
        ,"each"
        ,"few","for","from","further"
        ,"had","hadn't","hadnt","has","hasn't","hasnt","have","haven't","havent","having","he","he'd","he'll","he's","her","here","here's","heres","hers","herself","him","himself","his","how","how's","hows"
        ,"i","i'd","i'll","i'm","i've","if","in","into","is","isn't","isnt","it","it's","its","itself"
        #,"just"
        ,"let's","lets"
        ,"me","more","most","mustn't","mustnt","my","myself"
        ,"no","nor","not"
        ,"of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own"
        ,"same","shan't","shant","she","she'd","she'll","she's","should","shouldn't","shouldnt","so","some","such"
        ,"than","that","that's","thats","the","their","theirs","them","themselves","then","there","there's","theres","these","they","they'd","theyd","they'll","theyll","they're","theyre","they've","theyve","this","those","through","to","too"
        ,"under","until","up"
        ,"very"
        ,"was","wasn't","wasnt","we","we'd","we'll","we're","we've","were","weren't","werent","what","what's","whats","when","when's","whens","where","where's","wheres","which","while","who","who's","whos","whom","why","why's","whys","with","won't","wont","would","wouldn't","wouldnt"
        ,"you","you'd","youd","you'll","youll","you're","youre","you've","youve","your","yours","yourself","yourselves"
    ]
english_articles=['a','an','the']
salutation_generic=['jr.','mr.','ms.','mrs.','sr.']
company_generic=['ltd.', 'lp.','co.','llc.', 'inc.','corp.','pty']#pty for australia
common_company_words=['group','holding','holdings','llc','plc','industry','industries','us','usa','co','company','ltd','limited','pvt','private','inc','incorporated','corp','corporation','tech','technology','international','intl','sys','system']
#common_company_words and company_generic logically same but common_company_words is a broader category
norm_keywords = {'operations': 'Operation', 'limited': 'Limited', 'distributors': 'Distributor', 'llp': 'LLP', 'facilities': 'Facility', 
        'farms': 'Farm', 'solutions': 'Solution', 'llc': 'LLC', 'centers': 'Center', 'industries': 'Industry', 'partners': 'Partner', 
        'p.l.c': 'PLC', 'group': 'Group', 'sciences': 'Science', 'pharmacy': 'Pharmacy', 'systems': 'System', 'lp': 'LLP', 
        'division': 'Division', 'designs': 'Design', 'finance': 'Finance', 'professionals': 'Professional', 'food': 'Food', 
        'auto': 'Auto', 'outlet': 'Outlet', 'mgmt': 'Management', 'machineries': 'Machinery', 'investor': 'Investor', 
        'minerals': 'Mineral', 'furniture': 'Furniture', 'companies': 'Company', 'pharmacies': 'Pharmacy', 'pvt': 'Private', 
        'tec': 'Technology', 'gmbh': 'GmBh', 'design': 'Design', 'distributor': 'Distributor', 'laboratory': 'Lab', 'chem': 'Chemical', 
        'factory': 'Factory', 'trusts': 'Trust', 'international': 'International', 'technology': 'Technology', 'soln': 'Solution', 
        'associate': 'Associate', 'beverages': 'Beverage', 'agencies': 'Agency', 'labs': 'Lab', 'corp': 'Corp', 'groups': 'Group', 
        'acc': 'Account', 'industry': 'Industry', 'srl': 'Limited', 'supplies': 'Supply', 'estates': 'Estate', 'incorporated': 'Inc', 
        'ltd': 'Limited', 'plc': 'PLC', 'furnitures': 'Furniture', 'auto-motives': 'Auto', 'facility': 'Facility', 'intl': 'International', 
        'private': 'Private', 'services': 'Service', 'accounts': 'Account', 'motor': 'Motor', 'acct': 'Account', 'market': 'Market', 
        'pharmaceutical': 'Pharmaceutical', 'management': 'Management', 'estate': 'Estate', 'supply': 'Supply', 'holdings': 'Holding', 
        'svce': 'Service', 'system': 'System', 'pharmaceuticals': 'Pharmaceutical', 'solns': 'Solution', 'farming': 'Farm', 
        'markets': 'Market', 'finances': 'Finance', 'company': 'Company', 'chemicals': 'Chemical', 'metals': 'Metal', 'businesses' : 'Business',
        'factories': 'Factory', 'mineral': 'Mineral', 'serv': 'Service', 'divisions': 'Division', 'account': 'Account', 
        'science': 'Science', 'svcs': 'Service', 'distribution': 'Distribution', 'investors': 'Investor', 'u.s.a' : 'USA',
        'motors': 'Motor', 'fertilizers': 'Fertilizer', 'foods': 'Food', 'associates': 'Associate', 'technologies' : 'Technology',
        'ind': 'Industry', 'partner': 'Partner', 'distributions': 'Distribution', 'inc': 'Inc', 'grp': 'Group', 'corporation': 'Corp', 
        'agency': 'Agency', 'chemical': 'Chemical', 'l.t.d': 'Limited', 'holding': 'Holding', 'automotive': 'Auto', 'ltda': 'Limited',
        'apparels': 'Apparel', 'centre': 'Centre', 'farm': 'Farm', 'outlets': 'Outlet', 'lab': 'Lab', 'sys': 'System', 
        'fertilizer': 'Fertilizer', 'center': 'Center', 'commodity': 'Commodity', 'metal': 'Metal', 'svc': 'Service', 
        'l.l.c': 'LLC', 'commodities': 'Commodity', 'beverage': 'Beverage', 'tech': 'Technology', 'centres': 'Centre', 
        'apparel': 'Apparel', 'professional': 'Professional', 'laboratories': 'Lab', 'l.l.p': 'LLP',
        'and': '&', 'amp': '&', '&' : '&', 'st' : 'Saint', 'saint' : 'Saint'}
leader_generic=['download', 'photo','resolution','low']
months_long=['january','february','march','april','may','june','july','august','september','october','november','december']
week_days_long=['monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday']
months_short=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','june','july','sept']
months_index={'january':1
    ,'february':2
    ,'march':3
    ,'april':4
    ,'may':5
    ,'june':6
    ,'july':7
    ,'august':8
    ,'september':9
    ,'october':10
    ,'november':11
    ,'december':12
    ,'jan':1
    ,'feb':2
    ,'mar':3
    ,'apr':4
    ,'jun':6
    ,'jul':7
    ,'aug':8
    ,'sep':9
    ,'oct':10
    ,'nov':11
    ,'dec':12
    ,'sept':9}
month_normalize={'january':'january'
    ,'february':'february'
    ,'march':'march'
    ,'april':'april'
    ,'may':'may'
    ,'june':'june'
    ,'july':'july'
    ,'august':'august'
    ,'september':'september'
    ,'october':'october'
    ,'november':'november'
    ,'december':'december'
    ,'jan':'january'
    ,'feb':'february'
    ,'mar':'march'
    ,'apr':'april'
    ,'jun':'june'
    ,'jul':'july'
    ,'aug':'august'
    ,'sep':'september'
    ,'oct':'october'
    ,'nov':'november'
    ,'dec':'december'
    ,'sept':'september'}
calender_all_keywords=months_long + week_days_long + months_short
key_leadership_words=['ceo','president','executive','officer','officers','management','director','cfo','cio','cco','coo','cpo','chief','cso']#'mln','bln','million','billion']
key_events=['conference','growth','events','meeting']
adult_content_restriction=['ejaculation','foreclosure','intercourse','sexual','horny','penis','anal','babe','bitch','blowjob','boob','cock','cunt','fuck','gay','horny','lesbian','lesbians','masterbating','nude','orgasm','orgy','penis','porn','pussy','rape','sex','tit','tits','ass','crush']#,'dick'
stock_keywords=['strong','buy','accumulate','neutral','perform','hold','sell','underweight','rated','underperform','outperform','bid','bonus','low','market','pricing','product','revenue','shareholder','worth ','stock ','below','gain','raise','slow','fasts','share','earnings','eps','analyst','rating','estimate','operating','margin','investment','repurchase','put','call']
master_keyword_set_removable=stopwords_generic + calender_all_keywords + adult_content_restriction
REGEX_URL_PATTERN=r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^%s\s]|/)))' # ((\S+:\/\/\S+)|(\S*www.?[.]\S+[.]\S+))
COMP_EXTENSIONS = ['plc', 'llc', 'co', 'limited', 'corporation', 'corp', 'pvt', 'inc', 'incorporated', 'ltd', 'limited', 'international', 'intl','pty','proprietary']#pty and  proprietary added for australia
REGEX_HASHTAG = r"#\w{2,50}"

REGEX_BETWEEN_BRACKER=r"\([^\)\(]+\)"
REGEX_BETWEEN_BRACES=r"\{[^\{\}]+\}"
REGEX_BETWEEN_SQR_BRACKETS=r"\[[^\[\]]+\]"

def extract_exception_details(exception_info):
    if isinstance(exception_info,tuple):
        try:
            exception_tple=exception_info
            exception_type=exception_tple[0]
            exception=exception_tple[1]
            traceback_ins=exception_tple[2]
            tb_extract=traceback.extract_tb(traceback_ins)        
            error_details=tb_extract[-1]        
            exec_filename=error_details[0]
            exec_line_no=str(error_details[1])
            exec_function=error_details[2]
            exec_line=error_details[3]
            error_details_dict = {"file_name":exec_filename,"line_no":exec_line_no,"error":exception,"errorFunction":exec_function,"exception_type":exception_type,"traceback":str(tb_extract)}
            return error_details_dict
        except:
            return extract_exception_details(sys.exc_info())
            
def https_social_links(input_link):
    if not input_link: return input_link
    output_link=input_link
    if 'http:' in output_link: output_link=output_link.replace('http:','https:')
    if 'https://www.' not in output_link: output_link=output_link.replace('https://','https://www.')
    return output_link
def write_content_to_file(content_is,file_name,directory_name=None,developer_mode=False):
    try:
        output_file_name=''
        if directory_name:
            output_file_name=os.path.join(directory_name,file_name)
        else:
            output_file_name=file_name
        if len(output_file_name)>=256:
            if developer_mode:
                print 'File cannot be save with the name with length(' + str(len(output_file_name))+ '). Will be downloaded each time.Full Path:' + output_file_name
            return True
        w_h=open(output_file_name,'w')
        w_h.write(get_printable_string(content_is,unicode_to_entitiy_flag=True).replace('\\n','\n'))
        w_h.close
        return True
    except Exception as e:
        print 'write_content_to_file: error while saving content. Error : ', str(e)
        return False
def get_html_link_type(link_url,return_picture=True,return_special_for_special=False):
    #there are special schema in URI which takes format like tel: mailto:
    #<a href="tag:sample"> here tag: is a scheme whereas <a href="./tag:sample"> points to relative path
    if not link_url: return ''
    link_type_is='link'
    #pdf is removed from non_document_extensions.
    non_document_extensions=['xls','xlsx','doc','docx','ppt','pptx','zip','csv']
    picture_extensions=['jpg','eps','png','gif','ico','jpeg']
    social_media_check = ['facebook.com', 'twitter.com', 'linkedin.com', 'pinterest.com','youtube.com']
    if ':' in link_url:
        link_url_lower=link_url.lower()
        if '?' in link_url_lower:
            link_url_lower=link_url_lower[:link_url_lower.find('?')]
        if 'http://' not in link_url_lower.strip()[:9] and 'https://' not in link_url_lower.strip()[:9]:
            link_url_split=link_url_lower.split(':')
            if len(link_url_split[0]) > 0:
                if not return_special_for_special:
                    return link_url_split[0] #Example: javascript, mailto, tel, about, whatsapp
                else:
                    return 'Special'
    for social in social_media_check:
        if social in link_url:
            return 'social'
    if 'javascript' in link_url.lower():
        return 'java'
    if link_url.lower().startswith('mailto:'):
        return 'mail'
    if '/download/' in link_url.lower() or '/downloads/' in link_url.lower():
        return 'download'
    if '/' in link_url:
        last_part_of_url=link_url.split('/')[-1:][0]
        if '.' in last_part_of_url:#how about.jpg?id=123
            last_part_of_url=last_part_of_url.split('.')[-1:][0]
            last_part_of_url=last_part_of_url.lower()
            if last_part_of_url and last_part_of_url in non_document_extensions: return last_part_of_url
            if last_part_of_url and last_part_of_url in picture_extensions: 
                if return_picture: 
                    return 'picture'
                else:
                    return last_part_of_url
    return link_type_is
def read_content_from_file(file_name,directory_name=None):
    try:
        read_file_name=''
        if directory_name:
            read_file_name=os.path.join(directory_name,file_name)
        else:
            read_file_name=file_name
        r_h=open(read_file_name,'r')
        file_content=r_h.read()
        r_h.close
        return file_content
    except Exception as e:
        print 'read_content_from_file: error while saving content-',file_name,' Error : ', str(e)
        return False
def get_statement_for_word_count(in_statement):
    statement_is=get_printable_string(in_statement,replace_by=' ',unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
    statement_is=statement_is.replace('.','')
    statement_is=re.sub(r'[^\w]+',' ',statement_is)
    statement_is=re.sub(r' +',' ',statement_is)
    return statement_is
def is_pure_alphanum(input_string):
    if not input_string: return False
    if ' ' in input_string: return False
    alpha_found=False
    num_found=False
    for c in input_string:
        if c.isdigit(): num_found=True
        if c.isalpha(): alpha_found=True
        if num_found and alpha_found: return True
    return False
def is_number(input_text,check_for_integer=False):
    try:
        if len(re.sub(r'[a-zA-Z]+','',input_text)) != len(input_text): return False
        formatted_input=float(input_text)
        if check_for_integer and '.' in str(input_text): return False
        if check_for_integer: return int(formatted_input)
        return formatted_input
    except ValueError:
        #print 'ValueError:',input_text
        return False
    except OverflowError:
        #print 'OverflowError:',input_text,formatted_input
        return False
def is_html_doc(input_string):
    if not input_string: return False
    input_string=re.sub(r'((<!--)(?:(?!-->).)*(-->))','',input_string)
    length_is=len(input_string)
    if length_is < 100: return False
    html_last_m_char=input_string[-1000:]
    html_last_m_char=html_last_m_char.lower()
    html_first_n_char=input_string[:1000]
    html_first_n_char=re.sub(r' +',' ',html_first_n_char)
    html_first_n_char=re.sub(r' +',' ',html_first_n_char).lower().replace('\n',' ').replace('\r',' ').replace('\t',' ')
    if '<!doctype html ' in html_first_n_char or '<!doctype html>' in html_first_n_char: return True #Version 1.36
    if ('<html ' in html_first_n_char or '<html>' in html_first_n_char) and ('<head ' in html_first_n_char or '<head>' in html_first_n_char): return True#Version 1.36
    if '</html>' in html_last_m_char or '</body>' in html_last_m_char: return True
    return False
def get_smell_like_date_from_url(url_in,minimum_sub_folders=1,minimum_year=2000):
    developer_mode=False
    if not url_in: return None
    if '//' not in url_in: return None
    if (not minimum_sub_folders) or minimum_sub_folders < 1: minimum_sub_folders=1
    url_is=url_in.replace('//',' ')
    if url_is.count('/') < minimum_sub_folders: return None
    url_split=url_is.split('/')
    if minimum_sub_folders == 1:
        new_url_list=url_split[1:]
    else:
        new_url_list=url_split[1:-1]
    new_url=' ' + '/'.join(new_url_list) + ' '
    if developer_mode: print 'get_smell_like_date_from_url - modified url:',new_url
    new_url=re.sub('[^0-9]',' ',new_url)
    if developer_mode: print 'get_smell_like_date_from_url - After regex replace - modified url:',new_url
    date_like_search=re.search(r'[ ][0-9]{2,4}[^0-9][0-9]{2}[^0-9][0-9]{2,4}[ ]',new_url)
    year_end_flag=False
    if not date_like_search: 
        date_like_search=re.search(r'[ ]20[0-9]{2}[0-1][0-9]{3}[ ]',new_url)
    if not date_like_search: 
        date_like_search=re.search(r'[ ][0-1][0-9]{3}20[0-9]{2}[ ]',new_url)
        year_end_flag=True
    if not date_like_search: return None
    date_like_search=date_like_search.group(0).strip()
    if developer_mode: print 'get_smell_like_date_from_url - date_like_search Match found:',date_like_search
    if year_end_flag and len(date_like_search) == 8:
        date_like_search=date_like_search[-4:] + date_like_search[:-4]
        if developer_mode: print 'get_smell_like_date_from_url - Altered date_like_search Match:',date_like_search
    date_like_search_length=len(date_like_search)
    if date_like_search.count(' ') > 2:
        if developer_mode: print 'get_smell_like_date_from_url - More than two spaces in :',date_like_search
        return None
    is_date_like=is_date(date_like_search)
    if (not minimum_year) or minimum_year < 1900: minimum_year = 2000
    if is_date_like: 
        if developer_mode: print 'get_smell_like_date_from_url - converted to date :',is_date_like
        year_part=is_date_like.year
        if year_part >= minimum_year:
            return is_date_like
    return None
def is_a_press_release_link(press_release_link):
    if not press_release_link: return False
    news_link_like_keywords=['news','press','release','blog','media','article']
    if has_list_string_in_statement(press_release_link,news_link_like_keywords) or get_smell_like_date_from_url(press_release_link): return True
    return False
def get_smell_like_date_from_text(input_in,strict_year=False,consume_month_year=True,minimum_year=1900,maximum_year=0,developer_mode=False):
    #Return the value in the form of tuple where the first value is an integer and second value is date/None
    #The integer value can be from 0 to 4. 0 - no match found, 1 - found a proper date, 2 - found month + year (4 digit), 3 - found month + year (2 digit)
    developer_mode=developer_mode
    if (not minimum_year) or minimum_year < 1900: minimum_year = 2000
    if (not maximum_year) or maximum_year == 0: maximum_year = int(get_current_date('%Y'))
    input_data=str(get_printable_string(input_in,unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)).lower()
    input_data=input_data.replace('/','-')
    input_data=input_data.replace('\\','-')
    input_data=input_data.replace('.','-')
    valid_date_special_char=[',','-',':','\'']#,'(',')'] #single quote '13 for 2013
    input_data=re.sub(r"[^0-9a-z,:'-]",' ',input_data)
    input_data=re.sub(r',([0-9]{4})',r', \1',input_data)# daynumber,yearnumber
    input_data=re.sub(r' +',' ',input_data)
    if developer_mode: print '\nget_smell_like_date_from_text:Input=\'',input_in,'\' formatted input=',input_data
    text_found=''
    day_is=''
    day_found=False
    month_is=''
    month_found=False
    month_is_number=False
    year_is=''
    year_found=False
    input_data_list=input_data.split()
    valid_character_skipped_count=0
    for each_word in input_data_list:
        #if developer_mode: print 'START - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found
        each_word_string=str(each_word)
        comma_found=False
        if each_word_string[-1:] in valid_date_special_char:
            if each_word_string[-1:] == ',':comma_found=True
            each_word_string=each_word_string[:-1]
        good_string=False
        word_length=len(each_word_string)
        if word_length == 0: 
            if developer_mode: print 'get_smell_like_date_from_text:content with 0 characters[except symbols]:',each_word
            valid_character_skipped_count += 1
            if valid_character_skipped_count > 2:
                month_found=False
                month_is=''
                year_found=False
                year_is=''
                day_found=False
                day_is=''
                text_found=''
            continue
        valid_character_skipped_count=0
        if word_length>4 and word_length <= 10:
            if developer_mode: print '5 to 10 - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
            if each_word_string.count('-') == 2:
                date_found= is_date(each_word_string)
                if date_found:
                    year_part=date_found.year
                    if year_part>= minimum_year and year_part <=maximum_year:
                        text_found=text_found + ' ' +str(each_word)
                        return (1,date_found,text_found)
            else:
                if each_word_string in months_long:
                    if developer_mode: print '5 to 10 - valid month - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
                    month_found=True
                    month_is_number=False
                    month_is=each_word_string
                    text_found=text_found + ' ' +str(each_word)
                    good_string=True
        elif word_length>4:#Section added by Radha - why do we need this if we have >4 <=10 above. do we mean >10
            if developer_mode: print '5 to 10 - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
            if each_word_string.count('-') == 2:
                date_found= is_date(each_word_string)
                if date_found:
                    year_part=date_found.year
                    if year_part>= minimum_year and year_part <=maximum_year:
                        text_found=text_found + ' ' +str(each_word)
                        return (1,date_found,text_found)
            else:
                if each_word_string in months_long:
                    if developer_mode: print '5 to 10 - valid month - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
                    month_found=True
                    month_is_number=False
                    month_is=each_word_string
                    text_found=text_found + ' ' +str(each_word)
                    good_string=True
        elif word_length == 4:
            if developer_mode: print '4 - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
            if each_word_string in months_short or each_word_string in months_long:
                month_found=True
                month_is_number=False
                month_is=month_normalize[each_word_string]
                text_found=text_found + ' ' +str(each_word)
                good_string=True
                if developer_mode: print '4 - Month- get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
            elif is_number(each_word_string,check_for_integer=True):#How #1356, January 12, 2015
                year_found=True
                year_is=each_word_string
                text_found=text_found + ' ' +str(each_word)
                good_string=True
                if developer_mode: print '4 - Number Year- get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
            elif each_word_string[-2:] in ['th','st','nd','rd'] and is_number(each_word_string[:-2],check_for_integer=True):
                day_found=True
                day_is=each_word_string
                text_found=text_found + ' ' +str(each_word)
                good_string=True
                if developer_mode: print '4 - nth like day- get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
        elif word_length == 3:
            if developer_mode: print '3 - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
            if each_word_string[0] == '\'':
                if is_number(each_word_string[1:3]):
                    year_found=True
                    year_is='20' + str(each_word_string[1:3])
                    text_found=text_found + ' ' +str(each_word)
                    good_string=True
                if developer_mode: print '3 - quote two digit Year- get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
            elif each_word_string in months_short :
                month_found=True
                month_is_number=False
                month_is=each_word_string
                text_found=text_found + ' ' +str(each_word)
                good_string=True
                if developer_mode: print '3 - short month- get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
            elif each_word_string[-2:] in ['th','st','nd','rd'] and is_number(each_word_string[:-2],check_for_integer=True):
                day_found=True
                day_is=each_word_string
                text_found=text_found + ' ' +str(each_word)
                good_string=True
                if developer_mode: print '3 - nth like day- get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
        elif word_length <= 2:
            if developer_mode: print '2 - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is,'comma_found=',comma_found
            number_like=is_number(each_word_string,check_for_integer=True)
            if number_like:
                if developer_mode: print '2 Number - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is,'comma_found=',comma_found
                if month_found and day_found:
                    year_found=True
                    year_is=each_word_string
                    text_found=text_found + ' ' +str(each_word)
                    good_string=True
                    if developer_mode: print '2 Number - M and D Found so Y - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
                elif month_found:
                    if developer_mode: print '2 Number - M and No D Found - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
                    if comma_found:
                        day_found=True
                        day_is=each_word_string
                        text_found=text_found + ' ' +str(each_word)
                        good_string=True
                    elif not month_is_number and (not strict_year):#strict_year fails for August 15 but succeeds for August 2015
                        year_found=True
                        year_is=each_word_string
                        text_found=text_found + ' ' +str(each_word)
                        good_string=True
                    else: #fail on 12 06 15
                        pass
                elif day_found and (not year_found) and number_like <= 12: #12 2015 August is not a valid data
                    if developer_mode: print '2 Number - No M and D Found - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
                    month_found=True
                    month_is=each_word_string
                    text_found=text_found + ' ' +str(each_word)
                    month_is_number=True
                    good_string=True
                else:
                    if developer_mode: print '2 Number - No M and No D. so D - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
                    if day_found:
                        month_found=False
                        year_found=False
                    day_found=True
                    day_is=each_word_string
                    text_found=text_found + ' ' +str(each_word)
                    good_string=True
        if good_string:
            if developer_mode: print 'GOOD - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
            if day_found and month_found and year_found:
                if month_is_number:
                    date_found=is_date(str(day_is) + '/' + str(month_is) + '/' + str(year_is))
                    if developer_mode: print 'Found - get_smell_like_date_from_text month_is_number - current word:',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
                    #if date_found: 
                    #    year_part=date_found.year
                    #    if year_part>= minimum_year and year_part <=maximum_year:
                    #        return (1,date_found,text_found)
                else:
                    date_found=is_date(UpperCamelCase(str(month_is)) + ' ' + str(day_is) + ', ' + str(year_is))
                    if developer_mode: print 'Found - get_smell_like_date_from_text NOT month_is_number - current word:',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is,'"',UpperCamelCase(str(month_is)) + ' ' + str(day_is) + ', ' + str(year_is),'"'
                if date_found: 
                    year_part=date_found.year
                    #print 'DATE FOUND',minimum_year,maximum_year,year_part
                    if year_part>= minimum_year and year_part <=maximum_year:
                        return (1,date_found,text_found)
                    elif developer_mode:
                        print 'get_smell_like_date_from_text: date condition is not matching:year_part=',year_part,',minimum_year=',minimum_year,',maximum_year=',maximum_year
                month_found=False
                month_is=''
                year_found=False
                year_is=''
                day_found=False
                day_is=''
                text_found=''
        else:
            if month_found and (not month_is_number) and year_found and (not day_found) and consume_month_year:
                date_found=is_date(month_is + ' 01, ' + str(year_is))
                if developer_mode: print 'Found - get_smell_like_date_from_text NOT month_is_number and month_found and year_found - current word:',each_word_string,day_found,month_found,year_found,day_is,month_is,year_is
                if date_found: 
                    year_part=date_found.year
                    if year_part>= minimum_year and year_part <=maximum_year:
                        if len(year_is) == 4:
                            return (2,date_found,text_found)
                        else:
                            return (3,date_found,text_found)
            month_found=False
            month_is=''
            text_found=''
            year_found=False
            year_is=''
            day_found=False
            day_is=''
        if developer_mode: print 'END - get_smell_like_date_from_text - current word:\'',each_word_string,day_found,month_found,year_found
    return (0,None,text_found)
def is_date(sting_is):
    try:
        date_is_formatted=dateutil.parser.parse(sting_is)
        return date_is_formatted
    except Exception, e:
        #print e
        return False
def to_date(string_is,date_format='%Y-%m-%d'):
    try:
        return datetime.datetime.strptime(string_is, date_format).date()
    except Exception, e:
        print e
        return False
def get_file_size(file_name):
    if file_name:
        file_name_is=file_name
    else:
        return -1
    if os.path.isfile(file_name_is):
        statinfo = os.stat(file_name_is)
        return statinfo.st_size
    else:
        return -1
def get_time_stamp_for_file(include_milliseconds=False):
    if include_milliseconds:
        return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S%f'))
    else:
        return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'))
def get_current_date(format='%Y%m%d'):
    if format == 'date':
        return datetime.datetime.now()
    else:
        return str(datetime.datetime.fromtimestamp(time.time()).strftime(format))
def get_directory_name(file_name):
    if '\\' in file_name or '/' in file_name:
        return os.path.dirname(file_name)
    return ''
def get_relative_target_directory(file_name,relative_target='processed_files'):
    file_directory_name=''
    if os.path.isfile(file_name):
        file_directory_name=get_directory_name(file_name)
    if file_directory_name and len(file_directory_name)>0:
        return os.path.join(file_directory_name,relative_target)
    return relative_target
def get_file_name_with_time_stamp(file_name,check_file_existence=True,include_directory_name=True,skip_timestamp=False,include_milliseconds=False):
    if not file_name: return False
    if check_file_existence and (not os.path.isfile(file_name)): return False
    timestamp_is=get_time_stamp_for_file(include_milliseconds)
    file_directory_name=os.path.dirname(file_name)
    base_name_is=os.path.basename(file_name)
    file_name_base=os.path.splitext(base_name_is)[0]
    file_name_ext=os.path.splitext(base_name_is)[1].strip('.')
    if skip_timestamp:
        time_stamp_part=''
    else:
        time_stamp_part='_' + timestamp_is
    if include_directory_name:
        new_file_name_is=os.path.join(file_directory_name,file_name_base + time_stamp_part  + '.' + file_name_ext)
    else:
        new_file_name_is=file_name_base + time_stamp_part + '.' + file_name_ext
    return new_file_name_is
def rename_file_to_time_stamp_prefix(file_name,return_file_name=False,include_milliseconds=False):
    if file_name:
        file_name_is=file_name
    else:
        return False
    if os.path.isfile(file_name_is):
        if False:
            if '/' in file_name_is or '\\' in file_name_is:
                file_directory_name=os.path.dirname(file_name_is)
                file_base_name_is=os.path.basename(file_name_is)
                new_file_name_is=os.path.join(file_directory_name,get_time_stamp_for_file() + '_' + file_base_name_is)
            else:
                new_file_name_is=get_time_stamp_for_file() + '_' + file_name_is
        new_file_name_is= get_file_name_with_time_stamp(file_name_is,check_file_existence=False,include_milliseconds=include_milliseconds)
        try:
            print 'File to be renamed from ',file_name_is,' to ',new_file_name_is
            os.rename(file_name_is,new_file_name_is)
            if return_file_name: return new_file_name_is
            return True
        except Exception, e:
            print str(e),file_name
            return False
    else:
        print 'in rename_file_to_time_stamp_prefix():File does not exist:',file_name
        return False
def get_all_files(pattern,directory_is=None,full_path=True,recursive=False):
    #directory_is or self.directory_name is mandatory
    iter=0
    current_directory_is=None
    if directory_is:
        if os.path.isdir(directory_is):
            current_directory_is=directory_is
        else:
            print "get_all_files(): Director does not exist -'" + directory_is + "'"
            return False
    if '*' not in pattern or (not ('.psql' in pattern or '.log' in pattern or '.process' in pattern or '.txt' in pattern or '.search' in pattern or '.succu' in pattern)):
        print "get_all_files(): valid file extensions are - (psql,log,process,txt). Provided pattern - '" + pattern + "'"
        return False
    if not current_directory_is:
        current_directory_is=os.getcwd()
    result_file=[]
    for (root_path,dir_list,file_list) in walk(current_directory_is):
        iter_inner=0
        for f_name in file_list:
            if pattern:
                if full_path:
                    if fnmatch.fnmatch(f_name,pattern):
                        result_file.append(os.path.abspath(os.path.join(root_path, f_name)))
                else:
                    if fnmatch.fnmatch(f_name,pattern):
                        result_file.append(f_name)
            else:
                if full_path:
                    result_file.append(os.path.abspath(os.path.join(root_path, f_name)))
                else:
                    result_file.append(f_name)
        if not recursive:
            return result_file
    return result_file
def move_processed_file(file_name,target_directory,rename_with_timestamp=True,create_sub_directory=True,source_directory=None):
    if file_name:
        file_name_is=file_name
    else:
        return False
    file_name_list=[]
    file_name_list[:]=[]
    if '*' not in file_name_is:
        file_name_list.append(file_name_is)
    else:
        file_search_result=get_all_files(pattern=file_name_is,directory_is=source_directory)
        if not file_search_result:
            print "move_processed_file(): no file found with pattern - '" + file_name_is + "'"
            return False
        else:
            for each_file_found in file_search_result:
                file_name_list.append(each_file_found)
    is_process_success=False
    move_file_count=0
    move_file_total=len(file_name_list)
    #print file_name_list
    for each_file in file_name_list:
        print each_file
        file_name_is=each_file
        move_file_count += 1
        if os.path.isfile(file_name_is):
            if not os.path.isdir(target_directory): 
                if create_sub_directory:
                    if not create_directory(target_directory): 
                        print "move_processed_file(" + str(move_file_count) + ' of ' + str(move_file_total)  + "): Error while creating directory - '" + target_directory + "'"
                        return False
                else:
                    print "move_processed_file(" + str(move_file_count) + ' of ' + str(move_file_total)  + "): Directory does not exist - '" + target_directory + "'"
                    return False
            try:
                if rename_with_timestamp:
                    new_file_name=get_file_name_with_time_stamp(file_name_is,include_directory_name=False)
                else:
                    new_file_name=get_file_name_with_time_stamp(file_name_is,include_directory_name=False,skip_timestamp=True)
                #print 'code is here',new_file_name
                new_file_name=os.path.join(target_directory,new_file_name)
                #print 'code is here',new_file_name,target_directory
                os.rename(file_name_is,new_file_name)
                print "move_processed_file(" + str(move_file_count) + ' of ' + str(move_file_total)  + '):File is renamed from ',file_name_is,' to ',new_file_name
                is_process_success=True
            except Exception, e:
                print "move_processed_file(" + str(move_file_count) + ' of ' + str(move_file_total)  + '):' + str(e)
                return False
        else:
            print "move_processed_file(" + str(move_file_count) + ' of ' + str(move_file_total)  + "):File does not exist - '" + file_name_is + "'"
            return False
    return is_process_success
def UpperCamelCase(input_data):
    if not (isinstance(input_data,str) or isinstance(input_data,unicode)): return input_data
    input_data_string=input_data.strip()
    if len(input_data_string) == 1: return input_data_string.upper()
    result_camelcase=input_data_string[:1].upper()
    result_camelcase = result_camelcase + input_data_string[1:].lower()
    return result_camelcase
def list_to_dictionary(list_is,value_type='int'):
    if not list_is: return {}
    result_dictionary={}
    if value_type == 'boolean':
        for each_item in list_is:
            result_dictionary[each_item]=True
    elif value_type == 'int':
        for each_item in list_is:
            result_dictionary[each_item]=1
    elif value_type == 'self':
        for each_item in list_is:
            result_dictionary[each_item]=each_item
    else:
        for each_item in list_is:
            result_dictionary[each_item]=value_type
    return result_dictionary
def compare_two_objects(dictionary_1,dictionary_2,type='dict'):
    if (not dictionary_1) or (not dictionary_2): return False
    if len(dictionary_1) != len(dictionary_2): return False
    if isinstance(dictionary_1,dict) and isinstance(dictionary_2,dict):
        temp_dictionary_1=dictionary_1.copy()
        temp_dictionary_2=dictionary_2.copy()
    elif isinstance(dictionary_1,list) and isinstance(dictionary_2,list):
        temp_dictionary_1=list_to_dictionary(dictionary_1)
        temp_dictionary_2=list_to_dictionary(dictionary_2)
    else:
        return False
    for each_key in temp_dictionary_1:
        if each_key in temp_dictionary_2:
            del temp_dictionary_2[each_key]
        else:
            return False
    if temp_dictionary_2: return False
    return True
def log_time_stamp(column_delimit='\t'):
    return str(get_timestamp_for_file(True)) + ':' + column_delimit
def get_timestamp_for_file(include_seconds=False):
    if include_seconds:
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    else:
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M')
def get_date_from_text(input_data):
    posted_date = ''
    input_data_form=re.sub('[^\w,]',' ',str(input_data))
    input_data_form=re.sub(' +',' ',input_data_form)
    date_pattern = re.search('[a-zA-Z]{,9}[.]?\s[0-3]?[0-9][a-zA-Z]{0,2}[,]\s\d\d\d\d', input_data_form)
    if date_pattern is not None:
        #print date_pattern.group(0),has_list_word_in_statement(str(date_pattern.group(0)),months_short),months_short
        if has_list_word_in_statement(str(date_pattern.group(0)),months_short) or has_list_word_in_statement(str(date_pattern.group(0)),months_long):
            posted_date = date_pattern.group(0)
    if (not posted_date) or len(str(posted_date)) < 4:
        date_pattern = re.search('[a-zA-Z]{,9}[\s,.]+\d\d\d\d', input_data_form)
        if date_pattern is not None:
            #print str(date_pattern.group(0)),has_list_word_in_statement(str(date_pattern.group(0)),months_short),months_short
            if has_list_word_in_statement(str(date_pattern.group(0)),months_short) or has_list_word_in_statement(str(date_pattern.group(0)),months_long):
                posted_date_temp = date_pattern.group(0)
                posted_date_temp=re.sub(r'[,.]',' ',posted_date_temp)
                posted_date_temp=re.sub(r' +',' ',posted_date_temp)
                posted_date_temp_split=posted_date_temp.split()
                if len(posted_date_temp_split) > 1:
                    posted_date=posted_date_temp_split[0] + ' 01 ' + posted_date_temp_split[1]
                else:
                    posted_date=posted_date_temp
    #if (not posted_date) or len(str(posted_date)) < 4:
    #    date_pattern = re.search('[a-zA-Z]+\s\d\d[a-zA-Z]+\S\s\d\d\d\d', input_data_form)
    #    if date_pattern is not None:
    #        posted_date = date_pattern.group(0)
    #if (not posted_date) or len(str(posted_date)) < 4:
    #    date_pattern = re.search('[0-3]?[0-9]\s[a-zA-Z]+\s\d\d\d\d', input_data_form)
    #    if date_pattern is not None:
    #        posted_date = date_pattern.group(0)
    if (not posted_date) or len(str(posted_date)) < 4:
        date_pattern = re.search('[0-3]?[0-9]\S[0-3]?[0-9]\S(?:[0-9]{2})?[0-9]{2}', input_data_form)
        if date_pattern is not None:
            posted_date = date_pattern.group(0)
    return posted_date
def replace_selected_html(input_sentence):
    input_is=input_sentence
    input_sentence=input_sentence.replace('&ndash;','-')
    input_sentence=input_sentence.replace('&mdash;','-')
    input_sentence=input_sentence.replace('&quot;','"')
    input_sentence=input_sentence.replace('&ldquo;','"')
    input_sentence=input_sentence.replace('&rdquo;','"')
    input_sentence=input_sentence.replace('&lsquo;',"`")
    input_sentence=input_sentence.replace('&apos;',"`")
    input_sentence=input_sentence.replace('&rsquo;',"`")
    input_sentence=input_sentence.replace('&nbsp;',' ')
    input_sentence=input_sentence.replace('&amp;','&')
    input_sentence=input_sentence.replace('&gt;','>')
    input_sentence=input_sentence.replace('&lt;','<')
    input_sentence=input_sentence.replace('&lt;','<')
    input_sentence=re.sub(r'[&][#][0-9]{,5}[;]',' ',input_sentence)
    input_sentence=re.sub(r'[&][a-zA-Z]{,6}[;]',' ',input_sentence)
    input_sentence=re.sub(r'[&]#[x][a-zA-Z0-9]{,6}[;]',' ',input_sentence)
    #Removing non-printable characters
    input_sentence=re.sub(r'[\x00-\x08]+',' ',input_sentence)
    input_sentence=re.sub(r'[\x0B-\x0C]+',' ',input_sentence)
    input_sentence=re.sub(r'[\x0E-\x1F]+',' ',input_sentence)
    #Non - ascii characters > 128 decimal
    if re.search(r'\xE2\x80',input_sentence):
        #print '\nSpecial character found:',input_sentence
        input_sentence=re.sub(r'(\xE2\x80[\x90-\x95])+','-',input_sentence)
        input_sentence=re.sub(r'(\xE2\x80[\x98-\x9B])+','\'',input_sentence)
        input_sentence=re.sub(r'(\xE2\x80[\x9C-\x9F])+','"',input_sentence)
    #print input_sentence,'\n\t\t',simplified
    input_sentence=re.sub(r'[\x80-\xFF]+',' ',input_sentence)
    #print 'End of > 128 replacement:',input_sentence
    return input_sentence.strip()
def standardize_company_name(company_name):
    removable_words = ['ltd', 'l.t.d', 'lp', 'l.p','co.','systems','co', 'inc', 'llc', 'inc.','usa', 'us', 'international', 'ems','tech','technology']#,'corp','corporation','company'
    input_string=company_name.lower().replace('.',' ')
    input_string=re.sub(r"[^\w'-]", " ", input_string)
    input_string_words_list=input_string.split()
    for word in removable_words:
        if word in input_string_words_list:
            if len(input_string_words_list)>1:
                input_string_words_list.remove(word)
    output_string=' '.join(input_string_words_list)
    return output_string.strip()
def standardize_company_name_for_normalizer(company_name):
    removable_words = ['the','lp', 'l.p','ems','corp','tech','inc','ltd','co','com','corporation','limited','and','us','usa','corp','incorporated','llc','software','net','solution','solutions','company','system','systems','industry','industries','international','technologies','technology']
    input_string=replace_selected_html(company_name).lower()
    #input_string=re.sub(r'&amp;','&',input_string)
    #input_string=re.sub(r' &amp ',' & ',input_string)
    #remove 's or `s
    #input_string=re.sub(r'[\"]s\s','\'',input_string)
    input_string=re.sub(r'[\'`]s\s',' ',input_string)
    input_string=re.sub(r'[^\w]', ' ', input_string)
    input_string=re.sub(r'[_]', ' ', input_string)
    input_string=re.sub(r' +', ' ', input_string)
    input_string_words_list=input_string.split()
    for word in removable_words:
        if word in input_string_words_list:
            if len(input_string_words_list)>1:
                input_string_words_list.remove(word)
    company_name_high_norm=re.sub(r'[^\w]', ' ', company_name)
    company_name_high_norm=' ' + re.sub(r'[_]', ' ', company_name_high_norm) + ' '
    output_company_name=''
    last_norm_initial=False
    last_norm=''
    for each_norm in input_string_words_list:
        if len(each_norm) == 1:
            if ' ' + each_norm.upper() + ' ' in company_name_high_norm:
                if last_norm_initial:
                    output_company_name=output_company_name + each_norm
                    last_norm_initial=True
                else:
                    output_company_name=output_company_name + ' ' + each_norm
                    last_norm_initial=True
        elif len(each_norm) == 0:
            pass
        else:
            output_company_name=output_company_name + ' ' + each_norm
            last_norm_initial=False
        last_norm=each_norm
    return output_company_name.strip()
def select_company_name_based(company_name_in,page_title_in):
    company_name=company_name_in
    std_company_name=standardize_company_name(company_name)
    len_std_company=len(std_company_name.split())
    current_title=page_title_in
    current_title_lower=current_title.lower()
    count_matched=0
    for each_company_word in std_company_name.split():
        if each_company_word in current_title_lower: count_matched +=1
    if count_matched >= (len_std_company/2.0):
        return True
    return False
def select_company_name_ticker_based(company_name_in,page_title_in,company_ticker=None,news_must_match=None):
    developer_mode=False
    #if (not company_ticker) and (not news_must_match): 
    if (not news_must_match): 
        print 'Company Name without ticker or news must match',company_name_in,page_title_in,company_ticker,news_must_match
        custom_exit()
        return select_company_name_based(company_name_in,page_title_in)
    current_title=re.sub(r'[\d,]+[.][\d]+[MB]?',r' ',page_title_in)
    current_title=replace_selected_html(current_title)
    current_title_ticker=re.sub(r'[^\w\'`-]+',' ',current_title)
    current_title_ticker=re.sub(r' +',' ',current_title_ticker)
    if company_ticker:
        if len(company_ticker)>2:
            if company_ticker.upper() in current_title_ticker:
                if developer_mode: print 'processing statement_has_string_sequential():ticker matched >2'
                return True
        elif len(company_ticker)>0:
            if statement_has_string_sequential(current_title_ticker,'NYSE ' + company_ticker):
                if developer_mode: print 'processing statement_has_string_sequential():ticker matched >0'
                return True
    if developer_mode: print 'processing statement_has_string_sequential() with news_must_match'
    if '&' in news_must_match:
        current_title_must_match=re.sub(r'[^\w\'`&-]+',' ',current_title)
    else:
        current_title_must_match=re.sub(r'[^\w\'`-]+',' ',current_title)
    return statement_has_string_sequential(current_title_must_match,news_must_match,threshold_words=len(company_name_in.split()))
def statement_has_string_sequential(statement,string_to_search,threshold_words=2):
    developer_mode=False
    if developer_mode: print 'In statement_has_string_sequential(). statement=',statement,'.string_to_search=',string_to_search
    if (not statement) or (not string_to_search): return False
    if developer_mode: print 'after null check statement_has_string_sequential()'
    if len(statement.strip()) < 5 or len(string_to_search.strip())<2: return False
    if developer_mode: print 'after length check statement_has_string_sequential()'
    if '(' or ')' in string_to_search:
        if string_to_search.count('(') != string_to_search.count(')'):
            print 'invalid news_must_match pattern: count of ( and ) are not matching:' + str(string_to_search)
            custom_exit()#to error out and exit gracefully for multiprocessing
    if '|' in string_to_search:
        if '(' in string_to_search or ')' in string_to_search:
            all_brack=re.findall(r'\(([^\(\)]+)\)',string_to_search)
            if all_brack:
                for each_brack in all_brack:
                    if '|' in each_brack:
                        print 'invalid news_must_match pattern: | inside ():' + str(string_to_search)
                        custom_exit()#to error out and exit gracefully for multiprocessing
        string_to_search_list=string_to_search.split('|')
        for each_string_to_search in string_to_search_list:
            curr_result=statement_has_string_sequential(statement,each_string_to_search,threshold_words)
            if curr_result: return curr_result
        return False
    search_string=re.sub(r' +',' ',string_to_search.lower())
    current_index=0
    pattern_to_replace=r'[^\w\'`'
    if '&' in string_to_search:
        pattern_to_replace = pattern_to_replace + '&'
    if '#' in string_to_search:
        pattern_to_replace = pattern_to_replace + '#'
    if '-' in string_to_search:
        pattern_to_replace = pattern_to_replace + '-'
    pattern_to_replace = pattern_to_replace + ']+'
    if developer_mode: print 'Utilities.py:statement_has_string_sequential: pattern_to_replace:' + str(pattern_to_replace)
    standard_statement=re.sub(pattern_to_replace,r' ',statement.lower())
    sub_string_is=standard_statement
    if developer_mode: print 'Before string split statement_has_string_sequential()',search_string.split()
    index_found_list=[]
    previous_index=0
    no_of_word_in_pattern=0
    for each_word in search_string.split():
        sub_string_is=' ' + sub_string_is[current_index:] + ' '
        if ('(' in each_word) or (')' in each_word):
            temp_index=get_index_of_special_tuple(sub_string_is,each_word)
        else:
            temp_index=sub_string_is.find(' ' + str(each_word).encode('utf-8') + ' ')
        if developer_mode: print 'in search statement_has_string_sequential()','"' + each_word + '"','"' + sub_string_is + '"','\tINDEX',temp_index
        if temp_index >= 0:
            no_of_word_in_pattern += 1
            computed_index=previous_index+temp_index
            index_found_list.append(computed_index)
            previous_index=computed_index
            current_index=temp_index + 1 #len(each_word)
        else:
            return False
    if len(index_found_list)>1:
        matched_string_length=standard_statement[index_found_list[0]:index_found_list[-1]+1]
        no_of_words_in_pattern_found=matched_string_length.count(' ') + 1
    else:
        matched_string_length=standard_statement[index_found_list[0]]
        no_of_words_in_pattern_found=matched_string_length.count(' ') + 1
    if developer_mode:print 'statement_has_string_sequential' + '\t' + repr(statement)+ '\t' + repr(string_to_search)+ '\t' + str(index_found_list)+ '\t' + str(no_of_word_in_pattern)+ '\t' + str(no_of_words_in_pattern_found) + '\t' + matched_string_length + '\t' + get_word_from_statement(standard_statement,index_found_list[0])
    if (no_of_words_in_pattern_found - no_of_word_in_pattern) > threshold_words:
        first_word_found=get_word_from_statement(standard_statement,index_found_list[0])
        if len(first_word_found) == 0 or (not first_word_found):
            print 'Logical error search statement_has_string_sequential()',statement,string_to_search,threshold_words
            custom_exit()
        if standard_statement[index_found_list[0]+1:].find(first_word_found)>0: # This check for the second occurrence of the pattern
            return statement_has_string_sequential(standard_statement[index_found_list[0]+1:],string_to_search,threshold_words)
        else:
            if developer_mode: print 'in search statement_has_string_sequential()',' threshold not met : (' + str(no_of_words_in_pattern_found) + ' - ' + str(no_of_word_in_pattern) + ') > ' + str(threshold_words)
            return False
    if developer_mode: print 'statement_has_string_sequential' + '\t' + repr(statement)+ '\t' + repr(string_to_search)+ '\t' + str(index_found_list)+ '\t' + str(no_of_word_in_pattern)+ '\t' + str(no_of_words_in_pattern_found) + '\t' + matched_string_length + '\t' + get_word_from_statement(standard_statement,index_found_list[0])
    return True
def get_word_from_statement(statement,at_index):
    if len(statement)>0 and at_index>=0:
        sub_string_is=statement[at_index:]
        next_space_at=sub_string_is.find(' ')
        if next_space_at>0:
            #print next_space_at,sub_string_is
            return sub_string_is[0:next_space_at]
        elif next_space_at == 0:
            return ''
        else:
            return ''
    else:
        return ''
def get_index_of_special_tuple(statement,string_to_search):
    developer_mode=False
    if developer_mode: print 'In get_index_of_special_tuple()'
    if (not statement) or (not string_to_search): return -1
    if developer_mode: print 'after null check get_index_of_special_tuple()'
    if len(string_to_search.strip())<2 or len(statement.strip()) <2: return -1#< len(string_to_search.strip()): return -1
    #if len(string_to_search.strip())<2 or len(statement.strip()) < len(string_to_search.strip()): return -1
    if ('(' not in string_to_search) or (')' not in string_to_search) or (',' not in string_to_search): return -1#or ('|' not in string_to_search)
    if developer_mode: print 'after length check get_index_of_special_tuple()'
    search_string=re.sub(r'[()]+','',string_to_search.lower())
    search_string=re.sub(r' +',' ',search_string)
    index_found=-1
    standard_statement=statement.lower()#re.sub(r'[^\w\'`]+',r' ',statement.lower())#no character should be replaced since index is used in parent function
    sub_string_is=' ' + standard_statement + ' '
    if developer_mode: print 'Before string split get_index_of_special_tuple()',search_string.split()
    for each_word in search_string.split(','):
        temp_index=sub_string_is.find(' ' + str(each_word.strip()) + ' ')
        if developer_mode: print 'in search get_index_of_special_tuple()','"' + each_word + '"','"' + sub_string_is + '"','\tNNNZZZ',sub_string_is.find(' ' + str(each_word) + ' '),temp_index,index_found
        if temp_index >= 0:
            if index_found == -1:
                index_found = temp_index
            elif temp_index < index_found:
                index_found = temp_index
    return index_found
def string_list_in_statement_sequential(statement,string_to_search,replace_space_statement=True):
    if (not statement) or (not string_to_search): return []
    if isinstance(string_to_search,str) or isinstance(string_to_search,unicode): return string_list_in_statement_sequential(statement,string_to_search.strip().split())
    if isinstance(statement,str):
        unicode_statement=get_html_to_unicode_string(statement)
    else:
        unicode_statement=statement
    current_index=0
    output_list=[]
    standard_statement=unicode_statement.lower()
    if replace_space_statement: standard_statement = re.sub(r' +',r'',standard_statement)
    sub_string_is=standard_statement
    #if 'bench' in str(string_to_search).lower(): print '\n\nStatement',statement,'\tStringToSearch',string_to_search
    for each_word in string_to_search:
        #if 'bench' in str(string_to_search).lower(): print 'Loop:word=',each_word,'\tc_ind=',current_index,'\tfind=',sub_string_is.find(str(each_word))
        sub_string_is=sub_string_is[current_index:]
        if isinstance(each_word,str) or isinstance(each_word,unicode):
            modified_word=each_word
        else:
            modified_word=str(each_word)
        temp_index=sub_string_is.find(modified_word)#str() failed for unicode
        if temp_index >= 0:
            output_list.append(each_word)#output the exact string
            current_index=temp_index + len(modified_word)
    return output_list
def statement_has_just_string_sequential(statement,string_to_search):#will not add space before and after each word search
    if (not statement) or (not string_to_search): return False
    if len(statement.strip()) < 5 or len(string_to_search.strip())<2: return False
    search_string=re.sub(r' +',' ',string_to_search.lower())
    current_index=0
    if isinstance(statement,str):
        unicode_statement=get_html_to_unicode_string(statement)
    else:
        unicode_statement=statement
    standard_statement=re.sub(r'[^\w\'`&-]+',r' ',unicode_statement.lower())
    sub_string_is=standard_statement
    for each_word in search_string.split():
        sub_string_is=sub_string_is[current_index:]
        if isinstance(each_word,str) or isinstance(each_word,unicode):
            modified_word=each_word
        else:
            modified_word=str(each_word)
        temp_index=sub_string_is.find(modified_word)#str() failed for unicode
        if temp_index >= 0:
            current_index=temp_index + len(modified_word)
        else:
            return False
    return True
def get_encoding(statement):
    encoding_is=''
    if len(statement) >0 :
        result = chardet.detect(statement)
        encoding_is=result['encoding']
def guess_statement_language(statement):
    if isinstance(statement,unicode):
        u_statement=statement
    else:
        encoding_is=get_encoding(statement)
        if encoding_is:
            try:
                u_statement=unicode(statement,encoding_is)
            except Exception as e:
                print 'Utilities.py:guess_statement_language:Encoding Found: Error- ' + str(e) + repr(statement[:100])
                return 'error'
        else:
            try:
                u_statement=statement.decode('utf-8')
            except Exception as e:
                print 'Utilities.py:guess_statement_language:Encoding Not Found:Error- ' + str(e) + repr(statement[:100])
                return 'error'
    statement_language=guessLanguage(u_statement)
    return statement_language
    return encoding_is 
def is_english(statement):#TO BE ADDED: Try and except
    if isinstance(statement,unicode):
        u_statement=statement
    else:
        encoding_is=get_encoding(statement)
        try:
            u_statement=unicode(statement,encoding_is)
        except Exception as e:
            print 'Utilities.py:is_english:Error- ' + str(e) + repr(statement[:100])
            return 'error'
    statement_language=guessLanguage(u_statement)
    if statement_language == 'en':
        return 'en'
    if statement_language == 'UNKNOWN': #temp fix- how to handle <20 chars
        return 'en'
    return statement_language#TO BE DISCARDED BELOW SECTION DELETE
    input_statement=statement.lower().strip(' \t\r\n')
    input_statement_aeiou=re.sub(r'[^aeiou]','',input_statement)
    input_statement_others=re.sub(r'[^a-z]','',input_statement)
    input_statement_others=re.sub(r'[^aeiou]','',input_statement_others)
    if input_statement_aeiou < (len(input_statement_others)/5):
        pass#return False
    input_statement_norm=re.sub(r'[^\w\'-]',' ',input_statement)
    input_statement_norm=re.sub(r' +',' ',input_statement_norm)
    input_statement_length=len(input_statement.split(' '))
    input_statement_stop_word_count=count_list_word_in_statement(input_statement_norm,stopwords_generic)
    if stopwords_density_part > 0:
        stopwords_density_part_is = stopwords_density_part/1.0
    else:
        stopwords_density_part_is = 6.0
    #print statement,input_statement_stop_word_count,input_statement_length,stopwords_density_part_is
    if input_statement_stop_word_count >= minimum_stop_word and input_statement_stop_word_count >= (input_statement_length/stopwords_density_part_is):
        return True
    if has_list_word_in_statement(input_statement_norm,key_leadership_words): return True
    if has_list_word_in_statement(input_statement_norm,key_events): return True
    return False
def is_link_to_news(statement):
    statement_lower=statement.lower()
    statement_lower=re.sub(r'[^\w-]',' ',statement_lower)
    statement_lower=re.sub(r'  ',' ',statement_lower)
    news_action_words=['read','more','view']#see
    news_key_words=['news','press','release','release','article','details','detail','more']
    if len(statement_lower.split())<=5:
        if has_list_word_in_statement(statement_lower,news_action_words) and has_list_word_in_statement(statement_lower,news_key_words):
            return True
    return False
def count_list_word_in_statement_delete(statement,list_of_words):
    count=0
    developer_mode=True
    statement_lower=statement.lower()
    statement_lower=' ' +  re.sub(r'[^\w-]',' ',statement_lower)  + ' '
    if developer_mode: print 'Utilities.py:count_list_word_in_statement: updated statement \t :' + statement_lower
    for each_word in list_of_words:
        match_found=statement_lower.count(' ' + each_word.lower() + ' ')
        if developer_mode: print 'Utilities.py:count_list_word_in_statement: Word: ' + str(each_word) +'\t Match found:' + str(match_found)
        count=count + match_found
    return count
def count_list_word_occurence_in_statement(statement,list_of_words_in,developer_mode=False):#,case_sensitive=False
    #It creates duplicate of count_list_word_in_statement
    consumed_words={}
    developer_mode=developer_mode
    list_of_words=[]
    if isinstance(list_of_words_in,str) or isinstance(list_of_words_in,unicode):
        for each_word in list_of_words_in.split():
            list_of_words.append(each_word)
    elif isinstance(list_of_words_in,list):
        list_of_words=list_of_words_in
    else:
        print 'Utilities.py:count_list_word_in_statement: list_of_words_in is not of type string or list. the data type is :' + str(type(list_of_words_in))
        custom_exit(ignore_error=True)
        return occurrence_count
        
    statement_lower=re.sub(r'[^\w]+',' ',statement.lower())
    statement_lower=' ' + re.sub(r' +',' ',statement_lower) + ' '
    statement_formatted=re.sub(r'[^\w]+',' ',statement)
    statement_formatted=' ' + re.sub(r' +',' ',statement_formatted) + ' '
    for each_word in list_of_words:#statement.split(): #Splitting the statement will not work if there are multiple word item in list_of_words
        #each_word_norm=re.sub(r'[^\w]+',' ',each_word.lower())
        #each_word_norm=re.sub(r' +',' ',each_word_norm).strip()
        if each_word == each_word.lower(): 
            statement_to_check=statement_lower
        else:
            statement_to_check=statement_formatted
        if ' ' + each_word + ' ' in statement_to_check:
            consumed_words[each_word] = consumed_words.get(each_word,0) + 1
    if consumed_words:
        return consumed_words.keys()
        #return [k:consumed_words[k] for k in consumed_words]
    return []
def fetch_dict_pattern_matching_statement_from_article(article_content,dict_pattern,restrict_by=0,one_statement_per_paragraph=False):
    if 'search_keyword' not in dict_pattern:
        print 'search_keyword is not a key in dict_pattern'
        custom_exit()
    finding_collection=[]
    statement_found=0
    break_all_the_way=False
    for each_paragraph in article_content.split('\n'):
        skip_please=False
        for each_statement in paragraph_to_sentence(each_paragraph):
            if skip_please: continue
            found_key=has_dict_pattern_in_statement(each_statement,dict_pattern)
            if found_key:
                statement_found += 1
                found_dictionary={}
                found_dictionary['matching_keys']=found_key
                found_dictionary['statement']=each_statement.strip(' \r\t\n')
                found_dictionary['paragraph']=each_paragraph
                finding_collection.append(found_dictionary.copy())
                if one_statement_per_paragraph: skip_please=True
                if restrict_by>0 and statement_found>=restrict_by:
                    break_all_the_way=True
            if break_all_the_way:
                break
        if break_all_the_way:
            break
    return finding_collection
def has_dict_pattern_in_statement(statement,input_dictionary):
    if 'search_keyword' not in input_dictionary: return False
    if not isinstance(input_dictionary['search_keyword'],list): return False
    if len(statement)<8: return False
    statement_lower=statement.lower()
    statement_lower=' ' +  re.sub(r'[^\w-]',' ',statement_lower)  + ' '
    for each_list_item in input_dictionary['search_keyword']:
        if ' ' + each_list_item.lower() + ' ' in statement_lower:
            found_word=each_list_item
            if found_word in input_dictionary:
                found_word_second_level=has_list_word_in_statement_tuple(statement_lower,input_dictionary[found_word])
                if found_word_second_level:
                    return found_word + '-' + found_word_second_level
            else:
                return found_word
    return False
def has_list_word_in_statement_tuple(statement,list_of_words):
    statement_lower=statement.lower()
    statement_lower=' ' +  re.sub(r'[^\w-]',' ',statement_lower)  + ' '
    for each_word in list_of_words:
        if isinstance(each_word,str) or isinstance(each_word,unicode):
            if ' ' + each_word.lower() + ' ' in statement_lower:
                return each_word
        elif isinstance(each_word,tuple):
            tuple_result=has_all_list_word_in_statement(statement_lower,each_word)
            if tuple_result:
                return tuple_result
        else:
            print 'Utilities. List of list is not supported in has_list_word_in_statement_tuple: list passed - ' + str(list_of_words)
            custom_exit()
    return False
# def has_list_word_in_statement(statement,list_of_words,pattern_to_replace=''):
    # statement_lower=statement.lower()
    # if pattern_to_replace:
        # replace_pattern=pattern_to_replace
    # else:
        # replace_pattern=r'[^\w-]'
    # statement_lower=' ' +  re.sub(replace_pattern,' ',statement_lower)  + ' '
    # statement_lower=re.sub(r' +',' ',statement_lower)
    # statement_as_it_is=' ' +  re.sub(replace_pattern,' ',statement)  + ' '
    # statement_as_it_is=re.sub(r' +',' ',statement_as_it_is)
    # # statement_as_it_is=re.sub(r'&',' ',statement_as_it_is)
    # for each_word in list_of_words:
        # # each_word =re.sub(r' +',' ',each_word)
        # # each_word =re.sub(r'[^\w-]',' ',each_word)
        # upper_case_indicator=False
        # if each_word == each_word.upper() and each_word.isalnum(): upper_case_indicator=True
        # if (not upper_case_indicator) and ' ' + each_word.lower() + ' ' in statement_lower:
            # return each_word
        # elif upper_case_indicator and ' ' + each_word + ' ' in statement_as_it_is:
            # return each_word
    # return False
def has_list_word_in_statement(statement,list_of_words,pattern_to_replace='',return_all_matches=False,handle_unicode=False):
    #/[\u2000-\u206F\u2E00-\u2E7F\\'!"#$%&()*+,\-.\/:;<=>?@\[\]^_`{|}~]/ General Punctuation block is \u2000-\u206F, and the Supplemental Punctuation block is \u2E00-\u2E7F.
    #Punctuation: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    if (not statement) or len(statement.strip(' \r\t\n')) == 0: return False
    statement_lower=statement.lower()
    if handle_unicode and isinstance(statement_lower,str):
        statement_lower=get_html_to_unicode_string(statement_lower)
    if handle_unicode:
        replace_pattern='[\'!"#$%&()*+,.\/:;<=>?@\[\]^_`{|}~]'# - hyphen excluded
        #\u2000-\u206F\u2E00-\u2E7F
    elif pattern_to_replace:
        replace_pattern=pattern_to_replace
    else:
        replace_pattern=r'[^\w-]'
    statement_lower=u' ' +  re.sub(replace_pattern,' ',statement_lower)  + u' '
    statement_as_it_is=u' ' +  re.sub(replace_pattern,' ',statement)  + u' '
    if handle_unicode:
        statement_lower = re.sub(ur'[\u2000-\u206F\u2E00-\u2E7F]+',' ',statement_lower)
        statement_as_it_is = re.sub(ur'[\u2000-\u206F\u2E00-\u2E7F]+',' ',statement_as_it_is)
    statement_lower=re.sub(r' +',' ',statement_lower)
    statement_as_it_is=re.sub(r' +',' ',statement_as_it_is)
    if return_all_matches:
        return_list=[]
    for each_word in list_of_words:
        upper_case_indicator=False
        if each_word == each_word.upper() and each_word.isalnum(): upper_case_indicator=True
        if isinstance(each_word,unicode):
            compare_word=u' ' + each_word + u' '
        else:
            compare_word=u' ' + get_html_to_unicode_string(each_word) + u' '
        if (not upper_case_indicator) and compare_word.lower() in statement_lower:
            if return_all_matches:
                return_list.append(each_word)
            else:
                return each_word
        elif upper_case_indicator and compare_word in statement_as_it_is:
            if return_all_matches:
                return_list.append(each_word)
            else:
                return each_word
    if return_all_matches:
        return return_list
    else:
        return False

def has_list_string_in_statement(statement,list_of_words):#will not add spaces before and after words
    statement_lower=statement.lower()
    statement_lower=' ' + statement_lower  + ' '
    for each_word in list_of_words:
        if each_word.lower() in statement_lower:
            return each_word
    return False
def count_list_word_in_statement(statement,list_of_words_in,case_sensitive=False,distinct_word=False):
    occurrence_count=0
    developer_mode=False
    check_againts_list=[]
    list_of_words=[]
    if isinstance(list_of_words_in,str) or isinstance(list_of_words_in,unicode):
        for each_word in list_of_words_in.split():
            list_of_words.append(each_word)
    elif isinstance(list_of_words_in,list):
        list_of_words=list_of_words_in
    else:
        print 'Utilities.py:count_list_word_in_statement: list_of_words_in is not of type string or list. the data type is :' + str(type(list_of_words_in))
        custom_exit()
        return occurrence_count
    if case_sensitive:
        check_againts_list=list_of_words
    else:
        for each_word in list_of_words:
            check_againts_list.append(each_word.lower())
    if distinct_word: 
        consumed_words=[]
    if developer_mode:
        print 'Utilities.py:count_list_word_in_statement:List of words:' + ','.join(check_againts_list)
    for each_word in statement.split():
        each_word_norm=re.sub(r'[^\w]+',' ',each_word.lower())
        each_word_norm=re.sub(r' +',' ',each_word_norm).strip()
        if not case_sensitive: 
            each_word_norm=each_word_norm.lower()
        if each_word_norm in check_againts_list:
            if distinct_word:
                if each_word_norm in consumed_words:
                    pass
                else:
                    occurrence_count += 1
                    consumed_words.append(each_word_norm)
            else:
                occurrence_count += 1
            if developer_mode: print 'Utilities.py:count_list_word_in_statement:\t Match found:each_word_norm: ' + str(each_word_norm)
        elif developer_mode:
            print 'Utilities.py:count_list_word_in_statement:\t Match NOT found: each_word_norm: ' + str(each_word_norm)
    return occurrence_count
def remove_list_word_in_statement(statement,list_of_words,case_sensitive=False):
    output_string=''
    for each_word in statement.split():
        each_word_norm=re.sub(r'[^a-z]+',' ',each_word.lower())
        each_word_norm=re.sub(r' +',' ',each_word_norm).strip()
        if each_word_norm in list_of_words:
            pass
        else:
            output_string=output_string + ' ' + each_word
    return output_string.strip()
    statement_lower=statement.lower()
    statement_lower=' ' + statement_lower  + ' '
    for each_word in list_of_words:
        if ' ' + each_word.lower() + ' ' in statement_lower:
            statement_lower=statement_lower.replace(each_word, ' ')
    return statement_lower
def stem_the_statement(input_statement):
    stemmer = stem.PorterStemmer()
    output_statement=''
    for word in input_statement.split():
        output_statement=output_statement + ' ' + stemmer.stem(word)
    return output_statement
def has_list_word_in_statement_case_sensitive(statement,list_of_words):
    statement_lower=statement.lower()
    #statement_lower=' ' +  re.sub(r'[^\w-]',' ',statement_lower)  + ' '
    statement_lower=' ' + statement_lower  + ' '
    #print statement_lower,list_of_words
    for each_word in list_of_words:
        if (' ' + each_word.lower() + ' ') in statement_lower:
            return each_word
    return False
def has_all_list_word_in_statement(statement,list_of_words):
    if isinstance(list_of_words,tuple): return has_all_list_word_in_statement(statement,list(list_of_words))
    found_word=False
    found_word_list=''
    statement_lower=statement.lower()
    statement_lower=' ' +  re.sub(r'[^\w-]',' ',statement_lower)  + ' '
    if isinstance(list_of_words,list):
        for each_word in list_of_words:
            if (' ' + each_word.lower() + ' ') in statement_lower:
                found_word=True
                found_word_list=found_word_list + '-' + each_word
            else:
                return False
    if found_word: return found_word_list.strip('-')
    return False
def fetch_all_years(data):
    try:
        list_of_year=[]
        input_data=' ' + re.sub(r'[^0-9]',' ',data.strip(' \n\r\t')) + ' '
        capture_year=re.findall('(\d{4})',input_data)
        if not capture_year: return list_of_year
        for each_year in capture_year:
            year_is=int(each_year)
            if year_is >= 1990 :
                list_of_year.append(year_is)
        return list_of_year
    except:
        return list_of_year
def has_a_years(data):
    try:
        input_data=' ' + re.sub(r'[^0-9]',' ',data.strip(' \n\r\t')) + ' '
        capture_year=re.findall('(\d{4})',input_data)
        if not capture_year: return False
        for each_year in capture_year:
            year_is=int(each_year)
            if year_is >= 1990 :
                return year_is
        return False
    except:
        return False
def _is_year(data):
    try:
        input_data=data.strip(' \n\r\t')
        capture_year=re.findall('^(\d{4})$',input_data)
        if not capture_year: return False
        year_is=int(capture_year[0])
        if year_is >= 1990 :
            return True
        return False
    except:
        return False
def get_all_dates(input_string,restrict_to=1):
    date_collection=[]
    input_data=input_string.strip(' \n\r\t')
    all_dates_are=re.findall(r'(([\w]{3,9})[\s]*([0-9]{1,2})[ ,]*([0-9]{4}))',input_data)
    if all_dates_are:
        for each_date in all_dates_are:
            if isinstance(each_date,tuple) and len(each_date) == 4:
                #print 'Expected',each_date[1],each_date[2],each_date[3]
                if has_list_word_in_statement(str(each_date[0]),months_long):
                    date_collection.append(str(each_date[1]) + ' ' + str(each_date[2]) + ', ' + str(each_date[3]))
            else:
                print each_date
    if len(date_collection) > 0: return date_collection[0]
    return date_collection
def remove_middle_name(name_string):
    output_string=''
    input_string=name_string.strip(' \r\n\t')
    if len(input_string) < 1: return name_string
    input_string_split=input_string.split()
    for each_word in input_string_split:
        if len(each_word) <= 2:
            pass
        else:
            output_string =output_string + ' ' + str(each_word)
    return output_string.strip()
def get_filename_from_url(input_url):
    result_filename = re.sub(r"[^A-Za-z0-9]+",'', repr(input_url))
    return result_filename[:250]
def is_company_generic(input_word):
    curr_word=input_word.lower().strip(' \n')
    if input_word == '.': return False
    if len(curr_word) <2: return False
    if curr_word[-1] == '.':
        #if curr_word == curr_word.upper():
        if curr_word in company_generic:
            return True
        else:
            return False
    else:
        return False
def is_salutation(input_word):
    curr_word=input_word.lower().strip(' \n')
    if input_word == '.': return False
    if len(curr_word) <2: return False
    if curr_word[-1] == '.':
        #if curr_word == curr_word.upper():
        if curr_word in salutation_generic:
            return True
        else:
            return False
    else:
        return False
def is_abbr(input_word):
    #Not considering all caps
    regex_result=re.findall(r'^[A-Za-z][\.]([A-Za-z][\.])*$',input_word)
    if regex_result:
        return True
    return False
def is_ending_word(input_word):
    curr_word=input_word.strip(' \n')
    if input_word == '.': return True
    if len(curr_word) <2: return False
    if curr_word[-1] == '.':
        #if curr_word == curr_word.upper():
        if is_abbr(curr_word) or is_salutation(curr_word) or is_company_generic(curr_word):
            return False
        else:
            return True
    else:
        return False
def create_directory(directory_name):
    if (not directory_name.strip()) or len(directory_name.strip()) == 0: return False
    if os.path.isdir(directory_name): return True
    try:
        os.makedirs(directory_name)
        return True
    except Exception as e:
        return False
def paragraph_to_sentence(input_statements):
    input_statements_split=input_statements.split()
    output_statements=[]
    current_statement=''
    sentence_completed=True
    for each_word in input_statements_split:
        #print 'Word: Ending,Abbr,Salute,Comp\t',each_word,is_ending_word(each_word),is_abbr(each_word),is_salutation(each_word),is_company_generic(each_word)
        if is_ending_word(each_word):
            current_statement = current_statement + ' ' + each_word
            output_statements.append(current_statement)
            current_statement=''
            sentence_completed=True
        else:
            current_statement = current_statement + ' ' + each_word
            sentence_completed=False
        #print each_word,is_ending_word(each_word),is_abbr(each_word)
    if not sentence_completed:
        output_statements.append(current_statement)
    return output_statements
def data_detail_extraction(message,content_type='Others'):
    if content_type.lower() not in ('title','content'): return message
    news_message = message.strip()  # re.sub("<[^<]+?>", " ", message)
    news_message_len=len(news_message)
    news_message_qualified_len = news_message_len / 2.0
    news_message = re.sub(" +", " ", news_message)
    if '-' in news_message:
        split_news = news_message.split(" - ")
        if len(split_news) <= 1:  return news_message
        output_message = ''
        split_count=0
        for each_split in split_news:
            if split_count == 0:
                output_message=each_split
                if len(output_message) >= news_message_qualified_len: return output_message
            else:
                output_message = output_message + ' - ' + each_split
                if len(output_message) >= news_message_qualified_len: return output_message
            split_count += 1
        return news_message
    else:
        return news_message
def data_detail_extraction_old(message, iteration=1):
    news_message = message  # re.sub("<[^<]+?>", " ", message)
    news_message = re.sub(" +", " ", news_message)
    try:
        if '-' in news_message:
            split_val1 = news_message.split(" - ")[-1].strip()
            split_val = re.sub(r'\(.+?\)\s*', '', split_val1)
            process_further = False
            if iteration == 1 and len(split_val) > 1 and len(split_val.split()) < 5:
                process_further = True
            elif iteration == 2 and len(split_val) > 1 and len(split_val.split()) < 3:
                process_further = True
            if process_further:
                if has_list_word_in_statement_case_sensitive(split_val, SPLIT_VAL_LIST):
                    ind_val = news_message.rfind(" - " + split_val1)
                    news_message = news_message[:ind_val]
                    news_message = news_message.strip()
                    if iteration == 1 and '-' in news_message:
                        return data_detail_extraction_old(news_message, iteration=2)
                    else:
                        return news_message
                else:
                    return news_message
            else:
                return news_message
        else:
            return news_message
    except:
        return news_message
def data_feed_identifier_extraction(message):
    news_message=get_statement_without_bracket(message)
    news_message = news_message.lower() #re.sub("<[^<]+?>", " ", message.lower())
    news_message = re.sub(r'[^a-z0-9]+', ' ', news_message)
    news_message = re.sub(" +", " ", news_message)
    news_message = remove_list_word_in_statement(news_message, COMP_EXTENSIONS + stopwords_generic)
    news_message = stem_the_statement(news_message)
    news_message = re.sub(r'[^a-z0-9]+', '', news_message)
    if len(news_message) < 5: return message
    return news_message
def company_name_normalizer(message):
    news_message=message.lower() #re.sub("<[^<]+?>", " ", message.lower())
    news_message = re.sub(r'[^\w-]', '', news_message)
    return news_message
def has_stock_symbols(post_title,company_ticker=None):
    if not company_ticker: return False
    post_title_standardized=re.sub(r'[^a-zA-Z:\(\)]+',' ',post_title)
    if '(NYSE:' + company_ticker + ')' in post_title_standardized: return True
    if '(NASDAQ:' + company_ticker + ')' in post_title_standardized: return True
    if '(' + company_ticker + ')' in post_title_standardized: return True
    return False
def extract_stock_symbols(post_title,company_ticker=None):
    pass
def is_analyst_post(post_title,company_name=None,company_ticker=None):
    if not post_title: return False
    if len(post_title)<7: return False
    if len(post_title.split()) < 2: return False
    #import re
    ticker_available=has_stock_symbols(post_title,company_ticker)
    string_with_ticker=['movers']
    analyst_dict_pattern={'search_keyword':['analyst','analysts','stock','stocks','shares','insider','price target','closing','brokerages','brokerage'
                        ,'rating','closes','earnings','earning','large','pre market','pre-market'
                        ,'strong','short interest','dividend','hits','hitting'
                        ,'raises','raised','cut','reiterated','reiterates','upgraded','downgraded','upgrades','downgrades']
                        ,'insider': ['trading','selling']
                        ,'closing':[('bell','report'),('bell','reports')]
                        ,'rating':['buy','hold','sell','credit']
                        ,'closes':[('on','day')]
                        ,'large':['inflow','outflow']
                        ,'strong':['buy','sell','hold','rating']
                        ,'raises':['buy','sell','hold','rating']
                        ,'raised':['buy','sell','hold','rating']
                        ,'cut':['buy','sell','hold','rating']
                        ,'reiterated':['buy','sell','hold','rating']
                        ,'reiterates':['buy','sell','hold','rating']
                        ,'upgraded':['buy','sell','hold','rating','accumulate']
                        ,'downgraded':['buy','sell','hold','rating','accumulate']
                        ,'upgrades':['buy','sell','hold','rating','accumulate']
                        ,'downgrades':['buy','sell','hold','rating','accumulate']
                        ,'hits':[('week','high'),('52-week','high'),('week','low'),('52-week','low')]
                        ,'hitting':[('week','high'),('52-week','high'),('week','low'),('52-week','low')]
                        }
    post_title_lower=' ' +  post_title.lower() + ' '
    post_title_standardized=re.sub(r'[^a-zA-Z]+',' ',post_title_lower)
    post_title_standardized=re.sub(r' +',' ',post_title_standardized)
    if (post_title_standardized.count(' nyse ') + post_title_standardized.count(' nasdaq '))>1: return 'nyse-nasdaq'
    analyst_pattern_found = has_dict_pattern_in_statement(post_title_lower,analyst_dict_pattern)
    if analyst_pattern_found: return analyst_pattern_found
    return False
def get_statement_without_bracket(statement,remove_braces=False, remove_square_brackets=False,hard_remove=False):
    output_statement=re.sub(REGEX_BETWEEN_BRACKER,' ' ,statement)
    output_statement=re.sub(r' +',' ',output_statement).strip()
    if len(output_statement) < 2: 
        if not hard_remove:
            return statement
        else:
            return output_statement
    if remove_braces:
        current_output_statement=re.sub(REGEX_BETWEEN_BRACES,' ' ,output_statement)
        current_output_statement=re.sub(r' +',' ',current_output_statement).strip()
        if len(current_output_statement) < 2: 
            if not hard_remove:
                return output_statement
            else:
                return current_output_statement
        output_statement=current_output_statement
    if remove_square_brackets:
        current_output_statement=re.sub(REGEX_BETWEEN_SQR_BRACKETS,' ' ,output_statement)
        current_output_statement=re.sub(r' +',' ',current_output_statement).strip()
        if len(current_output_statement) < 2: 
            if not hard_remove:
                return output_statement
            else:
                return current_output_statement
        output_statement=current_output_statement
    return output_statement
def is_google_robot_detection(page_content):
    if (not page_content) or len(page_content) <10: return False
    if has_all_list_word_in_statement(page_content,['detected','unusual traffic','not a robot']): return 'detected-unusual-traffic-not a robot'
    if has_all_list_word_in_statement(page_content,['form','action','CaptchaRedirect','type','characters']): return 'form-action-CaptchaRedirect-type-characters'
    return False
def get_news_must_match(company_id_in,developer_mode=False):
    company_id=company_id_in
    developer_mode=developer_mode
    remove_on_encounter=['com','net','of','and']
    company_abbr_tuple={'co':'(co,company)'
        ,'company':'(co,company)'
        ,'ltd':'(ltd,limited)'
        ,'limited':'(ltd,limited)'
        ,'pvt':'(pvt,private)'
        ,'private':'(pvt,private)'
        ,'inc':'(inc,incorporated)'
        ,'incorporated':'(inc,incorporated)'
        ,'corp':'(corp,corporation)'
        ,'corporation':'(corp,corporation)'
        ,'tech':'(tech,technology)'
        ,'technology':'(tech,technology)'
        ,'international':'(intl,international)'
        ,'intl':'(intl,international)'
        ,'sys':'(sys,system)'
        ,'system':'(sys,system)'
        ,'pty':'(pty,proprietary)'
        ,'proprietary':'(pty,proprietary)'
        }
    input_company_name=''
    company_id=get_statement_without_bracket(company_id)
    company_id_len=len(company_id)
    for c_iter in range(company_id_len):#1. re.sub(r'[a-zA-Z][&'`-][a-zA-Z] 2. r' [&'`-]',' ',3. r'[&'`-] ',' '
        each_letter=company_id[c_iter]
        if each_letter.isalnum():
            input_company_name=input_company_name + each_letter
        elif each_letter == '&' or each_letter == '-' or each_letter == "'" or each_letter == '`':
            if c_iter > 0 and c_iter < (company_id_len - 1):
                if company_id[c_iter - 1].isalnum() and company_id[c_iter + 1].isalnum():
                    input_company_name=input_company_name + each_letter
                else:
                    input_company_name=input_company_name + ' '
            else:
                input_company_name=input_company_name + ' '
        else:
            input_company_name=input_company_name + ' '
    if developer_mode:
        print 'input_company_name=',type(input_company_name),get_printable_string(input_company_name)
    input_company_name=re.sub(r' +',' ',input_company_name).strip()
    input_company_name_list_words=input_company_name.split()
    if len(input_company_name_list_words) == 1 or len(input_company_name)<4: return input_company_name.lower()
    news_must_match=''
    word_found=0
    letters_found=0
    has_special_symbol=False
    abbr_expanded=False
    has_letter=False
    longest_word_found=False#>=8 characters
    company_normalized_name=standardize_company_name_for_normalizer(company_id)
    #print 'Start:' + '\tInput' + str(company_id) 
    for each_word in input_company_name_list_words:
        if developer_mode: print 'Start:' + '\tInput' + get_printable_string(company_id) + '\tCurr Word:' + get_printable_string(each_word) + '\tCurr Output:' + get_printable_string(news_must_match)
        if each_word.lower() in remove_on_encounter: continue
        #if each_word.lower() in stopwords_generic and each_word.lower() not in ['a']: continue
        if word_found <2:#True for 1st and 2nd word
            if len(each_word) == 1:
                news_must_match = news_must_match + ' ' + str(each_word)
                letters_found +=1
                has_letter=True
                if letters_found == 2:
                    word_found += 1
                    letters_found = 0
            elif "'" in each_word or '`' in each_word:
                if "'" in each_word:
                    news_must_match = news_must_match + ' (' + each_word[:each_word.find("'")] + ',' +each_word.replace("'","")+ ')'
                else:
                    news_must_match = news_must_match + ' (' + each_word[:each_word.find("`")] + ',' +each_word.replace("`","")+ ')'
                word_found += 1
            elif '&' in each_word:#when string with & symbol is encounter, it gets more weightage.
                news_must_match = news_must_match + ' ' + each_word
                word_found += 2
                has_special_symbol=True
            elif is_pure_alphanum(each_word) and len(each_word)>3:#when alphanumeric words encounter it gets more weightage 
                news_must_match = news_must_match + ' ' + each_word
                word_found += 2
                has_special_symbol=True
            elif '-' in each_word:#when string with & symbol is encounter, it gets more weightage. We have problem with A-1 Fire , A-1 Equipment
                index_of_hyp=each_word.find('-')
                if index_of_hyp > (len(each_word)/3.0) and len(each_word)>6:
                    news_must_match = news_must_match + ' ' + each_word.replace('-',' ')
                else:
                    news_must_match = news_must_match + ' ' + each_word
                word_found += 2
                has_special_symbol=True
            elif word_found >0 and each_word.lower() in company_abbr_tuple:
                news_must_match = news_must_match + ' ' + company_abbr_tuple[each_word.lower()]
                word_found += 1
                abbr_expanded=True
            else:
                news_must_match = news_must_match + ' ' + str(each_word)
                word_found += 1
        else:
            #break
            if len(company_normalized_name.split()) > 4:
                news_must_match = news_must_match + ' ' + company_normalized_name.split()[-1]
                if developer_mode: print 'consuming last word from "company_normalized_name"=',company_normalized_name
            else:
                if each_word.lower() not in common_company_words:
                    news_must_match = news_must_match + ' ' + str(each_word)
                    if developer_mode: print 'adding word as it is=',each_word
                elif has_special_symbol and len(news_must_match)<=3:
                    if each_word.lower() in company_abbr_tuple:
                        news_must_match = news_must_match + ' ' + company_abbr_tuple[each_word.lower()]
                        if developer_mode: print 'common company word: replacing with tuple',each_word
                    else:
                        news_must_match = news_must_match + ' ' + str(each_word)
                        if developer_mode: print 'common company word:adding word as it is=',each_word
            break
        news_must_match=news_must_match.strip()
        if len(each_word)>=8: longest_word_found=True
        if word_found == 2:# and False:
            if developer_mode: print 'at word_found == 2, break start'
            if longest_word_found or len(news_must_match)>=13:break
            if len(company_normalized_name.split()) >4: break#it will not occur in real time
            if has_special_symbol and len(news_must_match)>3:
                if developer_mode: print 'break on special symbol',len(news_must_match)
                break
            if developer_mode: print 'at word_found == 2, didn\' break'
        #print 'End:' + '\tInput' + str(company_id) + '\tCurr Word:' + str(each_word) + '\tCurr Output:' + str(news_must_match)
    return news_must_match.lower().strip()
def get_company_name_without_common_words(company_name,duplicate_for_amp_hyphen=False,replace_char_for_amp_hyphen=' '):
    remove_on_encounter=['com','net']
    #common_company_words=['group','holding','holdings','llc','plc','industry','industries','us','usa','co','company','ltd','limited','pvt','private','inc','incorporated','corp','corporation','tech','technology','international','intl','sys','system']
    input_company_name=''
    if isinstance(company_name,str) or isinstance(company_name,unicode):
        pass
    else:
        print 'get_company_name_without_common_words. Expected input is string or unicode. But received:' + str(type(company_name))
        custom_exit()
    company_id_len=len(company_name)
    for c_iter in range(company_id_len):
        each_letter=company_name[c_iter]
        if each_letter.isalnum():
            input_company_name=input_company_name + each_letter
        elif each_letter == '&' or each_letter == '-' or each_letter == "'" or each_letter == '`':
            if c_iter > 0 and c_iter < (company_id_len - 1):
                if company_name[c_iter - 1].isalnum() and company_name[c_iter + 1].isalnum():
                    input_company_name=input_company_name + each_letter
                else:
                    input_company_name=input_company_name + ' '
            else:
                input_company_name=input_company_name + ' '
        else:
            input_company_name=input_company_name + ' '
    input_company_name=re.sub(r' +',' ',input_company_name).strip()
    input_company_name_list_words=input_company_name.split()
    if len(input_company_name_list_words) == 1 or len(input_company_name)<4: return input_company_name.lower()
    news_must_match=''
    word_found=0
    letters_found=0
    for each_word in input_company_name_list_words:
        if each_word.lower() in remove_on_encounter: continue
        if each_word.lower() in stopwords_generic: continue
        if len(each_word) == 1:
            news_must_match = news_must_match + ' ' + each_word
            letters_found +=1
            if letters_found == 2:
                word_found += 1
                letters_found = 0
        elif "'" in each_word or '`' in each_word:
            if "'" in each_word:
                news_must_match = news_must_match + ' ' + each_word[:each_word.find("'")]
            else:
                news_must_match = news_must_match + ' ' + each_word[:each_word.find("`")]
            word_found += 1
        elif '&' in each_word:
            index_of_hyp=each_word.find('&')
            if duplicate_for_amp_hyphen:
                if len(news_must_match) == 0:
                    news_must_match = each_word + '|' + each_word.replace('&',' ') + '|' + each_word.replace('&','')
                else:
                    news_must_match = news_must_match + ' ' + each_word + '|' + news_must_match + ' ' + each_word.replace('&',' ') + '|' + news_must_match + ' ' + each_word.replace('&','')
            else:
                news_must_match = news_must_match + ' ' + each_word.replace('&',replace_char_for_amp_hyphen)
            word_found += 2
        elif '-' in each_word:
            index_of_hyp=each_word.find('-')
            if duplicate_for_amp_hyphen:
                if len(news_must_match) == 0:
                    news_must_match = each_word + '|' + each_word.replace('-',' ') + '|' + each_word.replace('-','')
                else:
                    news_must_match = news_must_match + ' ' + each_word + '|' + news_must_match + ' ' + each_word.replace('-',' ') + '|' + news_must_match + ' ' + each_word.replace('-','')
            else:
                news_must_match = news_must_match + ' ' + each_word.replace('-',replace_char_for_amp_hyphen)
            word_found += 2
        elif word_found >0 and each_word.lower() in common_company_words:
            pass
        else:
            news_must_match = news_must_match + ' ' + each_word
            word_found += 1
        if word_found >= 2:break
    return news_must_match.lower().strip()
def get_company_name_standard(company_id): #name to be changed
    remove_on_encounter=['com','net']
    company_abbr_tuple={'company':'co'
        ,'limited':'ltd'
        ,'private':'pvt'
        ,'incorporated':'inc'
        ,'corporation':'corp'
        ,'technology':'tech'
        ,'international':'intl'
        ,'system':'sys'
        ,'proprietary':'pty'
        }
    input_company_name=''
    company_id_len=len(company_id)
    for c_iter in range(company_id_len):
        each_letter=company_id[c_iter]
        if each_letter.isalnum():
            input_company_name=input_company_name + each_letter
        elif each_letter == '&' or each_letter == '-' or each_letter == "'" or each_letter == '`':
            if c_iter > 0 and c_iter < (company_id_len - 1):
                if company_id[c_iter - 1].isalnum() and company_id[c_iter + 1].isalnum():
                    input_company_name=input_company_name + each_letter
                else:
                    input_company_name=input_company_name + ' '
            else:
                input_company_name=input_company_name + ' '
        else:
            input_company_name=input_company_name + ' '
    input_company_name=re.sub(r' +',' ',input_company_name).strip()
    input_company_name_list_words=input_company_name.split()
    if len(input_company_name_list_words) == 1 or len(input_company_name)<4: return input_company_name.lower()
    news_must_match=''
    word_found=0
    letters_found=0
    for each_word in input_company_name_list_words:
        if each_word.lower() in remove_on_encounter: continue
        if each_word.lower() in stopwords_generic: continue
        if len(each_word) == 1:
            news_must_match = news_must_match + ' ' + str(each_word)
            letters_found +=1
            if letters_found == 2:
                word_found += 1
                letters_found = 0
        elif "'" in each_word or '`' in each_word:
            if "'" in each_word:
                news_must_match = news_must_match + ' ' + each_word[:each_word.find("'")]
            else:
                news_must_match = news_must_match + ' ' + each_word[:each_word.find("`")]
            word_found += 1
        elif '&' in each_word:
            news_must_match = news_must_match + ' ' + each_word
            word_found += 2
        elif '-' in each_word:
            index_of_hyp=each_word.find('-')
            if index_of_hyp > (len(each_word)/3.0) and len(each_word)>6:
                news_must_match = news_must_match + ' ' + each_word.replace('-',' ')
            else:
                news_must_match = news_must_match + ' ' + each_word
            word_found += 2
        elif word_found >0 and each_word.lower() in company_abbr_tuple:
            news_must_match = news_must_match + ' ' + company_abbr_tuple[each_word.lower()]
            word_found += 1
        else:
            news_must_match = news_must_match + ' ' + str(each_word)
            word_found += 1
        if word_found >= 2:break
    return news_must_match.lower().strip()
def get_url_pattern(input_url):
    if not input_url: return ''
    if not isinstance(input_url,str): return ''
    url_is=input_url.upper()
    url_is=re.sub(r'[A-Z]','X',url_is)
    url_is=re.sub(r'[0-9]','9',url_is)
    url_is=re.sub(r'[^X9/?=]','$',url_is)
    return url_is
def get_common_url_pattern(list_of_path,keep_schema_unchanged=False,type='ur'):
    if not isinstance(list_of_path,list): return {}
    if not list_of_path: return {}
    common_path_prefix=os.path.commonprefix(list_of_path)
    list_of_path_pattern=[]
    list_of_path_pattern[:]=[]
    for each_path in list_of_path:
        list_of_path_pattern.append(get_url_pattern(each_path))
    common_path_pattern=os.path.commonprefix(list_of_path_pattern)
    if len(common_path_prefix) >= len(common_path_pattern):
        return {'prefix':common_path_prefix,'pattern':common_path_pattern}
    else:
        last_split_index=common_path_prefix.rfind('/')
        if last_split_index >= 0:
            common_path_prefix_new=common_path_prefix[:last_split_index]
            return {'prefix':common_path_prefix_new,'pattern':common_path_pattern}
        else:
            return {'prefix':common_path_prefix,'pattern':common_path_pattern}
    return {}
def get_file_as_list(file_name,skip_empty_lines=True):
    if not os.path.isfile(file_name): return []
    output_list=[]
    fr=open(file_name,'r')
    for each_line in fr:
        current_line=each_line.strip('\n')
        if (len(current_line) == 0 or (not current_line)) and skip_empty_lines: continue
        output_list.append(current_line)
    fr.close()
    return output_list


        
def select_statement(statement_in,type='news'):
    statement=statement_in.strip()
    if not statement: return False
    #statement=get_statement_without_bracket(statement,remove_braces=True, remove_square_brackets=True,hard_remove=True)
    if len(statement) > 600 or len(statement)<11:
        return False
    word_found_count=0
    statement_split=statement.lower().split()
    if statement_split <=5:
        return False
    for each_word in statement_split:
        if each_word in stopwords_generic:
            pass
        elif len(each_word) > 3:
            word_found_count += 1
    if word_found_count <= 3:
        return False
    statement_formatted=get_statement_without_bracket(statement,remove_braces=True, remove_square_brackets=True,hard_remove=True)
    if len(statement_formatted.split())<3: return False
    if type=='news' and ((len(statement_formatted) * 1.0) / len(statement) < 0.5): return False
    if type=='news' and ((len(re.sub(r'[A-Z]+','',' ' + statement_formatted)) * 1.0) / len(statement_formatted) < 0.6): return False
    if type == 'newsnew' and (len(statement_formatted) - len(re.sub(r'<[\w-]+>','',statement_formatted)))>2: return False
    return True
def unicode_to_decimal(in_string):
    try:
        d_code=int(in_string,16)
        return d_code
    except:
        return False
def get_printable_for_ord(ord_is):
    if not isinstance(ord_is,int): return False
    unicode_to_ascii_map = {8208: '-',
                    8210: '-',
                    8211: '-',
                    8212: '-',
                    8213: '-',
                    8215: '=',
                    8216: "'",
                    8217: "'",
                    8218: "'",
                    8219: "'",
                    8220: '"',
                    8221: '"',
                    8222: '"',
                    8223: '"'
                }
    if (ord_is >=32 and ord_is<=126) or ord_is in [9,10,13]:
        return chr(ord_is)
    elif ord_is in unicode_to_ascii_map:
        return unicode_to_ascii_map[ord_is]
    return False
def select_statement_new(statement_in,type='news'):
    statement=statement_in.strip()
    if not statement: return False
    statement=get_statement_without_bracket(statement,remove_braces=True, remove_square_brackets=True,hard_remove=True)
    if len(statement) > 600 or len(statement)<11:
        return False
    word_found_count=0
    statement_split=statement.lower().split()
    if type == 'news':
        if statement_split <=5:
            return False
        for each_word in statement_split:
            if each_word in stopwords_generic:
                pass
            elif len(each_word) > 3:
                word_found_count += 1
        if word_found_count <= 3:
            return False
    elif type == 'title':
        if statement_split <=3:
            return False
    return True
def get_printable_string(input_string,replace_by=' ',unicode_to_entitiy_flag=True,replace_html_entities=False,replace_lt_gt_symbol=False,developer_mode=False):
    #HTML Entity (decimal)    &#8217;
    #HTML Entity (hex)    &#x2019;r'[&][#]([0-9]{,5})[;]'
    if not (isinstance(input_string,str) or isinstance(input_string,unicode)): return input_string
    if isinstance(input_string,str):
        try:
            input_string=unicode(input_string,'utf-8')
        except Exception as e:
            pass
    entity_to_ascii_map={
                    '&ndash;': '-',
                    '&mdash;': '-',
                    '&quot;': '"',
                    '&ldquo;': '"',
                    '&rdquo;': '"',
                    '&lsquo;': "`",
                    '&apos;': "`",
                    '&rsquo;': "`",
                    '&nbsp;': ' ',
                    '&amp;': '&',
                    '&gt;': '>',
                    '&lt;': '<'
                }
    output_string=''
    developer_mode=developer_mode
    #developer_mode=True
    #if 'six hospitals offer free help with affordable insurance coverage' in input_string: 
        #print repr(input_string),'unicode_to_entitiy_flag=',unicode_to_entitiy_flag,'\t replace_html_entities=',replace_html_entities
        #developer_mode=True
    char_collection=''
    character_representation=''
    type_of_representation=''
    representation_set=False
    input_string_len=len(input_string)
    if unicode_to_entitiy_flag and replace_html_entities:
        replace_html_entities=False
    for iter_i in range(input_string_len):
        each_char=input_string[iter_i]
        if developer_mode and representation_set: print 'Entity::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
        if replace_html_entities:
            if each_char == '&':
                if representation_set:
                    #concatenate already collected string to output
                    output_string=output_string + char_collection
                    char_collection=''
                    representation_set=False
                    character_representation=''
                    type_of_representation=''
                if (iter_i+3) < input_string_len and input_string[iter_i+1] ==  '#' and input_string[iter_i+2] ==  'x' and ';' in input_string[iter_i:]:
                    type_of_representation='hex'
                elif (iter_i+2) < input_string_len and input_string[iter_i+1] ==  '#' and input_string[iter_i+2] !=  'x' and ';' in input_string[iter_i:]:
                    type_of_representation='dec'
                elif (iter_i+1) < input_string_len and ';' in input_string[iter_i:]:
                    type_of_representation='entity'
                if len(type_of_representation)>0:
                    representation_set=True
                    char_collection='&'
                else:
                    representation_set=False
                    output_string=output_string + each_char
                continue
            elif each_char == '#' and representation_set:
                if char_collection == '&' and ((not character_representation) or len(character_representation) == 0):
                    char_collection = char_collection + '#'
                else:
                    if developer_mode and representation_set: print 'Entity::# else::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                    output_string=output_string + char_collection + '#'
                    char_collection=''
                    representation_set=False
                    character_representation=''
                    type_of_representation=''
                continue
            elif each_char == 'x' and representation_set:
                if char_collection == '&#' and ((not character_representation) or len(character_representation) == 0):
                    char_collection = char_collection + 'x'
                else:
                    output_string=output_string + char_collection + 'x'
                    char_collection=''
                    representation_set=False
                    character_representation=''
                    type_of_representation=''
                continue
            elif each_char == ';' and representation_set:
                if developer_mode and representation_set: print 'Entity::completing with ',each_char,'::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                if len(character_representation) > 0 and len(char_collection)>0:
                    if type_of_representation == 'hex':
                        if developer_mode and representation_set: print 'Entity::Complete-hex::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                        c_o=unicode_to_decimal(character_representation)
                        if c_o:
                            c_o_h=get_printable_for_ord(c_o)
                            if c_o_h:
                                output_string=output_string + c_o_h
                            elif replace_by:
                                output_string=output_string + replace_by
                        elif replace_by:
                            output_string=output_string + replace_by
                    elif type_of_representation == 'dec':
                        if developer_mode and representation_set: print 'Entity::Complete-dec::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                        c_o=int(character_representation,10)
                        c_o_h=get_printable_for_ord(c_o)
                        if developer_mode and representation_set: print 'Entity::Complete-dec-decode::','\tc_o=',c_o,'\tc_o_h=',c_o_h
                        if c_o_h:
                            output_string=output_string + c_o_h
                        elif replace_by:
                            output_string=output_string + replace_by
                    elif type_of_representation == 'entity':
                        if developer_mode and representation_set: print 'Entity::Complete-entity::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                        if '&' + character_representation + ';' in entity_to_ascii_map:
                            if (not replace_lt_gt_symbol) and character_representation in ('lt','gt'):
                                output_string=output_string + '&' + character_representation + ';'
                            else:
                                output_string=output_string + entity_to_ascii_map['&' + character_representation + ';']
                        elif replace_by:
                            output_string=output_string + replace_by
                    else:
                        print 'get_printable_string: Logical error - type_of_representation=',type_of_representation
                        custom_exit()
                else:
                    if developer_mode and representation_set: print 'Entity::Complete-other::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                    output_string=output_string + char_collection + ';'
                char_collection=''
                representation_set=False
                character_representation=''
                type_of_representation=''
                continue
            elif representation_set:
                if developer_mode and representation_set: print 'Entity::char rep starts for ',each_char,'::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                if (type_of_representation == 'hex' and char_collection == '&#x') or (type_of_representation == 'dec' and char_collection == '&#') or (type_of_representation == 'entity' and char_collection == '&'):
                    if (is_number(each_char) or each_char == '0') and type_of_representation in ('hex','dec'):
                        character_representation = character_representation + each_char
                        continue
                    elif each_char.isalpha() and (type_of_representation == 'entity' or (type_of_representation == 'hex' and each_char.lower() in 'abcdef')):
                        character_representation = character_representation + each_char
                        continue
                output_string=output_string + char_collection + character_representation + each_char
                char_collection=''
                representation_set=False
                character_representation=''
                type_of_representation=''
                continue
        c_o=ord(each_char)
        if c_o > 126 and unicode_to_entitiy_flag:
            if developer_mode: print "Input:",repr(each_char),'\t ord=',c_o,'\toutput_string=',output_string
            output_string=output_string + '&#' + str(c_o) + ';'
            continue
        c_o_h=get_printable_for_ord(c_o)
        if developer_mode: print "Input:",repr(each_char),'\t ord=',c_o,'\tprint=',c_o_h
        if c_o_h:
            output_string=output_string + c_o_h
        elif replace_by:
            output_string=output_string + replace_by
    return output_string
def print_list(list_is,beautiful_print=True):
    if isinstance(list_is,list) or isinstance(list_is,tuple):
        for each in list_is:
            if isinstance(each,dict):
                print 'New Dictionary Item in print_list'
                for each_key in each:
                    print '\t',each_key,'\t:', each[each_key]
                print '\n'
            else:
                print each
                print '\n'
    elif isinstance(list_is,dict):
        for each_key in list_is:
            if isinstance(list_is[each_key],list):
                print '\t',each_key
                for each_list_item in list_is[each_key]:
                    print '\t\t\t:', each_list_item
            else:
                print '\t',each_key,'\t:', list_is[each_key]
        print '\n'
    else:
        print list_is
def print_list_new(list_is,depth_level=0,beautiful_print=True):
    print_prefix=''
    if depth_level>0:
        for i in range(depth_level):
            print_prefix=print_prefix +'\t'
    if isinstance(list_is,list) or isinstance(list_is,tuple):
        for each in list_is:
            if isinstance(each,str) or isinstance(each,unicode):
                print print_prefix + str(each)
                if beautiful_print: print ''
            else:
                print_list_new(each,depth_level=depth_level+1,beautiful_print=beautiful_print)
    elif isinstance(list_is,dict):
        print_empty_line=True
        for each_key in list_is:
            if isinstance(list_is[each_key],str) or isinstance(list_is[each_key],unicode):
                print print_prefix + str(each_key) +'\t:' + str(list_is[each_key])
            else:
                print_list_new(list_is[each_key],depth_level=depth_level+1,beautiful_print=beautiful_print)
                print_empty_line=False
        if beautiful_print and print_empty_line: print ''
    else:
        print print_prefix + str(list_is)
        if beautiful_print: print ''
def get_file_age(filename,use_modified_time=True,format='tuple'):
    if os.path.isfile(filename):
        if use_modified_time:
            time_elapsed=time.time() - os.path.getmtime(filename) # file content change
        else:
            time_elapsed=time.time() - os.path.getctime(filename) # change time - metadata related to physical file location change.
        time_elapsed_minutes=time_elapsed / 60
        time_elapsed_hours=time_elapsed / 3600
        time_elapsed_days=time_elapsed / 86400 # 24 * 60 * 60
        if format == 'tuple':
            return (time_elapsed_days,time_elapsed_hours,time_elapsed_hours,time_elapsed)
        elif format == 'days' or format == 'd':
            return time_elapsed_days
        elif format == 'hours'  or format == 'h':
            return time_elapsed_hours
        elif format == 'minutes'  or format == 'm':
            return time_elapsed_minutes
        elif format == 'seconds'  or format == 's':
            return time_elapsed
        else:
            return (time_elapsed_days,time_elapsed_hours,time_elapsed_hours,time_elapsed)
    else:
        return None


def fuzzy_compare(companyname, name):
    company_name = companyname.lower()
    try:
        facebook_company_name = name.lower()
        # Get the partial ratio between the two company names
        # Get the partial ratio between the two company names
        partial_ratio = fuzz.partial_ratio(company_name, facebook_company_name)
        # Get the token set ratio between the two company names
        set_ratio = fuzz.token_set_ratio(company_name, facebook_company_name)
        # Get the token sort ratio between the two company names
        sort_ratio = fuzz.token_sort_ratio(company_name, facebook_company_name)
        partial_value = round(partial_ratio, 2)
        token_set_value = round(set_ratio, 2)
        token_sort_value = round(sort_ratio, 2)
        if partial_value < 85 or token_set_value < 85 or token_sort_value < 85:
            # Replaces corporation, company, llc, inc, ltd, usa, international in company list with blank space
            removable_words = ['services','ltd','l.t.d','company','industry','lp','l.p',
                   'co', 'corporation', 'corporate', 'inc','industry', 'limited', 'energy',
                   'llc', 'inc.','usa','us','international', 'ems']
            company_name = company_name.replace('.','')
            company_name = re.sub(r"[^\w'-]"," ", company_name)
            query = company_name.split()
            for word in removable_words:
                if len(query) > 1:
                    for i in range(1, len(query)):
                        query[i] = query[i].strip()
                        if word == query[i]:
                            query.remove(word)
                            break
            query = ' '.join(query)
            username = query.strip()
            facebook_company_name = facebook_company_name.replace('.', '')
            facebook_company_name = re.sub(r"[^\w'-]", " ", facebook_company_name)
            facebook_query = facebook_company_name.split()
            for word in removable_words:
                if len(facebook_query) > 1:
                    for i in range(1, len(facebook_query)):
                        facebook_query[i] = facebook_query[i].strip()
                        if word == facebook_query[i]:
                            facebook_query.remove(word)
                            break
            facebook_query = ' '.join(facebook_query)
            facebook_name = facebook_query.strip()
            partial_ratio_ref = fuzz.partial_ratio(username,facebook_name)
            set_ratio_ref = fuzz.token_set_ratio(username,
                                                 facebook_name)
            sort_ratio_ref = fuzz.token_sort_ratio(username,
                                                   facebook_name)
            partial_value_ref = round(partial_ratio_ref, 2)
            token_set_value_ref = round(set_ratio_ref, 2)
            token_sort_value_ref = round(sort_ratio_ref, 2)
            if partial_value_ref < 85 or token_set_value_ref < 85 or token_sort_value_ref < 85:
                return round((partial_value_ref+token_set_value_ref+token_sort_value_ref)/3)
            else:
                return round((partial_value_ref+token_set_value_ref+token_sort_value_ref)/3)
        #else:
        return round((partial_value+token_set_value+token_sort_value)/3)
    except:
        return 'N/A'


def remove_unhealthy_html_tags(input_content):
    article_content=input_content.replace('\n',' ').replace('\r',' ').replace('\t',' ')
    article_content=re.sub(r' +',' ',article_content)
    article_content=re.sub(r'((<script)(?:(?!<\/script>).)*(<\/script>))','',article_content)
    article_content=re.sub(r'((<style)(?:(?!<\/style>).)*(<\/style>))','',article_content)
    article_content=re.sub(r'((<!--)(?:(?!-->).)*(-->))','',article_content)
    return article_content
def exit_custom(exit_message=None):
    custom_exit(exit_message)
def custom_exit(exit_message=None):
    if exit_message: print exit_message
    exit()
def abbreviate_name(input_name_in,upper_case_indicator=True):
    if isinstance(input_name_in,(str,unicode)):
        if upper_case_indicator:
            input_name=input_name_in.upper()
        else:
            input_name=input_name_in.lower()
        result_name = "".join(item[0] for item in re.findall("\w+", input_name))
        return result_name
    else:
        return None
def get_statement_matching_list(statement,words_to_match,case_sensitive=False,combine_the_statements=False,match_as_word=False):
    #match_as_word : if True, then has_list_string_in_statement should not be called. Future use
    category_for_match=False
    if isinstance(words_to_match,list):
        list_word_to_match=copy.deepcopy(words_to_match)
    elif isinstance(words_to_match,dict):
        list_word_to_match=list(words_to_match.keys())
        category_for_match=True
    else:
        custom_exit('get_statement_matching_list list_word_to_match is not list type. Type is ' + str(type(list_word_to_match)))
    if len(statement) < 5:
        return []
    output_result=[]
    previous_line=''
    current_line=''
    match_found_line=''
    match_found_indicator=False
    current_match={'previous_line':'','match_line':'','next_line':'','consume_next_line':False}
    statement_split=statement.split('\n')
    for each_line in statement_split:
        current_line=each_line#.lower()
        if (not current_line) or len(current_line.strip(' \t\r')) == 0: continue
        match_found=has_list_string_in_statement(current_line,list_word_to_match)
        if match_found:
            if match_found_indicator:
                if category_for_match:
                    current_match['next_line']=current_line
                    output_result.append(current_match.copy())
                    current_match['previous_line']=previous_line
                    current_match['match_line']=current_line
                    current_match['next_line']=''
                    current_match['consume_next_line']=False
                    current_match['found']=words_to_match[match_found]
                else:
                    current_match['match_line']=current_match['match_line'] + '\n' + current_line
                    current_match['found']=match_found
            else:
                current_match['match_line']=current_line
                current_match['previous_line']=previous_line
                if category_for_match:
                    current_match['found']=words_to_match[match_found]
                else:
                    current_match['found']=match_found
                match_found_indicator=True
        if match_found_indicator:
            if current_match['consume_next_line']:
                current_match['next_line']=current_line
                match_found_indicator=False
                output_result.append(current_match.copy())
                current_match['previous_line']=''
                current_match['match_line']=''
                current_match['next_line']=''
                current_match['consume_next_line']=False
            else:
                current_match['consume_next_line']=True
        previous_line=current_line
    if match_found_indicator and len(current_match['next_line']) == 0:
        output_result.append(current_match.copy())
    if len(output_result)>0 and combine_the_statements:
        for i in range(len(output_result)):
            output_result[i]['match_line']=output_result[i]['previous_line'] + '\n' + output_result[i]['match_line'] + '\n' + output_result[i]['next_line']
            output_result[i]['previous_line']=''
            output_result[i]['next_line']=''
    return output_result
'''
def massage_string_for_escape_character(input_string):#Delete
    #developer_mode=False
    if (not input_string) or len(input_string)==0:
        return input_string
    if '\\' not in input_string: 
        return input_string.replace('\n','\\n').replace('\r','\\r').replace('\t','\\t')
    #if developer_mode: print 'massage_string_for_escape_character:Input:',input_string
    #if developer_mode: print 'massage_string_for_escape_character:escape character index list:',escape_char_index
    last_char_is_escape=False
    output_string=''
    for idx in range(len(input_string)):
        curr_char=input_string[idx]
        #if developer_mode: print 'massage_string_for_escape_character:current character:' + str(curr_char),last_char_is_escape
        if last_char_is_escape:
            output_string=output_string + curr_char
            last_char_is_escape=False
        else:
            if curr_char in ['\\']:
                next_char_is=''
                if (idx +1) < len(input_string):
                    next_char_is=input_string[idx+1]
                if next_char_is and next_char_is in ['\\','n','r','t']:
                    output_string=output_string + curr_cha
                else:
                    output_string=output_string + curr_char + curr_char
                last_char_is_escape=Tru
            else:
                output_string=output_string + curr_char
                last_char_is_escape=False
        #if developer_mode: print 'massage_string_for_escape_character:output_string:' + str(output_string)
    if len(output_string) > 0:
        return output_string.replace('\n','\\n').replace('\r','\\r').replace('\t','\\t')
    return input_string.replace('\n','\\n').replace('\r','\\r').replace('\t','\\t')
'''

def get_top_occurrence(input_list):
    if isinstance(input_list,list):
        count_dict={}
        current_occurrence=0
        current_selection=''
        occurrence_details=[]
        all_top_occurences=[]
        for each_item in list(set(input_list)):
            temp_count=input_list.count(each_item)
            occurrence_details.append([each_item,temp_count])
            if temp_count > current_occurrence:
                    current_occurrence=temp_count
                    current_selection=each_item
        occurrence_details.sort(key=lambda x: x[1],reverse=True)
        if current_occurrence <= 1:
            return (current_selection,0,occurrence_details,all_top_occurences)
        else:
            for each_record in occurrence_details:
                if each_record[1] == current_occurrence:
                    if each_record[0] not in all_top_occurences:
                        all_top_occurences.append(each_record[0])
            return (current_selection,current_occurrence,occurrence_details,all_top_occurences)
    if isinstance(input_list,str) or isinstance(input_list,unicode): return (input_list,0,[],[])
    if isinstance(input_list,tuple): return get_top_occurrence(list(input_list))
    return ('',0)
def get_html_to_unicode_string(input_string):
    print_prefix='get_html_to_unicode_string:\t'
    entity_to_ascii_map={
                    '&ndash;': '-',
                    '&mdash;': '-',
                    '&quot;': '"',
                    '&ldquo;': '"',
                    '&rdquo;': '"',
                    '&lsquo;': "`",
                    '&apos;': "`",
                    '&rsquo;': "`",
                    '&nbsp;': ' ',
                    '&amp;': '&',
                    '&gt;': '>',
                    '&lt;': '<'
                }
    
    entity_to_unicode_master={
                    #,'&lt;':60
                    #,'&gt;':62
                    '&quot;':34
                    ,'&amp;':38
                    ,'&apos;':39
                    ,'&nbsp;':160
                    ,'&iexcl;':161
                    ,'&cent;':162
                    ,'&pound;':163
                    ,'&curren;':164
                    ,'&yen;':165
                    ,'&brvbar;':166
                    ,'&sect;':167
                    ,'&uml;':168
                    ,'&copy;':169
                    ,'&ordf;':170
                    ,'&laquo;':171
                    ,'&not;':172
                    ,'&shy;':173
                    ,'&reg;':174
                    ,'&macr;':175
                    ,'&deg;':176
                    ,'&plusmn;':177
                    ,'&sup2;':178
                    ,'&sup3;':179
                    ,'&acute;':180
                    ,'&micro;':181
                    ,'&para;':182
                    ,'&middot;':183
                    ,'&cedil;':184
                    ,'&sup1;':185
                    ,'&ordm;':186
                    ,'&raquo;':187
                    ,'&frac14;':188
                    ,'&frac12;':189
                    ,'&frac34;':190
                    ,'&iquest;':191
                    ,'&Agrave;':192
                    ,'&Aacute;':193
                    ,'&Acirc;':194
                    ,'&Atilde;':195
                    ,'&Auml;':196
                    ,'&Aring;':197
                    ,'&AElig;':198
                    ,'&Ccedil;':199
                    ,'&Egrave;':200
                    ,'&Eacute;':201
                    ,'&Ecirc;':202
                    ,'&Euml;':203
                    ,'&Igrave;':204
                    ,'&Iacute;':205
                    ,'&Icirc;':206
                    ,'&Iuml;':207
                    ,'&ETH;':208
                    ,'&Ntilde;':209
                    ,'&Ograve;':210
                    ,'&Oacute;':211
                    ,'&Ocirc;':212
                    ,'&Otilde;':213
                    ,'&Ouml;':214
                    ,'&times;':215
                    ,'&Oslash;':216
                    ,'&Ugrave;':217
                    ,'&Uacute;':218
                    ,'&Ucirc;':219
                    ,'&Uuml;':220
                    ,'&Yacute;':221
                    ,'&THORN;':222
                    ,'&szlig;':223
                    ,'&agrave;':224
                    ,'&aacute;':225
                    ,'&acirc;':226
                    ,'&atilde;':227
                    ,'&auml;':228
                    ,'&aring;':229
                    ,'&aelig;':230
                    ,'&ccedil;':231
                    ,'&egrave;':232
                    ,'&eacute;':233
                    ,'&ecirc;':234
                    ,'&euml;':235
                    ,'&igrave;':236
                    ,'&iacute;':237
                    ,'&icirc;':238
                    ,'&iuml;':239
                    ,'&eth;':240
                    ,'&ntilde;':241
                    ,'&ograve;':242
                    ,'&oacute;':243
                    ,'&ocirc;':244
                    ,'&otilde;':245
                    ,'&ouml;':246
                    ,'&divide;':247
                    ,'&oslash;':248
                    ,'&ugrave;':249
                    ,'&uacute;':250
                    ,'&ucirc;':251
                    ,'&uuml;':252
                    ,'&yacute;':253
                    ,'&thorn;':254
                    ,'&yuml;':255
                    ,'&OElig;':338
                    ,'&oelig;':339
                    ,'&Scaron;':352
                    ,'&scaron;':353
                    ,'&Yuml;':376
                    ,'&fnof;':402
                    ,'&circ;':710
                    ,'&tilde;':732
                    ,'&Alpha;':913
                    ,'&Beta;':914
                    ,'&Gamma;':915
                    ,'&Delta;':916
                    ,'&Epsilon;':917
                    ,'&Zeta;':918
                    ,'&Eta;':919
                    ,'&Theta;':920
                    ,'&Iota;':921
                    ,'&Kappa;':922
                    ,'&Lambda;':923
                    ,'&Mu;':924
                    ,'&Nu;':925
                    ,'&Xi;':926
                    ,'&Omicron;':927
                    ,'&Pi;':928
                    ,'&Rho;':929
                    ,'&Sigma;':931
                    ,'&Tau;':932
                    ,'&Upsilon;':933
                    ,'&Phi;':934
                    ,'&Chi;':935
                    ,'&Psi;':936
                    ,'&Omega;':937
                    ,'&alpha;':945
                    ,'&beta;':946
                    ,'&gamma;':947
                    ,'&delta;':948
                    ,'&epsilon;':949
                    ,'&zeta;':950
                    ,'&eta;':951
                    ,'&theta;':952
                    ,'&iota;':953
                    ,'&kappa;':954
                    ,'&lambda;':955
                    ,'&mu;':956
                    ,'&nu;':957
                    ,'&xi;':958
                    ,'&omicron;':959
                    ,'&pi;':960
                    ,'&rho;':961
                    ,'&sigmaf;':962
                    ,'&sigma;':963
                    ,'&tau;':964
                    ,'&upsilon;':965
                    ,'&phi;':966
                    ,'&chi;':967
                    ,'&psi;':968
                    ,'&omega;':969
                    ,'&thetasym;':977
                    ,'&upsih;':978
                    ,'&piv;':982
                    ,'&ensp;':8194
                    ,'&emsp;':8195
                    ,'&thinsp;':8201
                    ,'&zwnj;':8204
                    ,'&zwj;':8205
                    ,'&lrm;':8206
                    ,'&rlm;':8207
                    ,'&ndash;':8211
                    ,'&mdash;':8212
                    ,'&lsquo;':8216
                    ,'&rsquo;':8217
                    ,'&sbquo;':8218
                    ,'&ldquo;':8220
                    ,'&rdquo;':8221
                    ,'&bdquo;':8222
                    ,'&dagger;':8224
                    ,'&Dagger;':8225
                    ,'&bull;':8226
                    ,'&hellip;':8230
                    ,'&permil;':8240
                    ,'&prime;':8242
                    ,'&Prime;':8243
                    ,'&lsaquo;':8249
                    ,'&rsaquo;':8250
                    ,'&oline;':8254
                    ,'&frasl;':8260
                    ,'&euro;':8364
                    ,'&image;':8465
                    ,'&weierp;':8472
                    ,'&real;':8476
                    ,'&trade;':8482
                    ,'&alefsym;':8501
                    ,'&larr;':8592
                    ,'&uarr;':8593
                    ,'&rarr;':8594
                    ,'&darr;':8595
                    ,'&harr;':8596
                    ,'&crarr;':8629
                    ,'&lArr;':8656
                    ,'&uArr;':8657
                    ,'&rArr;':8658
                    ,'&dArr;':8659
                    ,'&hArr;':8660
                    ,'&forall;':8704
                    ,'&part;':8706
                    ,'&exist;':8707
                    ,'&empty;':8709
                    ,'&nabla;':8711
                    ,'&isin;':8712
                    ,'&notin;':8713
                    ,'&ni;':8715
                    ,'&prod;':8719
                    ,'&sum;':8721
                    ,'&minus;':8722
                    ,'&lowast;':8727
                    ,'&radic;':8730
                    ,'&prop;':8733
                    ,'&infin;':8734
                    ,'&ang;':8736
                    ,'&and;':8743
                    ,'&or;':8744
                    ,'&cap;':8745
                    ,'&cup;':8746
                    ,'&int;':8747
                    ,'&there4;':8756
                    ,'&sim;':8764
                    ,'&cong;':8773
                    ,'&asymp;':8776
                    ,'&ne;':8800
                    ,'&equiv;':8801
                    ,'&le;':8804
                    ,'&ge;':8805
                    ,'&sub;':8834
                    ,'&sup;':8835
                    ,'&nsub;':8836
                    ,'&sube;':8838
                    ,'&supe;':8839
                    ,'&oplus;':8853
                    ,'&otimes;':8855
                    ,'&perp;':8869
                    ,'&sdot;':8901
                    ,'&lceil;':8968
                    ,'&rceil;':8969
                    ,'&lfloor;':8970
                    ,'&rfloor;':8971
                    ,'&lang;':9001
                    ,'&rang;':9002
                    ,'&loz;':9674
                    ,'&spades;':9824
                    ,'&clubs;':9827
                    ,'&hearts;':9829
                    ,'&diams;':9830
    }
    if isinstance(input_string,unicode):
        intermediate_string=input_string
    elif isinstance(input_string,str):
        current_encoding=get_encoding(input_string)
        #print 'current_encoding',current_encoding
        if current_encoding:
            try:
                intermediate_string=unicode(input_string,current_encoding)
            except Exception as e:
                print 'get_html_to_unicode_string: Logical:Encoding Found: Error-:' + str(e) + repr(input_string[:100])
                exit()
        else:
            try:
                intermediate_string=input_string.decode('utf-8')
            except Exception as e:
                #Temp approach to send get_printable_string
                #http://www.beyondsoft.com/aboutus#overview '\x81@ \x81@'
                print 'Utilities.py:get_html_to_unicode_string:Encoding Not Found:Error- ' + str(e) + '\t Input:' + repr(input_string[:100])
                return get_printable_string(input_string)
                exit()
    else:
        print 'Utilities.py:get_html_to_unicode_string: Either str or unicode expected. Received:'+ str(type(input_string))
        input_string.startswith('ErrorExit')
        custom_exit()
    output_string=u''
    output_list=[]
    output_list_method=True
    developer_mode=False
    char_collection=''
    character_representation=''
    type_of_representation=''
    representation_set=False
    replace_html_entities=True
    input_string_len=len(intermediate_string)
    if developer_mode: print print_prefix + '\t' + str(get_timestamp_for_file(True)) + '\t' + 'replace_html_entities:' + str(replace_html_entities)
    for iter_i in range(input_string_len):
        each_char=intermediate_string[iter_i]
        if developer_mode and representation_set: print 'Entity::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
        if replace_html_entities:
            if each_char == '&':
                if developer_mode: print print_prefix + '\t' + str(iter_i) + '\t:\t' + str(get_timestamp_for_file(True)) + '\t' + 'current character = &'
                if representation_set:
                    #concatenate already collected string to output
                    if not output_list_method:
                        output_string=output_string + char_collection
                    else:
                        output_list.append(char_collection)
                    char_collection=''
                    representation_set=False
                    character_representation=''
                    type_of_representation=''
                if (iter_i+3) < input_string_len and intermediate_string[iter_i+1] ==  '#' and intermediate_string[iter_i+2] ==  'x' and ';' in intermediate_string[iter_i:]:
                    type_of_representation='hex'
                elif (iter_i+2) < input_string_len and intermediate_string[iter_i+1] ==  '#' and intermediate_string[iter_i+2] !=  'x' and ';' in intermediate_string[iter_i:]:
                    type_of_representation='dec'
                elif (iter_i+1) < input_string_len and ';' in intermediate_string[iter_i:]:
                    type_of_representation='entity'
                if len(type_of_representation)>0:
                    representation_set=True
                    char_collection='&'
                else:
                    representation_set=False
                    if not output_list_method:
                        output_string=output_string + each_char
                    else:
                        output_list.append(each_char)
                continue
            elif each_char == '#' and representation_set:
                if developer_mode: print print_prefix + '\t' + str(iter_i) + '\t:\t' + str(get_timestamp_for_file(True)) + '\t' + 'current character = # and representation_set is True'
                if char_collection == '&' and ((not character_representation) or len(character_representation) == 0):
                    char_collection = char_collection + '#'
                else:
                    if developer_mode and representation_set: print 'Entity::# else::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                    if not output_list_method:
                        output_string=output_string + char_collection + '#'
                    else:
                        output_list.append(char_collection + '#')
                    char_collection=''
                    representation_set=False
                    character_representation=''
                    type_of_representation=''
                continue
            elif each_char == 'x' and representation_set:
                if developer_mode: print print_prefix + '\t' + str(iter_i) + '\t:\t' + str(get_timestamp_for_file(True)) + '\t' + 'current character = x and representation_set is True'
                if char_collection == '&#' and ((not character_representation) or len(character_representation) == 0):
                    char_collection = char_collection + 'x'
                else:
                    if not output_list_method:
                        output_string=output_string + char_collection + 'x'
                    else:
                        output_list.append(char_collection + 'x')
                    char_collection=''
                    representation_set=False
                    character_representation=''
                    type_of_representation=''
                continue
            elif each_char == ';' and representation_set:
                if developer_mode: print print_prefix + '\t'  + str(iter_i) + '\t:\t' + str(get_timestamp_for_file(True)) + '\t' + 'current character = ";" and representation_set is True'
                if developer_mode and representation_set: print 'Entity::completing with ',each_char,'::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                if len(character_representation) > 0 and len(char_collection)>0:
                    if type_of_representation == 'hex':
                        if developer_mode and representation_set: print 'Entity::Complete-hex::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                        c_o=unicode_to_decimal(character_representation)
                        if c_o:
                            try:
                                if not output_list_method:
                                    output_string=output_string + unichr(c_o)
                                else:
                                    output_list.append(unichr(c_o))
                            except:
                                if not output_list_method:
                                    output_string=output_string + ' '
                                else:
                                    output_list.append(' ')
                        else:
                            if not output_list_method:
                                output_string=output_string + ' '
                            else:
                                output_list.append(' ')
                    elif type_of_representation == 'dec':
                        if developer_mode and representation_set: print 'Entity::Complete-dec::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                        c_o=int(character_representation,10)
                        if c_o:
                            try:
                                if not output_list_method:
                                    output_string=output_string + unichr(c_o)
                                else:
                                    output_list.append(unichr(c_o))
                            except:
                                if not output_list_method:
                                    output_string=output_string + ' '
                                else:
                                    output_list.append(' ')
                        else:
                            if not output_list_method:
                                output_string=output_string + ' '
                            else:
                                output_list.append(' ')
                    elif type_of_representation == 'entity':
                        if developer_mode and representation_set: print 'Entity::Complete-entity::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                        if '&' + character_representation + ';' in entity_to_ascii_map:
                            if not output_list_method:
                                output_string=output_string + entity_to_ascii_map['&' + character_representation + ';']
                            else:
                                output_list.append(entity_to_ascii_map['&' + character_representation + ';'])
                        elif '&' + character_representation + ';' in entity_to_unicode_master:
                            try:
                                if not output_list_method:
                                    output_string=output_string + unichr(entity_to_unicode_master['&' + character_representation + ';'])
                                else:
                                    output_list.append(unichr(entity_to_unicode_master['&' + character_representation + ';']))
                            except:
                                if not output_list_method:
                                    output_string=output_string + ' '
                                else:
                                    output_list.append(' ')
                        else:
                            if not output_list_method:
                                output_string=output_string + ' '
                            else:
                                output_list.append(' ')
                    else:
                        print 'get_printable_string: Logical error - type_of_representation=',type_of_representation
                        sys.exit()
                else:
                    if developer_mode and representation_set: print 'Entity::Complete-other::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                    if not output_list_method:
                        output_string=output_string + char_collection + ';'
                    else:
                        output_list.append(char_collection + ';')
                char_collection=''
                representation_set=False
                character_representation=''
                type_of_representation=''
                continue
            elif representation_set:
                if developer_mode: print print_prefix + '\t' + str(iter_i) + '\t:\t' + str(get_timestamp_for_file(True)) + '\t'  + 'representation_set is True'
                if developer_mode and representation_set: print 'Entity::char rep starts for ',each_char,'::','\tchar_collection=',char_collection,'\tcharacter_representation=',character_representation,'\ttype_of_representation=',type_of_representation
                if (type_of_representation == 'hex' and char_collection == '&#x') or (type_of_representation == 'dec' and char_collection == '&#') or (type_of_representation == 'entity' and char_collection == '&'):
                    if (is_number(each_char) or each_char == '0') and type_of_representation in ('hex','dec'):
                        character_representation = character_representation + each_char
                        continue
                    elif each_char.isalpha() and (type_of_representation == 'entity' or (type_of_representation == 'hex' and each_char.lower() in 'abcdef')):
                        character_representation = character_representation + each_char
                        continue
                if not output_list_method:
                    output_string=output_string + char_collection + character_representation + each_char
                else:
                    output_list.append(char_collection + character_representation + each_char)
                char_collection=''
                representation_set=False
                character_representation=''
                type_of_representation=''
                continue
        if developer_mode: print print_prefix + '\t' + str(iter_i) + '\t:\t' + str(get_timestamp_for_file(True)) + '\t' + 'After replace_html_entities block'
        if not output_list_method:
            output_string=output_string + each_char
        else:
            output_list.append(each_char)
    if output_list_method:
        output_string=u''.join(output_list)
    return output_string
def check_all_combination_abbreviation(input_full_form,input_abbreviation,check_half_name_match,developer_mode=False,check_stopwords_removal_too=True):
    if check_stopwords_removal_too:
        current_result=check_all_combination_abbreviation(input_full_form=input_full_form,input_abbreviation=input_abbreviation,check_half_name_match=check_half_name_match,developer_mode=developer_mode,check_stopwords_removal_too=False)
        if current_result:
            return current_result
        stopwords_in_company=['and','of','the']
        temp_string=' ' + re.sub(r'[^a-z0-9]+',' ',input_full_form.lower()) + ' '
        for each_word in stopwords_in_company:
            temp_string=temp_string.replace(each_word,' ')
        temp_string=re.sub(r' +',' ',temp_string)
        current_result=check_all_combination_abbreviation(input_full_form=temp_string,input_abbreviation=input_abbreviation,check_half_name_match=check_half_name_match,developer_mode=developer_mode,check_stopwords_removal_too=False)
        return current_result
    #check_half_name_match - 8i Holding matches with 8i. When false, 8i Holding does not match with 8i but 8h or 8ih
    print_prefix='check_all_combination_abbreviation\t'
    name_full_form=input_full_form.strip().lower()
    name_full_form=re.sub(r'[^a-z0-9]+',' ',name_full_form)
    name_full_form=re.sub(r' +',' ',name_full_form)
    name_abbreviation=input_abbreviation.strip().lower()
    name_abbreviation=re.sub(r'[^a-z0-9]+','',name_abbreviation)
    abbreviation_length=len(name_abbreviation)
    if developer_mode: print print_prefix + 'Input:' + input_full_form + '\tAbbr:' + input_abbreviation
    if abbreviation_length <= 1 or len(name_full_form)<=1:
        if developer_mode: print print_prefix + 'Abbreviation/Input Legnth is less than 1'
        return False
    if ' ' not in name_full_form:
        if input_full_form == input_abbreviation:
            if developer_mode: print print_prefix + 'Single word input exactly matches with abbreviation'
            return True
        else:
            if developer_mode: print print_prefix + 'Single word input does not match with abbreviation'
            return False
    current_abbreviation_index=0
    looping_count=0
    name_full_form_words=name_full_form.split()
    name_full_form_words_length=len(name_full_form_words)
    current_input_index=0
    while looping_count <= (abbreviation_length + 1) and current_abbreviation_index < abbreviation_length:
        looping_count += 1
        current_input_word=name_full_form_words[current_input_index]
        current_remaining_abbreviation_part=name_abbreviation[current_abbreviation_index:]
        if developer_mode: print print_prefix + 'Abbrevation remaining:' + current_remaining_abbreviation_part + '(' + str(len(current_remaining_abbreviation_part)) + ')\tCurrent Input word:' + current_input_word
        if current_remaining_abbreviation_part.startswith(current_input_word):
            current_abbreviation_index += len(current_input_word)
            current_input_index += 1
            if developer_mode: print print_prefix + 'current word of input(' + current_input_word + ') is a part of abbrevation. Advance to next character.'
        elif current_input_word[0] == current_remaining_abbreviation_part[0]:
            if developer_mode: print print_prefix + 'Current character of abbrevation(' + current_input_word[0] + ') is matching with first char of input(' + current_input_word + '). Advance to next character.'
            current_abbreviation_index += 1
            current_input_index += 1
        else:
            if developer_mode: print print_prefix + 'Abbreviation does not match when processing word:' + current_input_word
            return False
        if current_abbreviation_index >= abbreviation_length:
            #Matches fully 
            if current_input_index >= name_full_form_words_length:
                if developer_mode: print print_prefix + 'All strings are consumed and matches with abbreviation'
                return True
            else:
                if check_half_name_match:
                    if developer_mode: print print_prefix + 'The part of input (first few words) are matching with abbreviation'
                    return True
                else:
                    if developer_mode: print print_prefix + 'Abbrevation is a part of input string and still a part of input string is unmatched'
                    return False
        if current_input_index >= name_full_form_words_length:
            #The function is at the deciding state
            if current_abbreviation_index >= name_full_form_words_length: #
                if developer_mode: print print_prefix + 'All strings are consumed and matches with abbreviation'
                return True
            else:
                if developer_mode: print print_prefix + 'All strings are consumed and but abbrevation is not matching completely'
                return False
    return False
def string_fits_one_in_another(string_1,string_2,perfect_fit=True):#unicode handling is pending
    developer_mode=False
    if (not string_1) or (not string_2): return False
    if len(string_1)<2 or len(string_2)<2: return False
    string_1_formatted=string_1.lower().strip()
    string_1_formatted=re.sub(r'[^a-z0-9]',' ',string_1_formatted)#removed all unicode data
    string_2_formatted=string_2.lower().strip()
    string_2_formatted=re.sub(r'[^a-z0-9]',' ',string_2_formatted)#removed all unicode data
    string_2_remaining=string_2_formatted
    string_matches=True
    found_atleast_once=False
    for each_word in string_1_formatted.split():
        string_2_formatted = ' ' + string_2_formatted.strip() + ' '
        if developer_mode:
            print 'String 1: current word:' + repr(each_word)
        compare_word=each_word
        if len(each_word) <= 2 or perfect_fit:#logical failure when als in minerals
            compare_word = ' ' + compare_word + ' '
        if compare_word in ' ' + string_2_remaining + ' ':
            string_2_remaining=string_2_remaining.replace(compare_word,' ',1)
            string_matches=True
            found_atleast_once=True
        else:
            string_matches=False
            break
    if string_matches and found_atleast_once:
        return True
    string_matches=True
    found_atleast_once=False
    for each_word in string_2_formatted.split():
        string_1_formatted = ' ' + string_1_formatted.strip() + ' '
        if developer_mode:
            print 'String 2: current word:' + repr(each_word)
        compare_word=each_word
        if len(each_word) <= 2 or perfect_fit:#logical failure when als in minerals
            compare_word = ' ' + compare_word + ' '
        if compare_word in ' ' + string_1_formatted + ' ':
            string_1_formatted=string_1_formatted.replace(compare_word,' ',1)
            string_matches=True
            found_atleast_once=True
        else:
            string_matches=False
            break
    if string_matches and found_atleast_once: return True
    return False
def make_company_name_comparable(input_company_name):
    developer_mode=False
    company_abbr_dot={
    'l.p':'lp'
    ,'p.l.c':'plc'
    }
    company_abbr_standardize={u'co':u'company'
        ,u'company':u'company'
        ,u'ltd':u'limited'
        ,u'limited':u'limited'
        ,u'pvt':u'private'
        ,u'private':u'private'
        ,u'pte':u'private'
        ,u'inc':u'incorporated'
        ,u'incorporated':u'incorporated'
        ,u'corp':u'corporation'
        ,u'corporation':u'corporation'
        ,u'tech':u'technology'
        ,u'technology':u'technology'
        ,u'international':u'international'
        ,u'intl':u'international'
        ,u'sys':u'system'
        ,u'system':u'system'
        ,u'pty':u'proprietary'
        ,u'proprietary':u'proprietary'
        }
    input_modified=get_html_to_unicode_string(input_company_name.lower())
    input_modified=get_html_to_unicode_string(input_modified)#do we need this?
    if u'.' in input_modified:
        intermediate_string=''
        for each_word in input_modified.split():
            if each_word.strip(',.') in company_abbr_dot:
                intermediate_string=intermediate_string + u' ' + company_abbr_dot[each_word.strip(',.')]
            else:
                intermediate_string=intermediate_string + u' ' + each_word
        input_modified=intermediate_string
    input_string_len=len(input_modified)
    
    output_string=u''
    current_word=u''
    for iter_i in range(input_string_len):
        each_char=input_modified[iter_i]
        char_code=ord(each_char)
        temp_char=u''
        break_happens=False
        if developer_mode:
            print str(iter_i) + '.Before:Char:' + get_printable_string(each_char) + '(' +str(char_code) + ')\tC-Word:' + get_printable_string(current_word) + '\tC-Output:' + get_printable_string(output_string)
        if char_code>126:
            if developer_mode:
                print str(iter_i) + ':Char:' + get_printable_string(each_char) + '(' +str(char_code) + '): Break point - Unicode'
            temp_char=each_char
            break_happens=True
        elif each_char.isdigit():
            current_word=current_word + each_char
        elif each_char.isalpha():
            current_word=current_word + each_char
        else:
            if developer_mode:
                print str(iter_i) + ':Char:' + get_printable_string(each_char) + '(' +str(char_code) + '): Break point - Non-Unicode'
            temp_char=u' '
            break_happens=True
        if break_happens or (iter_i+1) == input_string_len:
            if developer_mode:
                print str(iter_i) + ':Char:' + get_printable_string(each_char) + '(' +str(char_code) + '): Break point - Code'
            if len(current_word.strip())>0:
                if current_word.strip() in company_abbr_standardize:
                    output_string = output_string + u' ' + company_abbr_standardize[current_word.strip()]
                else:
                    output_string = output_string + current_word
                current_word=temp_char
            else:
                if developer_mode:
                    print str(iter_i) + ':Char:' + get_printable_string(each_char) + '(' +str(char_code) + '): Break point - Code : Current word is empty'
                current_word=temp_char
                output_string=output_string + u' '
        if (iter_i+1) == input_string_len:
            output_string=output_string + temp_char
            break
        if developer_mode:
            print str(iter_i) + '.After:Char:' + get_printable_string(each_char) + '(' +str(char_code) + ')\tC-Word:' + get_printable_string(current_word) + '\tC-Output:' + get_printable_string(output_string)
    return output_string
def get_absolute_path(parent_url,child_url):
    #self.current_function_name='get_absolute_path'
#view-source:http://www.asml.com/asml/show.do?lang=EN&ctx=231
# www.asml.com/asml/show.do?lang=EN&ctx=231 + show.do?lang=EN&amp;ctx=28904&amp;rid=16712 = http://www.asml.com/asml/show.do?lang=EN&ctx=28904&rid=16712
#Answer is given http://stackoverflow.com/questions/5559578/having-links-relative-to-root
#So doing / will make it relative to www.example.com, is there a way to specify what the root is, e.g what if i want the root to be www.example.com/fruits in www.example.com/fruits/apples/apple.html?

#Also handle "http://www.wabashnational.com/../news"
    if not (len(parent_url.strip())>1 and len(child_url.strip())>0): return parent_url
    try:
        return urljoin(parent_url,child_url)
    except ValueError as e:#To escape IPv4 Value error. Ex: url= http://www.balfourbeattyinvestments.com/cookies.aspx . href: http://www.balfourbeatty.com[insert 
        print 'get_absolute_path: Exception for P=' + parent_url + '. c=' + child_url + '. Error:' + str(e)
        return ''
def guess_name_for_domain(input_statement,domain_name,developer_mode=False,check_stopwords_removal_too=True):
    if check_stopwords_removal_too:
        current_result=guess_name_for_domain(input_statement=input_statement,domain_name=domain_name,developer_mode=developer_mode,check_stopwords_removal_too=False)
        if current_result:
            return current_result
        stopwords_in_company=['and','of','the']
        #temp_string=' ' + re.sub(r'[^a-z0-9]+',' ',input_statement.lower()) + ' '
        temp_string=' ' + re.sub(r'[^A-Za-z0-9]+',' ',input_statement) + ' '
        modified_string=''
        for each_word in temp_string.split():
            if each_word.lower() in stopwords_in_company:
                pass
            else:
                modified_string = modified_string + ' ' + each_word
        temp_string=modified_string
        temp_string=re.sub(r' +',' ',temp_string)
        current_result=guess_name_for_domain(input_statement=temp_string,domain_name=domain_name,developer_mode=developer_mode,check_stopwords_removal_too=False)
        return current_result
    print_prefix='guess_name_for_domain\t'
    name_full_form=get_html_to_unicode_string(input_statement).strip()
    name_full_form=re.sub(r'[^A-Za-z0-9]+',' ',name_full_form)
    name_full_form=re.sub(r' +',' ',name_full_form)
    domain_name_modified=domain_name.strip().lower()
    domain_name_modified=re.sub(r'[^a-z0-9]+','',domain_name_modified)
    domain_name_length=len(domain_name_modified)
    if developer_mode: print print_prefix + 'Input:' + name_full_form + '\t Domain Name:' + domain_name_modified
    if domain_name_length <= 1 or len(name_full_form)<=1:
        if developer_mode: print print_prefix + 'Domain Name/Input Legnth is less than 1'
        return False
    if ' ' not in name_full_form:
        if name_full_form.lower() == domain_name_modified:
            if developer_mode: print print_prefix + 'Single word input exactly matches with Domain Name'
            return name_full_form
        elif name_full_form.lower() in domain_name_modified:
            if developer_mode: print print_prefix + 'Single word input is part of Domain Name'
            return name_full_form
        else:
            if developer_mode: print print_prefix + 'Single word input does not match with Domain Name'
            return ''
    #return ''
    current_domain_index=0
    looping_count=0
    name_full_form_words=name_full_form.split()
    name_full_form_words_length=len(name_full_form_words)
    current_input_index=0
    matching_string=''
    while looping_count <= (domain_name_length + 1) and current_domain_index < domain_name_length:
        looping_count += 1
        current_input_word=name_full_form_words[current_input_index]
        current_input_word_lower=current_input_word.lower()
        current_remaining_domain_name_part=domain_name_modified[current_domain_index:]
        if developer_mode: print print_prefix + 'Domain Name remaining:' + current_remaining_domain_name_part + '(' + str(len(current_remaining_domain_name_part)) + ')\tCurrent Input word:' + current_input_word
        if current_remaining_domain_name_part.startswith(current_input_word_lower):
            matching_string = matching_string + ' ' + current_input_word
            current_domain_index += len(current_input_word)
            current_input_index += 1
            if developer_mode: print print_prefix + 'current word of input(' + current_input_word + ') is a part of abbrevation. Advance to next character.'
        elif current_input_word_lower[0] == current_remaining_domain_name_part[0]:
            matching_string = matching_string + ' ' + current_input_word
            if developer_mode: print print_prefix + 'Current character of abbrevation(' + current_input_word[0] + ') is matching with first char of input(' + current_input_word + '). Advance to next character.'
            current_domain_index += 1
            current_input_index += 1
        else:
            if developer_mode: print print_prefix + 'Abbreviation does not match when processing word:' + current_input_word
            return matching_string
        if current_domain_index >= domain_name_length:
            #Matches fully 
            return matching_string
        if current_input_index >= name_full_form_words_length:
            #The function is at the deciding state
            return matching_string
    return matching_string
if __name__ == '__main__':
    if True:
        keyword_list=[u'forespørsler']
        statement_is=u'Tradisjonelt har fasader i Norge, Sverige og Dan‘ ’ ‚ ‛ “ ” „ ‟ † ‡ • ‣ ․ ‥ …mark handlet om behandling av granpanel eller furukledning. Men de siste 3-5 årene har vi fått stadig flere forespørsler om andre treslag til fasade.'
        print repr(has_list_word_in_statement(statement_is,keyword_list,handle_unicode=True))
        exit()
    elif not True:
        company_name_list=[u'Dürr Systems Inc']
        for each_company in company_name_list:
            news_must_match=get_news_must_match(each_company,developer_mode=True)
            print get_printable_string(company_name_list),'news_must_match:',news_must_match,type(news_must_match)
        exit()
    elif not True:
        print has_list_word_in_statement('oil & gas exploration df natural gas & pipelines LynWoodward, Founder of the Activate Your Mind Program Lyn had been involved in the Health and Fitness Industry',['oil   gas'])
    elif not True:
        list_of_string_pair=[
            ('ATI Technologies','Empower Technologies Corporation'),
            ('Digital Journal Inc ','digitaljournal.com'),
            ('Noventis Credit Union Ltd ','Noventis Credit Union'),
            ('Choquette Cks Inc ','Choquette-cks'),
            ('Jog Capital Corp ','JOG Capital'),
            ('Istar Internet Inc','INTER.NET CANADA CORP'),
            ('Kronos Acquisition Holdings Inc ','KIK Custom Products Inc'),
            ('Kobelt Manufacturing Co Ltd','Kobelt Manufacturing Co. Ltd'),
            ('Greys Corp','Greys Paper Recycling Industries'),
            ('Nrt Technologies Inc ','NRT Technology Corp'),
            ('Nautical Lands Group ','Nautical Lands Group'),
            ('Fiera Properties Ltd ','Fiera Immobilier'),
            ('Liquid Capital Corp ','Liquid Capital'),
            ('Browning Insurance Ltd ','Browning Insurance Ltd'),
            ('Locemia Solutions Ulc ','Locemia Solutions'),
            ('தினமலர்','தின மலர் .com'),
            ('A2so4 Architecture LLC','これで解決！遺産相続にまつわる様々な問題'),
            ('Argosy Energy Inc ','売ってしまう事も土地活用方法の一つ～土地売却の注意点！ ALLRIGHTS RESERVED'),
            ('Casio Electronics Co. Ltd.','CASIO ELECTRONICS CO. LIMITED'),
            ('FilterBoxx Water and Environmental Corp','FilterBoxx Water & Environmental Corporation'),
            ('Bruce Power LP','Bruce Power L.P'),
            ('Alcidion Corp Pty Ltd','Alcidion Group Limited')
        ]
        for each_string_pair in list_of_string_pair:
            print 'String 1:\t' + get_printable_string(each_string_pair[0]) + '\tString 2:\t' + get_printable_string(each_string_pair[1]) + '\tResult:\t' + str(string_fits_one_in_another(each_string_pair[0],each_string_pair[1])) + '\tStandard Result:\t' + str(string_fits_one_in_another(make_company_name_comparable(each_string_pair[0]),make_company_name_comparable(each_string_pair[1]))) + '\tStr1 Standardized:\t' + get_printable_string(make_company_name_comparable(each_string_pair[0])) + '\tStr2 Standardized:\t' + get_printable_string(make_company_name_comparable(each_string_pair[1]))
            break
        custom_exit()
    elif not True:
        print get_all_files(directory_is=os.getcwd(),pattern='*.process')
        exit()
    elif not True:
        #print move_processed_file(file_name='core_stage_post_feed.log',target_directory='psql_processed',rename_with_timestamp=True,create_sub_directory=True)
        #print move_processed_file(file_name='core_stage_post_feed.psql',target_directory='psql_processed',rename_with_timestamp=True,create_sub_directory=True)
        print move_processed_file(file_name='*.txt',target_directory='D:\\_data\\logs',rename_with_timestamp=False,create_sub_directory=True)
        exit()
    elif not True:
        input_string='&#8220;some language display  &#x5A;&#x5a&#9986; &#90; space is "&#032;" "Hypher minus=&#045;".\nSingle quote="" &lt;'
        #input_string='some &#x5A;&#x5a;&#90; &lt; &venr;'
        print "input_string=",repr(input_string)
        print "Output=",get_printable_string(input_string,unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
        exit()
    elif not True:
        news_link_like_keywords=['news','press','releases','blog','media']
        statement_list=['https://inquicker.com/facility/medpost-urgent-care-gilbert'
                    ,'https://www.abrazohealth.com/our-locations/hospital-abrazo-scottsdale-campus/our-news'
                    ,'http://www.mediapost.com/publications/article/245469/in-store-wi-fi-40-now-going-to-76-this-year.html'
                    ,'http://www.atlantichealth.org/atlantic/media+center/contact+us:+public+relations+team'
                    ,'http://www.assurant.com/en/NewsRoom/AllNews/NewsReleases/2015/July/Assurant-2015-Property-Catastrophe-Reinsurance-Program'
                    ,'http://www.assurant.com/en/Room/All/2015/10/13/Assurant-2015-Property-Catastrophe-Reinsurance-Program'
                    ]
        for each_statement in statement_list:
            print each_statement,'\t=\t',is_a_press_release_link(each_statement),'\t',has_list_string_in_statement(each_statement,news_link_like_keywords),'\t',get_smell_like_date_from_url(each_statement)
        exit()
    if True:
        statement_is=['business---financial-press | Sep 4, 2015','07 August 2015','05/01/2015','07/23/2015','25/6/2015','25/23/2015'
                ,'by R Jagannathan  Aug 13, 2015 20:12 IST'
                ,'PTI | Aug 13, 2015, 02.39 PM IST'
                ,'Published August 2014 FoxNews.com'
                ,'Trade News | Aug 14, 2015'
                ,'The following Western Digital (WDC - Get Report) conference call took place on July 29, 2015, 05:00 PM ET. This is a '
                ,'PAYSON, Ariz. (July 30, 2015) &#8211;'
                ,'Western Digital Sets July 29 For Q4 Fiscal 2015 Financial Results Conference Call/Webcast'
                ,'Veronique Sablereau, Corporate Communications Manager -- Europe Phone: +33 1 30 60 70 68, '
                ,'NEW YORK, NY NATIONAL RETAIL FEDERATION SHOW, Booth #1356, January 12, 2015'
                ,'Technology transfer / Economic Impact (99)'
                ,'24 / Apr / 2015 &#160;&#160;Ambuj Parihar  '
                ,' &nbsp;(Dec. 31,2013) '
                ,' (Sept. 21, 2015)'
                ,' - October 16, 1996'
                ,'July 03, 2015'
                ]
        for each_statement in statement_is[-1:]:
            print 'is smell like date: ',each_statement,'=',get_smell_like_date_from_text(each_statement,maximum_year=2200,developer_mode=True)
            #print 'get_statement_for_word_count: ',each_statement,'=',get_statement_for_word_count(each_statement)
            #exit()
        for each_statement in statement_is:
            pass#print 'is smell like date: ','Valid ' + each_statement + ' execuse me' ,'=',get_smell_like_date_from_text('Valid ' + each_statement + ' execuse me')
        exit()
    elif not True:
        statement_is=['07 August 2015','05/01/2015','07/23/2015','25/6/2015','25/23/2015']
        for each_statement in statement_is:
            print 'is_date of ',each_statement,'=',is_date(each_statement)
        exit()
    elif not True:
        print get_file_as_list('Testing_semaphore.auto.process')
        print get_file_as_list('Testing_semaphore.auto.process',skip_empty_lines=False)
        exit()
    elif not True:
        companies=[
            '3M Company',
            '7-Eleven, Inc.',
            'A Schulman Inc',
            'A. O. Smith Corporation',
            'AAR Corp.',
            'AB Volvo',
            'ABB Ltd.',
            'Abbott Laboratories',
            'AbbVie Inc',
            'Abercrombie & Fitch Co.',
            'Macy`s, Inc.',
            'Macy\'s, Inc.'
            ]
        for each_company in companies:
            print each_company,'\t\t',standardize_company_name_for_normalizer(each_company)
        exit()
    elif not True:
        statement_is=''
        with open('D:\\_data\\post_feed\\Utitlities_samples.txt','r') as f:
            statement_is = f.read()
        print_list(fetch_dict_pattern_matching_statement_from_article(statement_is
            ,{'search_keyword':['acquisitions by','acquisition of ','acquired','to acquire','acquires','for acquiring']}
            ,restrict_by=0
            ,one_statement_per_paragraph=True
            ))
        exit()
    elif not True:
        statement_is='Mid-Day Changers: PHI Inc. (PHIIK), GoPro, Inc. (GPRO), Titan International Inc ... - WallStreet Scope'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='STMicroelectronics NV Upgraded by Banca Akros to Accumulate (STM) - Dakota Financial News'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Shares of General Mills, Inc. (NYSE:GIS) Sees Large Inflow of Net Money Flow - Money Flow Index'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Ecolab Schedules Webcast of Industry Conference for May 19 - Finances.com'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Consumer Goods Sector Movers: Ecolab Inc. (ECL), Dr Pepper Snapple Group ... - WallStreet Scope'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Can General Mills, Inc. (NYSE:GIS) Surprise Analysts? - Investor Newswire'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Consumer Goods Sector Movers: Ecolab Inc. (ECL), Sanderson Farms, Inc ... - WallStreet Scope'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='News Buzz - Applied Micro Circuits (AMCC), Ecolab (ECL), Net Ease (NTES ... - Techsonian (press release)'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Morning Stock Trends: J. C. Penney Company, Inc. (JCP), Adobe Systems ... - WallStreet Scope'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Can Estee Lauder (EL) Continue its Business Momentum? - Zacks.com'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Monday Pre-Market Info: Park-Ohio Holdings Corp. (PKOH), Michael Kors ... - WallStreet Scope'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='STMicroelectronics NV Stock Rating Upgraded by Banca Akros (STM) - The Legacy'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Stock Watchlist: Tempur Sealy International, Inc. (NYSE:TPX) - The Markets Daily'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='New Report From Adobe Systems Incorporated (NASDAQ:ADBE) Reveals Apple ... - WallStreetPR (blog)'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='Today`s Morning Insights: Everest Re Group Ltd. (RE), HSN, Inc. (HSNI), Energy ... - WallStreet Scope'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        statement_is='John B. Morse, Jr. Sells 10000 Shares of HSN Stock (HSNI) - WKRB News'
        print statement_is,'\nIs Analyst:',is_analyst_post(statement_is),'\nStatement with no bracker:',get_statement_without_bracket(statement_is),'\nRemove generic words:',remove_list_word_in_statement(statement_is,COMP_EXTENSIONS + stopwords_generic),'\n','Stemming:',stem_the_statement(statement_is),'\n','data_feed_identifier:',data_feed_identifier_extraction(statement_is),'\n'
        exit()
    elif not True:
        statement_is='Accuride Corp. (ACW) is Trading Lower on Unusual Volume for June 15 - Reuters - Reuters -  Thomson Reuters UK '
        print statement_is,':',has_dict_pattern_in_statement(statement_is,{'search_keyword':['trading','june'],'trading':['agust'],'june':['uk']})
        statement_is='Accuride Corp. (ACW) is Trading Lower on Unusual Volume for June 15 - Reuters - Reuters -  Thomson Reuters UK '
        print statement_is,':',has_dict_pattern_in_statement(statement_is,{'search_keyword':['trading','june'],'june':['uk']})
        statement_is='Accuride Corp. (ACW) is Trading Lower on Unusual Volume for June 15 - Reuters - Reuters -  Thomson Reuters UK '
        print statement_is,':',has_dict_pattern_in_statement(statement_is,{'search_keyword':['trading','june'],'trading':['agust']})
        statement_is='Accuride Corp. (ACW) is Trading Lower on Unusual Volume for June 15 - Reuters - Reuters -  Thomson Reuters UK '
        print statement_is,':',has_dict_pattern_in_statement(statement_is,{'search_keyword':['trading','june'],'trading':[('lower','june'),'thomson'],'june':[('lower','uk')]})
        exit()
    elif not True:
        statement_is='Slow it - Reuters - Firstpost (press release)'
        print statement_is,'=',data_detail_extraction(statement_is)
        statement_is='Nike seen avoiding charges in football bribery probe lawyers - Reuters - Firstpost (press release)'
        print statement_is,'=',data_detail_extraction(statement_is)
        statement_is='Mid-Day Changers: PHI Inc. (PHIIK), GoPro, Inc. (GPRO), Titan International Inc ... - WallStreet Scope'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='STMicroelectronics NV Upgraded by Banca Akros to Accumulate (STM) - Dakota Financial News'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Shares of General Mills, Inc. (NYSE:GIS) Sees Large Inflow of Net Money Flow - Money Flow Index'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Ecolab Schedules Webcast of Industry Conference for May 19 - Finances.com'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Consumer Goods Sector Movers: Ecolab Inc. (ECL), Dr Pepper Snapple Group ... - WallStreet Scope'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Can General Mills, Inc. (NYSE:GIS) Surprise Analysts? - Investor Newswire'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Consumer Goods Sector Movers: Ecolab Inc. (ECL), Sanderson Farms, Inc ... - WallStreet Scope'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='News Buzz - Applied Micro Circuits (AMCC), Ecolab (ECL), Net Ease (NTES ... - Techsonian (press release)'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Morning Stock Trends: J. C. Penney Company, Inc. (JCP), Adobe Systems ... - WallStreet Scope'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Can Estee Lauder (EL) Continue its Business Momentum? - Zacks.com'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Monday Pre-Market Info: Park-Ohio Holdings Corp. (PKOH), Michael Kors ... - WallStreet Scope'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='STMicroelectronics NV Stock Rating Upgraded by Banca Akros (STM) - The Legacy'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Stock Watchlist: Tempur Sealy International, Inc. (NYSE:TPX) - The Markets Daily'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='New Report From Adobe Systems Incorporated (NASDAQ:ADBE) Reveals Apple ... - WallStreetPR (blog)'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='Today`s Morning Insights: Everest Re Group Ltd. (RE), HSN, Inc. (HSNI), Energy ... - WallStreet Scope'
        print statement_is,':',data_detail_extraction(statement_is)
        statement_is='John B. Morse, Jr. Sells 10000 Shares of HSN Stock (HSNI) - WKRB News'
        print statement_is,':',data_detail_extraction(statement_is)
        print "****************"
        print statement_is1,'=',data_feed_identifier_extraction(data_detail_extraction(statement_is))
        #print statement_is,'=',has_list_word_in_statement_case_sensitive(statement_is,['equities.com'])
        exit()
    elif not True:
        statement_is=r'This is http://t.co/wrxeyhduis'
        print statement_is,' Remove URL:',re.sub(REGEX_URL_PATTERN,'',statement_is)
        exit()
    elif not True:
        print 'move_processed_file psql_processed:',move_processed_file('core_stage_topics_trending.psql','psql_processed')
        print 'rename_file_to_time_stamp_prefix:',rename_file_to_time_stamp_prefix(os.path.join(os.getcwd(),os.path.join('psql_processed','core_stage_topics_trending.psql')))
        exit()
    elif not True:
        print 'Create directory: psql_processed:',create_directory('psql_processed')
        exit()
    elif not True:
        statement_is='26 FAQs people freds ask about issuing fred\'s and transferring private company shares.'
        pattern_is='people transferring'
        print statement_is,'\t',pattern_is,'\t',statement_has_string_sequential(statement_is,pattern_is)
        pattern_is='people (transferring)'
        print statement_is,'\t',pattern_is,'\t',statement_has_string_sequential(statement_is,pattern_is)
        pattern_is='people (about,company) and'
        print statement_is,'\t',pattern_is,'\t',statement_has_string_sequential(statement_is,pattern_is)
        pattern_is='people (company,about) and'
        print statement_is,'\t',pattern_is,'\t',statement_has_string_sequential(statement_is,pattern_is)
        pattern_is='people (company,about) ask'
        print statement_is,'\t',pattern_is,'\t',statement_has_string_sequential(statement_is,pattern_is)
        pattern_is='(fred,fred\'s) (company,about) (share,shares)'
        print statement_is,'\t',pattern_is,'\t',statement_has_string_sequential(statement_is,pattern_is)
        exit()
    elif not True:
        print '(FAQs,public)','26   FAQs people ask about issuing and transferring private company shares.',get_index_of_special_tuple('26   FAQs people ask about issuing and transferring private company shares.','(FAQs,public)')
        print '\n\n\n\n','(public,FAQs)','26   FAQs people ask about issuing and transferring private company shares.',get_index_of_special_tuple('26   FAQs people ask about issuing and transferring private company shares.','(public,FAQs)')
        print '\n\n\n\n','(FAQspublic)','26  FAQs people ask about issuing and transferring private company shares.',get_index_of_special_tuple('26 FAQs people ask about issuing and transferring private company shares.','(FAQspublic)')
        print '\n\n\n\n','(ask,about,issuing,and,transferring,private,company,shares,26)','aa 26 FAQs people ask about issuing and transferring private company shares.',get_index_of_special_tuple(' 26 FAQs people ask about issuing and transferring private company shares.','(ask,about,issuing,and,transferring,private,company,shares,26)')
        exit()
    elif not True:
        print '26 FAQs people ask about issuing and transferring private company shares.',has_list_word_in_statement_tuple('26 FAQs people ask about issuing and transferring private company shares.',['FAQs','public'])
        print '26 FAQs people ask about issuing and transferring private company shares.',has_list_word_in_statement_tuple('26 FAQs people ask about issuing and transferring private company shares.',['public',('FAQs','public')])
        print '26 FAQs people ask about issuing and transferring private company shares.',has_list_word_in_statement_tuple('26 FAQs people ask about issuing and transferring private company shares.',['public',('FAQs','private')])
        print '26 FAQs fred\'s people ask about issuing and transferring private company shares.',has_list_word_in_statement_tuple('26 FAQs people ask about issuing and transferring private company shares.',['public',('FAQs','private')])
        print '26 FAQs people ask about freds issuing and fred\'s transferring private company shares.',has_list_word_in_statement_tuple('26 FAQs people ask about issuing and transferring private company shares.',['public',('FAQs','private')])
        exit()
    elif not True:
        print 'Get File Size of ' + r'D:\Projects\o9\Newsss' + ':',get_file_size(r'D:\Projects\o9\Newsss\ArticleHandling.py')
        print 'Get File Size of ' + r'D:\Projects\o9\Newss' + ':',get_file_size(r'D:\Projects\o9\Newss\ArticleHandling.py')
        time.sleep(10)
        exit()
    elif not True:
        print ['operating','system'],has_all_list_word_in_statement('Operating System is a subject',['operating','system'])
        print ['operating','system','5th'],has_all_list_word_in_statement('Operating System is a subject',['operating','system','5th'])
        print ('operating','system'),has_all_list_word_in_statement('Operating is a subject',('operating','system'))
        print ('operating','system','5th'),has_all_list_word_in_statement('Operating System is a 5th subject',('operating','system','5th'))
        exit()
    elif not True:
        print ['list'],UpperCamelCase(['list'])
        print 'prabu',UpperCamelCase('prabu')
        print 'PraBu',UpperCamelCase('PraBu')
        print 'PraBu  ',UpperCamelCase('Prabu  ')
        print '  Prabu  ',UpperCamelCase('  Prabu  ')
        print 'l',UpperCamelCase('l')
        print 'la',UpperCamelCase('la')
        exit()
    elif not True:
        print compare_two_objects({'prabu':'prabu','maay':'maay'},{'prabu':'prabus'})
        print compare_two_objects({'prabu':'prabu','maay':'maay'},{'prabu':'prabus','prabu':'prabu','check':'check'})
        print compare_two_objects({'prabu':'prabu','maay':'maay'},{})
        print compare_two_objects({},{'prabu':'prabu','maay':'maay'})
        print compare_two_objects({'prabu':'prabu','maay':'maay'},{'prabu':'prabu','maay':'maay'})
        print compare_two_objects(['prabu','maay'],['prabu'])
        print compare_two_objects(['prabu','maay'],['prabu','maay','check'])
        print compare_two_objects([],['prabu','maay','check'])
        print compare_two_objects(['prabu','maay'],[])
        print compare_two_objects(['prabu','maay'],['prabu','maay'])
        exit()
    elif not True:
        print '3M Co. (MMM) Falls 2.52% for April 17 - Equities.com' , select_company_name_ticker_based('3M Company','3M Co. (MMM) Falls 2.52% for April 17 - Equities.com','MMM','3m company')
        print 'SOFTlab, 3M & BBDO collaborate to create lifelab at SXSW - Designboom' , select_company_name_ticker_based('3M Company','SOFTlab, 3M & BBDO collaborate to create lifelab at SXSW - Designboom','MMM','3m company')
        print '3M Co. (MMM) Among Biggest DJIA Losers on April 23 - Equities.com' , select_company_name_ticker_based('3M Company','3M Co. (MMM) Among Biggest DJIA Losers on April 23 - Equities.com','MMM','3m company')
        print '3M Co. (MMM) Closes 0.42% Down on the Day for April 24 - Equities.com' , select_company_name_ticker_based('3M Company','3M Co. (MMM) Closes 0.42% Down on the Day for April 24 - Equities.com','MMM','3m company')
        print 'Interesting October Stock Options for 3M - Nasdaq' , select_company_name_ticker_based('3M Company','Interesting October Stock Options for 3M - Nasdaq','MMM','3m company')
        print 'Earnings: AT&T, Pfizer, Procter & Gamble, DuPont, Caterpillar, 3M, and Apple - Richmond.com' , select_company_name_ticker_based('3M Company','Earnings: AT&T, Pfizer, Procter & Gamble, DuPont, Caterpillar, 3M, and Apple - Richmond.com','MMM','3m company')
        print '3M Co. (MMM) Closes 0.64% Down on the Day for April 27 - Equities.com' , select_company_name_ticker_based('3M Company','3M Co. (MMM) Closes 0.64% Down on the Day for April 27 - Equities.com','MMM','3m company')
        print 'Block Trading and Options Highlights for 3M Company (MMM) - AVAFIN' , select_company_name_ticker_based('3M Company','Block Trading and Options Highlights for 3M Company (MMM) - AVAFIN','MMM','3m company')
        print '3M Co Beats Earnings Estimates; Misses on Revenue; Updates FY2014 Outlook ... - Dividend.com' , select_company_name_ticker_based('3M Company','3M Co Beats Earnings Estimates; Misses on Revenue; Updates FY2014 Outlook ... - Dividend.com','MMM','3m company')
        print '3M Co. (MMM) Closes 0.22% Up on the Day for April 28 - Equities.com' , select_company_name_ticker_based('3M Company','3M Co. (MMM) Closes 0.22% Up on the Day for April 28 - Equities.com','MMM','3m company')
        print 'Apple Watch launch may top 3M sales, analyst says - TechnoBuffalo' , select_company_name_ticker_based('3M Company','Apple Watch launch may top 3M sales, analyst says - TechnoBuffalo','MMM','3m company')
        print 'Radamel Falcao has cost Manchester United  3M in wages since his last shot ... - Daily Mail' , select_company_name_ticker_based('3M Company','Radamel Falcao has cost Manchester United  3M in wages since his last shot ... - Daily Mail','MMM','3m company')
        statement_is='AT&T Falls 2.52% for April 17 - Equities.com'
        print  statement_is, select_company_name_ticker_based('AT&T Inc',statement_is,'T','at&t')
        statement_is='conference at T-mobile shop Falls 2.52% for April 17 - Equities.com'
        print  statement_is, select_company_name_ticker_based('AT&T Inc',statement_is,'T','at&t')
        statement_is='conference at T-mobile(NYSE:T) shop Falls 2.52% for April 17 - Equities.com'
        print  statement_is, select_company_name_ticker_based('AT&T Inc',statement_is,'T','at&t')
        statement_is='conference at T-mobile and AT&T shop Falls 2.52% for April 17 - Equities.com'
        print  statement_is, select_company_name_ticker_based('AT&T Inc',statement_is,'T','at&t')
        exit()
    elif False:
        print '"Logitech","Analysts expect that Logitech International SA will post $0.89 EPS for the current fiscal year."' , select_company_name_based("Logitech","Analysts expect that Logitech International SA will post $0.89 EPS for the current fiscal year.")
        print '"Logitech","Analysts polled by Bloomberg indicates that the majority of the sell-side firms are bullish on Logitech."' , select_company_name_based("Logitech","Analysts polled by Bloomberg indicates that the majority of the sell-side firms are bullish on Logitech.")
        print '"Logitech","Bracken Darrell: Logitech ne sera frein par aucun obstacle (12.03.2015)"' , select_company_name_based("Logitech","Bracken Darrell: Logitech ne sera frein par aucun obstacle (12.03.2015)")
        print '"Logitech","Bracken P. Darrell, Konzernchef von Logitech."' , select_company_name_based("Logitech","Bracken P. Darrell, Konzernchef von Logitech.")
        print '"Logitech","Brian Westover is an Analyst for the Hardware Team, reviewing laptops, desktops, and storage devices."' , select_company_name_based("Logitech","Brian Westover is an Analyst for the Hardware Team, reviewing laptops, desktops, and storage devices.")
        print '"Logitech","By Brian Westover Analyst, Hardware"' , select_company_name_based("Logitech","By Brian Westover Analyst, Hardware")
        print '"Logitech","Click on This Logitech Mouse Deal From Best Buy - NerdWallet blog"' , select_company_name_based("Logitech","Click on This Logitech Mouse Deal From Best Buy - NerdWallet blog")
        print '"Logitech","Bon plan a Lensemble claviersouris MX800 de Logitech pour 90 a - Les NumAcriques"' , select_company_name_based("Logitech","Bon plan a Lensemble claviersouris MX800 de Logitech pour 90 a - Les NumAcriques")
        print '"Logitech","DD-DD34N D3DuD1D14DuNNDoD34D1 D14NNDoD Logitech Daedalus Apex G303 - Gagadget com D12DuNDoNND12ND1 NDdegD1N D34 NDuND12DDoDu"' , select_company_name_based("Logitech","DD-DD34N D3DuD1D14DuNNDoD34D1 D14NNDoD Logitech Daedalus Apex G303 - Gagadget com D12DuNDoNND12ND1 NDdegD1N D34 NDuND12DDoDu")
        print '"Logitech","Der Turnaround bei der Profitabilitt sei auf dem richtigen Weg dank hherer Bruttomargen und disziplinierten Ausgaben, liess sich CEO Bracken Darrell in der Mitteilung zitieren."' , select_company_name_based("Logitech","Der Turnaround bei der Profitabilitt sei auf dem richtigen Weg dank hherer Bruttomargen und disziplinierten Ausgaben, liess sich CEO Bracken Darrell in der Mitteilung zitieren.")
        print '"Logitech","Enter your email address below to get the latest news and analysts ratings for Logitech International SA with our FREE daily email newsletter:"' , select_company_name_based("Logitech","Enter your email address below to get the latest news and analysts ratings for Logitech International SA with our FREE daily email newsletter:")
        print '"Logitech","Focus In on Logitech Webcam Deal From Newegg - NerdWallet blog"' , select_company_name_based("Logitech","Focus In on Logitech Webcam Deal From Newegg - NerdWallet blog")
        print '"Logitech","H Logitech II-IIIII1I-IIu II G303 Daedalus Apex - NovaIPSI II FM 94 6"' , select_company_name_based("Logitech","H Logitech II-IIIII1I-IIu II G303 Daedalus Apex - NovaIPSI II FM 94 6")
        print '"Logitech","H Logitech IIIuII-I-IIu II I12II III III12II-IoI1 I-IoIII3II12II-I IIII gamers - I IIII IIII"' , select_company_name_based("Logitech","H Logitech IIIuII-I-IIu II I12II III III12II-IoI1 I-IoIII3II12II-I IIII gamers - I IIII IIII")
        exit()
    elif not True:
        print "EDITORIAL: Toyo Tire & Rubber`s appalling disregard for safety",is_english("EDITORIAL: Toyo Tire & Rubber`s append disregard for safety",1,10)
        print " Bracken Darrell: Logitech ne sera frein par aucun obstacle (12.03.2015)",  is_english("Bracken Darrell: Logitech ne sera frein par aucun obstacle (12.03.2015)")
        print " Bracken P. Darrell, Konzernchef von Logitech.",  is_english("Bracken P. Darrell, Konzernchef von Logitech.")
        print " Brian Westover is an Analyst for the Hardware Team, reviewing laptops, desktops, and storage devices.",  is_english("Brian Westover is an Analyst for the Hardware Team, reviewing laptops, desktops, and storage devices.")
        print " By Brian Westover Analyst, Hardware",  is_english("By Brian Westover Analyst, Hardware")
        print " Click on This Logitech Mouse Deal From Best Buy - NerdWallet blog",  is_english("Click on This Logitech Mouse Deal From Best Buy - NerdWallet blog")
        print " Bon plan a Lensemble claviersouris MX800 de Logitech pour 90 a - Les NumAcriques",  is_english("Bon plan a Lensemble claviersouris MX800 de Logitech pour 90 a - Les NumAcriques")
        print " DD-DD34N D3DuD1D14DuNNDoD34D1 D14NNDoD Logitech Daedalus Apex G303 - Gagadget com D12DuNDoNND12ND1 NDdegD1N D34 NDuND12DDoDu",  is_english("DD-DD34N D3DuD1D14DuNNDoD34D1 D14NNDoD Logitech Daedalus Apex G303 - Gagadget com D12DuNDoNND12ND1 NDdegD1N D34 NDuND12DDoDu")
        print " Der Turnaround bei der Profitabilitt sei auf dem richtigen Weg dank hherer Bruttomargen und disziplinierten Ausgaben, liess sich CEO Bracken Darrell in der Mitteilung zitieren.",  is_english("Der Turnaround bei der Profitabilitt sei auf dem richtigen Weg dank hherer Bruttomargen und disziplinierten Ausgaben, liess sich CEO Bracken Darrell in der Mitteilung zitieren.")
        print " Enter your email address below to get the latest news and analysts ratings for Logitech International SA with our FREE daily email newsletter:",  is_english("Enter your email address below to get the latest news and analysts ratings for Logitech International SA with our FREE daily email newsletter:")
        print " Focus In on Logitech Webcam Deal From Newegg - NerdWallet blog",  is_english("Focus In on Logitech Webcam Deal From Newegg - NerdWallet blog")
        print " H Logitech II-IIIII1I-IIu II G303 Daedalus Apex - NovaIPSI II FM 94 6",  is_english("H Logitech II-IIIII1I-IIu II G303 Daedalus Apex - NovaIPSI II FM 94 6")
    elif not True:
        input_combinations=[
                        ('1-PAGE LIMITED','1-page')
                        ,('Testing STring for Abbr','tsfa')
                        ,('Testing WORD string for Abbr','twordsfa')
                        ,('Testing string WORD for Abbr','tswordfa')
                        ,('Testing string for Abbr WORD','tsfaword')
                        ,('BREAK Testing string for Abbr WORD','tsfaword')
                        ,('Testing string BREAK for Abbr WORD','tsfaword')
                        ,('Testing string for Abbr WORD BREAK','tsfaword')
                        ,('WORD Testing string for Abbr ','wordtsfa')
                        ,('A-CAP RESOURCES LIMITED','acap')
                        ,('A1 CONSOLIDATED GOLD LIMITED','a1consolidated')
                        ,('A1 INVESTMENTS & RESOURCES LTD','a1investments')
                        ,('ABACUS PROPERTY GROUP','abacusproperty')
                        ,('ABERDEEN LEADERS LIMITED','aberdeenasset')
                        ,('ABILENE OIL AND GAS LIMITED','abilene')
                        ,('ABM RESOURCES NL','abmresources')
                        ,('ABSOLUTE EQUITY PERFORMANCE FUND LIMITED','efgfund')
                        ,('ABSOLUTE EQUITY PERFORMANCE FUND LIMITED','aepfund')
                        ,('ABSOLUTE EQUITY PERFORMANCE FUND','aepfund')
                        ,('ABUNDANT PRODUCE LIMITED','abundantproduce')
                        ,('ACACIA COAL LIMITED','acaciacoal')
                        ,('ACADEMIES AUSTRALASIA GROUP LIMITED','academies')
                        ,('ACCENT RESOURCES NL','accentresources')
                        ,('ACONEX LIMITED','aconex')
                        ,('ACORN CAPITAL INVESTMENT FUND LIMITED','acorncapital')
                        ,('ACRUX LIMITED','acrux')
                        ]
        for each_input in input_combinations:
            print 'Input:\t' + each_input[0] + '\tAbbrevations:\t'  + each_input[1] + '\tResult:\t' + str(check_all_combination_abbreviation(each_input[0],each_input[1],check_half_name_match=True,developer_mode=False))
        exit()
    elif not True:
        print_list(get_all_dates('On January 9, 2015, Emerson Electric Co. announced that Edgar M. Purvis, Jr. would be appointed as its new Chief Operating Officer, effective February 3, 2015. Mr. Purvis, 57, has been with Emerson for 31 years and has served as Executive Vice President and Business Leader for Emerson Climate Technologies since 2008. Edward L. Monser, 64, has held the title of Chief Operating Officer since 2001, and will continue to serve as President of Emerson, a position he has held since 2010.'))
        exit()
    elif not True:
        print_list(paragraph_to_sentence('On January 9, 2015, Emerson Electric Co. announced that Edgar M. Purvis, Jr. would be appointed as its new Chief Operating Officer, effective February 3, 2015.'))
        print_list(paragraph_to_sentence('On January 9, 2015, Emerson Electric Com. announced that Edgar M. Purvis, Jr. would be appointed as its new Chief Operating Officer, effective February 3, 2015.'))
        exit()
    elif not True:
        print_list(paragraph_to_sentence('Sales decreased by $27.1 million , or 2.9% , from 2012  to 2013 , due to lower unit sales volume and the unfavorable effects of movements in foreign currency exchange rates, partially offset by a favorable change in average selling prices and mix. The translation of foreign currency-denominated sales transactions decreased consolidated sales by $2.3 million  in 2013  compared to 2012 , primarily due to the relatively stronger U.S. Dollar in comparison to the Brazilian Real and Japanese Yen, partially offset by a relatively weaker U.S. Dollar in comparison to the Euro. International sales decreased by $30.0 million (5.8%), including the currency effects described above, while domestic sales increased by $2.9 million (0.7%). FLAG segment sales decreased $37.4 million , or 5.7% , FRAG segment sales increased $9.5 million , or 3.8% , and sales of concrete cutting and finishing products were up $0.9 million, or 3.2%. See further discussion below under Segment Results.'))
        print_list(paragraph_to_sentence('Sales order backlog for the FLAG segment at December 31, 2013  was $150.9 million  compared to $167.9 million  at December 31, 2012 . The reduction in sales order backlog reflects reduced demand for our FLAG products, as customers managed field inventory levels and deferred some orders to 2014.'))
    elif not True:
        print 'ThisName ThatName I.\t',remove_middle_name('ThisName ThatName I.')
        print 'I. ThisName ThatName\t',remove_middle_name('I. ThisName ThatName')
        print 'ThisName I. ThatName\t',remove_middle_name('ThisName I. ThatName')
        print 'ThisName I ThatName\t',remove_middle_name('ThisName I ThatName')
        print 'ThisName ThatName\t',remove_middle_name('ThisName ThatName')
    elif not True:
        list_of_url=['http://blog.executivebiz.com/2015/03/orbital-atk-helps-nasa-launch-scientific-balloon-on-test-flight-john-pullen-comments/',
                'http://techcrunch.com/2015/04/13/if-apple-designed-an-ios-user-interface-for-kids/',
                'http://electroiq.com/blog/2015/05/silicon-storage-technology-and-globalfoundries-announce-qualification-of-automotive-grade-55nm-embedded-flash-tech/',
                'http://www.vanguardtribune.com/2015/07/23/stock-update-agco-corporation-nyseagco-3/27201/',
                'http://www.lulegacy.com/2015/03/28/morningstar-assigns-bbb-credit-rating-to-altria-group-mo/426314/',
                'http://www.lulegacy.com/2015/06/05/insider-selling-prologis-ceo-sells-260650-00-in-stock-pld/505248/',
                'http://www.applianceretailer.com.au/2015/04/one-hot-topic-its-ars-ultimate-guide-to-heaters-for-winter-2015/',
                'http://globenewswire.com/news-release/2015/04/02/721374/0/en/Amer-Sports-first-quarter-results-published-on-April-23-2015.html',
                'http://www.twst.com/update/101728-illinois-tool-works-inc-itw-announces-conference-call-information-for-the-2015-first-quarter',
                'http://www.nasdaq.com/article/tuesday-morning-corp-tues-has-plummeted-to-a-new-low-after-cfo-departs-20150630-00646',
                'http://globenewswire.com/news-release/2015/02/05/703686/10118942/en/Investor-Lawsuit-Against-Acquisition-of-Regency-Energy-Partners-LP-RGP-Announced-by-Shareholders-Foundation.html',
                'http://www.lulegacy.com/2015/06/28/ppg-industries-earns-buy-rating-from-jefferies-group-ppg/527341/',
                'http://www.dentonrc.com/local-news/local-news-headlines/20150117-public-can-weigh-in-on-safety-kleens-permit.ece',
                'http://texas.realestaterama.com/2015/04/27/pete-neubig-of-empire-industries-property-management-in-houston-texas-wins-the-rocky-maxwell-award-from-the-national-association-of-residential-property-managers-narpm-ID0926.html',
                'http://www.marketwatch.com/story/oceaneering-announces-appointment-of-steve-barrett-as-senior-vice-president-subsea-products-2015-07-08',
                'http://www.suffolknewsherald.com/2015/07/23/bon-secours-sets-online-scheduling/',
                'http://www.lulegacy.com/2015/06/18/guggenheim-increases-valeant-pharmaceuticals-intl-price-target-to-300-00-vrx/517620/',
                'http://www.marketwatch.com/story/standard-motor-products-inc-announces-second-quarter-2015-earnings-conference-call-2015-07-27',
                'http://www.fool.com/investing/general/2015/05/09/read-this-before-you-sell-linkedin-corp-stock.aspx',
                'http://www.vanguardtribune.com/2015/07/23/stock-update-dunkin-brands-group-inc-nasdaqdnkn-3/27308/',
                'http://www.finances.com/company-news/91757-advanced-drainage-systems-to-announce-fourth-quarter-and-full-fiscal-year-2015-financial-results-on-may-12-2015.htm',
                'http://www.forbes.com/sites/stockoptionschannel/2015/02/26/first-week-of-thomson-reuters-october-16th-options-trading/',
                'http://www.dailytitan.com/2015/04/titan-baseball-wraps-up-nine-game-road-trip-against-cal-state-bakersfield/',
                'http://www.forbes.com/sites/walterloeb/2015/02/16/nordstrom-ties-the-knot-with-mickey-drexler/',
                'http://www.lulegacy.com/2015/06/29/cst-brands-receives-42-51-consensus-target-price-from-brokerages-nysecst/527812/',
                'http://www.nytimes.com/2015/05/03/opinion/sunday/that-handmade-scarf-wont-save-the-world.html',
                'http://www.fool.com/investing/general/2015/05/31/americans-dont-like-bank-of-america-for-yet-anothe.aspx',
                'http://www.valuewalk.com/2015/03/ackmans-key-aim-is-to-shutdown-herbalife/',
                'http://www.marketwatch.com/story/anadarko-announces-pricing-of-public-offering-of-8000000-wgp-linked-750-percent-tangible-equity-units-and-pricing-of-public-secondary-offering-of-2000000-of-its-wgp-common-units-2015-06-04',
                'http://www.itextreme.hu/hirek/2015,05,18/a_budapesti_honvdkrhz_a_ge_healthcare_innovatv_ct_berendezseit_helyezte_zembe',
                'http://www.lulegacy.com/2015/06/23/exact-sciences-sees-strong-trading-volume-after-analyst-upgrade-exas/521858/',
                'http://www.lulegacy.com/2015/04/06/insider-selling-wayfair-svp-sells-1974-shares-of-stock-w/433099/',
                'http://www.reuters.com/article/2015/03/17/alstom-ma-ge-eu-idUSL6N0WJ27A20150317',
                'http://www.vanguardtribune.com/2015/05/18/notable-session-mover-synaptics-incorporated-nasdaqsyna/9316/',
                'http://www.slate.com/articles/life/triumphs_and_fails/2015/04/triumphs_and_fails_parenting_triumphs_on_helping_your_children_try_new_things.html',
                'http://www.courier-journal.com/story/sports/horses/triple/derby/2015/04/24/kentucky-derby-2015--report-says-jockey-kent-desormeaux-lands-mount-on-keen-ice/26311599/',
                'http://www.lulegacy.com/2015/06/24/apogee-enterprises-apog-releases-quarterly-earnings-results-beats-estimates-by-0-04-eps/523114/',
                'http://hollywoodlife.com/2015/06/09/carolina-herrera-naked-dresses-disses-sheer-gowns-met-gala-beyonce/',
                'http://www.vanguardtribune.com/2015/06/08/stock-insights-ace-limited-nyseace/14880/',
                'http://www.marketwatch.com/story/courier-terminates-quadgraphics-agreement-and-separately-announces-agreement-with-rr-donnelley-2015-02-05',
                'http://www.carscoops.com/2015/03/haw-haw-minis-chrome-line-exterior.html'
            ]
        for each_url in list_of_url:
            print each_url,'=',get_smell_like_date_from_url(each_url)
        exit()
        