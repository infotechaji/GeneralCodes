"""
    Description: Python functions to fetch news from google
    Version    : v2.08
    History    :
                v1.0 - 01/01/2015 - Initial version
                v1.1 - 05/24/2015 - Added scoring parameters for google news in get_news_feeds_small
                v1.2 - 06/05/2015 - Function bing_news_search is added and imported ControlConfig for BING_API_KEY
                v1.3 - 07/14/2015 - Updated the function fetch_for_url to include time_out
                v1.4 - 10/22/2015 - Update fetch_for_url logic to handle space in url and added new function get_page_title
                v1.5 - 10/28/2015 - Added url_fix function. taken from http://stackoverflow.com/questions/120951/how-can-i-normalize-a-url-in-python
                v1.6 - 11/11/2015 - Added iteration to get_news_feeds_small
                v1.7 - 12/22/2015 - Added user_agent to get_news_feeds_small and used get_printable_string instead of unicode
                v1.8 - 01/07/2016 - Updated google news logic for splitting news link with =
                v1.9 - 01/10/2015 - country code logic for get_news_feeds_small
                v1.10 - 01/21/2015 - sent_process_status_mail: IP Address suffix to mail body
                v1.11 - 04/11/2016 - Moved function get_absolute_path from AnchorSupport
                v1.12 - 06/01/2016 - Flag added in fetch_for_url to read data from file for testing mode
                v1.13 - 08/02/2016 - Adding translate option
                v2.0  - 08/02/2016 - Consider as a major version
                v2.01 - 08/31/2016 - Removed function get_news_feeds_NOT_USED_TO_BE_DELETED code.
                v2.02 - 09/27/2016 - use get_html_to_unicode_string when default encoding logic fails. Retry for certificate_verify_failed and connection refused
                v2.03 - 10/07/2016 - Collect stats for each link passed to fetch_for_url and monkeypatch for SSL issue
                v2.04 - 10/13/2016 - Fix: unicode conversion when read from file and html/text encoding is provided
                v2.05 - 02/27/2016 - Exclude Multimedia url explicitly and also ignore if content size is greater than 3MB.
                v2.06 - 03/27/2016 - Strip url for space, slash , tab for function fetch_for_url
                v2.07 - 05/05/2017 - www issue in url. inx.co.jp and sangetsu.co.jp require www in the url. Otherwise does not work.
                v2.08 - 05/18/2017 - get_absolute_path is moved to Utilities. url_fix is not in use as well.
    Open Issues: None.
    Pending :    Javascript redirects http://www.spectrapremium.com/ to http://www.spectrapremium.com/Home.html
    http working https not workin https://www.cofomo.com/
    both http and https is not working https://www.e-sonic.com/
    certificate verification failed https://www.bridgestoneamericas.com/en/index.html
    redirects using form http://www.flightsafety.com/index_loading.php?_site_unique=3717854157e8f89489ea45.14777187
    
fetch_for_url:(1):http://www.omnicomgroup.com/media/1050/john-wren-photos.zip: 20161013_143807: :processing url: http://www.omnicomgroup.com/media/1050/john-wren-photos.zip :new url: http://www.omnicomgroup.com/media/1050/john-wren-photos.zip
fetch_for_url:(1):http://www.omnicomgroup.com/media/1050/john-wren-photos.zip: check for file: w_fiind_xyz8\httpwwwomnicomgroupcommedia1050johnwrenphotoszip
fetch_for_url:(1):http://www.omnicomgroup.com/media/1050/john-wren-photos.zip: 20161013_143807. HTML handling - before request open
fetch_for_url:(1):http://www.omnicomgroup.com/media/1050/john-wren-photos.zip: :content-type: application/x-zip-compressed
fetch_for_url:(1):http://www.omnicomgroup.com/media/1050/john-wren-photos.zip:Error while using encoding. Erro:unknown encoding: application/x-zip-compressed 
http://www.melon1.com/uploads/2/5/9/9/25998676/9784551_orig.jpg?238

application
	xhtml+xml
audio
example
image
message
model
multipart
text
video

https://www.shellvacationsclub.com/home.page - source code is build using onload function. How to deal with it.

www issue. the following websites work only when it has www schema inx.co.jp and sangetsu.co.jp
    http://kdc.com.hk	<urlopen error [Errno 10061] No connection could be made because the target machine actively refused it>. Same www issue
    http://stonebridgefarmcaravanpark.co.uk - this is not read properly

"""
# -*- coding: utf-8 -*-
import urllib
#import urlparse #for url_fix
import cookielib,urllib2
import json
import re
import feedparser
import requests
from BeautifulSoup import BeautifulSoup, SoupStrainer
import HTMLParser
from datetime import datetime, timedelta

import time
import email.Utils
from email.Utils import formatdate
from unidecode import unidecode
import sys

from ControlConfig import *

import socket
from Utilities import *
#version_info=sys.version_info
#print version_info,type(version_info),version_info.major,version_info.minor,version_info.micro,type(version_info.micro)
#if version_info.major == 2 and version_info.minor == 7 and version_info.micro > 8:
import ssl #To address SSL issues in 2.7.95
#ssl._create_default_https_context = ssl._create_unverified_context

def log_web_access_status(function_name,webpage_name,status_message,result_length=None,delimiter='\t'):
    if function_name == 'fetch_for_url':
        stats_file_name='web_access_' + 'fetch_for_url' + '_stats.txt'
    else:
        stats_file_name='web_access_' + function_name + '_stats.txt'
    s_h=open(stats_file_name,'a')
    write_string=log_time_stamp() + function_name + delimiter + webpage_name + delimiter + status_message
    if result_length:
        write_string = write_string + delimiter + 'Length:' + str(result_length)
    s_h.write(write_string + '\n')
    s_h.close()
def sent_process_status_mail(mail_subject,mail_body=None,suffix_ip_address_to_body=True):
    url_to_send_mail=API_HOST + ':' + str(API_PORT) + '/sendmail/to=' + MAIL_ADDRESS_PROCESS_NOTIFICATION
    ip_address_string=''
    if suffix_ip_address_to_body:
            ip_address=socket.gethostbyname(socket.gethostname())
            ip_address_string='\n IP Address:' +  str(ip_address)
    if mail_subject and len(mail_subject)>0: url_to_send_mail=url_to_send_mail + '&subject=' + urllib.quote(mail_subject)
    if mail_body: 
        if isinstance(mail_body,list):
            url_to_send_mail=url_to_send_mail + '&body=' + urllib.quote('\n'.join(mail_body)) + ip_address_string
        elif isinstance(mail_body,str):
            url_to_send_mail=url_to_send_mail + '&body=' + urllib.quote(mail_body) + ip_address_string
        else:
            if len(ip_address_string)>10:
                url_to_send_mail=url_to_send_mail + '&body=' + ip_address_string
            else:
                url_to_send_mail=url_to_send_mail + '&body=\'\''
    else:
        if len(ip_address_string)>10:
            url_to_send_mail=url_to_send_mail + '&body=' + ip_address_string
        else:
            url_to_send_mail=url_to_send_mail + '&body=\'\''
    #print url_to_send_mail#,'\n\n\Result:',fetch_for_url(url_to_send_mail)
    return fetch_for_url(url_to_send_mail,read_from_file=False)
def fetch_for_url(actual_url,time_out_in=10,read_from_file=True,developer_mode=False,iteration=1,unescape=True,file_only_mode=False,translate=False):
    developer_mode=developer_mode    
    #developer_mode=True
    new_url=actual_url.strip(' /\t\n')
    if iteration>3: return ''
    if unescape and '&' in new_url and ';' in new_url:
        new_url=get_printable_string(new_url,replace_by=' ',unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True,developer_mode=False)
    if 'http://' not in new_url and 'https://' not in new_url:
        new_url = 'http://' + new_url
    colon_slash_index=new_url.find(':/')
    if colon_slash_index < 0:
        colon_slash_index=0
    slash_after_domain_index=new_url.find('/',colon_slash_index+2)
    if slash_after_domain_index > colon_slash_index:
        #new_url=new_url[:slash_after_domain_index] + '/' + urllib.quote(new_url[slash_after_domain_index+1:]) Not the correct approach. It replaces ? = ..Individual stuff should be quoted not the parameters
        #http://stackoverflow.com/questions/120951/how-can-i-normalize-a-url-in-python
        quoted_part=new_url[slash_after_domain_index+1:]
        quoted_part=quoted_part.replace(' ','%20')#Temp fix
        new_url=new_url[:slash_after_domain_index] + '/' + quoted_part
    print_prefix='fetch_for_url:(' +str(iteration) + '):' + str(actual_url) +':'#+'mew_url:'+new_url
    if developer_mode: print print_prefix,log_time_stamp(),':processing url:',actual_url,':new url:',new_url
    actual_url_lower=new_url.lower()
    if 'linkedin.com' in actual_url_lower or 'facebook.com' in actual_url_lower or 'twitter.com' in actual_url_lower or '.google.com' in actual_url_lower or 'youtube.com' in actual_url_lower: 
        if developer_mode: print print_prefix,'Social Link page: Return '
        log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='Social Link',result_length=None)
        return ''
    SAVE_FILE_ALWAYS=True#to be moved to ControlConfig
    directory_to_save='w_fiind_xyz8'
    if not new_url: 
        log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='New url is not formed. Logical error',result_length=None)
        return ''
    if '.pdf' in new_url.lower(): 
        if developer_mode: print print_prefix,'PDF page: Return '
        log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='PDF',result_length=None)
        return ''
    if '.zip' in new_url.lower(): 
        if developer_mode: print print_prefix,'Zip File page: Return '
        log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='ZIP',result_length=None)
        return ''
    if '.mp4' in new_url.lower() or '.mp3' in new_url.lower() or '.wav' in new_url.lower() or '.avi' in new_url.lower() or '.mpeg' in new_url.lower() or '.mpg' in new_url.lower():
        if developer_mode: print print_prefix,'Multimedia File page: Return '
        log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='Multimedia',result_length=None)
        return ''
    if time_out_in <= 0 or time_out_in > 25: 
        timeout = 25
    else:
        timeout=time_out_in
    if read_from_file or SAVE_FILE_ALWAYS:
        guess_file_name=get_filename_from_url(new_url)
        guess_file_name=os.path.join(directory_to_save,guess_file_name)
    if read_from_file:
        if developer_mode: print print_prefix,'check for file:',guess_file_name
        if os.path.isfile(guess_file_name):
            if developer_mode: print print_prefix,'file exist:',guess_file_name
            url_content=read_content_from_file(guess_file_name)
            if developer_mode: print print_prefix,str(get_timestamp_for_file(True)) ,'converting the content to unicode. read from file length:',str(len(url_content))
            url_content=get_html_to_unicode_string(url_content)
            if developer_mode: print print_prefix,str(get_timestamp_for_file(True)) ,'converting the content to unicode. read from file after conversion length:',str(len(url_content))
            if url_content: 
                if developer_mode: print print_prefix,log_time_stamp(),':read content from file:',guess_file_name
                log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='Read content from file',result_length=str(len(url_content)))
                return url_content
        elif developer_mode:
            print print_prefix,'File does not exist:',guess_file_name
        if file_only_mode:
            if developer_mode: print print_prefix + '\t' + 'File only mode is enabled. Hence not processing on no file available'
            log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='File only mode. Not processed',result_length=None)
            return ''
    socket.setdefaulttimeout(timeout)
    #if version_info.major == 2 and version_info.minor == 7 and version_info.micro > 8:
    #ssl._create_default_https_context = ssl._create_unverified_context
    user_agent='Mozilla/%2F4.0'
    request = urllib2.Request(new_url)
    request.add_header('User-Agent', user_agent)
    request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    #request.encoding = 'utf-8'
    cj = cookielib.CookieJar()#to handle cookie
    request_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    response=None
    try:
        if developer_mode: print print_prefix,str(get_timestamp_for_file(True)) + '. HTML handling - before request open'
        response = request_opener.open(request)
        #time.sleep(10)
        #print 'get_content_charset:',response.headers['content-type']
        #print 'response.read()' ,response.read()
        url_content = response.read()
        if developer_mode: print print_prefix,str(get_timestamp_for_file(True)) + '. HTML handling - read from response instance'
        #print 'response:history' + str(response.history),type(response.history)
    except Exception as e:
        error_is=str(e)
        error_is=error_is.lower()
        if developer_mode: print print_prefix,log_time_stamp(),':encountered error for',new_url, '\t. Error:',str(e)
        if 'urlopen error' in error_is and ('getaddrinfo failed' in error_is or 'target machine actively refused' in error_is):
            if new_url.startswith('http://ww') or new_url.startswith('https://ww'):
                pass
            else:
                if developer_mode: print print_prefix,':URL Open Error - GetAddressInfo Failed Or target machine actively refused. Url does not have www in it. Adding and Retry.'
                if new_url.startswith('http://'):
                    new_url = new_url.replace('http://','http://www.')
                elif new_url.startswith('https://'):
                    new_url = new_url.replace('https://','https://www.')
                log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='GetAddressInfo/Target refused without WWW. Retry:' + repr(new_url),result_length=None)
                return fetch_for_url(new_url,time_out_in=time_out_in,read_from_file=read_from_file,developer_mode=developer_mode,iteration=iteration+1,unescape=unescape)
        elif 'urlopen error' in error_is and 'timed out' in error_is:
            if developer_mode: print print_prefix,':time_out'
            log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='Timeout. Retry',result_length=None)
            return fetch_for_url(new_url,time_out_in=time_out_in+2,read_from_file=read_from_file,developer_mode=developer_mode,iteration=iteration+1,unescape=unescape)
        elif 'https://' in new_url and ('certificate_verify_failed' in error_is or 'certificate verify failed' in error_is):
            if developer_mode: print print_prefix,':certificate_verify_failed'
            log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='SSL error. Retry ',result_length=None)
            return fetch_for_url(actual_url=new_url.replace('https://','http://'),time_out_in=time_out_in+2,read_from_file=read_from_file,developer_mode=developer_mode,iteration=iteration+1,unescape=unescape)
        elif 'https://' in new_url and 'no connection could be made' in error_is and 'refused' in error_is:
            if developer_mode: print print_prefix,':certificate_verify_failed'
            log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='Connection Error. Retry',result_length=None)
            return fetch_for_url(actual_url=new_url.replace('https://','http://'),time_out_in=time_out_in+2,read_from_file=read_from_file,developer_mode=developer_mode,iteration=iteration+1,unescape=unescape)
        elif 'no connection could be made' in error_is and 'refused' in error_is:
            if developer_mode: print print_prefix , 'Do we need to implement:' + '\t http://www.decalage.info/en/python/urllib2noproxy'
        log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message=str(e),result_length=None)
        url_content = ''
        return url_content
    try:
        if not response:
            log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='No response object',result_length=None)
            return ''
        if len(url_content) > (1048576 * 3):
            if developer_mode: print print_prefix + '\t' + 'Content size(' + str(len(url_content)) + ') is more than 3MB. Ignoring to process:'
            log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='Content size is huge',result_length=str(len(url_content)))
            return ''
        content_type=response.headers['content-type'].lower()
        if developer_mode: print print_prefix + ':content_type:\t' + content_type
        encoding=response.headers['content-type'].split('charset=')[-1]
        if developer_mode:
            print print_prefix,str(get_timestamp_for_file(True)) ,'content_type:Encoding:' ,content_type
        if 'video' in content_type or 'multipart' in content_type or 'model' in content_type or 'message' in content_type or 'image' in content_type or 'example ' in content_type or 'audio' in content_type:
            log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message=encoding,result_length=None)
            if developer_mode: print print_prefix,str(get_timestamp_for_file(True)) ,'content-type:' + content_type
            return ''
        if 'application' in content_type:
            if 'xhtml+xml' in content_type or '/xml' in content_type:
                pass
            else:
                log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message=encoding,result_length=None)
                if developer_mode: print print_prefix,str(get_timestamp_for_file(True)) ,'content-type:' + content_type
                return ''
        if encoding != 'text/html' and len(encoding)>0: #correct charset is not fetched.
            url_content = unicode(url_content, encoding)
        else:
            if developer_mode: print print_prefix,str(get_timestamp_for_file(True)) ,'converting the content to unicode. Content length:',str(len(url_content))
            url_content = get_html_to_unicode_string(url_content)
            if developer_mode: print print_prefix,str(get_timestamp_for_file(True)) ,'converting the content to unicode.Completed Length:',str(len(url_content))
    except Exception as e:
        if developer_mode:
            print print_prefix + 'Error while using encoding. Erro:' + str(e) + '\t Using get_html_to_unicode_string function now.'
        url_content = get_html_to_unicode_string(url_content)
        if developer_mode:
            print print_prefix + 'Error while using encoding. Erro:' + str(e) + '\t Using get_html_to_unicode_string function now.Completed'
    if translate:
        modified_url_content=re.sub(r'((<!--)(?:(?!-->).)*(-->))','',url_content.replace('\n',' ').replace('\r',' ').replace('\t',' '))
        modified_url_content=re.sub(r'((<style)(?:(?!<\/style>).)*(<\/style>))','',modified_url_content)
        modified_url_content=re.sub(r'((<script)(?:(?!<\/script>).)*(<\/script>))','',modified_url_content)
        modified_url_content=re.sub(r'<(\w+)(\s[^<>]+?)([/]?)>',r' ',modified_url_content)
        modified_url_content=re.sub(r'<(\w+)>',r' ',modified_url_content)
        modified_url_content=re.sub(r'(<\/\w+[ ]*>)',r' ',modified_url_content)
        #the below code on InputOutput is for testing purpose
        ins=InputOutput()
        ins.open(re.sub('[^a-z]+','',actual_url.lower()))
        ins.write(modified_url_content)
        ins.close()
        page_language=guess_statement_language(modified_url_content)
        print 'Websearch:' + actual_url + '\tLength=' + str(len(url_content)) + '\tLanguage:' + guess_statement_language(modified_url_content)
        if page_language != 'en' or len(page_language)>2:
            pass
            print 'Translation Page Hit'
            #WRITE code for translation.
    if developer_mode: print print_prefix,str(get_timestamp_for_file(True)) + '. HTML handling - After request read'
    if read_from_file or SAVE_FILE_ALWAYS:
        if create_directory(directory_to_save):
            write_content_to_file(url_content,guess_file_name,developer_mode=developer_mode)
            if developer_mode: print 'fetch_for_url:saved content to file:',guess_file_name
    log_web_access_status(function_name='fetch_for_url',webpage_name=actual_url,status_message='Content retrieved',result_length=str(len(url_content)))
    return url_content

def get_news_feeds_small(companyname,google_ned_country_code,print_instance=None,scoring=None,iteration=1):
    rss_lst = []
    if iteration>3: return rss_lst
    try:
        head = unicode(companyname)
    except Exception as e:
        print 'webSearch.py:get_news_feeds_small: Error while using unicode:' + repr(companyname) + '\t' + str(e)
        head=get_printable_string(companyname,replace_by=' ',unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True,developer_mode=False)
    wrd_clf = head.encode('utf-8', 'ignore')
    companyname_to_pass = re.sub(r'\\x..', '', str(wrd_clf))
    company_name = urllib.urlencode({'q': str(companyname_to_pass).lower()})
    #print 'https://news.google.com/news/feeds?pz=1&cf=all&ned=en&hl=en&' + company_name + '&output=rss&num=100'
    if print_instance: print_instance.customPrint('Requesting for ' + companyname_to_pass)
    country_code=google_ned_country_code
    if country_code not in ('au','us'):#in uk ca nz en_za en_sg
        print 'Invalid country code for google news. country code passed:' + str(country_code)
        exit()
    if not scoring or (scoring and scoring not in ('r','d')):
        search_link='https://news.google.com/news/feeds?pz=1&cf=all&ned=' + country_code + '&hl=en&' + company_name + '&output=rss&num=100'
    else:
        search_link='https://news.google.com/news/feeds?pz=1&cf=all&scoring=' + scoring + '&ned=' + country_code + '&hl=en&' + company_name + '&output=rss&num=100'
    print 'Google Search URL:',search_link
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(search_link, headers=headers).text
        #r = requests.get(search_link).text
    except Exception as e:
        if iteration == 3:
            print 'get_news_feeds_small:exception:',str(e)
            exit()
        if '[Errno 8] _ssl.c:504: EOF occurred' in str(e) or 'existing connection was forcibly closed by the remote host' in str(e) or 'connection attempt failed because the connected party did not properly respond' in str(e):
            time.sleep(1)
            print 'get_news_feeds_small:re-try(' + str(iteration) + '):',companyname
            return get_news_feeds_small(companyname,print_instance,scoring,iteration+1)
        print 'get_news_feeds_small:exception:',str(e)
        exit()
    if print_instance: print_instance.customPrint('Request completed for ' + companyname_to_pass)
    soup = BeautifulSoup(r)
    [s.extract() for s in soup('script')]
    m = soup.findAll("item")
    for i in range(len(m)):
        title = m[i].findAll("title")
        news_link = m[i].find("guid")
        pub_date = m[i].findAll("pubdate")
        description = m[i].findAll("description")
        title = str(title[0])
        pub_date = re.sub("<[^<]+?>", " ", str(pub_date[0]))
        news_link = re.sub("<[^<]+?>", " ", str(news_link))
        description = re.sub("<[^<]+?>", "", str(description[0]))
        if news_link: 
            #News Links can have = in it. Commenting below logic and split using first occurence of =
            #news_link = news_link.split("=")[1]
            first_eq_index=news_link.find('=')
            if first_eq_index < 0: continue
            news_link=news_link[first_eq_index+1:]
        else:
            continue
        result_temp_dict = {}
        result_temp_dict['message'] = title
        result_temp_dict['date'] = pub_date
        result_temp_dict['description'] = description
        if news_link: result_temp_dict['news_link'] = news_link
        #print result_temp_dict
        if len(title) > 15: rss_lst.append(result_temp_dict)
    #Exit on page thrown for robot detection with error message
    if (not rss_lst) or len(rss_lst) < 1:
        robot_detected=is_google_robot_detection(r)
        if robot_detected:
            print 'RSS feed response is \n',r,'\n'
            print 'Captcha enabled. Try after some time'
            print 'Mail sent status:',sent_process_status_mail(INSTANCE_NAME + ': Google RSS feed - Robot detection','The program Exit now')
            exit()
    return rss_lst

def bing_news_search(search_string, search_type='News', full_feed=False):
    '''Function to get the url that points to the page containing
    executive team details '''
    #search_type: Web, Image, News, Video
    search_string = urllib.quote(search_string)
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = (':%s' % BING_API_KEY).encode('base64')[:-1]
    auth = 'Basic %s' % credentials
    processed_urls_count = 0
    result_collection = []
    if full_feed:
        range_number = 5
    else:
        range_number = 1
    for i in range(0, range_number):
        bing_api_url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/' + search_type + '?Query=%27' + search_string + '%27&$format=json&Market=%27en-US%27&$skip=' + str(processed_urls_count)
        print 'Bing Search URL:',bing_api_url
        try:
            request = urllib2.Request(bing_api_url)
            request.add_header('Authorization', auth)
            request.add_header('User-Agent', user_agent)
            request_opener = urllib2.build_opener()
            response = request_opener.open(request)
            response_data = response.read()
            json_result = json.loads(response_data)
            result_list = json_result['d']['results']
            processed_urls_count += len(result_list)
            for r in range(len(result_list)):
                result_temp_dict = {}
                result_temp_dict['news_link'] = result_list[r]['Url']
                result_temp_dict['description'] = result_list[r]['Description']
                result_temp_dict['message'] = result_list[r]['Title']
                result_temp_dict['date'] = result_list[r]['Date']
                result_collection.append(result_temp_dict.copy())
        except Exception as e:
            print (("Error :" + str(e)))
    return result_collection
def get_page_title(article_url):
    developer_mode=True
    page_title=''
    page_content=fetch_for_url(article_url,developer_mode=developer_mode)
    if not page_content or len(page_content)<25: return page_title
    if developer_mode: 'get_page_title:',article_url,':content found with length:',len(page_content)
    all_title=re.findall(r'((<title)(?:(?!<\/title>).)*(<\/title>))',page_content)
    if developer_mode: print 'Grab title from page:',all_title
    if all_title:
        if isinstance(all_title,list) and len(all_title)>0:
            page_title=''            
            page_title= all_title[0][0]
            page_title=re.sub(r'<(\w+)(\s[^<>]+?)?([/]?)>',r' ',page_title)
            page_title=re.sub(r'</\w+\s*>',r' ',page_title)
            page_title=get_printable_string(page_title)
            if len(page_title)>2: 
                if developer_mode: print 'Title found:',page_title
                return page_title
            else:
                if developer_mode: print 'Title not found'
                return ''
    return page_title
def get_absolute_pathDoNotUse(parent_url,child_url,include_script_link=False):
#view-source:http://www.asml.com/asml/show.do?lang=EN&ctx=231
# www.asml.com/asml/show.do?lang=EN&ctx=231 + show.do?lang=EN&amp;ctx=28904&amp;rid=16712 = http://www.asml.com/asml/show.do?lang=EN&ctx=28904&rid=16712
#Answer is given http://stackoverflow.com/questions/5559578/having-links-relative-to-root
#So doing / will make it relative to www.example.com, is there a way to specify what the root is, e.g what if i want the root to be www.example.com/fruits in www.example.com/fruits/apples/apple.html?

#Also handle "http://www.wabashnational.com/../news"
    if not (len(parent_url.strip())>1 and len(child_url.strip())>0): return parent_url
    #print 'get_absolute_path:parent_url=',parent_url,'\t child_url=',child_url
    try:
        return urlparse.urljoin(parent_url,child_url)
    except ValueError as e:#To escape IPv4 Value error. Ex: url= http://www.balfourbeattyinvestments.com/cookies.aspx . href: http://www.balfourbeatty.com[insert 
        print 'get_absolute_path: Exception for P=',parent_url,'. c=',child_url,'. Error:',str(e)
        return ''
def url_fixDONTUSE(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklrung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """
    #If the url is already encoded, it encode it again.
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

if __name__ == '__main__':
    if not True:
        print repr(fetch_for_url('kdc.com.hk',developer_mode=True))[0:100]
        print repr(fetch_for_url('http://kdc.com.hk',developer_mode=True))[0:100]
        print repr(fetch_for_url('http://www.kdc.com.hk',developer_mode=True))[0:100]
        exit()
    elif True:
        print repr(fetch_for_url('inx.co.jp',developer_mode=True))[0:100]
        print repr(fetch_for_url('http://inx.co.jp',developer_mode=True))[0:100]
        print repr(fetch_for_url('http://www.inx.co.jp',developer_mode=True))[0:100]
        exit()
    if not True:
        print repr(fetch_for_url('sangetsu.co.jp',developer_mode=True))[0:100]
        print repr(fetch_for_url('http://sangetsu.co.jp',developer_mode=True))[0:100]
        print repr(fetch_for_url('http://www.sangetsu.co.jp',developer_mode=True))[0:100]
        exit()
    if not True:
        print repr(fetch_for_url('eegholm.dk',developer_mode=True))
        print repr(fetch_for_url('http://eegholm.dk',developer_mode=True))
        print repr(fetch_for_url('http://www.eegholm.dk',developer_mode=True))
        exit()
    if not True:
        print repr(fetch_for_url('https://www.shellvacationsclub.com/home.page ',developer_mode=True))
        exit()
    if not True:
        print  fetch_for_url(actual_url='http://yosefk.com/blog/do-you-really-want-to-be-making-this-much-money-when-youre-50.html',read_from_file=False,developer_mode=True)
        exit()
    if not True:
        print  fetch_for_url(actual_url='http://www.axydent.com/assets/1187799_10151499613591619_21299_n.mp4',read_from_file=False,developer_mode=True)
        exit()
        from InputOutput import *
        run_all=True#
        fetch_for_url(actual_url='http://cincysportszone.com/earnings-analysis-update-for-appfolio-inc-nasdaqappf/21766/',developer_mode=True)
        exit()
    if not True:
        print len(fetch_for_url(actual_url='https://www.caa.ca/about-us/',developer_mode=True))
        exit()
    elif not True:
        current_url='https://www.caa.ca/about-us/contact-us'
        content_result=fetch_for_url(actual_url=current_url,developer_mode=True)
        ins=InputOutput()
        ins.open('contactus_result_longer_method.txt')
        ins.write(content_result)
        ins.close()
        print 'URL:' + current_url + '\t' + 'Content Length:'  + str(len(content_result))
        exit()
    elif not True:#unicode
        current_url='http://www.dinamalar.com/'
        content_result=fetch_for_url(actual_url=current_url,developer_mode=True)
        ins=InputOutput()
        ins.open('dinamala_offline_result_longer_method.txt')
        ins.write(content_result)
        ins.close()
        print 'URL:' + current_url + '\t' + 'Content Length:'  + str(len(content_result))
        exit()
    elif True:
        current_url='https://www.caa.ca/about-us/contact-us'
        content_result=fetch_for_url(actual_url=current_url,developer_mode=True)
        print 'After Result\t',str(get_timestamp_for_file(True)) ,'.Before Printable.Length:',str(len(content_result))
        content_result=get_printable_string(content_result)
        print 'After Result\t',str(get_timestamp_for_file(True)) ,'.After Printable.Length:',str(len(content_result))
        ins=InputOutput()
        ins.open('contactus_printable_longer_method.txt')
        ins.write(content_result)
        ins.close()
        print 'URL:' + current_url + '\t' + 'Content Length:'  + str(len(content_result))
        exit()
    elif not True:#unicode
        current_url='http://www.dinamalar.com/'
        content_result=fetch_for_url(actual_url=current_url,developer_mode=True)
        print 'After Result\t',str(get_timestamp_for_file(True)) ,'.Before Printable.Length:',str(len(content_result))
        content_result=get_printable_string(content_result)
        print 'After Result\t',str(get_timestamp_for_file(True)) ,'.After Printable.Length:',str(len(content_result))
        ins=InputOutput()
        ins.open('dinamalar_printable_longer_method.txt')
        ins.write(content_result)
        ins.close()
        print 'URL:' + current_url + '\t' + 'Content Length:'  + str(len(content_result))
        exit()
        
    elif not True:
        print fetch_for_url(actual_url='http://www.arvindguptatoys.com/arvindgupta/cbt14-Short%20Stories%20For%20Children.pdf?123',developer_mode=True)
        exit()
    elif not True:
        print fetch_for_url(actual_url='http://www.melon1.com/uploads/2/5/9/9/25998676/9784551_orig.jpg?238',developer_mode=True)
        exit()
    elif not True:
        print fetch_for_url(actual_url='http://www.discounttire.com/dtcs/home.do',developer_mode=False)
        exit()
    elif not True:
        print fetch_for_url(actual_url='http://www.arrow.com/',developer_mode=True)
        exit()
    elif not True:
        print fetch_for_url(actual_url='https://www.cofomo.com/',developer_mode=True)
        exit()
    elif not  True:
        print fetch_for_url(actual_url='https://www.e-sonic.com/',developer_mode=True)
        exit()
    elif not  True:
        print fetch_for_url(actual_url='http://www.flightsafety.com/index_loading.php?_site_unique=3717854157e8f89489ea45.14777187',developer_mode=True)
        exit()
    elif not  True:
        print fetch_for_url(actual_url='https://www.bridgestoneamericas.com/en/index.html',developer_mode=True)
        exit()
    elif not  True:
        print fetch_for_url(actual_url='http://www.lumenpulse.com/',developer_mode=True)
        exit()
    elif not  True:
        print fetch_for_url(actual_url='http://www.spectrapremium.com/',developer_mode=True)
        exit()
    elif not  True:
        print fetch_for_url(actual_url='http://morrisonhershfield.com/',developer_mode=True)
        exit()
    elif not  True:
        print fetch_for_url(actual_url='http://www.nike.com/in/en_gb',file_only_mode=False,developer_mode=True) #http://www.nike.com/in/en_gb/  Vs http://www.nike.com
        exit()
    elif not  True:
        print fetch_for_url(actual_url='https://www.dwpv.com/',file_only_mode=False,developer_mode=True)
        exit()
    elif  True:
        for each_link in ['http://www.cihon.cn','http://www.pateo.com.cn','http://www.ilink-systems.com/','http://fiind.com/','http://studienseminar-os-ghrs.de','http://azimuts-agence.fr']:
            print each_link + '\tSTARTED'
            fetch_for_url(each_link,time_out_in=10,read_from_file=True,developer_mode=False,iteration=1,unescape=True,file_only_mode=False,translate=True)
        exit()
    elif not  True:
        list_data = bing_news_search('Univar')
        count=0
        for num in list_data:
            count += 1
            print str(count) + '. ' + unidecode(num['news_link']) + '\t' + unidecode(num['message']) + '\t' + unidecode(num['date']) + '\n'
        exit()