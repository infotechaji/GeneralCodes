#URL Refresh - view-source:http://www.servicepartnersco.com/
# # -*- coding: utf-8 -*-
"""
    Description: This python file provide the status of the website - active or not
    Version    : v2.3
    History    :
                v1.0 - 09/01/2016 - Initial published major version.
                v1.1 - 09/01/2016 - Added developer_mode mode and time out error
                v1.2 - 09/22/2016 - Added extensive set of status code
                v1.3 - 09/26/2016 - return key name and default values are changed
                v1.4 - 05/10/2017 - Paremeter ignore_errors is passed to WebURLParse
                v1.5 - 05/11/2017 - Removed get_website_domain_name_delete.
                v2.0 - 05/12/2017 - Function to Class approach. Domain for sale and Refresh redirect detection
                v2.1 - 05/17/2017 - www and refresh, redirect handling.
                v2.2 - 05/18/2017 - Frameset changes
                v2.3 - 05/29/2017 - consider www page as redirected url
    Procedure to use: TBD
    Open Issues: None.
    Pending :    stuck on onPool(host='www.solutionsbyshea.com', port=80): Max retries exceeded with url: / (Caused by ConnectTimeoutError(<requests.packages.urllib3.connection.HTTPConnection object at 0x0000000017C80A58>, 'Connection to www.solutionsbyshea.com timed out. (connect timeout=5)'))
    Empty Robots file http://www.moparaction.com/robots.txt
    http://thinkabel.com is not working but http://www.thinkabel.com is working. Same with http://douglassdist.com
    
    Works only with https://www.gallatinsteel.com/
"""
import requests,random
from WebsiteCodesSupport import *
from HTMLHandling import *
#http://www.pricegrabber.com exceeded 30 redirects
from webSearch import *
class URLStatus():
    def __init__(self,developer_mode=False,print_instance=None,log_process_status=True):
        self.developer_mode=developer_mode
        self.log_process_status=log_process_status
        self.initiate_print_instance(print_instance)
        self.set_config()
        if self.developer_mode:
            self._print_('__init__:\t' + ' Instance created with developer_mode:' + str(self.developer_mode) + ' \t Log Process:' + str(self.log_process_status))
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='URLStatus'
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
    def is_net_active(self):
        REMOTE_SERVERS=['www.google.com','www.bing.com','www.rediff.com','www.quora.com','duckduckgo.com']
        try:
            random_number=random.randrange(0,4,1)
            #print REMOTE_SERVERS[random_number]
            host = socket.gethostbyname(REMOTE_SERVERS[random_number])
            s = socket.create_connection((host, 80), 5)
            return True
        except:
            pass
        return False
    def get_page_content(self,page_url):
        self.page_content= fetch_for_url(actual_url=page_url,time_out_in=10,developer_mode=self.developer_mode)
        return self.page_content
    def set_config(self):
        self.url_dict={}
        self.status_code_details={
                100: {'message':'Continue','descriptioin':'The server has received the request headers, and the client should proceed to send the request body'}
                ,101: {'message':'Switching Protocols','descriptioin':'The requester has asked the server to switch protocols'}
                ,103: {'message':'Checkpoint','descriptioin':'Used in the resumable requests proposal to resume aborted PUT or POST requests'}
                ,200: {'message':'OK','descriptioin':'The request is OK (this is the standard response for successful HTTP requests)'}
                ,201: {'message':'Created','descriptioin':'The request has been fulfilled, and a new resource is created'}
                ,202: {'message':'Accepted','descriptioin':'The request has been accepted for processing, but the processing has not been completed'}
                ,203: {'message':'Non-Authoritative Information','descriptioin':'The request has been successfully processed, but is returning information that may be from another source'}
                ,204: {'message':'No Content','descriptioin':'The request has been successfully processed, but is not returning any content'}
                ,205: {'message':'Reset Content','descriptioin':'The request has been successfully processed, but is not returning any content, and requires that the requester reset the document view'}
                ,206: {'message':'Partial Content','descriptioin':'The server is delivering only part of the resource due to a range header sent by the client'}
                ,300: {'message':'Multiple Choices','descriptioin':'A link list. The user can select a link and go to that location. Maximum five addresses'}
                ,301: {'message':'Moved Permanently','descriptioin':'The requested page has moved to a new URL'}
                ,302: {'message':'Found','descriptioin':'The requested page has moved temporarily to a new URL'}
                ,303: {'message':'See Other','descriptioin':'The requested page can be found under a different URL'}
                ,304: {'message':'Not Modified','descriptioin':'Indicates the requested page has not been modified since last requested'}
                ,306: {'message':'Switch Proxy','descriptioin':'No longer used'}
                ,307: {'message':'Temporary Redirect','descriptioin':'The requested page has moved temporarily to a new URL'}
                ,308: {'message':'Resume Incomplete','descriptioin':'Used in the resumable requests proposal to resume aborted PUT or POST requests'}
                ,400: {'message':'Bad Request','descriptioin':'The request cannot be fulfilled due to bad syntax'}
                ,401: {'message':'Unauthorized','descriptioin':'The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided'}
                ,402: {'message':'Payment Required','descriptioin':'Reserved for future use'}
                ,403: {'message':'Forbidden','descriptioin':'The request was a legal request, but the server is refusing to respond to it'}
                ,404: {'message':'Not Found','descriptioin':'The requested page could not be found but may be available again in the future'}
                ,405: {'message':'Method Not Allowed','descriptioin':'A request was made of a page using a request method not supported by that page'}
                ,406: {'message':'Not Acceptable','descriptioin':'The server can only generate a response that is not accepted by the client'}
                ,407: {'message':'Proxy Authentication Required','descriptioin':'The client must first authenticate itself with the proxy'}
                ,408: {'message':'Request Timeout','descriptioin':'The server timed out waiting for the request'}
                ,409: {'message':'Conflict','descriptioin':'The request could not be completed because of a conflict in the request'}
                ,410: {'message':'Gone','descriptioin':'The requested page is no longer available'}
                ,411: {'message':'Length Required','descriptioin':'The "Content-Length" is not defined. The server will not accept the request without it'}
                ,412: {'message':'Precondition Failed','descriptioin':'The precondition given in the request evaluated to false by the server'}
                ,413: {'message':'Request Entity Too Large','descriptioin':'The server will not accept the request, because the request entity is too large'}
                ,414: {'message':'Request-URI Too Long','descriptioin':'The server will not accept the request, because the URL is too long. Occurs when you convert a POST request to a GET request with a long query information'}
                ,415: {'message':'Unsupported Media Type','descriptioin':'The server will not accept the request, because the media type is not supported'}
                ,416: {'message':'Requested Range Not Satisfiable','descriptioin':'The client has asked for a portion of the file, but the server cannot supply that portion'}
                ,417: {'message':'Expectation Failed','descriptioin':'The server cannot meet the requirements of the Expect request-header field'}
                ,500: {'message':'Internal Server Error','descriptioin':'A generic error message, given when no more specific message is suitable'}
                ,501: {'message':'Not Implemented','descriptioin':'The server either does not recognize the request method, or it lacks the ability to fulfill the request'}
                ,502: {'message':'Bad Gateway','descriptioin':'The server was acting as a gateway or proxy and received an invalid response from the upstream server'}
                ,503: {'message':'Service Unavailable','descriptioin':'The server is currently unavailable (overloaded or down)'}
                ,504: {'message':'Gateway Timeout','descriptioin':'The server was acting as a gateway or proxy and did not receive a timely response from the upstream server'}
                ,505: {'message':'HTTP Version Not Supported','descriptioin':'The server does not support the HTTP protocol version used in the request'}
                ,511: {'message':'Network Authentication Required','descriptioin':'The client needs to authenticate to gain network access'}
                }
    def set_variables(self,website_url):
        print_prefix='set_variables:\t'
        self.url_dict.clear()
        self.url_dict={
            'URL':website_url,
            'URL_Active':'No',
            'status_code':None,
            'Redirected':'No',
            'url_status_info':'',
            'Redirected_URL':'',
            'Robots.txt_isPresent':'No',
            'page_length':0,
            'page_title':''
            }
        self.page_content=''
        self.website_url=website_url
        self.ins_url=WebURLParse(website_url,developer_mode=self.developer_mode,ignore_errors=True)
        self.domain_name=self.ins_url.get_website_parent() + '.' + self.ins_url.get_website_suffix()
        self.domain_details=self.ins_url.get_domain_details()
        if self.developer_mode:
            self._print_(print_prefix + 'Domain Details:' + self.domain_details['schema'] + '\t://' + self.domain_details['www_type'] + '.\t' + self.domain_details['sub_domain'] + '\t.' + self.domain_details['domain_alone'] + '.\t' + self.domain_details['suffix'] + '/\t' + self.domain_details['path'] + '?\t' + self.domain_details['param'])
    def suspect_frameset(self,website_url,page_content=None):
        #4 Frames links - outtechinc.com. Consider only when there is only one domain referred in the frame.
        #will ignore if it is from same domain.
        if page_content:
            current_page_content=page_content
        else:
            html_ins=HTMLHandlingNews(webpage_url=website_url,developer_mode=self.developer_mode,log_process_status=self.log_process_status,print_instance=self.print_instance,deep_developer_mode=False)
            current_page_content=fetch_for_url(website_url)
        f_match=re.search('<[i]?frame ([^><]+)>',current_page_content,re.IGNORECASE)
        if f_match:
            current_page_content=f_match.group(1)
            if 'src' in current_page_content:
                f_match=re.search('src\s*=\s*["\']([^ "\']+)[ "\']',current_page_content,re.IGNORECASE)
                if f_match and len(f_match.group(1))>3:
                    if 'http://' in f_match.group(1) or 'https://' in f_match.group(1):
                        return f_match.group(1)
        return ''
    def check_soft_redirects(self,website_url,no_of_redirects=1):
        if no_of_redirects > 3:
            return website_url
        #print 'check_soft_redirects:self.url_dict',self.url_dict
        html_ins=HTMLHandlingNews(webpage_url=website_url,developer_mode=self.developer_mode,log_process_status=self.log_process_status,print_instance=self.print_instance,deep_developer_mode=False)
        page_content=fetch_for_url(website_url)
        redirect_meta=html_ins.get_meta_data()
        self.url_dict['page_title']=html_ins.get_page_title()
        if 'refresh' in redirect_meta:
            if len(redirect_meta['refresh'])>3:
                absolute_path=get_absolute_path(website_url,redirect_meta['refresh'])
                if len(absolute_path) > 3:
                    return self.check_soft_redirects(absolute_path,no_of_redirects=no_of_redirects+1)
                else:
                    return redirect_meta['refresh']
                return self.check_soft_redirects(redirect_meta['refresh'],no_of_redirects=no_of_redirects+1)
        if 'window.location' in page_content[0:1000]:
            #http://stackoverflow.com/questions/9889459/which-one-is-better-approach-window-parent-location-href-or-window-top-location
            wl_match=re.search('window.location\s*=\s*["\']([^"\']+)["\']\s*;',page_content, re.IGNORECASE)
            if wl_match:
                absolute_path=get_absolute_path(website_url,wl_match.group(1))
                if len(absolute_path) > 3:
                    return self.check_soft_redirects(absolute_path,no_of_redirects=no_of_redirects+1)
                else:
                    return wl_match.group(1)
        if len(page_content) <= 1000 and 'window.parent.location.href' in page_content:
            #view-source:http://mcc.godaddy.com/park/Mzq2n2MbL2A5oP5jLab=
            #window.parent.location.href = 'http://stixsupply.com?reqp=1&reqr=';
            
            #http://stackoverflow.com/questions/9889459/which-one-is-better-approach-window-parent-location-href-or-window-top-location
            wl_match=re.search('window.parent.location.href\s*=\s*["\']([^"\']+)["\']\s*;',page_content, re.IGNORECASE)
            if wl_match:
                absolute_path=get_absolute_path(website_url,wl_match.group(1))
                if len(absolute_path) > 3:
                    return self.check_soft_redirects(absolute_path,no_of_redirects=no_of_redirects+1)
                else:
                    return wl_match.group(1)
        if 'http-equiv' in page_content[0:1000].lower() and 'refresh' in page_content[0:1000].lower() and 'url' in page_content[0:1000].lower():
            #Not picked: view-source:http://www.interactive.com.hk/
            #<meta HTTP-EQUIV="REFRESH" content="0; url=http://www.interactive.com.hk/zen">
            wl_match=re.search('<meta\s*http-equiv\s*=\s*["\']refresh["\']\s*content=["\']([^"\'><]+)["\'\s]*\/>',page_content, re.IGNORECASE)
            if wl_match:
                pattern_found=wl_match.group(1)
                if ';' in pattern_found:
                    p_split=pattern_found.split(';')
                    if len(p_split[1]) > len(p_split[0]):
                        pattern_found= p_split[1].strip()
                    else:
                        pattern_found= p_split[0].strip()
                if pattern_found.lower().startswith('url'):#Is this redundant of refresh
                    pattern_found=pattern_found[3:].strip(' =')
                    absolute_path=get_absolute_path(website_url,pattern_found)
                    if len(absolute_path) > 3:
                        return self.check_soft_redirects(absolute_path,no_of_redirects=no_of_redirects+1)
                    else:
                        return redirect_meta['refresh']
                    #return self.check_soft_redirects(pattern_found,no_of_redirects=no_of_redirects+1)
        if len(page_content) <= 1000 and ('<iframe ' in page_content.lower() or '<frameset ' in page_content.lower()):
            #If there are multiple frame what will happen
            frame_found=self.suspect_frameset(website_url,page_content)
            #print 'frame_found:',frame_found
            if frame_found and len(frame_found)>3:
                return self.check_soft_redirects(frame_found,no_of_redirects=no_of_redirects+1)
        return website_url
    def domain_expired(self):
        #print 'domain_expired:self.url_dict',self.url_dict
        if len(self.url_dict['page_title'])>= len(self.domain_name) and len(self.domain_name)>3:
            title_trimmed=self.url_dict['page_title'].strip(' |-').lower()
            page_content_lower=self.page_content.lower()
            #print 'page_content_lower',repr(page_content_lower)
            if title_trimmed == self.domain_name:
                if len(self.page_content)> 10 and ('buy this domain' in page_content_lower or ('buy ' in page_content_lower and ' domain' in page_content_lower)):
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain is title and Buy Domain in content'
                    return True
                elif len(self.page_content)> 10 and ('is expired' in page_content_lower or ' for sale' in page_content_lower):
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain is title and sale in content'
                    return True
                elif len(self.page_content)> 10 and 'whois' in page_content_lower and 'domain' in page_content_lower:
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain is title and whois in content'
                    return True
                elif len(self.page_content)> 10 and 'domain' in page_content_lower and 'owner' in page_content_lower:
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain is title and owner in content'
                    return True
                elif len(self.page_content)> 10 and (' expired' in page_content_lower and 'domain' in page_content_lower):
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain is title and expired in content'
                    return True
                elif len(self.page_content)> 10 and ('parked ' in page_content_lower and ('domain' in page_content_lower or 'page' in page_content_lower)):
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain is title and parked in content'
                    return True
                elif len(self.page_content)> 10 and 'registered' in page_content_lower and 'domain' in page_content_lower:
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain is title and registered in content'
                    return True
                else:
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain is title.'
                    return True
            elif self.domain_name in title_trimmed:#parked page registered domain
                if 'for sale' in title_trimmed or 'expired' in title_trimmed:
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain in title with sale'
                    return True
                elif len(self.page_content)> 10 and ('is expired' in page_content_lower or ' for sale' in page_content_lower):
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain in title and sale in content'
                    return True
                elif len(self.page_content)> 10 and ('whois' in page_content_lower and 'domain' in page_content_lower):
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain in title and whois in content'
                    return True
                elif len(self.page_content)> 10 and ('parked ' in page_content_lower and ('domain' in page_content_lower or 'page' in page_content_lower)):
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain in title and parked in content'
                    return True
                elif len(self.page_content)> 10 and 'registered' in page_content_lower and 'domain' in page_content_lower:
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain in title and registered in content'
                    return True
                elif len(self.page_content)> 10 and ('buy this domain' in page_content_lower or ('buy ' in page_content_lower or ' domain' in page_content_lower)):
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain in title and Buy Domain in content'
                    return True
                elif len(self.page_content)> 10 and (' expired' in page_content_lower and 'domain' in page_content_lower):
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain in title and expired in content'
                    return True
                else:
                    self.url_dict['url_status_info'] = self.url_dict['url_status_info'] +  ' | Domain in title.'
                    return True
        return False
    def different_domain(self,website_1,website_2):
        domain_input_1=self.ins_url.get_website_parent(website_1) + '.' + self.ins_url.get_website_suffix()
        domain_input_2=self.ins_url.get_website_parent(website_2) + '.' + self.ins_url.get_website_suffix()
        if len(domain_input_1)>2 and len(domain_input_2)>2:
            if domain_input_1 != domain_input_2:
                return True
        return False
    def add_https(self,website_url):
        if website_url.lower().startswith('http://'):
            return 'https://' + website_url[7:]
        else:
            return webpage_url
    def add_www(self,website_url):
        interest_index=website_url.find('://')
        self.domain_details=self.ins_url.get_domain_details(website_url)
        if interest_index >= 0 or (len(self.domain_details['www_type']) == 0):
            pre_part=website_url[:interest_index]
            post_part=website_url[interest_index+3:]
            return  pre_part + '://www.'+ post_part
        else:
            return website_url
    def check_url_status(self,current_url):
        print_prefix='check_url_status:\t'
        temp_url_dict={}
        temp_url_dict.clear()
        temp_url_dict['URL_Active']=''
        temp_url_dict['current_url']=current_url
        temp_url_dict['status_code']=None
        temp_url_dict['Redirected']=''
        temp_url_dict['url_status_info']=''
        temp_url_dict['Redirected_URL']=''
        temp_url_dict['connection_abortted']=False
        try:
            req=requests.get(current_url, timeout=10)
            temp_url_dict['status_code']=req.status_code
            if self.developer_mode:
                self._print_(print_prefix + 'URL:' + current_url + '\tstatus_code:' + str(req.status_code))
            if req.status_code==200:
                temp_url_dict['URL_Active']='Yes'
            elif req.status_code == 403:
                temp_url_dict['URL_Active']='Forbidden'
            elif req.status_code == 404:
                temp_url_dict['URL_Active']='Not Found'
            else:
                if req.status_code in self.status_code_details:
                    temp_url_dict['URL_Active']=self.status_code_details[req.status_code]['message']
                    temp_url_dict['url_status_info']=str(req.status_code) + ':' + self.status_code_details[req.status_code]['message']
                else:
                    temp_url_dict['URL_Active']='Status:' + str(req.status_code)
            if len(req.history)>0:
                status=req.history[0].status_code
                #print status
                if status>=300 and status<400:
                    temp_url_dict['Redirected']='Yes'
                    if not self.different_domain(current_url,req.url):
                        temp_url_dict['url_status_info']='Same Domain'
                    else:
                        temp_url_dict['url_status_info']='Different Domain'
                    temp_url_dict['Redirected_URL']=req.url
                else:
                    temp_url_dict['Redirected']='No'
            else:
                temp_url_dict['Redirected_URL']=''#No need to pass since there is no action
        except Exception as e:
            if self.developer_mode:
                print 'Error while accessing the website:' ,repr(current_url),'.Error:' + str(e)
            if 'time out' in str(e).lower() or 'timed out' in str(e).lower():
                temp_url_dict['url_status_info']='Timeout'
            elif 'connection aborted' in str(e).lower():
                temp_url_dict['url_status_info']='Connection Aborted'
            else:#violation of protocol (_ssl
                temp_url_dict['url_status_info']='Error:' + str(e)
            temp_url_dict['connection_abortted']=True
            if len(temp_url_dict['URL_Active']) <= 1 or (not temp_url_dict['URL_Active']):
                temp_url_dict['URL_Active']='No'
        return temp_url_dict.copy()
    def does_have_www(self,website_url):
        self.domain_details=self.ins_url.get_domain_details(website_url)
        if len(self.domain_details['www_type'])>1:
            return True
        else:
            return False
    def does_have_https(self,website_url):
        if website_url.lower().startswith('https://'): 
            return True
        return False
    def check_status(self,website_url):
        print_prefix='check_status:\t'
        self.set_variables(website_url)
        no_of_status_check_iteration=0
        current_url=website_url
        current_url_result={}
        result_to_pass={}
        #https://www.robertabbey.biz/fine-lighting/designs.aspx
        #http://www.centurycentech.com/frames3.html
        #http://www.kvaerner.com/chemetics
        #print 'before:self.url_dict:',self.url_dict
        www_added=False
        www_have_data=False
        www_url=''
        while True:
            no_of_status_check_iteration += 1
            current_url_result=self.check_url_status(current_url=current_url)#This part is to frame the valid first url only like add missing www or https
            #print 'current_url_result',current_url_result
            url_changed=False
            page_content=self.get_page_content(current_url)
            if self.developer_mode:
                self._print_(print_prefix + 'Result for ' + repr(current_url) + '\t' + repr(current_url_result))
            #print www_added,len(page_content),www_have_data,www_url
            if www_added and '://www.' in current_url.lower() and len(page_content) > 30 and (not www_have_data):
                www_have_data=True
                www_url=current_url
            #print 'AFTER',www_added,len(page_content),www_have_data,www_url
            if current_url_result['connection_abortted'] or (current_url_result['status_code']>401 and current_url_result['status_code']<=503) or (len(page_content)<30):#<html><meta src="/"></html>
                if (('violation of protocol' in current_url_result['url_status_info'].lower() or 'certificate_verify_failed' in current_url_result['url_status_info'].lower()) and 'ssl' in current_url_result['url_status_info'].lower()) or current_url_result['status_code'] == 505:
                    if not self.does_have_https(current_url):
                        new_url=self.add_https(current_url)
                        if len(new_url)>3 and new_url != current_url:
                            url_changed=True
                            current_url=new_url
                else:
                    if not self.does_have_www(current_url):
                        #print current_url,'No www'
                        new_url=self.add_www(current_url)
                        #print current_url,'No www','new',new_url
                        if len(new_url)>3 and new_url != current_url:
                            url_changed=True
                            www_added=True
                            current_url=new_url
                            #print 'new url set true'
            if no_of_status_check_iteration > 4 or (not url_changed):
                break
        if current_url_result['status_code'] or len(current_url_result['url_status_info'])>2:
            self.url_dict.update(current_url_result)
        #print 'after:self.url_dict:',self.url_dict
        if self.url_dict['URL_Active'] == 'No' and 'httpconnectionpool' in self.url_dict['url_status_info'].lower() and 'getaddrinfo failed' in self.url_dict['url_status_info'].lower():
            if self.is_net_active():
                self.url_dict['URL_Active']='Not Exist'
        #print 'self.url_dict',self.url_dict
        #print 'website_url',website_url,"self.url_dict['Redirected']",self.url_dict['Redirected'],www_added,www_have_data,www_url
        if '://www.' not in website_url and  (len(self.url_dict['Redirected'])==0 or self.url_dict['Redirected'] == 'No') and www_added and www_have_data and len(www_url)>3:
            #print 'INSIDE SET'
            self.url_dict['Redirected']='Yes'
            self.url_dict['Redirected_URL']=www_url
            self.url_dict['url_status_info']=self.url_dict['url_status_info'] + ':' + ' www added'
        if not current_url_result['connection_abortted']:
            if website_url[-1]=='/':
                robots_url=website_url+'robots.txt'
            else:
                robots_url=website_url+'/robots.txt'
            try:
                robots_req=requests.get(robots_url)
                if robots_req.status_code==200:
                    self.url_dict['Robots.txt_isPresent']='Yes'
            except:
                self.url_dict['Robots.txt_isPresent']='Too Many Redirects'
        #print 'website_url',website_url,"self.url_dict['Redirected_URL']",self.url_dict['Redirected_URL']
        page_content=self.get_page_content(website_url)
        self.url_dict['page_length']=len(page_content)
        redirect_result=self.check_soft_redirects(website_url)
        if redirect_result == website_url:
            pass
        else:
            self.url_dict['current_url']=redirect_result
            self.url_dict['Redirected']='Yes'
            if self.different_domain(website_url,redirect_result):
                self.url_dict['url_status_info']='Different Domain'
            else:
                self.url_dict['url_status_info']='Same Domain'
            self.url_dict['Redirected_URL']=redirect_result
        #page_content=self.get_page_content(website_url)
        #self.url_dict['page_length']=len(page_content)
        if len(self.url_dict['Redirected_URL']) > 0:
            #print "self.url_dict['Redirected_URL']",self.url_dict['Redirected_URL']
            html_ins=HTMLHandlingNews(webpage_url=self.url_dict['Redirected_URL'],developer_mode=self.developer_mode,log_process_status=self.log_process_status,print_instance=self.print_instance,deep_developer_mode=False)
            page_content=self.get_page_content(self.url_dict['Redirected_URL'])
            self.url_dict['page_title']=html_ins.get_page_title()
        if self.domain_expired():
            if self.url_dict['Redirected'] == 'Yes':
                self.url_dict['Redirected'] = 'Yes and Expired'
            else:
                self.url_dict['Redirected'] = 'Expired'
            self.url_dict['url_status_info']=self.url_dict['url_status_info'].strip()
        if '| Domain is title ' in self.url_dict['url_status_info'] or ' | Domain in title ' in self.url_dict['url_status_info']:
            self.url_dict['URL_Active']='Expired'
        if self.developer_mode:
            self._print_(print_prefix + 'Final Result for url ' + repr(website_url) + '\t' + repr(self.url_dict))
        return self.url_dict
def url_check_status(req_url,developer_mode=False):
    print_prefix='url_check_status:\t'
    developer_mode=developer_mode
    ins=URLStatus(developer_mode=developer_mode)
    return ins.check_status(website_url=req_url)
    url_dict={
        'URL':req_url,
        'URL_Active':'No',
        'status_code':None,
        'Redirected':'No',
        'url_status_info':'',
        'Redirected_URL':'',
        'Robots.txt_isPresent':'No'
        }
    status_code_details={
            100: {'message':'Continue','descriptioin':'The server has received the request headers, and the client should proceed to send the request body'}
            ,101: {'message':'Switching Protocols','descriptioin':'The requester has asked the server to switch protocols'}
            ,103: {'message':'Checkpoint','descriptioin':'Used in the resumable requests proposal to resume aborted PUT or POST requests'}
            ,200: {'message':'OK','descriptioin':'The request is OK (this is the standard response for successful HTTP requests)'}
            ,201: {'message':'Created','descriptioin':'The request has been fulfilled, and a new resource is created'}
            ,202: {'message':'Accepted','descriptioin':'The request has been accepted for processing, but the processing has not been completed'}
            ,203: {'message':'Non-Authoritative Information','descriptioin':'The request has been successfully processed, but is returning information that may be from another source'}
            ,204: {'message':'No Content','descriptioin':'The request has been successfully processed, but is not returning any content'}
            ,205: {'message':'Reset Content','descriptioin':'The request has been successfully processed, but is not returning any content, and requires that the requester reset the document view'}
            ,206: {'message':'Partial Content','descriptioin':'The server is delivering only part of the resource due to a range header sent by the client'}
            ,300: {'message':'Multiple Choices','descriptioin':'A link list. The user can select a link and go to that location. Maximum five addresses'}
            ,301: {'message':'Moved Permanently','descriptioin':'The requested page has moved to a new URL'}
            ,302: {'message':'Found','descriptioin':'The requested page has moved temporarily to a new URL'}
            ,303: {'message':'See Other','descriptioin':'The requested page can be found under a different URL'}
            ,304: {'message':'Not Modified','descriptioin':'Indicates the requested page has not been modified since last requested'}
            ,306: {'message':'Switch Proxy','descriptioin':'No longer used'}
            ,307: {'message':'Temporary Redirect','descriptioin':'The requested page has moved temporarily to a new URL'}
            ,308: {'message':'Resume Incomplete','descriptioin':'Used in the resumable requests proposal to resume aborted PUT or POST requests'}
            ,400: {'message':'Bad Request','descriptioin':'The request cannot be fulfilled due to bad syntax'}
            ,401: {'message':'Unauthorized','descriptioin':'The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided'}
            ,402: {'message':'Payment Required','descriptioin':'Reserved for future use'}
            ,403: {'message':'Forbidden','descriptioin':'The request was a legal request, but the server is refusing to respond to it'}
            ,404: {'message':'Not Found','descriptioin':'The requested page could not be found but may be available again in the future'}
            ,405: {'message':'Method Not Allowed','descriptioin':'A request was made of a page using a request method not supported by that page'}
            ,406: {'message':'Not Acceptable','descriptioin':'The server can only generate a response that is not accepted by the client'}
            ,407: {'message':'Proxy Authentication Required','descriptioin':'The client must first authenticate itself with the proxy'}
            ,408: {'message':'Request Timeout','descriptioin':'The server timed out waiting for the request'}
            ,409: {'message':'Conflict','descriptioin':'The request could not be completed because of a conflict in the request'}
            ,410: {'message':'Gone','descriptioin':'The requested page is no longer available'}
            ,411: {'message':'Length Required','descriptioin':'The "Content-Length" is not defined. The server will not accept the request without it'}
            ,412: {'message':'Precondition Failed','descriptioin':'The precondition given in the request evaluated to false by the server'}
            ,413: {'message':'Request Entity Too Large','descriptioin':'The server will not accept the request, because the request entity is too large'}
            ,414: {'message':'Request-URI Too Long','descriptioin':'The server will not accept the request, because the URL is too long. Occurs when you convert a POST request to a GET request with a long query information'}
            ,415: {'message':'Unsupported Media Type','descriptioin':'The server will not accept the request, because the media type is not supported'}
            ,416: {'message':'Requested Range Not Satisfiable','descriptioin':'The client has asked for a portion of the file, but the server cannot supply that portion'}
            ,417: {'message':'Expectation Failed','descriptioin':'The server cannot meet the requirements of the Expect request-header field'}
            ,500: {'message':'Internal Server Error','descriptioin':'A generic error message, given when no more specific message is suitable'}
            ,501: {'message':'Not Implemented','descriptioin':'The server either does not recognize the request method, or it lacks the ability to fulfill the request'}
            ,502: {'message':'Bad Gateway','descriptioin':'The server was acting as a gateway or proxy and received an invalid response from the upstream server'}
            ,503: {'message':'Service Unavailable','descriptioin':'The server is currently unavailable (overloaded or down)'}
            ,504: {'message':'Gateway Timeout','descriptioin':'The server was acting as a gateway or proxy and did not receive a timely response from the upstream server'}
            ,505: {'message':'HTTP Version Not Supported','descriptioin':'The server does not support the HTTP protocol version used in the request'}
            ,511: {'message':'Network Authentication Required','descriptioin':'The client needs to authenticate to gain network access'}
            }
    try:
        ins_url=WebURLParse(req_url,developer_mode=developer_mode,ignore_errors=True)
        domain_input=ins_url.get_website_parent()
        req=requests.get(req_url, timeout=5)
        url_dict['status_code']=req.status_code
        if developer_mode:
            print print_prefix + 'URL:' + req_url + '\tstatus_code:' + str(req.status_code)
        if req.status_code==200:
            url_dict['URL_Active']='Yes'
        elif req.status_code == 403:
            url_dict['URL_Active']='Forbidden'
        elif req.status_code == 404:
            url_dict['URL_Active']='Not Found'
        else:
            if req.status_code in status_code_details:
                url_dict['URL_Active']=status_code_details[req.status_code]['message']
            else:
                url_dict['URL_Active']='Status:' + str(req.status_code)
        #print req.history
        #print req.headers
        #print req.url
        if len(req.history)>0:
            status=req.history[0].status_code
            #print status
            if status>=300 and status<400:
                url_dict['Redirected']='Yes'
                # if 'www.' in req_url:
                    # domain_index=req_url.index('www.')
                    # domain_name=req_url[domain_index+4:]
                # else:
                    # domain_index=req_url.index('://')
                    # domain_name=req_url[domain_index+3:]
                domain_target = ins_url.get_website_parent(req.url)
                #print "DOMAIN_NAME    ",domain_name
                if domain_target == domain_input:
                    url_dict['url_status_info']='Same Domain'
                else:
                    url_dict['url_status_info']='Different Domain'
                url_dict['Redirected_URL']=req.url
                if False:#commented below section
                    if status==301 or status==308:
                        if domain_name in req.url:
                            url_dict['url_status_info']='Same Domain'
                        else:
                            url_dict['url_status_info']='Different Domain'
                    elif status==302 or status==303 or status==307:
                        url_dict['url_status_info']='Same Domain'
        else:
            url_dict['Redirected_URL']=''#No need to pass since there is no action
    except Exception as e:
        if developer_mode:
            print 'Error while accessing the website:' ,req_url,'.Error:' + str(e)
        if 'time out' in str(e).lower() or 'timed out' in str(e).lower():
            url_dict['url_status_info']='Timeout'
        elif 'connection aborted' in str(e).lower():
            url_dict['url_status_info']='Connection Aborted'
        else:
            url_dict['url_status_info']='Error:' + str(e)
        return url_dict
    if req_url[-1]=='/':
        robots_url=req_url+'robots.txt'
    else:
        robots_url=req_url+'/robots.txt'
    try:
        robots_req=requests.get(robots_url)
        if robots_req.status_code==200:
            url_dict['Robots.txt_isPresent']='Yes'
    except:
        url_dict['Robots.txt_isPresent']='Too Many Redirects'
    return url_dict


if __name__=='__main__':
    if True:
        links=['http://quadreliservice.com/','http://spaldingdedecker.com','https://www.quadreliservice.com/redirect/default.aspx']
        record_count=0
        for each_url in links:
            record_count += 1
            print url_check_status(each_url,developer_mode=False)
            #if record_count > 0 : break
    elif not True:
        #url_tocheck_from_excel()
        links=['http://www.thealbertasupernet.com/about_us/about_us.html'#NOT Found
            ,'http://www.nike.com'#Redirect not detected
            ,'http://www.caracalenergy.com'
            ,'http://www.flightsafety.com/'
            ,'http://www.247rad.com'
            ,'http://www.ultragreenhome.com'
            ,'http://www.5htech.com'
            ,'http://www.abcoscale.com'
            ,'http://www.wholesaleglassandmirror.net'
            ,'http://www.a-1transfer.com'
            ,'http://www.ablecommtech.com'
            ,'http://www.mauilock.com'
            ,'http://www.aaatexas.com'
            ,'http://www.1stvalleycu.com'
            ,'http://www.ablecofinance.com'
            ,'http://www.abcobramer.com'
            ,'http://www.7actech.com'
            ,'http://www.dnatestingcanada.com'
            ,'http://www.benevity.com'
            ,'http://www.fastfilemedia.com'
            ,'http://www.ipec.ca'
            ,'http://www.aquasource.net'
            ,'http://www.lofli.com'
            ,'http://www.millhouse.co/private'
            ,'http://www.microtissuetechplc.com'
            ,'http://www.momentouscorp.com'
            ,'http://www.ghcg.com'
            ,'http://www.cipriani.com/locations/london.php'
            ,'http://www.cains.co.uk'
            ,'http://www.charterbankec.com'
            ,'http://www.321studios.com'
            ,'http://theadvocate.com/news/neworleans/neworleansnews/15770108-70/covingtons-resource-bank-enters-baton-rouge-market'
            ,'http://www.abilitycrm.com'
            ,'http://www.abbyy.com'
            ,'http://www.clickpointsoftware.com'
            ,'http://www.6figurejobs.com'
            ,'http://www.asmallorange.com'
            ,'http://www.abacustranscriptions.net'
            ,'http://www.abilitycrm.com'
            ,'http://www.ableco.com'
        ]
        record_count=0
        for each_url in links:
            record_count += 1
            print url_check_status(each_url,developer_mode=False)
            #if record_count > 0 : break


