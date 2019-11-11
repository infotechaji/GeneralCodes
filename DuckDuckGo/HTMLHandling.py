"""
    Version    : v2.8
    History    :
                1.0 - 07/31/2015 - Initial Version
                1.1 - 10/29/2015 - updated fetch_content_for_url to fetch data from fetch_from_url
                1.2 - 02/04/2016 - Addding class for HTML Handling - new method
                1.3 - 02/15/2016 - Adding class for HTMLHandlingNews for News
                1.4 - 02/24/2016 - get_news_from_index - making it recursive to handle article and div
                1.5 - 02/25/2016 - get_news_from_index - Enhanced news detection. Ignored Figure tag
                1.6 - 03/01/2016 - Removed new lines and tabs in fetch_title before extracting title using re.
                1.7 - 03/04/2016 - Added new function get_content_from_page to get all text, other than anchored, from page body.
                                   Renamed __initiate_print_instance__ to initiate_print_instance. Added body tag to get_tag_analysis_from_html_content.CONTAINER_TAGS
                1.8 - 03/08/2016 - Added 'html' as top most in get_tag_analysis_from_html_content and default parent data in get_parent_child_relationship
                1.9 - 03/09/2016 - Do we need to replace li and <ol> <ul> by /n
                1.10 - 03/10/2016 - tag with no content and no child will be ignore if include_empty_tags=False in get_all_childs_and_tags
                1.11 - 03/14/2016 - get_focused_content: Minimum length of article whene no common parent is detected is reduced to 500
                1.12 - 03/16/2016 - Adding svg to image tags to ignore in support_tag_analysis_reduce_tag
                1.12 - 03/17/2016 - Fetching Menus from website. Adding function get_menus_from_website and supporting function
                1.13 - 04/07/2016 - Completed a version of get_menus_from_website
                1.14 - 04/08/2016 - Create object and access archived page in fetch_pr_archival_details
                1.15 - 04/08/2016 - Removing menus from news and content
                1.16 - 05/25/2016 - fetch_all_links_for_website - Fetch links - recursive logic
                1.17 - 05/25/2016 - Import WebsiteCodesSupport for restrict linked url by domain
                1.18 - 05/26/2016 - New function is added to get metadata - get_meta_data()
                1.19 - 06/02/2016 - added no_exclusion arg in get_content_from_page to get menu details as well.
                1.20 - 14/07/2016 - added functionality to get date from data feed
                1.21 - 14/07/2016 - added functionality to get date from source url
                1.22 - 14/07/2016 - restricted data feed of length less than 20 and trimmed the data feed greater than 20 in length
                1.23 - 14/07/2016 - restricted data feed based on the words given in press_release_stop_words list
                v2.0 - 07/20/2016 - Code check-in to common repository
                v2.1 - 08/03/2016 - Used WebURLParse class to get domain name and added TRACK_TIME_MODE as a class variable
                v2.2 - 08/12/2016 - Fix in get_all_anchor_tags. Passed absolute_path instead of a_tag_href
                v2.3 - 09/29/2016 - Cosmetics and youtube added in social links
                v2.4 - 10/20/2016 - deep_developer_mode is added
                v2.5 - 11/25/2016 - variable for all_social_domains
                v2.6 - 05/10/2017 - link_type Special is allowed if include_script_link in fetch_all_anchor. Special is tel: , mailto:, etc
                v2.7 - 05/11/2017 - meta tag og:image and description are added. added refresh meta tag
                v2.8 - 05/17/2017 - Included link tag for html head parse. link[rel='shortcut icon',icon,'apple-touch-icon'] has place holder for image.
p    A p element's end tag may be omitted if the p element is immediately followed by an address, article, aside, blockquote, div, dl, fieldset, footer, form, h1, h2, h3, h4, h5, h6, header, hgroup, hr, main, nav, ol, p, pre, section, table, or ul, element, or if there is no more content in the parent element and the parent element is not an a element.
p    An li element's end tag may be omitted if the li element is immediately followed by another li element or if there is no more content in the parent element.
        CONTAINER_TAGS=['div','table','td','tr','h1','h2','h3','h4','h5','h6','p','a','span','area','ul','li','article']#ul,li are added
        BLOCK_TAGS=['div','table','p','ul','article']#does not allow text tags
        TEXT_ONLY_TAGS=['p']#can not be in text tags
    Pending Issues:
        Article not fetched fully: http://www.fool.co.uk/investing/2016/01/14/can-you-trust-the-7-yields-at-aberdeen-asset-management-plc-bp-plc/
                                   http://www.afr.com/business/retail/2xu-hoping-for-a-touchdown-with-600m-listing-20150325-1m76al
        Article not fetched      : http://www.ferret.com.au/c/gorter-hatches/gorter-hatches-introduces-their-scissor-stairs-and-attic-ladders-n1833003
                                   http://www.englandhockey.co.uk/news.asp?itemid=34192&itemTitle=2XU+becomes+Official+Compression+Equipment+Supplier+of+Great+Britain+and+England+Hockey&section=22
                                   http://www.insurancejournal.com/services/newswire/2015/11/16/388964.htm
        Link is not fetched properly when link has preceeding space  <li><a href=" http://goo.gl/iQ30as" target="_blank">Windows 10 for Enterprise: More secure and up to date</a></li>
        fetch_pr_archival_page_links - http://www.halliburton.com/en-US/news/press-releases.page?DocListingBundle=2B3D3E82&node-id=hgeyxtfr - links inside the scripts are not fetched.
        unhandled closing tags - view-source:http://www.ilink-systems.com/Thinking-Beyond/Blogs - <a id="EDS2696Pagging1" class="active page" href="http://www.ilink-systems.com/thinking-beyond/blogs/PgrID/2696/PageID/1"/>1</a> /> is not proper closing here. How to handle it?
00A0--NBSP

To identify comments section and to cut off.
Reader comments on this site are moderated before publication to promote lively and civil debate. We encourage your comments but submitting one does not guarantee publication. We publish hundreds of comments daily, and if a comment is rejected it is likely because it does not meet with our comment guidelines, which you can read here . No correspondence will be entered into if a comment is declined.
Load Comments Loading Comments...
Reader comments on this site are moderated before publication to promote lively and civil debate. We encourage your comments but submitting one does not guarantee publication. We publish hundreds of comments daily, and if a comment is rejected it is likely because it does not meet with our comment guidelines, which you can read here . No correspondence will be entered into if a comment is declined.
Be the first to comment on this article.
You Might Like
Join the discussion
Our Commenting Policies
5 years 1 Day
Last updated: Updating...
Last updated: Updating...
View full quote
ASX Announcements Expand
ASX Announcements
View all announcements
Newsletter Sign Up
Register to receive the latest news straight to your inbox. There are different newsletters to suit all your hockey needs, each containing exciting and exclusive features.
Don't show again
Issues Faced: No Body tag(populated using script) - http://www.dailyexcelsior.com/ips-officer-promoted/

New Lines in anchor value:
CARTER GRANGE HOMES PTY LTD HYPERLINK http://cartergrange.com.au/ http://cartergrange.com.au
CARTER NEWELL HYPERLINK http://www.carternewell.com/ http://www.carternewell.com
No body but header
CAY'S ENGINEERING http://www.cays.com.au/
www.ieso.ca/Pages/News.aspx - News links are not fetched properly - newlines are there
http://www.ieso.ca/Pages/ - no record_type 

Fetching multiple time: https://www.caa.ca : https://www.caa.ca/about-us/contact-us/

News: http://cincysportszone.com/earnings-analysis-update-for-appfolio-inc-nasdaqappf/21766/ still ads are coming
get_content_from_page: not working for 'https://www.shellvacationsclub.com/home.page'

Include area tag for fetch_all_links_for_website
"""
import re
from Utilities import *
from webSearch import *
from urlparse import urlparse,urljoin
import socket
import copy
from WebsiteCodesSupport import *
import requests

all_social_domains=['twitter','facebook','google','pinterest','linkedin','fb','flickr','instagram','tumblr']
all_special_links_schema=['tel','mailto']
stopwords_generic=[
        "a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at"
        ,"be","because","been","before","being","below","between","both","but","by"
        ,"can't","cannot","could","couldn't"
        ,"did","didn't","do","does","doesn't","doing","don't","down","during"
        ,"each"
        ,"few","for","from","further"
        ,"had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's"
        ,"i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself"
        #,"just"
        ,"let's"
        ,"me","more","most","mustn't","my","myself"
        ,"no","nor","not"
        ,"of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own"
        ,"same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such"
        ,"than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too"
        ,"under","until","up"
        ,"very"
        ,"was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't"
        ,"you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"
    ]
press_release_stop_words = ['contact us', 'watch our', 'choose', 'click to zoom', 'read more', 'click here', 'load more', 'find an expert', 'watch more', 'subscribe', 'read full', 'news archive']
def what_is_the_object_type(input_is_input):
    #Improve this
    special_words=['and','of','for','&']
    developer_mode=False
    if len(input_is_input.strip()) == 0 or not input_is_input:
        return {'type':'Blank','sub_type':'','code':'BLK'}
    input_statement=get_html_to_unicode_string(input_is_input.strip())
    if len(input_statement.strip()) == 0 or not input_statement:
        if len(input_statement.strip()) == 0 and len(input_statement) > 0:
            return {'type':'Spaces','sub_type':'','code':'SSS'}
        return {'type':'Blank','sub_type':'','code':'BLK'}
    #w_h=open('product.unicode.txt','ab')
    #print repr(input_is_input)
    #if isinstance(input_is_input,unicode):
    #    w_h.write(input_is_input.encode('utf-8') +'\t' + input_statement.encode('utf-8') +'\n')
    #else:
    #    w_h.write(input_is_input +'\t' + input_statement.encode('utf-8') +'\n')
    #w_h.close()
    if developer_mode: print 'Current Word:' + input_statement.encode('utf-8')
    if input_statement == re.sub(r'[a-zA-Z0-9]+','',input_statement):
        return {'type':'NoAlpha','sub_type':'','code':'NA'}
    if ' ' not in input_statement:
        #All single word input should be classified here
        if developer_mode: print 'Single Word:' + input_statement.encode('utf-8')
        if input_statement.lower() in special_words:
            return {'type':'Word','sub_type':'Special','code':'WSP'}
        if input_statement.lower() in english_articles:
            return {'type':'Word','sub_type':'Articles','code':'WSA'}
        if input_statement.lower() in stopwords_generic:
            return {'type':'Word','sub_type':'StopWords','code':'WSW'}
        if input_statement.lower() in salutation_generic:
            return {'type':'Word','sub_type':'Salutation','code':'WSL'}
        if input_statement.lower() in week_days_long:
            return {'type':'Word','sub_type':'Day','code':'WDA'}
        if input_statement.lower() in month_normalize:
            return {'type':'Word','sub_type':'Month','code':'WMO'}
        data_type_result=is_number(input_statement)
        if data_type_result:
            return {'type':'Number','sub_type':'','code':'WNU'}
        data_type_result=is_date(input_statement)
        if data_type_result and (len(input_statement) - len(re.sub(r'[0-9]+','',input_statement)))>1:
            return {'type':'Date','sub_type':'','code':'WDT'}
        if input_statement == input_statement.upper():
            #all upper, how about 12ABC
            return {'type':'Entity','sub_type':'AllUpper','code':'WAU'}
        if input_statement == UpperCamelCase(input_statement):
            #upper camelcase, how about A12
            return {'type':'Entity','sub_type':'CamelUpper','code':'WCU'}
        if input_statement == input_statement.lower():
            return {'type':'Word','sub_type':'AllLower','code':'WAL'}
        #print 'No classification found',input_statement
        return {'type':'Word','sub_type':'Mix','code':'WMI'}
    if '.' in input_statement:
        if developer_mode: print 'Statements:' + input_statement.encode('utf-8')
        #email, url
        input_intermediate_result=paragraph_to_sentence(input_statement)
        if len(input_intermediate_result) > 1:
            return {'type':'Statement','sub_type':'Multiple','code':'SMU'}
        return {'type':'Statement','sub_type':'Single','code':'SSI'}
    else:
        if developer_mode: print 'Set of Words:' + input_statement.encode('utf-8')
        #print 'Looping block'
        #basically a block of words which does not looks like a line/statement - probably some heading for the following block
        #First will identify all upper case or upper camel case
        # Then further can be split using stopwords or punctuation
        input_split=input_statement.split(' ')
        output_patter=what_is_the_object_type(input_split[0])['code']
        for i in range(len(input_split)):
            if i == 0: continue
            each_word=input_split[i]
            sub_pattern=what_is_the_object_type(each_word)
            if developer_mode: print 'Each Word:' +'\t' +each_word.encode('utf-8') + '\t' + sub_pattern['code']
            #print '"' + each_word +'"\t' + sub_pattern['sub_type']
            output_patter = output_patter + '-' + sub_pattern['code']
        return {'type':'Block','sub_type':output_patter,'code':output_patter}
    #phone number   http://stackoverflow.com/questions/2113908/what-regular-expression-will-match-valid-international-phone-numbers
    return {'type':'None','sub_type':'','code':'NO'}
class URLStatusDoNotUse():
    def __init__(self,developer_mode=False,debug_mode=[],print_instance=None):
        self.developer_mode=developer_mode
        self.debug_mode=debug_mode
        status_code_map={
            100: {'message':'Continue','description':'The server has received the request headers, and the client should proceed to send the request body'}
            ,101: {'message':'Switching Protocols','description':'The requester has asked the server to switch protocols'}
            ,103: {'message':'Checkpoint','description':'Used in the resumable requests proposal to resume aborted PUT or POST requests'}
            ,200: {'message':'OK','description':'The request is OK (this is the standard response for successful HTTP requests)'}
            ,201: {'message':'Created','description':'The request has been fulfilled, and a new resource is created'}
            ,202: {'message':'Accepted','description':'The request has been accepted for processing, but the processing has not been completed'}
            ,203: {'message':'Non-Authoritative Information','description':'The request has been successfully processed, but is returning information that may be from another source'}
            ,204: {'message':'No Content','description':'The request has been successfully processed, but is not returning any content'}
            ,205: {'message':'Reset Content','description':'The request has been successfully processed, but is not returning any content, and requires that the requester reset the document view'}
            ,206: {'message':'Partial Content','description':'The server is delivering only part of the resource due to a range header sent by the client'}
            ,300: {'message':'Multiple Choices','description':'A link list. The user can select a link and go to that location. Maximum five addresses'}
            ,301: {'message':'Moved Permanently','description':'The requested page has moved to a new URL'}
            ,302: {'message':'Found','description':'The requested page has moved temporarily to a new URL'}
            ,303: {'message':'See Other','description':'The requested page can be found under a different URL'}
            ,304: {'message':'Not Modified','description':'Indicates the requested page has not been modified since last requested'}
            ,306: {'message':'Switch Proxy','description':'No longer used'}
            ,307: {'message':'Temporary Redirect','description':'The requested page has moved temporarily to a new URL'}
            ,308: {'message':'Resume Incomplete','description':'Used in the resumable requests proposal to resume aborted PUT or POST requests'}
            ,400: {'message':'Bad Request','description':'The request cannot be fulfilled due to bad syntax'}
            ,401: {'message':'Unauthorized','description':'The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided'}
            ,402: {'message':'Payment Required','description':'Reserved for future use'}
            ,403: {'message':'Forbidden','description':'The request was a legal request, but the server is refusing to respond to it'}
            ,404: {'message':'Not Found','description':'The requested page could not be found but may be available again in the future'}
            ,405: {'message':'Method Not Allowed','description':'A request was made of a page using a request method not supported by that page'}
            ,406: {'message':'Not Acceptable','description':'The server can only generate a response that is not accepted by the client'}
            ,407: {'message':'Proxy Authentication Required','description':'The client must first authenticate itself with the proxy'}
            ,408: {'message':'Request Timeout','description':'The server timed out waiting for the request'}
            ,409: {'message':'Conflict','description':'The request could not be completed because of a conflict in the request'}
            ,410: {'message':'Gone','description':'The requested page is no longer available'}
            ,411: {'message':'Length Required','description':'The "Content-Length" is not defined. The server will not accept the request without it'}
            ,412: {'message':'Precondition Failed','description':'The precondition given in the request evaluated to false by the server'}
            ,413: {'message':'Request Entity Too Large','description':'The server will not accept the request, because the request entity is too large'}
            ,414: {'message':'Request-URI Too Long','description':'The server will not accept the request, because the URL is too long. Occurs when you convert a POST request to a GET request with a long query information'}
            ,415: {'message':'Unsupported Media Type','description':'The server will not accept the request, because the media type is not supported'}
            ,416: {'message':'Requested Range Not Satisfiable','description':'The client has asked for a portion of the file, but the server cannot supply that portion'}
            ,417: {'message':'Expectation Failed','description':'The server cannot meet the requirements of the Expect request-header field'}
            ,500: {'message':'Internal Server Error','description':'A generic error message, given when no more specific message is suitable'}
            ,501: {'message':'Not Implemented','description':'The server either does not recognize the request method, or it lacks the ability to fulfill the request'}
            ,502: {'message':'Bad Gateway','description':'The server was acting as a gateway or proxy and received an invalid response from the upstream server'}
            ,503: {'message':'Service Unavailable','description':'The server is currently unavailable (overloaded or down)'}
            ,504: {'message':'Gateway Timeout','description':'The server was acting as a gateway or proxy and did not receive a timely response from the upstream server'}
            ,505: {'message':'HTTP Version Not Supported','description':'The server does not support the HTTP protocol version used in the request'}
            ,511: {'message':'Network Authentication Required','description':'The client needs to authenticate to gain network access'}
        }
        self.initiate_print_instance(print_instance)
        self.basic_info()
    def basic_info(self):
        print_prefix='basic_info\t'
        if self.developer_mode: self._print_(print_prefix + 'Started')
        if 'basic_info' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        self.url_status={}
        self.url_status['url_status']=''
        self.url_status['url_redirected']='No'
        self.url_status['no_of_redirections']=None
        self.url_status['url_redirect_list']=[]
        self.url_status['status_code_list']=[]
        self.url_status['final_url']=''
        self.url_status['status_code']=None
        self.url_status['input_url']=''
        self.url_status['parsed_url']=''
        self.url_status['error']=''
        return True
    def check_url(self,url):
        print_prefix='check_url\t'
        if self.developer_mode: self._print_(print_prefix + 'Started')
        if 'check_url' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if not url or len(url) < 4:
            self.basic_info()
            return self.url_status
        if 'http://' in url.lower() or 'https://' in url.lower():
            current_url= url
        else:
            current_url='http://' + url
        self.url_status['parsed_url']=current_url
        self.url_status['input_url']=url
        try:
            url_response=requests.get(current_url)
            if url_response:
                self.url_status['url_status']='Active'
                self.url_status['status_code']=url_response.status_code
                self.url_status['final_url']=current_url
                if url_response.history:
                    self.url_status['url_status']='Redirected'
                    self.url_status['url_redirected']='No'
                    self.url_status['no_of_redirections']=len(url_response.history)
                    for each_hist in url_response.history:
                        self.url_status['url_redirect_list'].append((each_hist.status_code,each_hist.url))
                        self.url_status['status_code_list'].append(each_hist.status_code)
                        self.url_status['final_url']=each_hist.url
            else:
                self.url_status['url_status']='Error'
                self._print_(print_prefix + 'No output from requests.get()\t Technical error.')
                custom_exit()
        except Exception as e:
            self.url_status['url_status']='Error'
            self.url_status['error']=str(e)
        return self.url_status
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True):
        input_string=input_string_in
        if len(self.current_function_name) > 1:
            #input_string='HTMLHandling_New:' + self.current_function_name + ':' + input_string
            input_string='HTMLHandlingNews:' + input_string
        else:
            input_string='HTMLHandlingNews:' + input_string
        if self.print_instance:
            self.print_instance.customPrint(input_string,skip_timestamp=skip_timestamp,add_leading_space=add_leading_space)
        else:
            print input_string
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

class HTMLHandlingNews():
    def __init__(self,webpage_url,html_content_in=None,use_selenium=False,developer_mode=False,print_instance=None,debug_mode=[],work_offline=False,log_process_status=True,deep_developer_mode=False):
        self.use_selenium=use_selenium
        #self.include_script_link=include_script_link #Commented in 1.14
        self.developer_mode=developer_mode
        self.deep_developer_mode=deep_developer_mode
        self.debug_mode=debug_mode
        self.current_function_name=''
        self.log_process_status=log_process_status
        self.webpage_url=webpage_url
        self.html_content=html_content_in
        self.basic_info_collected=False
        self.url_of_basic_info_collected=''
        self.tag_details_result=None
        self.head_tag_details_result=None
        self.work_offline=work_offline
        self.key_indexes={}
        self.TRACK_TIME_MODE=False
        self.initiate_print_instance(print_instance)
        self.ins_weburlparse=WebURLParse(webpage_url,ignore_errors=True)
        if self.developer_mode:
            self._print_('__init__:\t' + ' Instance created with developer_mode:' + str(self.developer_mode) + ' \t Log Process:' + str(self.log_process_status))
        self.HTMLHandling_New_ins=HTMLHandling_New(developer_mode=self.developer_mode,debug_mode=self.debug_mode,work_offline=self.work_offline,log_process_status=self.log_process_status,print_instance=self.print_instance)
        self.basic_info()
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='HTMLHandlingWrapper'
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
    def basic_info(self):
        print_prefix='basic_info\t'
        if self.developer_mode: self._print_(print_prefix + 'Started')
        if 'basic_info' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if (not self.basic_info_collected) or (self.basic_info_collected and self.webpage_url != self.url_of_basic_info_collected):
            if debug_mode:
                self._print_(print_prefix + 'processing tag details for ' + self.webpage_url)
            tag_details_result=self.HTMLHandling_New_ins.get_tag_analysis_from_html_content(url_path=self.webpage_url,html_content_in=self.html_content,use_selenium=self.use_selenium,process_menu=True,remove_header=False,remove_footer=False,developer_mode=False,use_head=False,tags_to_collect=['div','article','p','a','ol','ul','body','header','footer'])
            if debug_mode:
                self._print_(print_prefix + 'No of records in tag details : ' + str(len(tag_details_result)))
            head_tag_details_result=self.HTMLHandling_New_ins.get_tag_analysis_from_html_content(url_path=self.webpage_url,html_content_in=self.html_content,use_selenium=self.use_selenium,process_menu=True,remove_header=False,remove_footer=False,developer_mode=False,use_head=True,tags_to_collect=['title','meta','base'])
            if debug_mode:
                self._print_(print_prefix + 'No of records in head tag details : ' + str(len(head_tag_details_result)))
            if tag_details_result:
                self.tag_details_result=tag_details_result
                self.url_of_basic_info_collected=self.webpage_url
                if debug_mode: self._print_(print_prefix + 'Body Tag details available')
            if head_tag_details_result:
                self.head_tag_details_result=head_tag_details_result
                self.url_of_basic_info_collected=self.webpage_url
                if debug_mode: self._print_(print_prefix + 'Head tag details available')
            if self.head_tag_details_result:
                if 'base_url' in self.head_tag_details_result:
                    self.base_url=self.head_tag_details_result['base_url'][5]
                    if debug_mode: self._print_(print_prefix + 'Base url given:\t' + str(self.base_url))
                else:
                    self.base_url=self.webpage_url
            else:
                self.base_url=self.webpage_url
            if not tag_details_result and not head_tag_details_result:
                if debug_mode: self._print_(print_prefix + 'Both body and head tag details are not available')
                self.tag_details_result=None
                self.head_tag_details_result=None
                self.url_of_basic_info_collected=''
                self.basic_info_collected=False
                return False
            if not tag_details_result:
                self.tag_details_result={}
                self.tag_details_result['header']=[]
                self.tag_details_result['footer']=[]
                self.tag_details_result['a']=[]
            self.basic_info_collected=True
            self.key_indexes['menu']=[]
            self.key_indexes['news']=[]
            self.key_indexes['sitemap']=[]
            if self.tag_details_result['header']:
                self.add_key_index('header',self.tag_details_result['header'])
            else:
                self.key_indexes['header']=[]
            if self.tag_details_result['footer']:
                self.add_key_index('footer',self.tag_details_result['footer'])
            else:
                self.key_indexes['footer']=[]
            for each_tag in self.tag_details_result['a']:
                reduced_tag=self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(self.tag_details_result,each_tag,process_anchors=True)
                if len(reduced_tag)>=7:
                    reduced_tag=re.sub(r'[^a-z]+','',reduced_tag.lower())
                    if len(reduced_tag)>=7 and len(reduced_tag)<=10 and 'sitemap' in reduced_tag and len(self.tag_details_result[each_tag][5])>3:
                        self.key_indexes['sitemap'].append(each_tag)
            self.menu_data=self.get_menus_from_website()
            if self.key_indexes['menu']:
                for each_index in self.key_indexes['menu']:
                    self.key_indexes['news'].append(each_index)
            if self.key_indexes['footer']:
                for each_index in self.key_indexes['footer']:
                    self.key_indexes['news'].append(each_index)
            if debug_mode:# or self.developer_mode:
                for each_tag in self.tag_details_result:
                    self._print_(print_prefix + 'TAG:\t' + str(each_tag) + ':' + str(self.tag_details_result[each_tag]))
                for each_tag in self.head_tag_details_result:
                    self._print_(print_prefix + 'HEAD TAG:\t' + str(each_tag) + ':' + str(self.head_tag_details_result[each_tag]))
        return True
    def get_page_title(self):
        print_prefix='get_page_title\t:\t'
        if 'get_page_title' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        page_title=''
        if self.head_tag_details_result:
            if 'title' in self.head_tag_details_result:
                if self.head_tag_details_result['title']:
                    page_title_at=self.head_tag_details_result['title'][0]
                    if debug_mode: self._print_(print_prefix + 'page title details:' + str(self.head_tag_details_result[page_title_at]))
                    if len(self.head_tag_details_result[page_title_at][1])>0:
                        page_title=self.head_tag_details_result[page_title_at][1]
        return page_title
    def get_meta_data(self):
        print_prefix='get_meta_data\t:\t'
        if 'get_meta_data' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        meta_data_details={'keywords':'','description':'','robots':'','copyright':'','viewport':'','og:image':'','og:description':'','refresh':''}
        my_base=self.base_url
        if self.head_tag_details_result:
            if 'meta' in self.head_tag_details_result:
                for each_tag in self.head_tag_details_result['meta']:
                    meta_tag_details=self.head_tag_details_result[each_tag][8]
                    if 'name' in meta_tag_details:
                        current_meta_data_name=meta_tag_details['name'].lower()
                        current_meta_data_content=''
                        if 'content' in meta_tag_details:
                            current_meta_data_content=meta_tag_details['content']
                        if debug_mode: self._print_(print_prefix + str(current_meta_data_name) + '\t' + str(current_meta_data_content))
                        if current_meta_data_name in meta_data_details and len(current_meta_data_content)>0:
                            meta_data_details[current_meta_data_name]=current_meta_data_content
                    elif 'property' in meta_tag_details:
                        current_meta_data_name=meta_tag_details['property'].lower()
                        current_meta_data_content=''
                        if 'content' in meta_tag_details:
                            current_meta_data_content=meta_tag_details['content']
                        if debug_mode: self._print_(print_prefix + str(current_meta_data_name) + '\t' + str(current_meta_data_content))
                        if current_meta_data_name in meta_data_details and len(current_meta_data_content)>0:
                            meta_data_details[current_meta_data_name]=current_meta_data_content
                    elif 'http-equiv' in meta_tag_details:
                        current_meta_data_name=meta_tag_details['http-equiv'].lower()
                        current_meta_data_content=''
                        if 'content' in meta_tag_details:
                            current_meta_data_content=meta_tag_details['content']
                        else:
                            continue
                        if debug_mode: self._print_(print_prefix + str(current_meta_data_name) + '\t' + str(current_meta_data_content))
                        if current_meta_data_name in meta_data_details and 'url' in current_meta_data_content.lower() and '=' in current_meta_data_content:
                            if ';' in current_meta_data_content:
                                current_meta_data_content_split=current_meta_data_content.split(';')
                                if 'url' in current_meta_data_content_split[0].lower() and '=' in current_meta_data_content_split[0]:
                                    current_meta_data_content=current_meta_data_content_split[0].strip()
                                else:
                                    current_meta_data_content=current_meta_data_content_split[1].strip()
                            if current_meta_data_content.lower().startswith('url'):
                                current_meta_data_content=current_meta_data_content[3:].strip(' =')
                                meta_data_details[current_meta_data_name]=current_meta_data_content
            if 'link' in self.head_tag_details_result:
                for each_tag in self.head_tag_details_result['link']:
                    meta_tag_details=self.head_tag_details_result[each_tag][8]
                    if 'rel' in meta_tag_details and 'href' in meta_tag_details:
                        current_meta_data_name=meta_tag_details['rel'].lower()
                        current_meta_data_content=meta_tag_details['href']
                        if debug_mode: self._print_(print_prefix + str(current_meta_data_name) + '\t' + str(current_meta_data_content))
                        if current_meta_data_name in ['icon','shortcut icon','apple-touch-icon'] and len(current_meta_data_content)>3:
                            if current_meta_data_name in ['icon','shortcut icon']:
                                current_meta_data_name='favicon'
                                if current_meta_data_name in meta_data_details and len(meta_data_details[current_meta_data_name])>1: continue
                            meta_data_details[current_meta_data_name]=self.HTMLHandling_New_ins.get_absolute_path(my_base,current_meta_data_content)
        return meta_data_details
        '''
        <meta id="MetaKeywords" name="KEYWORDS"
        <meta id="MetaDescription" name="DESCRIPTION"
        <meta id="MetaRobots" name="ROBOTS"
        <meta id="MetaCopyright" name="COPYRIGHT" content="Copyright &amp;copy; 2016 by iLink Systems, Inc." />
        <meta name="viewport"
        '''
    def fetch_all_anchor(self,restrict_domain=False,allow_social=True):
        print_prefix='fetch_all_anchor\t:'
        if 'fetch_all_anchor' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if not self.basic_info_collected:
            if debug_mode: self._print_(print_prefix + 'basic_info_collected is not set to True')
            return []
        return self.HTMLHandling_New_ins.get_all_anchor_tags(self.tag_details_result,self.base_url,restrict_domain=restrict_domain,allow_social=allow_social)
    def fetch_all_links_for_website(self,max_depth_level=2,maximum_links=200,restrict_domain=True,allow_social=True):
        #Include area tag: http://queenwood.co.uk/ 
        print_prefix='fetch_all_links_for_website\t:'
        consumed_links=[]
        output_anchor_list=[]
        if 'fetch_all_links_for_website' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if not self.basic_info_collected:
            if debug_mode: self._print_(print_prefix + 'basic_info_collected is not set to True')
            return []
        curr_depth_level=1
        site_map_consumed=False
        current_list_of_links=[]
        next_set_of_links=[]
        if self.webpage_url[-1] == '/':
            current_list_of_links.append(self.webpage_url[:-1])
        else:
            current_list_of_links.append(self.webpage_url)
        domain_of_page=self.ins_weburlparse.get_website_parent(self.webpage_url)
        exit_all_loops=False
        while curr_depth_level <= max_depth_level:
            if current_list_of_links and len(current_list_of_links) > 0:
                pass
            else:
                if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'No more links to process')
                break
            for each_link in current_list_of_links:
                if self.ins_weburlparse.get_website_parent(each_link) in all_social_domains: continue #['twitter','facebook','google','pinterest','linkedin']:continue #SOCIAL
                if max_depth_level>1 and len(output_anchor_list) > maximum_links:
                    self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'Maximum links found:' +  str(len(output_anchor_list)))
                    exit_all_loops=True
                    break
                curr_clone=HTMLHandlingNews(each_link,use_selenium=self.use_selenium,developer_mode=self.developer_mode,print_instance=self.print_instance,debug_mode=self.debug_mode,work_offline=self.work_offline,log_process_status=self.log_process_status,deep_developer_mode=self.deep_developer_mode)
                if not curr_clone.basic_info_collected:
                    curr_clone=None
                    continue
                if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'Processing link:' + each_link)
                if curr_clone.key_indexes['sitemap'] and (not site_map_consumed):
                    site_map_consumed=True
                    if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'Hey It is sitemap')
                    if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'sitemap is not empty. Sitemap details:' + str(curr_clone.key_indexes['sitemap']))
                    for each_index in curr_clone.key_indexes['sitemap']:
                        if debug_mode: self._print_(print_prefix + 'sitemap tag details:' + str(curr_clone.tag_details_result[each_index]))
                        self_clone=HTMLHandlingNews(get_absolute_path(curr_clone.base_url,curr_clone.tag_details_result[each_index][5]),use_selenium=self.use_selenium,developer_mode=self.developer_mode,print_instance=self.print_instance,debug_mode=self.debug_mode,work_offline=self.work_offline,log_process_status=self.log_process_status,deep_developer_mode=self.deep_developer_mode)
                        links_for_current_url=self_clone.fetch_all_anchor(restrict_domain=restrict_domain)
                        for each_found_link in links_for_current_url:
                            if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'Link Found:' + str(each_found_link))
                            if each_found_link['href'][-1] == '/':
                                each_found_link['href']=each_found_link['href'][:-1]
                            link_domain=self.ins_weburlparse.get_website_parent(each_found_link['href'])
                            if each_found_link['href'] not in consumed_links:
                                output_anchor_list.append({'link':each_found_link['href'],'value':each_found_link['value'],'parent_url':each_link,'website_domain':domain_of_page,'link_domain':link_domain})
                                consumed_links.append(each_found_link['href'])
                                next_set_of_links.append(each_found_link['href'])
                        self_clone=None
                        if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'Sitemap URL:' + str(curr_clone.tag_details_result[each_index][5]) + '\t Links found:' + str(len(links_for_current_url)))
                    #if len(output_anchor_list)>5:
                    #    return output_anchor_list
                elif curr_clone.menu_data:
                    if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'Hey It is menu')
                    if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'menu is available. Length of items:' + str(len(curr_clone.menu_data)))
                    for each_menu in curr_clone.menu_data:
                        for each_item in each_menu:
                            curr_link_found=get_absolute_path(curr_clone.base_url,each_menu[each_item]['link'])
                            if curr_link_found == '/':
                                curr_link_found=curr_link_found[:-1]
                            link_domain=self.ins_weburlparse.get_website_parent(curr_link_found)
                            if restrict_domain:
                                #print 'print',link_domain,curr_link_found,domain_of_page
                                if link_domain != domain_of_page:
                                    if link_domain in all_social_domains: #['twitter','facebook','google','pinterest','linkedin']:
                                        pass
                                    else:
                                        if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'Domains not matching:' + domain_of_page + ' \tVs\t ' + link_domain)
                                        continue
                            if curr_link_found not in consumed_links:
                                if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'From Menu:' + str(each_menu[each_item]))
                                output_anchor_list.append({'link':curr_link_found,'value':each_menu[each_item]['value'],'parent_url':each_link,'website_domain':domain_of_page,'link_domain':link_domain})
                                consumed_links.append(curr_link_found)
                                next_set_of_links.append(curr_link_found)
                    #if len(output_anchor_list)>5:
                    #    return output_anchor_list
                else:
                    if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'Hey It is anchor')
                    if self.developer_mode:
                        self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + 'No Sitemap and No Menu')
                    get_all_anchor_tags_result=self.HTMLHandling_New_ins.get_all_anchor_tags(curr_clone.tag_details_result,curr_clone.base_url,restrict_domain=restrict_domain,allow_social=allow_social)
                    for each_item in get_all_anchor_tags_result:
                        if each_item['href'] == '/':
                            each_item['href']=each_item['href'][:-1]
                        link_domain=self.ins_weburlparse.get_website_parent(each_item['href'])
                        if each_item['href'] not in consumed_links:
                            output_anchor_list.append({'link':each_item['href'],'value':each_item['value'],'parent_url':each_link,'website_domain':domain_of_page,'link_domain':link_domain})
                            consumed_links.append(each_item['href'])
                            next_set_of_links.append(each_item['href'])
                curr_clone=None
            if exit_all_loops: break
            current_list_of_links[:]=[]
            if next_set_of_links:
                if debug_mode: self._print_(print_prefix + '(' + str(curr_depth_level) + '):' + ' Links found in current level:' + str(len(next_set_of_links)))
                for each_next_link in next_set_of_links:
                    current_list_of_links.append(each_next_link)
            next_set_of_links[:]=[]
            curr_depth_level +=1
        return output_anchor_list
    def ignore_tag_for_process(tag_index,function_type='news'):
        if function_type == 'news':
            if self.key_indexes['news']:
                if self.HTMLHandling_New_ins.has_index_as_parent(self.tag_details_result,tag_index,self.key_indexes['news']):
                    return True
        return False
    def has_related_content_indicators(self,input_statement_in):
        input_statement=input_statement_in.strip('\n').strip().strip('\n\t\r ')
        input_statement_line_split=input_statement.split('\n')
        for each_line in input_statement_line_split:
            each_line_lower=each_line.strip('\n').strip().strip('\n\t\r ').lower()
            if len(each_line_lower) == 0 or (not each_line_lower): continue
            first_word=each_line.split()[0]
            if first_word.lower() in ['read','subscribe','sign','comments','about'] and first_word[0] == first_word[0].upper() and len(each_line.split()) < 20:
                return UpperCamelCase(first_word)
            if 'forward' in each_line_lower and 'looking' in each_line_lower and 'statement' in each_line_lower:
                return 'Forward'
            if each_line_lower.startswith('recommended for'):
                return 'Recommend'
        return None
    #news_key_words=['news','press','article','more']#Subscribe to , Sign up,Commetns,About Edgewater #Forward-Looking and Cautionary Statements
    def fetch_pr_archival_details(self,include_script_link=False,already_processed_pages=None,developer_mode=False):
        #This is the only function which refers url which is not used to initialize the class.
        #Hence creating an object for this class and fetch the link. i.e, inside the for loop, create object and access extract_news_like_link_from_html_content
        if 'fetch_pr_archival_details' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        all_pr_links=[]
        if self.developer_mode: print 'fetch_pr_archival_details: ',self.webpage_url
        pr_list=self.extract_news_like_link_from_html_content(include_script_link=include_script_link)
        if pr_list:
            if debug_mode: print 'fetch_pr_archival_details(self): ',len(pr_list),' links found in ',self.webpage_url
            for each_link in pr_list:
                all_pr_links.append({'archive_url':self.webpage_url,'source_url':self.webpage_url,'archival_value':'','text':each_link['text'],'href':each_link['href'],'link_type':each_link['type'],'record_type':each_link['record_type'],'date':each_link['date']})
        else:
            if debug_mode: print 'fetch_pr_archival_details(self): ZERO(0) link found in ',self.webpage_url
            
        archival_page_links=self.fetch_pr_archival_page_links(include_script_link=include_script_link)
        #print archival_page_links
        if not archival_page_links:
            if self.developer_mode: print 'fetch_pr_archival_details: ',self.webpage_url,': No archival links found'
            return all_pr_links
        if self.developer_mode: print 'fetch_pr_archival_details: ',self.webpage_url,': the page has press release data. analysing links for archives..'
        for each_record in archival_page_links:
            display_value=each_record['value']
            archival_href=each_record['href']
            #print archival_href
            if already_processed_pages and archival_href in already_processed_pages: continue
            #print archival_href,'continue...'
            obj_archival_page=HTMLHandlingNews(webpage_url=archival_href,use_selenium=self.use_selenium,developer_mode=self.developer_mode,print_instance=self.print_instance,debug_mode=self.debug_mode,work_offline=self.work_offline,log_process_status=self.log_process_status,deep_developer_mode=self.deep_developer_mode)
            pr_list=obj_archival_page.extract_news_like_link_from_html_content(include_script_link=include_script_link)
            #print 'list:',pr_list
            if pr_list:
                if debug_mode: print 'fetch_pr_archival_details: ',len(pr_list),' links found in ',self.webpage_url,'-->',archival_href
                for each_link in pr_list:
                    all_pr_links.append({'archive_url':archival_href,'source_url':self.webpage_url,'archival_value':display_value,'text':each_link['text'],'href':each_link['href'],'link_type':each_link['type'],'record_type':each_link['record_type'],'date':each_link['date']})
            else:
                if debug_mode: print 'fetch_pr_archival_details: ZERO(0) link found in ',self.webpage_url,'-->',archival_href
            obj_archival_page=None
        return all_pr_links
    def fetch_pr_archival_page_links(self,include_script_link=False,developer_mode=False):
        #PENDING: Archives in http://investor.lundbeck.com/releases.cfm
        print_prefix='fetch_pr_archival_page_links\t'
        if 'fetch_pr_archival_page_links' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if self.developer_mode:  self._print_( 'fetch_pr_archival_page_links: ' + str(self.webpage_url) + ': the page has press release data. analysing links for archives..')
        if not self.basic_info_collected:
            return []
        tag_details_result=self.tag_details_result
        if 'a' not in tag_details_result:
            developer_mode=True
            if self.developer_mode:  self._print_( 'fetch_pr_archival_page_links: ' + str(self.webpage_url) + ': No <a> tags')
            developer_mode=False
            return []
        base_url=self.base_url
        if debug_mode:
            self._print_(print_prefix + 'List of all tags')
            for each_of in tag_details_result:
                 self._print_( str(each_of) + '\t' + str(tag_details_result[each_of]))
        collect_highlevel_a_press_release=[]
        collect_highlevel_a_press_release_links=[]
        a_tag_with_data_index=0
        current_year=int(get_current_date('%Y'))
        for each_a in tag_details_result['a']:
            a_tag_display=get_printable_string(self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,each_a),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
            a_tag_display=a_tag_display.strip(' \n\r\t')
            if len(a_tag_display)>0: a_tag_with_data_index += 1
            a_tag_href=tag_details_result[each_a][5].strip(' \n\r\t')
            if not a_tag_href or (len(a_tag_href) == 0): continue
            year_data=has_a_years(a_tag_display)
            number_data=is_number(a_tag_display,check_for_integer=True)
            if not year_data: year_data=0
            if year_data > current_year: year_data=0
            if not number_data: number_data=0
            if debug_mode:  self._print_( 'fetch_pr_archival_page_links:inside a tag:' + str(a_tag_with_data_index) + '\tyear_data=' + str(year_data) + '\tnumber_data=' + str(number_data) +  '\t' + str(each_a) + '\t' + str(tag_details_result[each_a]) + '\t' +  str(a_tag_display))
            if len(a_tag_display.split())<4 and (year_data or number_data):
                if debug_mode:  self._print_( 'fetch_pr_archival_page_links:Link smell like archival hint:' + str(tag_details_result[each_a]))
                link_type=get_html_link_type(a_tag_href,return_special_for_special=True)
                if link_type == 'Special':
                    absolute_path=a_tag_href
                else:
                    absolute_path=self.HTMLHandling_New_ins.get_absolute_path(base_url,a_tag_href)
                if (not include_script_link) and link_type != 'link':
                    if debug_mode:  self._print_(print_prefix + 'include_script_link-' + str(include_script_link) + '\tlink_type:' + str(link_type))
                    continue
                collect_highlevel_a_press_release.append({'year':year_data,'number':number_data,'a_tag_idx':a_tag_with_data_index,'value':a_tag_display,'parents':tag_details_result[each_a][4],'href':absolute_path,'class':tag_details_result[each_a][6],'tag_idx':tag_details_result[each_a][7]})
                if absolute_path  not in collect_highlevel_a_press_release_links:
                #t_tag,t_value,t_p_index,t_childs,t_parents,t_href,t_class,t_index
                    collect_highlevel_a_press_release_links.append(absolute_path)
        if not collect_highlevel_a_press_release_links or (len(collect_highlevel_a_press_release_links) < 2):
            if self.developer_mode:  self._print_('fetch_pr_archival_page_links:no archival like hint:' + str(self.webpage_url))
            return False
        count_of_selected=0
        previous_a_tag_index=0
        previous_selection_type='nothing'
        previous_selection_data=0
        min_year_selection=2
        min_number_selection=3
        if debug_mode and collect_highlevel_a_press_release:
            for each_data in collect_highlevel_a_press_release:
                 self._print_( 'fetch_pr_archival_page_links:selected a tag:'  + str(each_data))
        result_list=[]
        temp_list=[]
        for each_pr_page_data in collect_highlevel_a_press_release:
            if each_pr_page_data['year'] > 0:
                if not temp_list or count_of_selected == 0:
                    if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:year-new:previous_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                    temp_list[:]=[]
                    count_of_selected = 1
                    previous_a_tag_index=each_pr_page_data['a_tag_idx']
                    previous_selection_type='year'
                    previous_selection_data=each_pr_page_data['year']
                    temp_list.append(each_pr_page_data)
                    continue
                elif previous_selection_type != 'year' or (previous_a_tag_index>0 and previous_a_tag_index+1 != each_pr_page_data['a_tag_idx']) or (previous_selection_data>0 and abs(each_pr_page_data['year'] - previous_selection_data) != 1):
                #The year may increase or decrease
                    if (previous_selection_type == 'year' and count_of_selected >= min_year_selection) or (previous_selection_type == 'number' and count_of_selected >= min_number_selection):
                        if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:extend result_list:year-break:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                        result_list.extend(temp_list)
                    else:
                        if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:year break result_list:year-break:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                    temp_list[:]=[]
                    count_of_selected = 1
                    previous_a_tag_index=each_pr_page_data['a_tag_idx']
                    previous_selection_type='year'
                    previous_selection_data=each_pr_page_data['year']
                    temp_list.append(each_pr_page_data)
                    continue
                elif previous_selection_type == 'year' and (previous_a_tag_index>0 and previous_a_tag_index+1 == each_pr_page_data['a_tag_idx']) and (previous_selection_data>0 and abs(each_pr_page_data['year'] - previous_selection_data) == 1):
                #The year may increase or decrease
                    if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:year-additional:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                    count_of_selected += 1
                    previous_a_tag_index=each_pr_page_data['a_tag_idx']
                    previous_selection_type='year'
                    previous_selection_data=each_pr_page_data['year']
                    temp_list.append(each_pr_page_data)
                    continue
                else:
                    if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:year-logical flow error:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                    exit()
            elif each_pr_page_data['number'] > 0:
                if not temp_list or count_of_selected == 0:
                    if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:number-new:previous_selection_type='  + str(previous_selection_type) + 'data:' + str(each_data))
                    temp_list[:]=[]
                    count_of_selected = 1
                    previous_a_tag_index=each_pr_page_data['a_tag_idx']
                    previous_selection_type='number'
                    previous_selection_data=each_pr_page_data['number']
                    temp_list.append(each_pr_page_data)
                    continue
                elif previous_selection_type != 'number' or (previous_a_tag_index>0 and previous_a_tag_index+1 != each_pr_page_data['a_tag_idx']) or (previous_selection_data>0 and abs(each_pr_page_data['number'] - previous_selection_data) != 1):
                #The number may increase or decrease
                    if (previous_selection_type == 'year' and count_of_selected >= min_year_selection) or (previous_selection_type == 'number' and count_of_selected >= min_number_selection):
                        if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:extend result_list:number-break:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                        result_list.extend(temp_list)
                    else:
                        if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:number break result_list:number-break:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                    temp_list[:]=[]
                    count_of_selected = 1
                    previous_a_tag_index=each_pr_page_data['a_tag_idx']
                    previous_selection_type='number'
                    previous_selection_data=each_pr_page_data['number']
                    temp_list.append(each_pr_page_data)
                    continue
                elif previous_selection_type == 'number' and (previous_a_tag_index>0 and previous_a_tag_index+1 == each_pr_page_data['a_tag_idx']) and (previous_selection_data>0 and abs(each_pr_page_data['number'] - previous_selection_data) == 1):
                #The number may increase or decrease
                    if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:number-additional:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                    count_of_selected += 1
                    previous_a_tag_index=each_pr_page_data['a_tag_idx']
                    previous_selection_type='number'
                    previous_selection_data=each_pr_page_data['number']
                    temp_list.append(each_pr_page_data)
                    continue
                else:
                    if debug_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:year-logincal flow error:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                    exit()
            else:
                self._print_( 'fetch_pr_archival_page_links:selection process:no-y-no-n-logincal flow error:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
                exit()
        if (previous_selection_type == 'year' and count_of_selected >= min_year_selection) or (previous_selection_type == 'number' and count_of_selected >= min_number_selection):
            if self.developer_mode:  self._print_( 'fetch_pr_archival_page_links:selection process:extend result_list:end:previous_a_tag_index=' + str(previous_a_tag_index) + '\tcount_of_selected='  + str(count_of_selected) + '\tprevious_selection_type='  + str(previous_selection_type) + 'data:' + str(each_pr_page_data))
            result_list.extend(temp_list)
            temp_list[:]=[]
        return result_list
    def extract_news_like_link_from_html_content(self,include_script_link=False):
        #PENDING: Ignore http://investor.fei.com/News#  in http://investor.fei.com/News
        #Exclude topics,category links http://today.duke.edu/topic/research
        #No News--http://www.montefiore.org/body.cfm?id=1738
        #didn't fetch correct list https://share.sandia.gov/news/resources/news_releases/
        #mixed and incorrect list http://umm.edu/news-and-events/news-releases
        #CHECK PENDING: http://www.etransmedia.com/author/connie_smith/
        self.current_function_name='extract_news_like_link_from_html_content'
        collect_links_details=[]
        collected_links=[]
        consumed_links=[]
        consumed_links[:]=[]
        #collect_links_suspected=[]
        print_prefix='extract_news_like_link_from_html_content:\t'
        if 'extract_news_like_link_from_html_content' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if self.basic_info_collected:
            tag_details_result=self.tag_details_result
        else:
            if self.developer_mode or debug_mode: self._print_(print_prefix + ' basic_info_collected not set True')
            return collect_links_details
        base_url=self.base_url
        #print 'base_url',base_url
        if self.developer_mode:# or True:
            print print_prefix + '\nList of all tags'
            for each_of in tag_details_result:
                print each_of,'\t',tag_details_result[each_of]
        collect_highlevel_a_press_release=[]
        collect_highlevel_a_press_release_links=[]
        if self.TRACK_TIME_MODE or self.developer_mode: 
            self._print_(print_prefix + 'collecting news like tags')
        for each_a in tag_details_result['a']:
            if self.ignore_tag_for_process(each_a):
                if debug_mode: self._print_(print_prefix + ' Tag [' + str(each_a) + '] has a parent to be ignored')
                continue
            a_tag_display=get_printable_string(self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,each_a),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
            if debug_mode: print print_prefix + str(each_a) + '\t' + str(tag_details_result[each_a]) + '\t' + str(a_tag_display)
            if len(a_tag_display.split())>5 or ('read more' in a_tag_display.lower() and len(a_tag_display)<15):#Temp fix for read more
                if debug_mode: print print_prefix + 'Link smell like news:',tag_details_result[each_a]
                article_date=self.HTMLHandling_New_ins.find_date_for_news(tag_details_result,each_a,0,self.developer_mode)
                if (not article_date):
                    if debug_mode: print print_prefix + 'date found for ',tag_details_result[each_a]
                    continue
                else:
                    if debug_mode: print print_prefix + 'date found : ',article_date,tag_details_result[each_a]
                collect_highlevel_a_press_release.append(tag_details_result[each_a][4])
                if tag_details_result[each_a][5]  not in collect_highlevel_a_press_release_links:
                    collect_highlevel_a_press_release_links.append(tag_details_result[each_a][5])
        if self.developer_mode:
            print print_prefix + '\n\n\nCollected LINKS length=',len(collect_highlevel_a_press_release)
            for each_list in collect_highlevel_a_press_release:
                print each_list
        if self.TRACK_TIME_MODE or self.developer_mode: self._print_(print_prefix + 'identify common parent')
        comm_parent=self.HTMLHandling_New_ins.get_common_parent_in_html(collect_highlevel_a_press_release,developer_mode=self.developer_mode)
        multi_link_selection_list={}
        length_of_initial_selection=len(collect_highlevel_a_press_release_links)
        if (not length_of_initial_selection) or length_of_initial_selection == 0 or (not collect_highlevel_a_press_release_links): return collect_links_details
        if self.developer_mode: print print_prefix + 'Common Parent:',comm_parent,'\tLength:',length_of_initial_selection
        if self.TRACK_TIME_MODE or self.developer_mode: self._print_(print_prefix + 'fetch news using the common parent')
        lnk_to_news_count=0
        for each_a in sorted(tag_details_result['a']):
            if self.ignore_tag_for_process(each_a):
                if debug_mode: self._print_(print_prefix + ' Tag [' + str(each_a) + '] has a parent to be ignored. Tag details:' + str(tag_details_result[each_a]))
                continue
            parent_list=tag_details_result[each_a][4]
            if parent_list:
                if comm_parent in parent_list:
                    a_tag_display=get_printable_string(self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,each_a),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
                    if len(a_tag_display.strip(' \n\r\t'))<5: continue
                    a_tag_href=tag_details_result[each_a][5]
                    link_type=get_html_link_type(a_tag_href,return_special_for_special=True)
                    if (not include_script_link) and link_type != 'link': 
                        if debug_mode: print print_prefix + str(tag_details_result[each_a]), ':@ a and href. include_script_link-',include_script_link,'\tlink_type:',link_type
                        continue
                    article_date=self.HTMLHandling_New_ins.find_date_for_news(tag_details_result,each_a,comm_parent,self.developer_mode)
                    #If there is no date surrounding the title of feed, then check date in the title
                    if not article_date:
                        try:
                            is_there_a_date=get_smell_like_date_from_text(a_tag_display,strict_year=False,consume_month_year=False)
                            if is_there_a_date:
                                if is_there_a_date[0]>0:
                                    if is_there_a_date[1] <= get_current_date(format='date'):
                                        article_date = is_there_a_date[1]
                                        a_tag_display = re.sub('(^\d\S*)', '',re.split('\d\d\d\d\S?\s?', a_tag_display)[1]).strip()
                        except:
                            pass
                    #If there is no date in the feed, then check date in the news url
                    if not article_date:
                        is_there_a_date=get_smell_like_date_from_url(a_tag_display)#strict_year and consume_month_year is used in get_smell_like_date_from_text ,strict_year=False,consume_month_year=False)
                        if is_there_a_date:
                            article_date = is_there_a_date
                    if link_type == 'Special':
                        absolute_path=a_tag_href
                    else:
                        absolute_path=self.HTMLHandling_New_ins.get_absolute_path(base_url,a_tag_href)                    
                    if absolute_path not in consumed_links:
                        lnk_to_news=is_link_to_news(a_tag_display)
                        if lnk_to_news and len(a_tag_display)<15:
                            lnk_to_news_count += 1
                        collect_links_details.append({'href':absolute_path,'text':a_tag_display,'type':link_type})
                        consumed_links.append(absolute_path)
                    if absolute_path not in multi_link_selection_list:
                        multi_link_selection_list[absolute_path]=[]
                    date_analysis=get_smell_like_date_from_text(a_tag_display,consume_month_year=False)
                    date_found=None
                    date_text=''
                    date_percentage=0
                    stopwords_count=count_list_word_in_statement(a_tag_display,stopwords_generic)
                    if date_analysis:
                        if date_analysis[0]>0:
                            date_found=date_analysis[1]
                            date_text=date_analysis[2]
                            date_percentage=len(date_text.strip())*1.0/len(a_tag_display)
                    multi_link_selection_list[absolute_path].append((absolute_path,a_tag_display,link_type,each_a,comm_parent,parent_list,date_found,date_text,date_percentage,stopwords_count,is_link_to_news(a_tag_display),len(paragraph_to_sentence(a_tag_display)),article_date))
        if self.developer_mode: print_prefix + '\n\nSELECTED with COMMON Parents:',print_list( multi_link_selection_list)
        collect_news_links=[]
        length_of_common_parent_selectioin=len(multi_link_selection_list)
        record_type='news'
        selection_ratio=length_of_common_parent_selectioin*1.0/length_of_initial_selection
        if selection_ratio>=0.5 and selection_ratio<=1.5:
            record_type='news'
        else:
            record_type='news_like:' + str(length_of_initial_selection) + ' to ' + str(length_of_common_parent_selectioin)
        #print '\n\n\n'
        if self.TRACK_TIME_MODE or self.developer_mode: self._print_(print_prefix + 'process the selected links(multiple occurrence of same link)')
        for each_url in multi_link_selection_list:
            current_news_data=multi_link_selection_list[each_url]
            select_record=None
            if len(current_news_data) > 1:
                if debug_mode: 
                    print print_prefix + ' multiple records:',each_url
                news_title=''
                for each_url_data in current_news_data:
                    if debug_mode: printprint_prefix + 'multiple records:Inside\t\t',each_url_data
                    if each_url_data[10]: 
                        if debug_mode: print print_prefix + 'multiple records:#link to news\t\t',each_url_data
                        continue #link to news
                    if each_url_data[8] > 0.25 and each_url_data[9] ==0 : 
                        if debug_mode: print print_prefix + ' multiple records:#most of the part is date\t\t',each_url_data
                        continue #most of the part is date
                    if each_url_data[9] < 5 and each_url_data[10] <= 1: 
                        if debug_mode: print print_prefix + 'multiple records:#selected\t\t',each_url_data
                        select_record=each_url_data
                        break
            if not select_record:#tag_details_result
                select_record=current_news_data[0]
            article_date=select_record[12]
            pr_title=select_record[1].replace('\n',' ')
            if lnk_to_news_count == length_of_common_parent_selectioin: # no link to actual news. Read more takes to actual message
                if debug_mode: print print_prefix + ' read more links alone:',select_record[0]
                title_like_text = ''
                #The below line is commented in the latest version but need to check why
                #title_like_text=find_pr_title_for_lnk_to_news(tag_details_result,select_record[3],comm_parent,self.developer_mode)
                
                if title_like_text:
                    if debug_mode: print print_prefix + ' read more links alone:',select_record[0],':found "',title_like_text,'" for index=',select_record[3],':common parent=',comm_parent
                    pr_title=title_like_text
                else:
                    if debug_mode: print print_prefix + ' read more links alone:',select_record[0],':not found : for index=',select_record[3],':common parent=',comm_parent
                    if record_type == 'news': record_type='Indirect'
            else:
                pass#
            keyword_check = False
            if len(pr_title) > 20:
                pr_title = pr_title.strip()
                for keywords in press_release_stop_words:
                    if keywords.lower() in pr_title.lower():
                        keyword_check = True
                if not keyword_check:
                    collect_news_links.append({'href':select_record[0],'text':pr_title,'type':select_record[2],'record_type':record_type,'index':select_record[3],'date':article_date})
        if self.TRACK_TIME_MODE or self.developer_mode: self._print_(print_prefix + 'completed')
        #HTMLHandling_New_ins=None
        return collect_news_links
    def get_news_from_index(self,tag_details_result,article_start_at,article_title=None,process_each_child=False,length_of_article=0,depth_level=0,called_for_prefix=None):
        print_prefix='get_news_from_index (' + str(article_start_at) + ':' + str(depth_level) + ') :'
        if not called_for_prefix:
            if depth_level == 0 and process_each_child:
                called_for_prefix = ' Building content for ' + str(article_start_at)
                print_prefix = print_prefix + ' ' + str(called_for_prefix) + ':\t'
            elif depth_level > 0:
                self._print_(print_prefix + ' Logical error depth_level > 0 but no called_for_prefix')
                exit()
        else:
            print_prefix = print_prefix + ' ' + str(called_for_prefix) + ':\t'
        if 'get_news_from_index' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        process_child_tags=['section','div']
        focused_content_data=''
        article_content=''
        process_each_child_indicator=False
        if depth_level == 0 and process_each_child:
            length_of_article_derived=len(self.get_news_from_index(tag_details_result,article_start_at,process_each_child=False,depth_level=0,called_for_prefix= ' entire content for ' + str(article_start_at)))
        else:
            length_of_article_derived = length_of_article
        if process_each_child and length_of_article_derived >0 :
            process_each_child_indicator = True
        if debug_mode: self._print_(print_prefix + 'process_each_child_indicator:' + str(process_each_child_indicator) +' \t length_of_article_derived:' + str(length_of_article_derived))
        if depth_level > 10: return focused_content_data
        if article_start_at < 0 : return focused_content_data
        comm_parent=article_start_at
        #article_content_reduced=get_printable_string(self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,comm_parent),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
        article_content_reduced=self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,comm_parent)
        replace_tag_by={
            'br':'\n'
            ,'p':'\n'
            ,'span':' '
            ,'h1':'\n'
            ,'h2':'\n'
            ,'h3':'\n'
            ,'h4':'\n'
            ,'h5':'\n'
            ,'h6':'\n'
            ,'section':'\n'
            ,'td':' '
            ,'tr':'\n'
            ,'div':'\n'
            ,'li':'\n' #Version 1.9
        }
        if tag_details_result[comm_parent][3]:
            for each_child in tag_details_result[comm_parent][3]:
                #reduced_content_is=get_printable_string(self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,each_child),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
                reduced_content_is=self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,each_child)
                reduced_content_is=reduced_content_is.strip('\n').strip().strip('\n')
                reduced_content_length_is=len(reduced_content_is)
                tag_type=self.HTMLHandling_New_ins.get_tag_group_type(tag_details_result,each_child)
                if tag_type in ['AL','LL','LTL','IM','EM','SL','DC']:
                    ignore_content=True
                else:
                    ignore_content=False
                if article_title and tag_type in ['LTS'] and len(article_title)>10 and len(reduced_content_is) > 2 * len(article_title):
                    if debug_mode: self._print_(print_prefix + '\t LTS tag special processing')
                    article_title_word_count=len(article_title.split())
                    title_population=count_list_word_in_statement(reduced_content_is,article_title.split(),case_sensitive=False,distinct_word=False)
                    if title_population < article_title_word_count * 0.25:#This may become bottle nect at one time
                        if debug_mode: self._print_(print_prefix + 'tag type:  ' + tag_type + '.\t The content has title population ' + str(title_population) + '.\t reduced_content_is:' + str(len(reduced_content_is)) + '.\t article_title(' + str(article_title_word_count) + '):' + str(article_title))
                        ignore_content=True
                if debug_mode and ignore_content:
                    self._print_(print_prefix + 'Index:' + str(each_child) + '\t TAG_TYPE:' + str(tag_type) + ' \t Ignore content:' + str(ignore_content) + '\t TAG_CONTENT:' + str(reduced_content_is))
                if ignore_content: continue
                if process_each_child_indicator and tag_details_result[each_child][0] in process_child_tags and length_of_article/10.0 < reduced_content_length_is:
                    if debug_mode:
                        self._print_(print_prefix + 'Child Process-' + tag_details_result[each_child][0] + ': Index:' + str(each_child) + '\t TAG_TYPE:' + str(tag_type) + ' \t Ignore content:' + str(ignore_content) + '\t TAG_CONTENT:' + str(reduced_content_is))
                    if debug_mode: self._print_(print_prefix + ' Loop\tTag :' + tag_details_result[each_child][0] + ' at ' + str(each_child) + ' with length ' + str(reduced_content_length_is) + ' and tag_type:' + tag_type)
                    temp_reduced_content_is=self.get_news_from_index(tag_details_result,article_start_at=each_child,article_title=article_title,process_each_child=process_each_child,length_of_article=length_of_article_derived,depth_level=depth_level+1,called_for_prefix=called_for_prefix)
                    article_content = article_content + replace_tag_by[tag_details_result[each_child][0]] + temp_reduced_content_is
                else:
                    off_news_available=self.has_related_content_indicators(reduced_content_is)#'read','subscribe','sign','comments','about'
                    if debug_mode: self._print_(print_prefix + 'No Child Process-' + tag_details_result[each_child][0] + ': Index:' + str(each_child) + '\t TAG_TYPE:' + str(tag_type) + ' \t Off News Indicator:' + str(off_news_available) + ' \t Ignore content:' + str(ignore_content) + '\t TAG_CONTENT:' + str(reduced_content_is))
                    if off_news_available:
                        if off_news_available.lower() in ['read','sign','subscribe','recommend']:
                            ignore_content=True
                        elif off_news_available.lower() in ['comments']:
                            ignore_content=True
                            break
                        elif off_news_available.lower() in ['forward']:
                            ignore_content=True
                            break
                        elif off_news_available.lower() in ['about']:
                            ignore_content=True
                            break
                        if debug_mode:
                            self._print_(print_prefix + 'Index:' + str(each_child) + '\t TAG_TYPE:' + str(tag_type) + ' \t Off News Indicator:' + str(off_news_available) + ' \t Off news Ignore content:' + str(ignore_content) + '\t TAG_CONTENT:' + str(reduced_content_is))
                        if ignore_content: continue
                    if reduced_content_is.strip() > 0:
                        if len(tag_details_result[each_child][0]) > 0:
                            if tag_details_result[each_child][0] in replace_tag_by:
                                article_content = article_content + replace_tag_by[tag_details_result[each_child][0]] + reduced_content_is.strip()
                            else:
                                article_content = article_content + ' ' + reduced_content_is.strip()
        else:
            if len(article_content_reduced) > 10 and depth_level == 0:#It is possible scenario. The entire article can be in <article /> tag
                if len(article_content_reduced) > 100:
                    article_content=article_content_reduced
                else:
                    self._print_(print_prefix + ' Logical Error: Article content is there but no child')
                    exit()
        if len(article_content)>0 :
            if self.developer_mode: self._print_(print_prefix + 'Article Content found with length:' + str(len(article_content)))
            for each_line in article_content.split('\n'):
                if len(each_line.strip().strip('\t'))>0:
                    focused_content_data = focused_content_data + each_line.strip().strip('\t') + '\n'
            focused_content_data=focused_content_data.strip('\n')
            focused_content_data=re.sub(' +',' ',focused_content_data)
        return focused_content_data
    def trim_news_for_dissipated_cloud(self,article_content,article_title):
        print_prefix='trim_news_for_dissipated_cloud :\t'
        if 'trim_news_for_dissipated_cloud' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if not article_content: return article_content
        article_content_list=article_content.split('\n')
        output_article_content=''
        if len(article_content_list)  <= 5 : 
            title_population=count_list_word_in_statement(article_content,article_title,case_sensitive=False,distinct_word=True)
            if title_population > len(article_title.split()) * 0.25:
                return article_content
            else:
                return output_article_content
        temp_holder_content=''
        no_of_cloud_found=0
        MINIMUM_CLOUD_TO_FILTER=3
        for each_line in article_content_list:
            each_line_formatted=each_line.strip()
            if not each_line_formatted:continue
            each_line_word_count=len(each_line_formatted.split())
            if debug_mode: self._print_(print_prefix + 'no_of_cloud_found=' + str(no_of_cloud_found) +'\t temp_holder_content=' + str(len(temp_holder_content))+ '\toutput_article_content=' + str(len(output_article_content))+'\tProcessing Line : no of words=' + str(each_line_word_count) + '\t Content: ' + str(each_line_formatted))
            if each_line_word_count <= 5:
                no_of_cloud_found += 1
                temp_holder_content = temp_holder_content + '\n' + each_line_formatted
                if debug_mode: self._print_(print_prefix + 'identified cloud\tno_of_cloud_found=' + str(no_of_cloud_found) +'\t temp_holder_content=' + str(len(temp_holder_content))+ '\toutput_article_content=' + str(len(output_article_content)))
            else:
                if each_line_word_count <= 10:
                    if no_of_cloud_found > 2:
                        no_of_cloud_found += 1
                        temp_holder_content = temp_holder_content + '\n' + each_line_formatted
                        if debug_mode: self._print_(print_prefix + 'Comparatively lenghtier line\tno_of_cloud_found=' + str(no_of_cloud_found) +'\t temp_holder_content=' + str(len(temp_holder_content))+ '\toutput_article_content=' + str(len(output_article_content)))
                        continue
                    if no_of_cloud_found > 0 :
                        no_of_cloud_found=0
                        temp_holder_content=''
                        output_article_content = output_article_content + '\n' + temp_holder_content
                    output_article_content = output_article_content + '\n' + each_line_formatted
                else:
                    if no_of_cloud_found >= MINIMUM_CLOUD_TO_FILTER:
                        pass #Do nothing
                    else:
                        output_article_content = output_article_content + '\n' + temp_holder_content
                    no_of_cloud_found = 0
                    temp_holder_content=''
                    output_article_content = output_article_content + '\n' + each_line_formatted
        return output_article_content.replace('\n\n','\n').strip('\n')
    def get_content_from_page(self,news_title=None,process_anchors=False,no_exclusion=False):
        #https://www.booktopia.com.au ABN number and Mobile store is got clubbed PENDING
        #Pending : If length is wrong -- should be related to title
        self.current_function_name='get_content_from_page'
        content_data=''
        print_prefix='get_content_from_page:\t'
        tags_to_look=['body']
        if 'get_content_from_page' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if not self.basic_info_collected:
            if debug_mode: self._print_(print_prefix + ' basic_info_collected is not set to True.')
            return content_data
        tag_details_result=self.tag_details_result
        if not tag_details_result:
            if self.developer_mode or debug_mode: self._print_(print_prefix + 'No data from tag details analysis')
        if debug_mode: 
            self._print_(print_prefix + ' List of indexes in tag_details_result')
            for each_key in tag_details_result:
                self._print_(print_prefix + str(each_key) + '\t' + repr(tag_details_result[each_key]))
        #if 2 not in tag_details_result:
        if tags_to_look[0] in tag_details_result:
            if not tag_details_result[tags_to_look[0]]:
                if self.developer_mode or debug_mode: self._print_(print_prefix + log_time_stamp() + ' No body tag found')
                return content_data
            else:
                if debug_mode: self._print_(print_prefix + str(tags_to_look[0]) + ' details at index: ' + str(tag_details_result[tags_to_look[0]][0]))
            #full_text_content=get_printable_string(self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,tag_details_result[tags_to_look[0]][0],process_anchors=False),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
            if no_exclusion:
                full_text_content=self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,tag_details_result[tags_to_look[0]][0],process_anchors=process_anchors,already_processed_index=None)
            else:
                full_text_content=self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,tag_details_result[tags_to_look[0]][0],process_anchors=process_anchors,already_processed_index=copy.deepcopy(self.key_indexes['menu']))
            if full_text_content:
                full_text_content_list=full_text_content.split('\n')
                for each_line in full_text_content_list:
                    if each_line and len(each_line.strip(' \t'))>0:
                        content_data=content_data + '\n' + each_line.strip(' \t')
            if debug_mode: self._print_(print_prefix + ' Full text content found with length :' + str(len(full_text_content)) + '\t First 100 Chars:' + full_text_content[:100])
            #(self,data_tag_analysis,index,already_processed_index=None,type=None,reduce_tag_depth=0,process_anchors=True,ignore_image=True):
        return content_data.strip('\n')
    def get_focused_content(self,news_title=None,ignore_long_hyperlinks=True):
        #Pending : If length is wrong -- should be related to title
        self.current_function_name='get_focused_content'
        collect_links_details=[]
        focused_content_data=''
        collected_links=[]
        consumed_links=[]
        consumed_links[:]=[]
        tags_to_look=['article','div','p']
        ignore_branches_for_tags=['a']
        MINIMUM_WORDS_TO_SELECT=20
        processed_indexes=[]
        ignored_indexes=[]
        print_prefix='get_focused_content:\t'
        if 'get_focused_content' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if not self.basic_info_collected:
            if debug_mode: self._print_(print_prefix + 'basic_info_collected is not set to True')
            return focused_content_data
        tag_details_result=self.tag_details_result
        #INDEX=(TAGNAME, TAGTEXT,PARENT_INDEX,ALL_CHILDS,ALL_PARENTS,HREF,CLASS,INDEX,TAG_INFO)
        #print 'base_url',base_url
        temp_flag=False
        for each_tag in tags_to_look:
            if each_tag in tag_details_result:
                temp_flag=True
                break
        if not temp_flag:
            if self.developer_mode: self._print_('Tags to be searched not available in the HTML analysis result: Tags to be search are : ' + ','.join(tags_to_look))
            return focused_content_data
        if debug_mode:# or True:
            self._print_( print_prefix + '\nList of all tags')
            for each_of in tag_details_result:
                self._print_(print_prefix + str(each_of) + '\t' + str(tag_details_result[each_of]))

        news_news_title=news_title
        if not news_news_title:
            news_news_title=self.fetch_title(url_path=self.webpage_url,html_content_in=self.html_content)
        if not news_news_title:
            if debug_mode: self._print_(print_prefix + '\t Title not fetched:' + str(self.webpage_url))
            return focused_content_data
        news_news_title=remove_list_word_in_statement(news_news_title,stopwords_generic,case_sensitive=False)
        if not news_news_title:
            return focused_content_data
        news_news_title=news_news_title.replace(' | ',' - ')
        news_news_title=re.sub(r' +',' ',news_news_title)
        news_news_title=data_detail_extraction(news_news_title,content_type='Title')
        news_news_title_list=news_news_title.lower().split()
        news_news_title_list_length=len(news_news_title_list)
            
        collect_highlevel_data=[]
        collect_highlevel_data_details=[]
        if self.TRACK_TIME_MODE or self.developer_mode: 
            self._print_(print_prefix + 'collecting news like tags')
        for each_ignore_tag in ignore_branches_for_tags:
            if each_ignore_tag in tag_details_result:
                for each_index in tag_details_result[each_ignore_tag]:
                    for each_child in tag_details_result[each_index][3]:
                        if each_child not in ignored_indexes:
                            if debug_mode: self._print_(print_prefix + 'Index ' + str(each_child) + ' is an ignore tag "' + each_ignore_tag + '" and it will not be processed')
                            ignored_indexes.append(each_child)
        if 'article' in tag_details_result:
            for each_index in tag_details_result['article']:
                article_content=''
                for each_child_index in tag_details_result['article']:
                    curr_article_content=self.get_news_from_index(tag_details_result,each_index,article_title=news_news_title,process_each_child=True)
                    title_population=count_list_word_in_statement(curr_article_content,news_news_title_list,case_sensitive=False,distinct_word=False)
                    if title_population >= news_news_title_list_length and len(curr_article_content) > 4 * len(news_news_title):
                        if debug_mode: self._print_(print_prefix + 'article tag: Trace content with len:'  + str(len(curr_article_content)) + '\t' + 'title_population:' + str(title_population))
                        return curr_article_content
        if 'p' in tag_details_result:
            for each_index in tag_details_result['p']:
                if each_index not in ignored_indexes and each_index not in processed_indexes:
                    #tag_content=get_printable_string(self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,each_index),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
                    tag_content=self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,each_index)
                    tag_content=re.sub(' +',' ',tag_content)
                    if len(tag_content.split()) > MINIMUM_WORDS_TO_SELECT:
                        if debug_mode: self._print_(print_prefix + ' Index identified:' + str(each_index) + '\t Current Tag Name:' + str(tag_details_result[each_index][0]) + '\t Index details: Parents:' + str(tag_details_result[each_index][4]) + '\t  Childs:' + str(tag_details_result[each_index][3]) + '\t  Content (' + str(len(tag_content))+ '):' + str(tag_details_result[each_index][1]))
                        collect_highlevel_data.append(tag_details_result[each_index][4])
                        collect_highlevel_data_details.append([each_index,tag_details_result[each_index][0],tag_content,tag_details_result[each_index]])
        if debug_mode: self._print_(print_prefix + ' No of p tag collected:' + str(len(collect_highlevel_data)))
        if len(collect_highlevel_data) <= 3 and 'div' in tag_details_result:
            for each_index in tag_details_result['div']:
                if each_index not in ignored_indexes and each_index not in processed_indexes:
                    current_tag_details=self.HTMLHandling_New_ins.get_all_childs_and_tags(tag_details_result,each_index)
                    if 'div' not in current_tag_details:
                        #tag_content=get_printable_string(self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,each_index),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
                        tag_content=self.HTMLHandling_New_ins.support_tag_analysis_reduce_tag(tag_details_result,each_index,process_anchors=False)
                        tag_content=re.sub(' +',' ',tag_content)
                        title_population=count_list_word_in_statement(tag_content,news_news_title_list,case_sensitive=False,distinct_word=False)
                        if len(tag_content.split()) > MINIMUM_WORDS_TO_SELECT and title_population > 0:
                            if debug_mode: self._print_(print_prefix + 'IDENTIFIED\tIndex identified:' + str(each_index) + '\t Current Tag Name:' + str(tag_details_result[each_index][0]) + '\t Index details: Parents:' + str(tag_details_result[each_index][4]) + '\t  Childs:' + str(tag_details_result[each_index][3]) + '\t  Content (' + str(len(tag_content))+ '):' + str(tag_details_result[each_index][1]))
                            collect_highlevel_data.append(tag_details_result[each_index][4])
                            collect_highlevel_data_details.append([each_index,tag_details_result[each_index][0],tag_content,tag_details_result[each_index]])
                        else:
                            if debug_mode: self._print_(print_prefix + 'IGNORE\tDiv tag(' + str(each_index) + ') with no child div - stats: Len=' + str(len(tag_content)) + '\t stats:' + str(current_tag_details))
                    else:
                        if debug_mode: self._print_(print_prefix + ' Div tag(' + str(each_index) + ') stats:' + str(current_tag_details))
        length_of_initial_selection=len(collect_highlevel_data)
        if (not length_of_initial_selection) or length_of_initial_selection < 2:
            if self.developer_mode: self._print_('No tag with number of words greater than ' + str(MINIMUM_WORDS_TO_SELECT))
            return focused_content_data
        if debug_mode: 
            self._print_('\n')
            self._print_(print_prefix + 'Collected LINKS length='  + str(len(collect_highlevel_data)))
            for each_list in collect_highlevel_data_details:
                self._print_(print_prefix + str(each_list))
            self._print_('\n')
        if self.TRACK_TIME_MODE or self.developer_mode: self._print_( print_prefix + log_time_stamp() + ':identify common parent')
        comm_parent=self.HTMLHandling_New_ins.get_common_parent_in_html(collect_highlevel_data)
        if self.developer_mode: self._print_(print_prefix + 'Common Parent:' + str(comm_parent) + '\tLength:' + str(length_of_initial_selection))
        if comm_parent <= 0:
            if self.developer_mode: self._print_(print_prefix + 'Common Parent: No common Parent')
            collect_highlevel_data_details.sort(key=lambda x: x[0])#,reverse=True
            flagged_content_length=0
            flagged_content=''
            if self.developer_mode: self._print_(print_prefix + 'No common Parent:standard title:' + repr(news_news_title))
            for each_item in collect_highlevel_data_details:
                if debug_mode: self._print_(print_prefix + '\t No-Common-Parent: current content length - (' +  str(flagged_content_length) + ') :Data to process:'  + str(each_item))
                current_tag_length=len(each_item[2])
                if flagged_content_length == 0 or flagged_content_length < current_tag_length:
                    title_population=count_list_word_in_statement(each_item[2],news_news_title_list,case_sensitive=False,distinct_word=False)
                    if title_population >= news_news_title_list_length:
                        flagged_content=each_item[2]
                        flagged_content_length=current_tag_length
                        if debug_mode: self._print_(print_prefix + 'Trace content with len:'  + str(flagged_content_length) + '\t' + 'title_population:' + str(title_population))
                if flagged_content_length > 500:
                    if debug_mode: self._print_(print_prefix + 'Selected content with len:'  + str(flagged_content_length) + '\t' + 'Content:' + repr(flagged_content))
                    return flagged_content
            return focused_content_data
        if self.developer_mode: self._print_(print_prefix + 'Common Parent details:' + str(tag_details_result[comm_parent]))
        if self.TRACK_TIME_MODE or self.developer_mode: self._print_(print_prefix + log_time_stamp() + ':fetch news using the common parent')
        if comm_parent <= 0:
            if self.developer_mode: self._print_(print_prefix + log_time_stamp() + ':No common parent')
            return focused_content_data
        return self.get_news_from_index(tag_details_result,comm_parent,article_title=news_news_title,process_each_child=True)
    def beautify_menu_from_website_result(self,menu_result_from_website,group_id=1):
        print_prefix='beautify_menu_from_website_result:\t'
        if 'beautify_menu_from_website_result' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if not menu_result_from_website: return []
        if not isinstance(menu_result_from_website,list):
            self._print_(print_prefix + ' menu_result_from_website is not of list type. Received:' + str(type(menu_result_from_website)))
            custom_exit()
        #start here #starthere
        index_level=1
        current_list_of_items=[]
        output_collection_list_temp=[]
        for each_item in menu_result_from_website:
            current_list_of_items.append({'parent':index_level,'data':each_item})
        temp_list_of_items=[]
        temp_list_of_items[:]=[]
        print_prefix='beautify_menu_from_website_result[' + str(index_level) + ']:\t'
        iteration_count=0
        while current_list_of_items:
            iteration_count += 1
            for each_item in current_list_of_items:
                each_list_item=each_item['data']
                parent_index=each_item['parent']
                if debug_mode: self._print_(print_prefix + 'Iteration:[' + str(iteration_count)+ '].\t current list item data:--' + str(each_item['parent']) + '--\t' + str(each_item['data']))
                if isinstance(each_list_item,dict):
                    parent_changed=False
                    if debug_mode: self._print_(print_prefix + ' current item:' + str(each_list_item) + '\t Type:' + str(type(each_list_item)))
                    temp_dict={}
                    temp_dict['link']=''
                    temp_dict['value']=''
                    temp_dict['desc']=''
                    temp_dict['parent']=parent_index
                    has_value=False
                    if 'link' in each_list_item:
                        temp_dict['link']=each_list_item['link']
                        has_value=True
                    if 'value' in each_list_item:
                        temp_dict['value']=each_list_item['value']
                        has_value=True
                    if 'desc' in each_list_item:
                        temp_dict['desc']=each_list_item['desc']
                        has_value=True
                    if has_value:
                        index_level += 1
                        parent_changed=True
                        print_prefix='beautify_menu_from_website_result[' + str(index_level) + ']:\t'
                        temp_dict['index']=index_level
                        if debug_mode: self._print_(print_prefix + ' Added to output:' + str(temp_dict))
                        output_collection_list_temp.append(temp_dict.copy())
                    if 'inner-loop' in each_list_item:
                        current_sub_item=copy.deepcopy(each_list_item['inner-loop'])
                        if parent_changed:
                            new_parent_index=index_level #Default before parent change logic
                        else:
                            new_parent_index=parent_index
                        while True:
                            current_length=len(current_sub_item)
                            if current_length == 1:
                                if isinstance(current_sub_item,list):
                                    current_sub_item=copy.deepcopy(current_sub_item[0])
                                    if debug_mode: self._print_(print_prefix + 'current sub item\t L1 List:Continue:\t' + str(current_sub_item))
                                    continue
                                elif isinstance(current_sub_item,dict):
                                    if 'inner-loop' in current_sub_item:
                                        current_sub_item=copy.deepcopy(current_sub_item['inner-loop'])
                                        if debug_mode: self._print_(print_prefix + 'current sub item\t L1 Dict Inner Loop:Continue:\t' + str(current_sub_item))
                                        continue
                                    else:
                                        if debug_mode: self._print_(print_prefix + 'current sub item\t L1 Dict No Inner Loop:Break:\t' + str(current_sub_item))
                                        temp_list_of_items.append({'parent':new_parent_index,'data':current_sub_item.copy()})
                                        break
                                else:
                                    self._print_(print_prefix + 'current sub item type:' + str(type(current_sub_item)) + '\t Logical flow error.' + '\t item:' + str(each_sub_item) )
                                    exit()
                            else:
                                if isinstance(current_sub_item,dict):
                                    if debug_mode: self._print_(print_prefix + 'current sub item\t LN Dict :Add:\t' + str(current_sub_item))
                                    temp_list_of_items.append({'parent':new_parent_index,'data':current_sub_item.copy()})
                                elif isinstance(current_sub_item,list):
                                    for each_sub_item in current_sub_item:
                                        if isinstance(each_sub_item,list):
                                            if debug_mode: self._print_(print_prefix + 'current sub item\t LN list list :Add:\t' + str(current_sub_item))
                                            temp_list_of_items.append({'parent':new_parent_index,'data':copy.deepcopy(each_sub_item)})
                                        elif isinstance(each_sub_item,dict):
                                            if debug_mode: self._print_(print_prefix + 'current sub item\t LN list dict :Add:\t' + str(current_sub_item))
                                            temp_list_of_items.append({'parent':new_parent_index,'data':each_sub_item.copy()})
                                        else:
                                            if debug_mode: self._print_(print_prefix + 'current sub item type:' + str(type(each_sub_item)) + '\t Length:' + str(current_length) + '\t item:' + str(each_sub_item) )
                                            exit()
                            break
                elif isinstance(each_list_item,list):#the new introduction is a problem
                    for each_list_sub_item in each_list_item:
                        if isinstance(each_list_sub_item,dict):
                            parent_changed=False
                            temp_dict={}
                            temp_dict['link']=''
                            temp_dict['value']=''
                            temp_dict['desc']=''
                            temp_dict['parent']=parent_index
                            has_value=False
                            if 'link' in each_list_sub_item and 'value' in each_list_sub_item:
                                temp_dict['link']=each_list_sub_item['link']
                                temp_dict['value']=each_list_sub_item['value']
                                index_level += 1
                                parent_changed=True
                                print_prefix='beautify_menu_from_website_result[' + str(index_level) + ']:\t'
                                temp_dict['index']=index_level
                                if debug_mode: self._print_(print_prefix + ' Added to output:' + str(temp_dict))
                                output_collection_list_temp.append(temp_dict.copy())
                            if 'inner-loop' in each_list_sub_item:
                                current_sub_item=copy.deepcopy(each_list_sub_item['inner-loop'])
                                if parent_changed:
                                    new_parent_index=index_level #Default before parent change logic
                                else:
                                    new_parent_index=parent_index
                                while True:
                                    current_length=len(current_sub_item)
                                    if current_length == 1:
                                        if isinstance(current_sub_item,list):
                                            current_sub_item=copy.deepcopy(current_sub_item[0])
                                            if debug_mode: self._print_(print_prefix + 'current sub item\t L1 List:Continue:\t' + str(current_sub_item))
                                            continue
                                        elif isinstance(current_sub_item,dict):
                                            if 'inner-loop' in current_sub_item:
                                                current_sub_item=copy.deepcopy(current_sub_item['inner-loop'])
                                                if debug_mode: self._print_(print_prefix + 'current sub item\t L1 Dict Inner Loop:Continue:\t' + str(current_sub_item))
                                                continue
                                            else:
                                                if debug_mode: self._print_(print_prefix + 'current sub item\t L1 Dict No Inner Loop:Break:\t' + str(current_sub_item))
                                                temp_list_of_items.append({'parent':new_parent_index,'data':current_sub_item.copy()})
                                                break
                                        else:
                                            self._print_(print_prefix + 'current sub item type:' + str(type(current_sub_item)) + '\t Logical flow error.' + '\t item:' + str(each_sub_item) )
                                            exit()
                                    else:
                                        if isinstance(current_sub_item,dict):
                                            if debug_mode: self._print_(print_prefix + 'current sub item\t LN Dict :Add:\t' + str(current_sub_item))
                                            temp_list_of_items.append({'parent':new_parent_index,'data':current_sub_item.copy()})
                                        elif isinstance(current_sub_item,list):
                                            for each_sub_item in current_sub_item:
                                                if isinstance(each_sub_item,list):
                                                    if debug_mode: self._print_(print_prefix + 'current sub item\t LN list list :Add:\t' + str(current_sub_item))
                                                    temp_list_of_items.append({'parent':new_parent_index,'data':copy.deepcopy(each_sub_item)})
                                                elif isinstance(each_sub_item,dict):
                                                    if debug_mode: self._print_(print_prefix + 'current sub item\t LN list dict :Add:\t' + str(current_sub_item))
                                                    temp_list_of_items.append({'parent':new_parent_index,'data':each_sub_item.copy()})
                                                else:
                                                    if debug_mode: self._print_(print_prefix + 'current sub item type:' + str(type(each_sub_item)) + '\t Length:' + str(current_length) + '\t item:' + str(each_sub_item) )
                                                    exit()
                                    break
                            
                            #if len(each_list_sub_item.keys()) > 2:
                            #    self._print_(print_prefix + ' current item:' + str(each_list_sub_item) + '\t of parent Type:' + str(type(each_list_item)))
                            #    print 'The dictionary has more keys than expected?'
                            #    exit()
                        else:
                            self._print_(print_prefix + ' current item:' + str(each_list_sub_item) + '\t of parent Type:' + str(type(each_list_item)))
                            print 'Do I have place here?'
                            exit()
            current_list_of_items[:]=[]
            if temp_list_of_items:
                current_list_of_items=copy.deepcopy(temp_list_of_items)
                temp_list_of_items[:]=[]
            else:
                break
        output_collection_list={}
        output_collection_list[1]={'link':'','value':'','desc':'','parent':0,'childs':[]}
        for each_item in output_collection_list_temp:
            output_collection_list[each_item['index']]={'link':each_item['link'],'value':each_item['value'].strip('\n'),'desc':each_item['desc'].strip('\n'),'parent':each_item['parent'],'childs':[]}
            output_collection_list[each_item['parent']]['childs'].append(each_item['index'])
        return output_collection_list
    def get_menus_from_website(self):
        #Pending : If length is wrong -- should be related to title
        #a with div and no ul ol: http://www.itnews.com.au/news/aarnet-increases-basslink-capacity-to-10-gbps-250466
        self.current_function_name='get_menus_from_website'
        collect_menu_details=[]
        collected_links=[]
        tags_to_look=['ul','ol']
        ignore_branches_for_tags=[]
        MINIMUM_WORDS_TO_SELECT=20
        processed_indexes=[]
        ignored_indexes=[]
        print_prefix='get_menus_from_website:\t'
        if 'get_menus_from_website' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if not self.basic_info_collected:
            if debug_mode: self._print_(print_prefix + 'basic_info_collected is not set to True')
            return collect_menu_details
        tag_details_result=self.tag_details_result
        #INDEX=(TAGNAME, TAGTEXT,PARENT_INDEX,ALL_CHILDS,ALL_PARENTS,HREF,CLASS,INDEX,TAG_INFO)
        #print 'base_url',base_url
        temp_flag=False
        for each_tag in tags_to_look:
            if each_tag in tag_details_result:
                temp_flag=True
                break
        if not temp_flag:
            if self.developer_mode: self._print_('Tags to be searched not available in the HTML analysis result: Tags to be search are : ' + ','.join(tags_to_look))
            return collect_menu_details
        if debug_mode:# or True:
            self._print_( print_prefix + '\nList of all tags')
            for each_of in tag_details_result:
                self._print_(print_prefix + str(each_of) + '\t' + str(tag_details_result[each_of]))       
        collect_highlevel_data=[]
        collect_highlevel_data_details=[]
        if self.TRACK_TIME_MODE or self.developer_mode: 
            self._print_(print_prefix + 'collecting Menus')
        for each_ignore_tag in ignore_branches_for_tags:
            if each_ignore_tag in tag_details_result:
                for each_index in tag_details_result[each_ignore_tag]:
                    for each_child in tag_details_result[each_index][3]:
                        if each_child not in ignored_indexes:
                            if debug_mode: self._print_(print_prefix + 'Index ' + str(each_child) + ' is an ignore tag "' + each_ignore_tag + '" and it will not be processed')
                            ignored_indexes.append(each_child)
        for each_tag in tags_to_look:
            if each_tag in tag_details_result:
                for each_index in tag_details_result[each_tag]:
                    if each_index not in ignored_indexes and each_index not in processed_indexes:
                        already_processed_indicator=False
                        for each_processed in processed_indexes:
                            if each_processed in tag_details_result[each_index][4]:# ul within ul
                                already_processed_indicator=True
                        if already_processed_indicator:
                            if debug_mode: self._print_(print_prefix + ' Index:' + str(each_index) + ' -  has a parent which is processed already')
                            processed_indexes.append(each_index)
                            continue
                        #if each_index != 124: continue
                        current_menu_uo_list=self.HTMLHandling_New_ins.get_processed_un_ordered_list(tag_details_result,each_index)
                        if current_menu_uo_list:
                            if debug_mode:
                                self._print_(print_prefix + 'Obtained Menu:' + str(current_menu_uo_list))
                            collect_menu_details.append(self.beautify_menu_from_website_result(current_menu_uo_list))
                            self.add_key_index('menu',each_index)
                        #print_list_new(self.HTMLHandling_New_ins.get_processed_un_ordered_list(tag_details_result,each_index))
                        processed_indexes.append(each_index)
                        continue
        return collect_menu_details
    def fetch_title(self,url_path,html_content_in=None): # Avoid fetch_for_url and move to core
        self.current_function_name='fetch_title'
        print_prefix='fetch_title:\t'
        web_url_title=''
        if 'fetch_title' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if not url_path:
            self._print_(print_prefix + ' url_path is not provided')
            exit()
        if html_content_in:
            html_content=html_content_in
        else:
            if self.use_selenium:
                html_content=get_url_page_source_via_selenium(url_path)
            else:
                html_content=fetch_for_url(url_path,file_only_mode=self.work_offline)
        if not html_content: 
            if self.developer_mode: self._print_(print_prefix + log_time_stamp() + ' No html_content')
            return web_url_title
        if not is_html_doc(html_content):
            if self.developer_mode: self._print_(print_prefix + log_time_stamp() + ' Not a html document')
            return web_url_title
        html_content=re.sub(r'([\t\n]+)',' ',html_content)
        web_url_title_html=re.findall(r'(<title(?:(?!<\/title>).)*<\/title>)',html_content)
        if web_url_title_html:
            web_url_title_html=web_url_title_html[0]
        if debug_mode: self._print_(print_prefix + ' html title tag:' + repr(web_url_title_html))
        if not web_url_title_html: 
            return web_url_title
        web_url_title_html_parse=self.HTMLHandling_New_ins.get_html_tag_properties(web_url_title_html)
        if debug_mode: self._print_(print_prefix + ' html title tag parse:' + repr(web_url_title_html_parse))
        if web_url_title_html_parse and 'tag_content_value' in web_url_title_html_parse and 'current_tag_name' in web_url_title_html_parse:
            if web_url_title_html_parse['current_tag_name'] == 'title':
                web_url_title = web_url_title_html_parse['tag_content_value']
        return web_url_title
    def add_key_index(self,category,index_to_be_added_in):
        print_prefix='add_key_index\t'
        if 'add_key_index' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        index_to_be_added=[]
        if isinstance(index_to_be_added_in,(int,long)):
            index_to_be_added.append(index_to_be_added_in)
        else:
            for each_index in index_to_be_added_in:
                index_to_be_added.append(each_index)
        if category not in self.key_indexes:
            self.key_indexes[category]=[]
        for each_index in index_to_be_added:
            self.key_indexes[category].append(each_index)
        return True
    def display_class_data(self):
        print_prefix='display_class_data\t'
        self._print_(print_prefix + 'Website:\t' + str(self.webpage_url))
        for each_key in self.key_indexes:
            self._print_(print_prefix + 'key_indexes:\t' + str(each_key) + ':' + str(self.key_indexes[each_key]))
        return True
class HTMLHandling_New():
    def __init__(self,developer_mode=False,print_instance=None,debug_mode=[],work_offline=False,log_process_status=True,deep_developer_mode=False):
        self.input_content=''
        self.developer_mode=developer_mode
        self.deep_developer_mode=deep_developer_mode
        self.debug_mode=debug_mode
        self.current_function_name=''
        self.work_offline=work_offline
        self.log_process_status=log_process_status
        self.tags_list_special=['code','var','address']
        self.initiate_print_instance(print_instance)
        self.TRACK_TIME_MODE=False
        self.CONTAINER_TAGS=['div','table','td','tr','h1','h2','h3','h4','h5','h6','p','a','span','area','ul','li','article','section']#ul,li are added
        self.BLOCK_TAGS=['div','table','p','ul','article']#does not allow text tags
        self.TEXT_ONLY_TAGS=['p']
        
        self.COLLECTED_INLINE_ELEMENTS=['b','big','i','small','tt','abbr','acronym','cite','code','dfn','em','kbd','strong','samp','time','var','a','bdo','br','img','map','object','q','script','span','sub','sup','button','input','label','select','textarea']
        self.COLLECTED_BLOCK_ELEMENTS=['address','blockquote','center','dir','div','dl','fieldset','form','h1','h2','h3','h4','h5','h6','isindex','menu','noframes','noscript','ol','p','pre','table','ul']
        self.COLLECTED_TEXT_FORMATTING=['a','abbr','acronym','address','b','basefont','bdo','big','blink','center','cite','code','comment','del','dfn','em','font','i','ins','kbd','marquee','nobr','noscript','plaintext','pre','q','rb','rbc','rp','rt','rtc','ruby','s','samp','small','span','strike','strong','sub','sup','tt','u','var','wbr','xmp']
        self.COLLECTED_IMAGE_MEDIA=['applet','area','bgsound','embed','img','map','noembed','object','param']

        self.TAG_TEXT=['style','abbr','acronym','b','em','i','small','strong','sub','sup','ins','del','mark']
        self.TAG_LINK=['a']
        self.TAG_IMAGE=['applet','area','bgsound','embed','img','map','noembed','object','param']
        self.TAG_CONTAINER=['address','blockquote','center','dir','div','dl','fieldset','form','h1','h2','h3','h4','h5','h6','isindex','menu','noframes','noscript','ol','p','pre','table','ul','article','li']
        self.TAG_TEXT_CONTAINER=['h1','h2','h3','h4','h5','h6','p']
        self.TAG_PICTURE=['figcaption','figure','svg']
        self.ins_weburlparse=WebURLParse('none.com',ignore_errors=True)
        if self.developer_mode:
            self._print_('__init__:\t' + ' Instance created with developer_mode:' + str(self.developer_mode) + ' \t Log Process:' + str(self.log_process_status))
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='HTMLHandling'
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
    def get_html_closing_tags(self,statement):
        #self.current_function_name='get_html_closing_tags'
        if not statement: return []
        if '</' not in statement: return []
        try:
            tag_list=re.findall(r'<\/(\w+)>',statement.strip().lower())
        except :
            return []
        if not tag_list: return []
        return tag_list
    def get_absolute_path(self,parent_url,child_url):
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
            self._print_('get_absolute_path: Exception for P=' + parent_url + '. c=' + child_url + '. Error:' + str(e))
            return ''
    def get_text_from_html_string(self,in_input_line):
        #self.current_function_name='get_text_from_html_string'
        if not in_input_line: return ''
        if not (isinstance(in_input_line,str) or isinstance(in_input_line,unicode)): return ''
        input_line=re.sub(r'<(\w+)(\s[^<>]+?)([/]?)>',r' ',in_input_line)
        input_line=re.sub(r'<(\w+)>',r' ',input_line)
        input_line=re.sub(r'(<\/\w+[ ]*>)',r' ',input_line)
        return input_line
    def get_html_tag_properties_short(self,in_input_line):
        print_prefix='get_html_tag_properties_short:\t'
        #self.current_function_name='get_html_tag_properties_short'
        #gets the first tag as tag and entire text as content
        if self.developer_mode: self._print_(print_prefix + str(in_input_line))
        output_dict={}
        input_line=in_input_line.strip()
        if not re.findall(r'^<\w+',input_line): return False
        tag_list=re.search(r'<(\w+)(\s[^<>]+?)([/]?)>',input_line)
        tag_name_is=''
        if tag_list:
            try:
                tag_name_is=tag_list.group(1)
            except:
                pass
        input_line=re.sub(r'<(\w+)(\s[^<>]+?)([/]?)>',r' ',input_line)
        input_line=re.sub(r'(<\/\w+[ ]*>)',r' ',input_line)
        return {'current_tag_name':tag_name_is.lower(),'tag_content_value':input_line,'find method':'exception'}
    def is_closing_tag(self,in_input_line):
        #self.current_function_name='is_closing_tag'
        CLOSING_TAG_REGEX=r'^</(\w+)>$'
        closing_tag_found=re.findall(CLOSING_TAG_REGEX,in_input_line.strip().lower())
        if not closing_tag_found:
            return False
        return closing_tag_found[0]
    def get_html_tag_properties(self,in_input_line,filter_tags=[],consume_all_content=True,developer_mode=False):
    #assumption: each line has content for only one tag; else first tag information alone processed
    #assumption: each line has a tag at the start of the line except leading spaces
    #Failed on <div style="display: inline; text-transform: uppercase;"> New York </div> &nbsp;&ndash;&nbsp;February 28, 2013&nbsp;/Press Release/ &nbsp;&ndash;&ndash;&nbsp; </b>  
        self.current_function_name='get_html_tag_properties'
        print_prefix='get_html_tag_properties:\t'
        if 'get_html_tag_properties' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        output_dict={}
        input_line=get_printable_string(in_input_line)#.strip() #Strip commented
        task_completed=False
        tag_found=False
        tag_started=False
        roaming_tag=False
        attribute_found=False
        attribute_started=False
        attribute_value_started=False
        content_started=False
        tag_name=''
        attribute_name=''
        attribute_value=''
        tag_value=''
        escape_character_started=False
        escape_character_found=''
        TAG_START='<'
        TAG_END='>'
        input_line_length=len(input_line)
        if debug_mode: self._print_(print_prefix + ' Input:' + input_line)
        if debug_mode: self._print_('\nIteration\tCharacter\tTask Completed\tTag Found\tTag Started\tRoaming Tag\tAttribute Found\tAttribute Started\tAttribute Value Started\tContent Started\tEscape Char Started\tEscape Character Found\tTag Name\tAttribute Name\tAttribute Value\tTag Value')
        next_character=''
        processed_index=0
        end_tag_found=False

        for iter_i in range(input_line_length):
            each_char=input_line[iter_i]
            if (iter_i+1) < input_line_length:
                next_character=input_line[iter_i+1]
            else:
                next_character=''
            if  debug_mode: self._print_(print_prefix + str(iter_i) + '\t\'' + str(each_char) + '\t' + str(task_completed) + '\t' + str(tag_found) + '\t' + str(tag_started) + '\t' + str(roaming_tag) + '\t' + str(attribute_found) + '\t' + str(attribute_started) + '\t' + str(attribute_value_started) + '\t' + str(content_started) + '\t' + str(escape_character_started) + '\t' + str(escape_character_found) + '\t' + str(tag_name) + '\t' + str(attribute_name) + '\t' + str(attribute_value) + '\t' + str(tag_value),skip_timestamp=True)
            if task_completed: break
            if each_char == TAG_START:
                if roaming_tag: # < should come when processing tag or attribute but it can visible after content to mark the end of the task
                    if  debug_mode: self._print_(print_prefix + '.@ TAG_START - roaming_tag',skip_timestamp=True)
                    if  debug_mode: self._print_(print_prefix + 'get_html_tag_properties() - Logical error: TAG_START encountered when TAG already started',skip_timestamp=True)
                    return self.get_html_tag_properties_short(input_line)
                if content_started:
                    if  debug_mode: self._print_(print_prefix + '.@ TAG_START - content_started',skip_timestamp=True)
                    # a tag and content has processed; hence breaking the line and return the dictionary
                    output_dict['tag_content_value']=tag_value
                    task_completed=True
                    processed_index=(iter_i - 1)
                    break
                if not tag_found:#Marking the start of the tag i.e, < encountered
                    if next_character == '/':
                        if  debug_mode: self._print_(print_prefix + '.@ TAG_START - next tag is closing tag. closing tag without starting the tag',skip_timestamp=True)
                        return False
                    else:
                        if  debug_mode: self._print_(print_prefix + '.@ TAG_START - not roaming_tag',skip_timestamp=True)
                        roaming_tag=True
                        tag_started=True
                        tag_name=''
                        attribute_name=''
                        attribute_value=''
                        tag_value=''
                        continue
            elif each_char == TAG_END:#<tag> <tag attribute> <tag attribute=""> <tag attribute=value>
                if not roaming_tag:
                    if  debug_mode: self._print_(print_prefix + '.@ TAG_END - not roaming_tag',skip_timestamp=True)
                    if  debug_mode: self._print_(print_prefix + 'get_html_tag_properties() - Logical error: TAG_END encountered without TAG_START',skip_timestamp=True)
                    return self.get_html_tag_properties_short(input_line)
                roaming_tag=False
                if tag_started: #<tag>
                    if  debug_mode: self._print_(print_prefix + '.@ TAG_END - tag_started',skip_timestamp=True)
                    tag_found=True
                    tag_started=False
                    output_dict['current_tag_name']=tag_name
                    continue
                if tag_found:#<tag >
                    if  debug_mode: self._print_(print_prefix + '.@ TAG_END - tag_found',skip_timestamp=True)
                    continue
                #attribute_started: <tag attribute>
                #tag_found: <tag attribute=""> <tag attribute=value>
                if attribute_started:#attribute_started: either first attr or other attr
                    if  debug_mode: self._print_(print_prefix + '.@ TAG_END - attribute_started',skip_timestamp=True)
                    attribute_found=False
                    attribute_started=False
                    output_dict[attribute_name]=''
                    continue
                if attribute_found and (not attribute_started):#<tag attribute >
                    if  debug_mode: self._print_(print_prefix + '.@ TAG_END - attribute_found and not attribute_started',skip_timestamp=True)
                    attribute_found=False
                    continue
                if attribute_found:#<tag attribute=value>
                    if  debug_mode: self._print_(print_prefix + '.@ TAG_END - attribute_found',skip_timestamp=True)
                    attribute_found=False
                    attribute_value_started=False
                    output_dict[attribute_name]=attribute_value
                    attribute_name=''
                    attribute_value=''
                    continue
            elif each_char in ['"',"'"]:#Tuple to list () to []
                if roaming_tag:
                    if escape_character_started:
                        if  debug_mode: self._print_(print_prefix + '.@ " - roaming_tag + escape_character_started',skip_timestamp=True)
                        if attribute_value_started:
                            if escape_character_found and escape_character_found != each_char:
                                if  debug_mode: self._print_(print_prefix + '.@ " - roaming_tag + escape_character_started + attribute_value_started + other escape found: continuing',skip_timestamp=True)
                                attribute_value=attribute_value+each_char
                            else:
                                if  debug_mode: self._print_(print_prefix + '.@ " - roaming_tag + escape_character_started + attribute_value_started + ending escape',skip_timestamp=True)
                                escape_character_started=False
                                escape_character_found=''
                                attribute_value_started=False
                                attribute_found=False
                                output_dict[attribute_name]=attribute_value.strip('"')
                                attribute_name=''
                                attribute_value=''
                            continue
                        else:
                            if  debug_mode: self._print_(print_prefix + '.@ " - roaming_tag  + escape_character_started + not attribute_value_started',skip_timestamp=True)
                            if  debug_mode: self._print_(print_prefix + 'get_html_tag_properties() - Logical error: double quote encountered without starting double quote for attribute value',skip_timestamp=True)
                            return self.get_html_tag_properties_short(input_line)
                    else:
                        if attribute_found:
                            if  debug_mode: self._print_(print_prefix + '.@ " - roaming_tag + not escape_character_started + attribute_found',skip_timestamp=True)
                            if attribute_value_started:
                                if  debug_mode: self._print_(print_prefix + '.@ " - roaming_tag + not escape_character_started + attribute_found + attribute_value_started',skip_timestamp=True)
                                if  debug_mode: self._print_(print_prefix + 'get_html_tag_properties() - Logical error: double quote encountered in mid of attribute value',skip_timestamp=True)
                                return self.get_html_tag_properties_short(input_line)
                            else:
                                if  debug_mode: self._print_(print_prefix + '.@ " - roaming_tag+ not escape_character_started + attribute_found + not attribute_value_started',skip_timestamp=True)
                                attribute_value_started=True
                                escape_character_started=True
                                escape_character_found=each_char
                        else:
                            if  debug_mode: self._print_(print_prefix + '.@ " - roaming_tag+ not escape_character_started + not attribute_found',skip_timestamp=True)
                            if  debug_mode: self._print_(print_prefix + 'get_html_tag_properties() - Logical error: double quote encountered without attribute value',skip_timestamp=True)
                            return self.get_html_tag_properties_short(input_line)
                else:
                    if  debug_mode: self._print_(print_prefix + '.@ " - Not roaming_tag',skip_timestamp=True)
                    if content_started:
                        if  debug_mode: self._print_(print_prefix + '.@ " - Not roaming_tag + content_started',skip_timestamp=True)
                        tag_value=tag_value+each_char
                        output_dict['tag_content_value']=tag_value
                    elif tag_found:
                        if  debug_mode: self._print_(print_prefix + '.@ " - Not roaming_tag + tag_found + not content_started',skip_timestamp=True)
                        content_started=True
                        tag_value=each_char
                        output_dict['tag_content_value']=tag_value
            elif each_char == '=':
                if  debug_mode: self._print_(print_prefix + '.@ = ',skip_timestamp=True)
                if roaming_tag:
                    if  debug_mode: self._print_(print_prefix + '.@ = - roaming_tag',skip_timestamp=True)
                    if attribute_started:
                        if  debug_mode: self._print_(print_prefix + '.@ = - roaming_tag + attribute_started',skip_timestamp=True)
                        attribute_found=True
                        attribute_started=False
                        output_dict[attribute_name]=''
                    elif attribute_value_started:
                        if  debug_mode: self._print_(print_prefix + '.@ = - roaming_tag + not attribute_started + attribute_value_started',skip_timestamp=True)
                        attribute_value=attribute_value+each_char
                    else:
                        if  debug_mode: self._print_(print_prefix + '.@ = - roaming_tag + not attribute_started + not attribute_value_started',skip_timestamp=True)
                        if  debug_mode: self._print_(print_prefix + 'get_html_tag_properties() - Logical error: = encountered attribute or attribute value',skip_timestamp=True)
                        return self.get_html_tag_properties_short(input_line)
                else:
                    if  debug_mode: self._print_(print_prefix + '.@ = - Not roaming_tag',skip_timestamp=True)
                    if content_started:
                        if  debug_mode: self._print_(print_prefix + '.@ = - Not roaming_tag + content_started',skip_timestamp=True)
                        tag_value=tag_value+each_char
                        output_dict['tag_content_value']=tag_value
                    elif tag_found:
                        if  debug_mode: self._print_(print_prefix + '.@ = - Not roaming_tag + not content_started + tag_found',skip_timestamp=True)
                        content_started=True
                        tag_value=each_char
                        output_dict['tag_content_value']=tag_value
            elif each_char == ' ':
                if  debug_mode: self._print_(print_prefix + '.@ space',skip_timestamp=True)
                if roaming_tag:
                    if  debug_mode: self._print_(print_prefix + '.@ space - roaming_tag',skip_timestamp=True)
                    if attribute_started:#if next char is space = or > pass otherwise complete attributenmae
                        if  debug_mode: self._print_(print_prefix + '.@ space - roaming_tag + attribute_started',skip_timestamp=True)
                        if iter_i < (input_line_length-1):
                            if input_line[iter_i+1] in ['=','>',' ']:
                                pass
                            else:
                                attribute_started=False
                                output_dict[attribute_name]=''
                        else:
                            if  debug_mode: self._print_(print_prefix + '.@ space - roaming_tag + not attribute_started',skip_timestamp=True)
                            attribute_started=False
                            output_dict[attribute_name]=''
                    elif attribute_value_started:
                        #The attribute value ends if it starts without escape character
                        if escape_character_started:
                            if  debug_mode: self._print_(print_prefix + '.@ space - roaming_tag + attribute_value_started + escape_character_started',skip_timestamp=True)
                            attribute_value=attribute_value+each_char
                        else:
                            if  debug_mode: self._print_(print_prefix + '.@ space - roaming_tag + attribute_value_started + not escape_character_started +escape_character_found=' + str(escape_character_found),skip_timestamp=True)
                            #escape_character_found=each_char
                            attribute_value_started=False
                            attribute_found=False
                            output_dict[attribute_name]=attribute_value.strip('"')
                            attribute_name=''
                            attribute_value=''
                            escape_character_started=False
                            escape_character_found=''
                    elif tag_started:# next char is alpha pass else complete tag name
                        if  debug_mode: self._print_(print_prefix + '.@ space - roaming_tag + not attribute_value_started + tag_started',skip_timestamp=True)
                        tag_started=False
                        tag_found=True
                        output_dict['current_tag_name']=tag_name
                    else:
                        if  debug_mode: self._print_(print_prefix + '.@ space - roaming_tag + else',skip_timestamp=True)
                        pass
                else:
                    if  debug_mode: self._print_(print_prefix + '.@ space - Not roaming_tag',skip_timestamp=True)
                    if content_started:
                        if  debug_mode: self._print_(print_prefix + '.@ space - Not roaming_tag + content_started',skip_timestamp=True)
                        tag_value=tag_value+each_char
                        output_dict['tag_content_value']=tag_value
                    elif tag_found:
                        if  debug_mode: self._print_(print_prefix + '.@ space - Not roaming_tag + not content_started + tag_found',skip_timestamp=True)
                        content_started=True
                        tag_value=each_char
                        output_dict['tag_content_value']=tag_value
            elif each_char == '/' and roaming_tag and next_character == '>':
                #if the attribute value started without escape character then it should be completed properly
                if  debug_mode: self._print_(print_prefix + '.@ slash - roaming_tag and next character is >',skip_timestamp=True)
                if attribute_value_started and (not escape_character_started) and escape_character_found=='alpha':
                    if  debug_mode: self._print_(print_prefix + '.@ slash - roaming_tag and next character is > and attribute_value_started and escape_character_found=alpha',skip_timestamp=True)
                    attribute_value_started=False
                    attribute_found=False
                    output_dict[attribute_name]=attribute_value.strip('"')
                    attribute_name=''
                    attribute_value=''
                    escape_character_started=False
                    escape_character_found=''
                end_tag_found=True
                continue
            else:
                if roaming_tag:
                    if  debug_mode: self._print_(print_prefix + '.@ Other - roaming_tag',skip_timestamp=True)
                    if tag_started:
                        if  debug_mode: self._print_(print_prefix + '.@ Other - roaming_tag + tag_started',skip_timestamp=True)
                        tag_name=tag_name + each_char
                    elif attribute_started:
                        if  debug_mode: self._print_(print_prefix + '.@ Other - roaming_tag + not tag_started + attribute_started',skip_timestamp=True)
                        attribute_name=attribute_name + each_char
                    elif attribute_value_started:
                        if  debug_mode: self._print_(print_prefix + '.@ Other - roaming_tag + not tag_started + not attribute_started + attribute_value_started',skip_timestamp=True)
                        attribute_value=attribute_value + each_char
                    elif tag_found:
                        if  debug_mode: self._print_('.attribute found='  + str(attribute_found) + '\t.@ Other - roaming_tag + not tag_started + not attribute_started +  not attribute_value_started + not tag_found',skip_timestamp=True)
                        if attribute_found and each_char.isalpha():
                            if  debug_mode: self._print_(print_prefix + '.@ Other - roaming_tag + not tag_started + not attribute_started +  not attribute_value_started + tag_found and current value is alpha.hence starting attribute value',skip_timestamp=True)
                            attribute_value_started=True
                            escape_character_started=False
                            escape_character_found='alpha'
                            attribute_value=each_char
                        else:
                            if  debug_mode: self._print_(print_prefix + '.@ Other - roaming_tag + not tag_started + not attribute_started +  not attribute_value_started + tag_found and current value is not alpha',skip_timestamp=True)
                            #If part is added to handle attribute values which starts without escape characters
                            attribute_name=each_char
                            attribute_started=True#assumption is wrong
                            attribute_value_started=False
                            attribute_value=''
                else:
                    if  debug_mode: self._print_(print_prefix + '.@ Other - Not roaming_tag',skip_timestamp=True)
                    if content_started:
                        if  debug_mode: self._print_(print_prefix + '.@ Other - Not roaming_tag + content_started',skip_timestamp=True)
                        tag_value=tag_value+each_char
                        output_dict['tag_content_value']=tag_value
                    elif tag_found:
                        if  debug_mode: self._print_(print_prefix + '.@ Other - Not roaming_tag + not content_started + tag_found',skip_timestamp=True)
                        content_started=True
                        tag_value=each_char
                        output_dict['tag_content_value']=tag_value
        if 'current_tag_name' in output_dict:
            output_dict['current_tag_name']=output_dict['current_tag_name'].lower()
        if 'tag_content_value' in output_dict:
            if debug_mode: self._print_(print_prefix + 'tag_content_value is available output_dict=' + str(output_dict['tag_content_value']))
            if output_dict['current_tag_name'] not in ['p']: #Tuple to list () to []
                output_dict['tag_content_value']=output_dict['tag_content_value'].strip()
        else:
            if debug_mode: self._print_(print_prefix + 'tag_content_value is not output_dict:' + str(output_dict))
            output_dict['tag_content_value']=''
        if processed_index>0 and 'tag_content_value' in output_dict and consume_all_content and processed_index < (input_line_length-3): 
            if self.developer_mode: self._print_(print_prefix + 'fetching content using get_text_from_html_string')
            un_processed_content=self.get_text_from_html_string(input_line)
            if len(un_processed_content) > len(output_dict['tag_content_value']): output_dict['tag_content_value']=un_processed_content
        if end_tag_found:
            output_dict['closing tags']=[]#'self-ended' need to be added .. < /> </p></b>
            output_dict['closing tags'][:]=[]#'self-ended' need to be added .. < /> </p></b>
            output_dict['closing tags'].append(output_dict['current_tag_name'])
            c_tags_other=self.get_html_closing_tags(in_input_line)
            if c_tags_other:
                for each_tag in c_tags_other:
                    output_dict['closing tags'].append(each_tag)
        else:
            output_dict['closing tags']=self.get_html_closing_tags(in_input_line)
        if True:#This section is to lowercase all attribute names
            output_dict_formatted={}
            for each_key in output_dict:
                output_dict_formatted[each_key.lower()]=output_dict[each_key]
            return output_dict_formatted
        return output_dict
    def remove_unhealthy_tags(self,input_content,remove_header=True,remove_footer=True):
        if 'remove_unhealthy_tags' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        print_prefix='remove_unhealthy_tags\t'
        #self.current_function_name='remove_unhealthy_tags'
        article_content=input_content.replace('\n',' ').replace('\r',' ').replace('\t',' ')
        article_content=re.sub(r' +',' ',article_content)
        if debug_mode: self._print_(print_prefix + 'whitespace handling: Length = ' + str(len(article_content)))
        article_content=re.sub(r'((<script)(?:(?!<\/script>).)*(<\/script>))','',article_content)
        if debug_mode: self._print_(print_prefix + '<script> handling: Length = ' + str(len(article_content)))
        #article_content=re.sub(r'((<noscript)(?:(?!<\/noscript>).)*(<\/noscript>))','',article_content)
        article_content=re.sub(r'((<style)(?:(?!<\/style>).)*(<\/style>))','',article_content)
        if debug_mode: self._print_(print_prefix + '<style> handling: Length = ' + str(len(article_content)))
        if remove_header: 
            article_content=re.sub(r'((<header)(?:(?!<\/header>).)*(<\/header>))','',article_content)
            if debug_mode: self._print_(print_prefix + '<header> handling: Length = ' + str(len(article_content)))
        if remove_footer: 
            article_content=re.sub(r'((<footer)(?:(?!<\/footer>).)*(<\/footer>))','',article_content)
            if debug_mode: self._print_(print_prefix + '<footer> handling: Length = ' + str(len(article_content)))
        article_content=re.sub(r'((<!--)(?:(?!-->).)*(-->))','',article_content)
        if debug_mode: self._print_(print_prefix + 'comments<!-- !--> handling: Length = ' + str(len(article_content)))
        return article_content
    def get_html_head(self,input_content,remove_header=True,remove_footer=True):
        #self.current_function_name='get_html_head'
        matched_tags=input_content
        matched_tags=re.sub(r'(<!--[^>]+-->)',r'',matched_tags)
        matched_tags=re.sub(r'([\t\n]+)',' ',matched_tags)
        matched_tags=re.sub(r'</',' </',matched_tags)
        matched_tags=re.sub(r'>','> ',matched_tags)
        matched_tags=re.sub(r'<(\w+[^<]*[/]?)>',r'\n<\1>',matched_tags)
        matched_tags=re.sub(r'>([\s]*)<',r'>\1\n<',matched_tags)
        index_first=matched_tags.lower().find('<head')
        index_last=matched_tags.lower().find('</head')
        if index_first>0 and index_last>index_first:
            head_content=matched_tags[index_first:index_last+7]
        else:
            head_content=''
        head_content=re.sub(r' +',' ',head_content)
        return head_content
    def html_massage(self,input_content):
        #self.current_function_name='html_massage'
        matched_tags=input_content
        #matched_tags=re.sub(r'<(\w+)(\s[^<]+?)([/]?)>',r'<\1\3>',matched_tags)
        matched_tags=re.sub(r'(<!--[^>]+-->)',r'',matched_tags)
        matched_tags=re.sub(r'([\t\n]+)',' ',matched_tags)
        matched_tags=re.sub(r'</',' </',matched_tags)
        matched_tags=re.sub(r'>','> ',matched_tags)
        matched_tags=re.sub(r'<(\w+[^<]*[/]?)>',r'\n<\1>',matched_tags)
        matched_tags=re.sub(r'>([\s]*)<',r'>\1\n<',matched_tags)#Added to handle unfinished tags like <P> <TABLE style="WIDTH: 225px" border=1 cellSpacing=0 borderColor=#cccccc cellPadding=5 bgColor=#f1f1f1 align=right hspace="6" vspace="6"
        #beautified_html_content=re.sub(r'(<\/\w+[ ]*>)',r'\n\1',matched_tags)
        index_first=matched_tags.lower().find('<body')
        index_last=matched_tags.lower().find('</body')
        if index_first>0 and index_last>index_first:
            body_content=matched_tags[index_first:index_last+7]
        else:
            body_content=matched_tags[:]
        body_content=re.sub(r' +',' ',body_content)
        return body_content
    def split_on_end_tags(self,input_content):
        #self.current_function_name='split_on_end_tags'
        matched_tags=input_content
        matched_tags=re.sub(r'<\/([\w]+)>',r'\n</\1>',matched_tags)
        matched_tags=re.sub(r'\n+','\n',matched_tags)
        return matched_tags
    def merge_on_end_tags(self,input_content):
        #self.current_function_name='merge_on_end_tags'
        matched_tags=input_content
        matched_tags=re.sub(r'\n<\/([a-z]+)>',r'</\1>',matched_tags)
        matched_tags=re.sub(r'\n+','\n',matched_tags)
        return matched_tags
    def get_all_parents(self,data_parent_child_relationship,parent_index):
        #self.current_function_name='get_all_parents'
        #Logic change: here the logic can be changed as if a parent has all his parent , then we can use that instead of re-calculating again
        if not data_parent_child_relationship or (not isinstance(data_parent_child_relationship,dict)):return False
        all_parent_list=[]
        current_parent=parent_index
        all_parent_list.append(current_parent)
        while current_parent in data_parent_child_relationship:
            parent_tag_key_str=str(current_parent) + '_p'
            if parent_tag_key_str in data_parent_child_relationship:
                if data_parent_child_relationship[parent_tag_key_str] < current_parent:
                    current_parent=data_parent_child_relationship[parent_tag_key_str]
                    all_parent_list.append(current_parent)
                else:
                    break
            else:
                break
        return all_parent_list
    def get_deepest_child(self,data_from_tag_analysis,index_to_be_start,depth_level=0):
        #DEEPEST should be the deepest not based on index number
        self.current_function_name='get_deepest_child'
        print_prefix='get_deepest_child(' + str(depth_level) + '):\t'
        if 'get_deepest_child' in self.debug_mode or self.deep_developer_mode:
            debug_mode = True
        else:
            debug_mode = False
        deepest_child=-1
        if depth_level > 25:
            if debug_mode: self._print_(print_prefix + 'Depth Level(' + str(depth_level) + ') is greater than 25')
            return deepest_child
        if not data_from_tag_analysis or (not isinstance(data_from_tag_analysis,dict)):
            if self.developer_mode: self._print_(print_prefix + 'Logical error: data_from_tag_analysis is not dictionary')
            self.current_function_name=''
            return deepest_child
        if data_from_tag_analysis[index_to_be_start][3]:
            for each_child_index in data_from_tag_analysis[index_to_be_start][3]:
                if each_child_index <= index_to_be_start: continue
                if deepest_child < each_child_index:
                    deepest_child = each_child_index
                if data_from_tag_analysis[each_child_index][3]:
                    deepest_grand_child=self.get_deepest_child(data_from_tag_analysis,each_child_index,depth_level=depth_level+1)
                    if debug_mode: self._print_(print_prefix + 'Deepest child for ' + str(each_child_index) + ' is ' + str(deepest_grand_child))
                    if deepest_child < deepest_grand_child:
                        deepest_child = deepest_grand_child
        else:
            return deepest_child
        return deepest_child
    def get_all_childs_and_tags(self,data_from_tag_analysis,index_to_be_start,depth_level=0,include_empty_tags=False):
        self.current_function_name='get_all_childs_and_tags'
        print_prefix='get_all_childs_and_tags(' + str(depth_level) + '):\t'
        if 'get_all_childs_and_tags' in self.debug_mode or self.deep_developer_mode:
            debug_mode = True
        else:
            debug_mode = False
        all_childs_and_tags={'deepest_child':-1,'all_childs':[],'empty':0}
        if depth_level > 25:
            if debug_mode: self._print_(print_prefix + 'Depth Level(' + str(depth_level) + ') is greater than 25')
            return all_childs_and_tags
        if not data_from_tag_analysis or (not isinstance(data_from_tag_analysis,dict)):
            if self.developer_mode: self._print_(print_prefix + 'Logical error: data_from_tag_analysis is not dictionary')
            self.current_function_name=''
            return all_childs_and_tags
        if data_from_tag_analysis[index_to_be_start][3]:
            for each_child_index in data_from_tag_analysis[index_to_be_start][3]:
                if each_child_index <= index_to_be_start: continue
                tag_name=data_from_tag_analysis[each_child_index][0]
                tag_content=data_from_tag_analysis[each_child_index][1]
                tag_content=tag_content.strip().strip('\n\r\t')
                #if (not include_empty_tags) and len(tag_name) == 0 and len(tag_content) == 0 and (not data_from_tag_analysis[each_child_index][3]): 
                if (not include_empty_tags) and len(tag_content) == 0 and (not data_from_tag_analysis[each_child_index][3]): 
                    if debug_mode: self._print_(print_prefix + 'Index ' + str(each_child_index) + ' is an empty tag')
                    continue
                if each_child_index not in all_childs_and_tags['all_childs']:
                    all_childs_and_tags['all_childs'].append(each_child_index)
                if len(tag_name) == 0 or (not tag_name):
                    all_childs_and_tags['empty']=all_childs_and_tags['empty'] + 1
                else:
                    all_childs_and_tags[tag_name]=all_childs_and_tags.get(tag_name,0) + 1
                if all_childs_and_tags['deepest_child'] < each_child_index:
                    all_childs_and_tags['deepest_child'] = each_child_index
                if data_from_tag_analysis[each_child_index][3]:
                    grand_child_details=self.get_all_childs_and_tags(data_from_tag_analysis,each_child_index,depth_level=depth_level+1)
                    if debug_mode: self._print_(print_prefix + 'Deepest child details for ' + str(each_child_index) + ' is ' + str(grand_child_details))
                    if all_childs_and_tags['deepest_child'] < grand_child_details['deepest_child']:
                        all_childs_and_tags['deepest_child'] = grand_child_details['deepest_child']
                    for each_tag in grand_child_details['all_childs']:
                        if each_tag not in all_childs_and_tags['all_childs']:
                            all_childs_and_tags['all_childs'].append(each_tag)
                    for each_key in grand_child_details:
                        if each_key not in ['all_childs','deepest_child']:
                            all_childs_and_tags[each_key]=all_childs_and_tags.get(each_key,0) + grand_child_details[each_key]
        else:
            return all_childs_and_tags
        return all_childs_and_tags
    def dissipated_cloud(self,dict_of_list_of_statements):
        self.current_function_name='dissipated_cloud'
        if 'dissipated_cloud' in self.debug_mode or self.deep_developer_mode:
            debug_mode = True
        else:
            debug_mode = False
        print_prefix='dissipated_cloud:\t'
        t_less_than_3=0
        t_less_than_5=0
        t_long=0
        t_less_than_3_length=0
        t_less_than_5_length=0
        t_long_length=0
        collected_statements=[]
        if not dict_of_list_of_statements: return False
        if isinstance(dict_of_list_of_statements,dict):
            for each_key in dict_of_list_of_statements:
                if isinstance(dict_of_list_of_statements[each_key],list):
                    for each_list_item in dict_of_list_of_statements[each_key]:
                        text_is=each_list_item.strip()
                        if len(text_is) > 0 :
                            collected_statements.append(text_is)
                else:
                    if debug_mode:
                        self._print_(print_prefix + ' dict_of_list_of_statements: the dict member type(' + str(type(dict_of_list_of_statements[each_key])) + ' ) is not list')
                        exit()
        elif isinstance(dict_of_list_of_statements,list):
            for each_list_item in dict_of_list_of_statements[each_key]:
                text_is=each_list_item.strip()
                if len(text_is) > 0 :
                    collected_statements.append(text_is)
        else:
            if debug_mode:
                self._print_(print_prefix + ' dict_of_list_of_statements type(' + str(type(dict_of_list_of_statements)) + ' ) is neither dict nor list')
                exit()
        if debug_mode:
            self._print_(print_prefix + ' Number of statements collected:' + str(len(collected_statements)))
        if not collected_statements: return False
        for each_list_item in collected_statements:
            each_list_item_length=len(each_list_item.split())
            if each_list_item_length <= 3:
                t_less_than_3 += 1
                t_less_than_3_length += each_list_item_length
            elif each_list_item_length > 3 and each_list_item_length <= 5:
                t_less_than_5 += 1
                t_less_than_5_length += each_list_item_length
            else:
                t_long += 1
                t_long_length += each_list_item_length
        if debug_mode: 
            self._print_(print_prefix + ' Count t_less_than_3:' + str(t_less_than_3))
            self._print_(print_prefix + ' Count t_less_than_5:' + str(t_less_than_5))
            self._print_(print_prefix + ' Count t_long:' + str(t_long))
            self._print_(print_prefix + ' Count t_less_than_3_length:' + str(t_less_than_3_length))
            self._print_(print_prefix + ' Count t_less_than_5_length:' + str(t_less_than_5_length))
            self._print_(print_prefix + ' Count t_long_length:' + str(t_long_length))
        if t_long == 0: 
            if debug_mode: self._print_(print_prefix + ' No lengthier statement:')
            return True
        if (t_less_than_3 + t_less_than_5 +t_long ) * .75 < (t_less_than_3 + t_less_than_5):
            if debug_mode: self._print_(print_prefix + 'Smaller statements are more than(>75%)')
            return True
        if (t_less_than_3_length + t_less_than_5_length +t_long_length ) * .50 < (t_less_than_3_length + t_less_than_5_length):
            if debug_mode: self._print_(print_prefix + 'Smaller statements length is more than(>50%)')
            return True
        return False
    def get_tag_group_type(self,data_from_tag_analysis,index_to_be_checked,depth_level=0):
        #Types are: AL (All Links)
        #,LTS (Links + Text - Small Group) 
        #,LTL (Links + Text - Large Group)
        #,AT (All Text) 
        #,IM (Images)
        #,LL (Listed Links)
        #,LT (Listed Text)
        #,EM (Empty or No Tags)
        #,SL (Small Links <=3)
        #,LL (Lengthier Links >3)
        #,TS (Text short <=3)
        #,TL (Text Long >3)
        #,DC (Dissipated Cloud)
        self.current_function_name='get_tag_group_type'
        if 'get_tag_group_type' in self.debug_mode or self.deep_developer_mode:
            debug_mode = True
        else:
            debug_mode = False
        print_prefix='get_tag_group_type(' + str(depth_level) + '):\t'
        tag_group_type='EM'
        if depth_level > 25:
            if debug_mode: self._print_(print_prefix + ' Depth level() is greater than 25')
            return tag_group_type
        if not data_from_tag_analysis or (not isinstance(data_from_tag_analysis,dict)):
            if self.developer_mode: self._print_(print_prefix + 'Logical error: data_from_tag_analysis is not dict')
            self.current_function_name=''
            return tag_group_type
        if index_to_be_checked not in data_from_tag_analysis:
            if self.developer_mode: self._print_(print_prefix + 'Index ' + str(index_to_be_checked) + ' not exist in data_from_tag_analysis')
            self.current_function_name=''
            return tag_group_type
        if data_from_tag_analysis[index_to_be_checked][0] == 'a':
            a_tag_display=get_printable_string(self.support_tag_analysis_reduce_tag(data_from_tag_analysis,index_to_be_checked),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
            a_tag_display=re.sub(r' +',' ',a_tag_display)
            if debug_mode: self._print_(print_prefix + 'Index ' + str(index_to_be_checked) + ' is a tag with len=' + str(len(a_tag_display)))
            if not a_tag_display: return 'SL'
            if len(a_tag_display.split())>3:return 'LL'
            return 'SL'
        list_child_group=self.get_all_childs_and_tags(data_from_tag_analysis,index_to_be_checked)
        if debug_mode:
            self._print_(print_prefix + 'Range to check : ' + str(index_to_be_checked) + ' to ' + str(list_child_group['deepest_child']))
            self._print_(print_prefix + 'Child Details ' + str(list_child_group))
        if list_child_group['deepest_child'] <= 0:
            if debug_mode: self._print_(print_prefix + 'No childs for ' + str(index_to_be_checked))
            if len(data_from_tag_analysis[index_to_be_checked][1].strip()) > 1: 
                tag_group_type='AT'
            return tag_group_type
        processed_indexes=[]
        text_tag_long_count=0
        text_tag_short_count=0
        a_tag_long_count=0
        a_tag_short_count=0
        list_tag_count=0
        image_tag_count=0
        count_data_details={'al':[],'as':[],'tl':[],'ts':[]}
        list_child_group['all_childs'].append(index_to_be_checked)
        length_of_child=len(list_child_group['all_childs'])
        for each_child in list_child_group['all_childs']:
            if each_child in processed_indexes:
                length_of_child = length_of_child - 1
                if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t PROCESSED INDEX')
                continue
            current_tag=data_from_tag_analysis[each_child][0]
            current_tag_content=data_from_tag_analysis[each_child][1]
            current_tag_content=current_tag_content.strip()
            if debug_mode: self._print_(print_prefix + 'Processing Childs: Index:' + str(each_child) + ' (' + str(length_of_child) + ')\t TAG:' + current_tag + '\t CONTENT:' + current_tag_content)
            if (not current_tag) or len(current_tag) == 0 or current_tag in self.TAG_TEXT or current_tag in self.TAG_TEXT_CONTAINER:
                if each_child not in processed_indexes: processed_indexes.append(each_child)
                if len(current_tag_content) == 0: 
                    length_of_child = length_of_child - 1
                    if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t TEXT EMPTY TAG:' + current_tag)
                    continue
                if len(current_tag_content.split()) > 3:
                    text_tag_long_count = text_tag_long_count + 1
                    count_data_details['tl'].append(current_tag_content)
                    if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t TEXT LONG TAG:' + current_tag)
                else:
                    text_tag_short_count = text_tag_short_count + 1
                    count_data_details['ts'].append(current_tag_content)
                    if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t TEXT SHORT TAG:' + current_tag)
                    #print 'text tag('+ str(each_child) + ') short "' + str(data_from_tag_analysis[each_child][1]) + '"'
                continue
            if current_tag in ['a','area']:
                if each_child not in processed_indexes: processed_indexes.append(each_child)
                current_tag_all_childs=self.get_all_childs_and_tags(data_from_tag_analysis,each_child,depth_level=0)
                for each_item in current_tag_all_childs['all_childs']:
                    if each_item not in processed_indexes:
                        processed_indexes.append(each_item)
                current_tag_content=get_printable_string(self.support_tag_analysis_reduce_tag(data_from_tag_analysis,each_child),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
                current_tag_content=re.sub(' +',' ',current_tag_content)
                if len(current_tag_content.split()) > 3:
                    if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t ANCHOR LONG TAG:' + current_tag)
                    count_data_details['al'].append(current_tag_content)
                    a_tag_long_count = a_tag_long_count + 1
                else:
                    if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t ANCHOR SHORT TAG:' + current_tag)
                    count_data_details['as'].append(current_tag_content)
                    a_tag_short_count = a_tag_short_count + 1
                continue
            if current_tag in ['ul','ol']:
                if each_child not in processed_indexes: processed_indexes.append(each_child)
                list_tag_count = list_tag_count + 1
                if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t LIST TAG:' + current_tag)
                continue
            if current_tag in self.TAG_IMAGE:
                if each_child not in processed_indexes: processed_indexes.append(each_child)
                image_tag_count = image_tag_count + 1
                if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t IMAGE TAG:' + current_tag)
                continue
            #if each_child not in processed_indexes: processed_indexes.append(each_child)
            if len(current_tag_content) == 0: 
                length_of_child = length_of_child - 1
                if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t Empty TAG:' + current_tag)
                continue
            if len(current_tag_content.split()) > 3:
                if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t OTHER TEXT LONG TAG:' + current_tag)
                text_tag_long_count = text_tag_long_count + 1
                count_data_details['tl'].append(current_tag_content)
            else:
                if debug_mode: self._print_(print_prefix + 'Index:' + str(each_child) + '\t OTHER TEXT SHORT TAG:' + current_tag)
                count_data_details['ts'].append(current_tag_content)
                text_tag_short_count = text_tag_short_count + 1
                #print 'Other tag('+ str(each_child) + ') short "' + str(data_from_tag_analysis[each_child][1]) + '"'
        if debug_mode:
            self._print_(print_prefix + ' Count length_of_child=' +str(length_of_child))
            self._print_(print_prefix + ' Count text_tag_long_count=' +str(text_tag_long_count))
            self._print_(print_prefix + ' Count text_tag_short_count=' +str(text_tag_short_count))
            self._print_(print_prefix + ' Count a_tag_long_count=' +str(a_tag_long_count))
            self._print_(print_prefix + ' Count a_tag_short_count=' +str(a_tag_short_count))
            self._print_(print_prefix + ' Count list_tag_count=' +str(list_tag_count))
            self._print_(print_prefix + ' Count image_tag_count=' +str(image_tag_count))
            self._print_(print_prefix + ' Count processed_indexes=' +str(processed_indexes))
            self._print_(print_prefix + ' Count count_data_details=' +str(count_data_details))
        if a_tag_long_count+a_tag_short_count > 0:
            a_strength=''.join(count_data_details['as']) + ''.join(count_data_details['al'])
            t_strength=''.join(count_data_details['ts']) + ''.join(count_data_details['tl'])
            if list_tag_count > 0 and len(a_strength + t_strength ) * 0.5 <= len(a_strength):
                tag_group_type ='LL'##Concentrate
                if debug_mode: self._print_(print_prefix + 'Tag A; Tag L')
            elif text_tag_long_count+text_tag_short_count > 0:#What if there are more text and anchors
                if a_tag_long_count + text_tag_long_count > 2 or (a_tag_long_count+a_tag_short_count+text_tag_long_count+text_tag_short_count)>5:
                    if len(a_strength + t_strength ) * 0.25 >= len(a_strength):
                        if self.dissipated_cloud(count_data_details):
                            tag_group_type='DC'
                            if debug_mode: self._print_(print_prefix + 'Tag A; No L; More A and T with Limited A - Dissipated cloud of words')
                        else:
                            tag_group_type='LTS'
                            if debug_mode: self._print_(print_prefix + 'Tag A; No L; More A and T with Limited A')
                    else:
                        tag_group_type='LTL'
                        if debug_mode: self._print_(print_prefix + 'Tag A; No L; More A and T')
                else:
                    if len(a_strength + t_strength ) * 0.75 < len(a_strength):
                        tag_group_type='LTL'
                        if debug_mode: self._print_(print_prefix + 'Tag A; No L; Less A and T with Rich A')
                    elif a_tag_short_count >0  and len(a_strength + t_strength ) * 0.15 > len(a_strength) and a_tag_long_count < a_tag_short_count :
                        tag_group_type='TL'
                        if debug_mode: self._print_(print_prefix + 'Tag A; No L; Less A and T with Rich A')
                    else:
                        tag_group_type='LTS'
                        if debug_mode: self._print_(print_prefix + 'Tag A; No L; Less A(' + str(len(a_strength)) + ') and T(' + str(len(t_strength)) + '):' + str(len(a_strength)/(1.0 * len(a_strength + t_strength))))
            else:
                if a_tag_long_count + a_tag_short_count == 1:
                    if a_tag_long_count > 0 :
                        tag_group_type ='LL'
                        if debug_mode: self._print_(print_prefix + 'Tag A; No L; only Long A')
                    else:
                        tag_group_type='SL'
                        if debug_mode: self._print_(print_prefix + 'Tag A; No L; only Small A')
                else:
                    tag_group_type='AL'
                    if debug_mode: self._print_(print_prefix + 'Tag A; No L; More As')
        else:
            if list_tag_count >0:
                if text_tag_short_count+text_tag_long_count > 0 :
                    tag_group_type='LT'
                    if debug_mode: self._print_(print_prefix + 'No A; L Tag')
            elif text_tag_long_count+text_tag_short_count > 0:
                if debug_mode: self._print_(print_prefix + 'Texts')
                if text_tag_long_count+text_tag_short_count == 1:
                    if text_tag_long_count > 0 :
                        if debug_mode: self._print_(print_prefix + 'No A; No L; Only Long T')
                        tag_group_type='TL'
                    else:
                        if debug_mode: self._print_(print_prefix + 'No A; No L; Only small T')
                        tag_group_type='TS'
                else:
                    if text_tag_long_count <=1 and tag_group_type <= 3:
                        if debug_mode: self._print_(print_prefix + 'No A; No L; Less Ts')
                        tag_group_type='TL'
                    else:
                        if text_tag_long_count+text_tag_short_count > 3:
                            if self.dissipated_cloud(count_data_details):
                                tag_group_type='DC'
                                if debug_mode: self._print_(print_prefix + 'No A; No L; More Ts - Dissipated cloud of words')
                        if debug_mode: self._print_(print_prefix + 'No A; No L; More Ts')
                        tag_group_type='AT'
            elif image_tag_count >0 :
                if debug_mode: self._print_(print_prefix + 'Images')
                tag_group_type='IM'
            else:
                if debug_mode: self._print_(print_prefix + 'No scenario matched for tag_group_type')
                tag_group_type='EM'
        if debug_mode: self._print_(print_prefix + 'Dervied tag_group_type:' + tag_group_type)
        return tag_group_type
    def get_parent_child_relationship(self,data_from_tag_analysis):
        self.current_function_name='get_parent_child_relationship'
        if not data_from_tag_analysis or (not isinstance(data_from_tag_analysis,list)):
            self.current_function_name=''
            return False
        parent_child_details={}
        parent_child_details['0_p_a']=[]
        parent_child_details['-1_p_a']=[] # Default for top most
        for each_tag in data_from_tag_analysis:
            tag_index=each_tag[2]
            parent_tag_key_str=str(tag_index) + '_p'
            parent_tag_key_str_all=parent_tag_key_str + '_a'
            parent_index=each_tag[3]
            parent_child_details[tag_index]=[]
            parent_child_details[parent_tag_key_str]=parent_index
            #parent_child_details[parent_tag_key_str + '_a']=get_all_parents(parent_child_details.copy(),parent_index)
            parent_child_details[parent_tag_key_str_all]=[parent_index]
            for each_index in parent_child_details[str(parent_index) + '_p_a']:
                parent_child_details[parent_tag_key_str_all].append(each_index)
            if parent_index not in parent_child_details:
                parent_child_details[parent_index]=[]
            parent_child_details[parent_index].append(tag_index)
        self.current_function_name=''
        return parent_child_details
        
    def support_tag_analysis_has_child_tag_of_type(self,data_tag_analysis,index,tag_to_search,type=None,reduce_tag_depth=0):
        #self.current_function_name='support_tag_analysis_has_child_tag_of_type'
        replace_tag_by={
            'br':'\n'
            ,'p':'\n'
            ,'span':' '
            ,'h1':'\n'
            ,'h2':'\n'
            ,'h3':'\n'
            ,'h4':'\n'
            ,'h5':'\n'
            ,'h6':'\n'
            ,'section':'\n'
            ,'td':' '
            ,'tr':'\n'
            ,'div':'\n'
        }
        reduce_tag_depth += 1
        if self.developer_mode and reduce_tag_depth == 1: self._print_('\nSTART')
        if self.developer_mode: self._print_('support_tag_analysis_has_child_tag_of_type:d-level=' + str(reduce_tag_depth) + '.index=' + str(index) + '\ttype=' + str(type))
        if (not isinstance(data_tag_analysis,dict)) or index not in data_tag_analysis: 
            if self.developer_mode: self._print_('support_tag_analysis_has_child_tag_of_type: not dictionary or index not found' + str(index))
            return ''
        result_content=''
        child_tags=data_tag_analysis[index][3]
        tag_name=data_tag_analysis[index][0]
        if reduce_tag_depth > 1 and tag_name == tag_to_search: return True
        if self.developer_mode: self._print_('support_tag_analysis_has_child_tag_of_type:index=' + str(index) + '\ttag_name=' + tag_name)
        processed_index=[]
        if child_tags:
            for each_child in child_tags:
                if each_child > index:
                    if each_child in processed_index: continue
                    if self.developer_mode: self._print_('support_tag_analysis_has_child_tag_of_type: recursive call: index,child index' + str(index) + each_child)
                    result_content = support_tag_analysis_has_child_tag_of_type(data_tag_analysis,each_child,tag_to_search,type,reduce_tag_depth)
                    if result_content: return True
                else:
                    return False
        return False
    def find_date_for_news(self,all_tags_details,current_index,common_parent=0,developer_mode=False):
        #developer_mode=developer_mode
        if 'find_date_for_news' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if self.developer_mode: self._print_( 'find_date_for_news:given index' + str(current_index) + ' . Common Parent:' + str(common_parent))
        if current_index not in all_tags_details:
            if self.developer_mode: self._print_( 'find_date_for_news:given index=common_parent' + str(current_index) + ' is not in all_tags_details')
            return False
        if common_parent>0 and common_parent not in all_tags_details:
            if self.developer_mode: self._print_( 'find_date_for_news:given index' + str(current_index) + ':common_parent=' + str(common_parent) + ' is not in all_tags_details')
            return False
        if self.developer_mode: self._print_( 'find_date_for_news: index details for ' + str(current_index) + ' is=' + str(all_tags_details[current_index]))
        processed_index=[]
        processed_index.append(current_index)
        selected_string=''
        child_parents_are=all_tags_details[current_index][4]
        parent_count=0
        if child_parents_are:
            for each_parent in child_parents_are:
                parent_count += 1
                if each_parent == current_index or each_parent <= common_parent or each_parent in processed_index: continue
                if common_parent == 0 and parent_count > 3: break
                parent_details=self.support_tag_analysis_reduce_tag(all_tags_details,each_parent,processed_index,type='news')
                parent_details=parent_details.strip(' \n\r\t')
                parent_details=re.sub(r'\n+','\n',parent_details) #added to break when parent with large section is encountered
                if debug_mode: self._print_( 'find_date_for_news:given index' + str(current_index) + ':Processing Parent(' + str(parent_count) + ')' + str(each_parent) + ' Content=' + str(parent_details),skip_timestamp=True)
                if parent_details:
                    for each_line in parent_details.split('\n'):
                        is_there_a_date=get_smell_like_date_from_text(each_line,strict_year=False,consume_month_year=False)
                        if is_there_a_date:
                            if is_there_a_date[0]>0:
                                if debug_mode: self._print_( 'find_date_for_news:given index' + str(current_index) + ':date found for parent' + str(each_parent) + ' detail='  + str(is_there_a_date),skip_timestamp=True)
                                if is_there_a_date[1] <= get_current_date(format='date'):
                                    if debug_mode: self._print_( 'find_date_for_news:given index' + str(current_index) + ':return date is' + str(is_there_a_date),skip_timestamp=True)
                                    return is_there_a_date[1]
                                else:
                                    if debug_mode: self._print_('find_date_for_news:given index' + str(current_index) + ':date is greater than current date: given date=' + str(is_there_a_date),skip_timestamp=True)
                if len(parent_details.split('\n')) > 20: 
                    if debug_mode: self._print_( 'find_date_for_news:given index' + str(current_index) + ':breaking for large data:' + str(parent_details),skip_timestamp=True)
                    break #added to break when parent with large section is encountered
                processed_index.append(each_parent)
        if self.developer_mode: self._print_('find_date_for_news:return No date found')
        return False
    def support_tag_analysis_reduce_tag(self,data_tag_analysis,index,already_processed_index=None,type=None,reduce_tag_depth=0,process_anchors=True,ignore_image=True):
        #self.current_function_name='support_tag_analysis_reduce_tag'
        replace_tag_by={
            'br':'\n'
            ,'p':'\n'
            ,'span':' '
            ,'h1':'\n'
            ,'h2':'\n'
            ,'h3':'\n'
            ,'h4':'\n'
            ,'h5':'\n'
            ,'h6':'\n'
            ,'section':'\n'
            ,'td':' '
            ,'tr':'\n'
            ,'div':'\n'
            ,'li':'\n' #Version 1.9
            ,'address':'\n' #Has address. It is block
            ,'a':' ' #critical one. will introduce disruptance
        }
        if 'support_tag_analysis_reduce_tag' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        print_prefix='support_tag_analysis_reduce_tag:d-level=' + str(reduce_tag_depth)  +  ':'
        reduce_tag_depth += 1
        if reduce_tag_depth > 50: return ''
        if debug_mode and reduce_tag_depth == 1: self._print_(print_prefix + 'START with ' + 'process_anchors=' + str(process_anchors) + ' & ignore_image=' + str(ignore_image))
        if debug_mode: self._print_(print_prefix + '.index=' + str(index) + '\talready_processed_index=' + str(already_processed_index) + '\ttype=' + str(type))
        if (not isinstance(data_tag_analysis,dict)) or index not in data_tag_analysis: 
            if debug_mode: self._print_(print_prefix + ' not dictionary or index not found' + str(index))
            return ''
        result_content=''
        child_tags=data_tag_analysis[index][3]
        content_value=data_tag_analysis[index][1]
        tag_name=data_tag_analysis[index][0]
        if debug_mode:
            self._print_(print_prefix + ' tag_name=' + tag_name + '\t' +'content_value=' + str(content_value))
        if (not process_anchors) and tag_name in ['a']:
            if debug_mode: self._print_(print_prefix + 'process_anchors is disabled and current tag is ' + tag_name)
            return ''
        if ignore_image and tag_name in self.TAG_PICTURE: #,'img'
            if debug_mode: self._print_(print_prefix + 'Image tag is ignored. Image tag:' + tag_name)
            return ''
        if tag_name in replace_tag_by:
            result_content=replace_tag_by[tag_name]
        else:
            result_content=''
        result_content=result_content + content_value
        if debug_mode: self._print_(print_prefix + ' index=' + str(index) + '\ttag_name='  + str(tag_name) +'\t result_content' + result_content + '\t content_value=' + content_value)
        processed_index=[]
        if already_processed_index:#Removed condition type == 'news' and  in 1.15
            for each_index in already_processed_index:
                processed_index.append(each_index)
        if child_tags:
            for each_child in child_tags:
                if each_child > index:
                    if each_child in processed_index: 
                        continue
                    if debug_mode: self._print_(print_prefix + ' recursive call: index,child index = ' + str(index) + ',' + str(each_child),skip_timestamp=True)
                    result_content = result_content + self.support_tag_analysis_reduce_tag(data_tag_analysis,each_child,processed_index,type,reduce_tag_depth,process_anchors=process_anchors)
                else:
                    if debug_mode: self._print_(print_prefix + 'Child is less than parent. should not reach end' + str(index))
                    return result_content#.strip(' \n\r\t')
            return result_content#.strip(' \n\r\t')
        else:
            if reduce_tag_depth == 0:
                print result_content, ' at reduce_tag_depth==0'
            return result_content#.strip(' \n\r\t')
        if debug_mode: self._print_(print_prefix + ' should not reach end' + str(index))
    def is_new_parent_has_current_parent(self,list_of_list_of_integers,current_parent,new_parent,developer_mode=False):
        #self.current_function_name='is_new_parent_has_current_parent'
        if not isinstance(list_of_list_of_integers,list): return False
        current_parent_encountered=False
        for each_list in list_of_list_of_integers:
            if new_parent in each_list:
                current_parent_encountered=True
                if current_parent not in each_list:
                    if self.developer_mode: self._print_('is_new_parent_has_current_parent:current_parent=' + str(current_parent) + ' not found in ' + str(each_list))
                    return False
        if not current_parent_encountered:
            if self.developer_mode: self._print_('is_new_parent_has_current_parent:new_parent=' + str(current_parent) + ' not found in ' + str(list_of_list_of_integers))
        return current_parent_encountered
    def get_common_parent_in_html(self,list_of_list_of_integers,grand_parent_index=0,developer_mode=False,minimum_childs=0):
        if 'get_common_parent_in_html' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        self.current_function_name='get_common_parent_in_html - pre'
        print_prefix='get_common_parent_in_html:\t'
        if self.TRACK_TIME_MODE or developer_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ':Start')
        if not isinstance(list_of_list_of_integers,list): 
            self._print_(print_prefix + log_time_stamp() + '\t' + ':list_of_list_of_integers is not list type,type=' + str(type(list_of_list_of_integers)))
            exit()
            return False
        max_count_length=0
        high_index=0
        high_count_selected=0
        high_value_count_dict={}
        no_of_childs=len(list_of_list_of_integers)
        if self.developer_mode: self._print_(print_prefix + 'grand_parent_index = ' + str(grand_parent_index) + ',no_of_childs=' + str(no_of_childs))
        if grand_parent_index <= 0 and no_of_childs<=2 : 
            return -1
        if grand_parent_index>0 and no_of_childs<2 : 
            return -1
        if self.TRACK_TIME_MODE or developer_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ':Finding occurrence for each index')
        for each_list in list_of_list_of_integers:
            if grand_parent_index >0 and grand_parent_index not in each_list: return -2
            for each_index in each_list:
                if each_index>1:
                    high_value_count_dict[each_index]=high_value_count_dict.get(each_index,0)+1
                    if debug_mode: self._print_(print_prefix + 'Occurence for index (' + str(each_index) + ') is ' + str(high_value_count_dict[each_index]))
        self.current_function_name='get_common_parent_in_html'
        if self.developer_mode: self._print_(print_prefix + 'high_value_count_dict - ' + str(high_value_count_dict))
        #The below code will find lowest index with maximum occurrence
        #Also create dictionary with count of occurrence  
        high_value_count_population_dict={}
        distinct_counts=[]
        if self.TRACK_TIME_MODE or developer_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ':Finding distribution based on occurrence')
        for each_index in high_value_count_dict:
            curr_count=high_value_count_dict[each_index]
            if grand_parent_index <= 0 and curr_count <= 2: continue# for search with no grand parent 
            if grand_parent_index > 0 and curr_count <= 1: continue# for the search with grand parent. so a parent can have two children alone while grandparent should have more than 2 children
            if curr_count not in distinct_counts: distinct_counts.append(curr_count)
            #high_value_count_population_dict[curr_count]=high_value_count_population_dict.get(curr_count,0)+1
            if curr_count not in high_value_count_population_dict:
                high_value_count_population_dict[curr_count]=[]
            high_value_count_population_dict[curr_count].append(each_index)
        if self.developer_mode: self._print_(print_prefix + 'high_value_count_population_dict - ' + str(high_value_count_population_dict))
        parent_depth=0
        if self.TRACK_TIME_MODE or developer_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ':Selecting the common parent')
        for each_high_count in list(reversed(sorted(distinct_counts))):
            if each_high_count < (no_of_childs * 1.0/5): continue
            if minimum_childs>0 and each_high_count < minimum_childs: continue
            if debug_mode: self._print_(print_prefix + 'processing count : ' + str(each_high_count))
            curr_index_list=high_value_count_population_dict[each_high_count]
            curr_high_index=list(reversed(sorted(curr_index_list)))[0]
            if debug_mode: self._print_(print_prefix + 'processing count : '+ str(each_high_count) + '\tcurr_high_index=' + str(curr_high_index) + '\thigh_index=' + str(high_index),skip_timestamp=True)
            if grand_parent_index > 0 and curr_high_index <= grand_parent_index: continue
            curr_count_length=len(curr_index_list)
            if debug_mode: self._print_(print_prefix + 'processing count : ' + str(each_high_count) + '\tcurr_high_index=' + str(curr_high_index) + '\thigh_index=' + str(high_index) + '\tcurr_count_length=' + str(curr_count_length) + '\tmax_count_length=' + str(max_count_length),skip_timestamp=True)
            if grand_parent_index > 0 and curr_count_length < no_of_childs: continue
            #New logic starts from here
            parent_depth += 1
            if max_count_length == 0: #First iteration i.e., max count of the list
                if  debug_mode: self._print_(print_prefix + 'processing count : max_count_length=0' + str(max_count_length) + ' . curr_count_length=' + str(curr_count_length),skip_timestamp=True)
                max_count_length = curr_count_length
                high_index=curr_high_index
                #high_count_selected=each_high_count
            elif max_count_length>0 and self.is_new_parent_has_current_parent(list_of_list_of_integers,high_index,curr_high_index,developer_mode=developer_mode):
                if  debug_mode: self._print_(print_prefix + ' is_new_parent_has_current_parent=True for current_parent=' + str(high_index) + '. new_parent=' + str(curr_high_index),skip_timestamp=True)
                max_count_length = curr_count_length
                high_index=curr_high_index
                #high_count_selected=each_high_count
            #Blocking the below section for new logic--i.e, curr_count_length will not be compared with max_count_length
            '''
            if curr_count_length > max_count_length:
                if self.developer_mode: self._print_('get_common_parent_in_html:processing count : curr_count_length & max_count_length=',curr_count_length,'>',max_count_length
                max_count_length = curr_count_length
                high_index=curr_high_index
                high_count_selected=each_high_count
            elif curr_count_length == max_count_length:
                if self.developer_mode: self._print_('get_common_parent_in_html:processing count : curr_count_length & max_count_length=',curr_count_length,'==',max_count_length
                if curr_high_index > high_index:
                    if self.developer_mode: self._print_('get_common_parent_in_html:processing count curr_high_index & high_index: ',curr_high_index,'>',high_index
                    high_index=curr_high_index
                    high_count_selected=each_high_count
            '''
            #END Blocking the below section for new logic--i.e, curr_count_length will not be compared with max_count_length
        if self.developer_mode: self._print_(print_prefix + 'Common Parent : ' + str(high_index))
        if self.TRACK_TIME_MODE or developer_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ':Completed')
        self.current_function_name=''
        return high_index
    def get_base_href(self,content):#temp function to be deleted
        #self.current_function_name='get_base_href'
        if len(content)<=10: return False
        formatted_output=re.sub(r'(</\w+>)',r'\n\1\n',content)
        formatted_output=re.sub(r'(/>)',r'\1\n',formatted_output)
        formatted_output=re.sub(r'\n\n',r'\n',formatted_output)
        for each_line in formatted_output.split('\n'):
            if 'base' in each_line.lower():
                base_detail= self.get_html_tag_properties(each_line)
                if base_detail:
                    if 'current_tag_name' in base_detail and 'href' in base_detail:
                        if 'base' == base_detail['current_tag_name']:
                            return base_detail['href']
        return False
    def get_tag_analysis_from_html_content(self,url_path,html_content_in=None,use_selenium=False,process_menu=False,remove_header=True,remove_footer=True,developer_mode=False,use_head=False,tags_to_collect=None):
        self.current_function_name='get_tag_analysis_from_html_content - pre'
        CONTAINER_TAGS=['body','div','table','td','tr','h1','h2','h3','h4','h5','h6','p','a','span','area','ol','ul','li','article','section','figure','svg']#ul,li are added 1.5 figure # svg to ignore the whole content
        BLOCK_TAGS=['div','table','p','ul','article']#does not allow text tags
        TEXT_ONLY_TAGS=['p']#can not be in text tags
        if not use_head:
            COLLECT_TAGS=['table','a','area','base']
        else:
            COLLECT_TAGS=['meta','title','base','link']
        if tags_to_collect:
            for each_tag in tags_to_collect:
                if each_tag not in COLLECT_TAGS:
                    COLLECT_TAGS.append(each_tag)
        print_prefix='get_tag_analysis_from_html_content:\t'
        if 'get_tag_analysis_from_html_content' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
            self._print_(print_prefix + ' Start:' + url_path)
        else:
            debug_mode=False
        container_list=[]#[(tag , its position)]
        collected_tags=[]
        collect_links_details={}
        collected_links=[]
        if not url_path:
            self._print_(print_prefix + log_time_stamp() + '\t' + 'url_path is not provided')
            return ''
            exit()
        if html_content_in:
            html_content=html_content_in
            if debug_mode:
                self._print_(print_prefix + 'HTML content passed with length=' + str(len(html_content_in)))
        else:
            if use_selenium:
                html_content=get_url_page_source_via_selenium(url_path)
                if debug_mode:
                    self._print_(print_prefix + 'Fetching using selenium')
            else:
                if debug_mode:
                    self._print_(print_prefix + 'Fetching using fetch_for_url with file_only_mode=' + str(self.work_offline))
                html_content=fetch_for_url(url_path,file_only_mode=self.work_offline)
        if not html_content: 
            if self.developer_mode or debug_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ' No html_content')
            return collect_links_details
        if not is_html_doc(html_content):
            if self.developer_mode or debug_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ' Not a html document')
            return collect_links_details
        self.current_function_name='get_tag_analysis_from_html_content'
        if use_head:
            formatted_output_temp=self.get_html_head(self.remove_unhealthy_tags(html_content,remove_header=remove_header,remove_footer=remove_footer))
            formatted_head_content=formatted_output_temp
        else:
            formatted_output_temp=self.html_massage(self.remove_unhealthy_tags(html_content,remove_header=remove_header,remove_footer=remove_footer))
            formatted_head_content=self.get_html_head(self.remove_unhealthy_tags(html_content,remove_header=remove_header,remove_footer=remove_footer))
        base_url=self.get_base_href(formatted_head_content)
        #print html_content
        if not base_url:
            base_url=url_path
        if not process_menu: 
            formatted_output=self.remove_menu_like_section(formatted_output_temp)
        else:
            formatted_output=formatted_output_temp
        if (not formatted_output) and formatted_output_temp:
            self._print_(print_prefix + log_time_stamp() + '\t' + ' content is empty after remove_menu_like_section')
            return ''
            exit()
        formatted_output=re.sub(r'(</\w+>)',r'\n\1\n',formatted_output)
        formatted_output=re.sub(r'(/>)',r'\1\n',formatted_output)
        formatted_output=re.sub(r'\n\n',r'\n',formatted_output)
        line_index=0
        no_value_tags=0
        tag_index=1
        container_list.append(('html',-1))
        container_list.append(('body',0))
        if self.TRACK_TIME_MODE or self.developer_mode: self._print_(print_prefix + log_time_stamp() + '\t' + 'Processing the content')
        for each_line in formatted_output.split('\n'):
            printable_each_line=get_printable_string(each_line)
            printable_each_line=printable_each_line.strip('\n')#Space Removed
            if (not printable_each_line) or  len(printable_each_line) == 0:
                if debug_mode : self._print_(print_prefix + log_time_stamp() + '\t' + 'Empty Line - Ignoring:' + printable_each_line ,skip_timestamp=True)
                continue
            if  debug_mode: self._print_(print_prefix + log_time_stamp() + '\t' + 'PROCESSING LINE:' + printable_each_line ,skip_timestamp=True)
            tag_details=self.get_html_tag_properties(each_line)
            if  debug_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ':tag_details:' + str(tag_details),skip_timestamp=True)
            if (not tag_details):
                if  debug_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ': no tag_details',skip_timestamp=True)
                closing_tag=self.is_closing_tag(each_line.strip())
                if closing_tag:
                    tag_index += 1
                    if  debug_mode: self._print_(print_prefix  + log_time_stamp() + str(tag_index)+ '\t Closing tag (' + closing_tag + ') in ' + '.' + printable_each_line + '\t' + str(tag_details),skip_timestamp=True)
                    if closing_tag in CONTAINER_TAGS and len(container_list)>0:
                        if closing_tag == container_list[-1:][0][0]:
                            if debug_mode: self._print_(print_prefix  + log_time_stamp() + str(tag_index) + '\t Removing tag (' + container_list[-1:][0][0] +') from container_list for Closing tag (' + closing_tag + ')')
                            container_list.pop()
                        else:
                            if  debug_mode: self._print_(print_prefix + log_time_stamp() + '\t' + 'How to handle - end block tag with not matching start' + str(closing_tag) + str(container_list[-1:][0]),skip_timestamp=True)
                    elif debug_mode:
                        self._print_(print_prefix + str(tag_index) + log_time_stamp() + '\t No action for Closing tag (' + closing_tag + ')')
                else:
                    if  debug_mode: self._print_(print_prefix + log_time_stamp() + '\t' + ' How to handle - not a tag and not a end tag' + printable_each_line,skip_timestamp=True)
                    collected_tags.append(('',each_line,tag_index,container_list[-1:][0][1],{}))
                    tag_index += 1
                if  debug_mode: self._print_(print_prefix + str(tag_index) + '.' + str(container_list) + '\t\t\t' + str(tag_details),skip_timestamp=True)
                if  debug_mode: self._print_(print_prefix + str(tag_index) + '.' + str(container_list[-8:]),skip_timestamp=True)
                if  debug_mode and len(collected_tags) > 0: self._print_(print_prefix + '\tOUTPUT:Closing tag:' + str(closing_tag) + '\tIndex:' + str(collected_tags[-1:][0][2]) + '\tParent Index:' + str(collected_tags[-1:][0][3]),skip_timestamp=True)
                continue
            elif tag_details:
                if 'current_tag_name' in tag_details:
                    if 'closing tags' in tag_details:
                        if tag_details['closing tags']:
                            if debug_mode: self._print_(print_prefix + log_time_stamp() + '\t' + 'inside closing_tags with ClosingTag with current_tag_name',skip_timestamp=True)
                            if tag_details['closing tags'][0] == tag_details['current_tag_name']:
                                collected_tags.append((tag_details['current_tag_name'].lower(),'',tag_index,container_list[-1:][0][1],tag_details))#Adding tag_details[4 use_head] for this line which is missing
                                tag_index += 1
                            else:
                                if  debug_mode: self._print_(print_prefix + log_time_stamp()  + 'How to handle this start and end tags are not matching- ' + printable_each_line,skip_timestamp=True)
                        else:
                            if debug_mode: self._print_(print_prefix + log_time_stamp() + '\t' + 'inside closing_tags with NoClosingTag with current_tag_name',skip_timestamp=True)
                            if tag_details['current_tag_name'].lower() in CONTAINER_TAGS:
                                #Moving collect_tag addition to after TEXT_ONLY_TAGS removal
                                if debug_mode: self._print_(print_prefix + 'Current tag(' + tag_details['current_tag_name'] + ') is CONTAINER_TAGS' + '\t Container List length:' + str(len(container_list)))
                                if tag_details['current_tag_name'] in BLOCK_TAGS:#UNBALANCING
                                    if debug_mode: self._print_(print_prefix + 'Current tag(' + tag_details['current_tag_name'] + ') is CONTAINER_TAGS and BLOCK_TAGS' + '\t Container List length:' + str(len(container_list)))
                                    while container_list[-1:][0][0] in TEXT_ONLY_TAGS and len(container_list)>1:
                                        if debug_mode: self._print_(print_prefix + 'TEXT_ONLY_TAGS(' + container_list[-1:][0][0] + ') as parent for BLOCK_TAGS(' + tag_details['current_tag_name'] + ')')
                                        if debug_mode: self._print_(print_prefix + 'Current Parent Details : ' + str(container_list[-1:]))
                                        container_list.pop()
                                        if debug_mode: self._print_(print_prefix + 'Now the parent is ' + container_list[-1:][0][0] + '\t Container List length:' + str(len(container_list)))
                                        if debug_mode: self._print_(print_prefix + 'Current Parent Details : ' + str(container_list[-1:]))
                                collected_tags.append((tag_details['current_tag_name'].lower(),tag_details['tag_content_value'],tag_index,container_list[-1:][0][1],tag_details))
                                container_list.append((tag_details['current_tag_name'].lower(),tag_index))
                                tag_index += 1
                            else:
                                collected_tags.append((tag_details['current_tag_name'].lower(),tag_details['tag_content_value'],tag_index,container_list[-1:][0][1],tag_details))
                                tag_index += 1
                    else:
                        if  debug_mode: self._print_(print_prefix + log_time_stamp() + 'inside no closing_tags with current_tag_name',skip_timestamp=True)
                        if tag_details['current_tag_name'].lower() in CONTAINER_TAGS:
                            #Moving collect_tag addition to after TEXT_ONLY_TAGS removal
                            if tag_details['current_tag_name'] in BLOCK_TAGS:#UNBALANCING
                                if debug_mode: self._print_(print_prefix + 'Current tag(' + tag_details['current_tag_name'] + ') is CONTAINER_TAGS and BLOCK_TAGS' + '\t Container List length:' + str(len(container_list)))
                                while container_list[-1:][0][0] in TEXT_ONLY_TAGS and len(container_list)>1: 
                                    if debug_mode: self._print_(print_prefix + 'TEXT_ONLY_TAGS(' + container_list[-1:][0][0] + ') as parent for BLOCK_TAGS(' + tag_details['current_tag_name'] + ')')
                                    if debug_mode: self._print_(print_prefix + 'Current Parent Details : ' + str(container_list[-1:]))
                                    container_list.pop()
                                    if debug_mode: self._print_(print_prefix + 'Now the parent is ' + container_list[-1:][0][0] + '\t Container List length:' + str(len(container_list)))
                                    if debug_mode: self._print_(print_prefix + 'Current Parent Details : ' + str(container_list[-1:]))
                            collected_tags.append((tag_details['current_tag_name'].lower(),tag_details['tag_content_value'],tag_index,container_list[-1:][0][1],tag_details))
                            container_list.append((tag_details['current_tag_name'].lower(),tag_index))
                            tag_index += 1
                else:
                    if  debug_mode: self._print_(print_prefix + log_time_stamp()  + 'text only line' + printable_each_line,skip_timestamp=True)
                    if  debug_mode: self._print_(print_prefix + str(tag_index) + '.' + str(container_list) + '\t\t\t' + str(tag_details),skip_timestamp=True)
                    if  debug_mode: self._print_(print_prefix + str(tag_index) + '.' + str(container_list[-8:]),skip_timestamp=True)
                    if  debug_mode and len(collected_tags) > 0: self._print_(print_prefix + '\t\tOUTPUT:' + '\tIndex:' + str(collected_tags[-1:][0][2]) + '\tParent Index:' + str(collected_tags[-1:][0][3]),skip_timestamp=True)
                    collected_tags.append(('',each_line,tag_index,container_list[-1:][0][1],tag_details))
                    tag_index += 1
                    continue
            if  debug_mode and len(collected_tags) > 0: self._print_(print_prefix + log_time_stamp() + '\t' + '\t\tOUTPUT:current tag:' + str(tag_details['current_tag_name']) + '\tIndex:' + str(collected_tags[-1:][0][2]) + '\tParent Index:' + str(collected_tags[-1:][0][3]),skip_timestamp=True)
            if  debug_mode: self._print_(print_prefix + 'EOL stats\t' + str(tag_index) + '.' + str(container_list) + '\t\t\t' + str(tag_details),skip_timestamp=True)
            if  debug_mode: self._print_(print_prefix + 'EOL stats\t' + str(tag_index) + '.' + str(container_list[-8:]) + '\n',skip_timestamp=True)
        if self.TRACK_TIME_MODE or developer_mode: self._print_(print_prefix + log_time_stamp() + '\t' + 'get parent child relationship')
        parent_child_details=self.get_parent_child_relationship(collected_tags)
        if self.TRACK_TIME_MODE or developer_mode: self._print_(print_prefix + log_time_stamp() + '\t' + 'completed parent child relationship')
        result_master_tag_dictionary={}
        for collect_tag in COLLECT_TAGS:
            result_master_tag_dictionary[collect_tag]=[]
        for each_tag in collected_tags:
            t_tag=each_tag[0]
            t_value=each_tag[1]
            t_index=each_tag[2]
            t_p_index=each_tag[3]
            t_info=each_tag[4]
            if len(t_tag)>0:
                if t_tag in result_master_tag_dictionary:
                    result_master_tag_dictionary[t_tag].append(t_index)
            if 'href' in t_info:
                t_href=t_info['href']
            else:
                t_href=''
            if 'class' in t_info:
                t_class=t_info['class']
            else:
                t_class=''
            if t_index in parent_child_details:
                t_childs=parent_child_details[t_index]
            else:
                t_childs=[]
            if str(t_index) + '_p_a' in parent_child_details:
                t_parents=parent_child_details[str(t_index) + '_p_a']
            else:
                t_parents=[]
            result_master_tag_dictionary[t_index]=[t_tag,t_value,t_p_index,t_childs,t_parents,t_href,t_class,t_index,t_info,what_is_the_object_type(t_value)]#added tag at the end #Tuple to List
        result_master_tag_dictionary['base_url']=['base','',0,[],[],base_url,'',0,{}]#added tag at the end #Tuple to List
        if self.TRACK_TIME_MODE or developer_mode: self._print_(print_prefix + log_time_stamp() + '\t' + 'completed processing the content')
        self.current_function_name=''
        #self.remove_empty_tags_from_analysis(result_master_tag_dictionary)
        #return result_master_tag_dictionary #INDEX=(TAGNAME, TAGTEXT,PARENT_INDEX,ALL_CHILDS,ALL_PARENTS,HREF,CLASS,INDEX,TAG_INFO)
        return self.remove_empty_tags_from_analysis(result_master_tag_dictionary)
    def remove_empty_tags_from_analysis(self,data_tag_analysis):
        #http://www.augsburgfortress.org copyright is not fetched due to text only tag PENDING
        empty_tag_list=[]
        print_prefix='remove_empty_tags_from_analysis:\t'
        if 'remove_empty_tags_from_analysis' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
            self._print_(print_prefix + ' Start')
        else:
            debug_mode=False
        result_tag_analysis=copy.deepcopy(data_tag_analysis)
        if not data_tag_analysis:
            return result_tag_analysis
        for each_tag in result_tag_analysis:
            if isinstance(each_tag,int):
                if len(result_tag_analysis[each_tag][0]) == 0 and (not result_tag_analysis[each_tag][3]) and each_tag in result_tag_analysis:
                    if len(result_tag_analysis[each_tag][1].strip()) > 0:
                        if debug_mode: self._print_(print_prefix + str(each_tag) +  ': Text only tag :details - ' + str(result_tag_analysis[each_tag]))
                        continue
                    if debug_mode: self._print_(print_prefix + str(each_tag) +  ': Empty tag :details - ' + str(result_tag_analysis[each_tag]))
                    if result_tag_analysis[each_tag][2] in result_tag_analysis:
                        result_tag_analysis[result_tag_analysis[each_tag][2]][3].remove(each_tag)
                        empty_tag_list.append(each_tag)
                else:
                    if debug_mode: self._print_(print_prefix + str(each_tag) + ':Not an empty tag:details - ' + str(result_tag_analysis[each_tag]))
            else:
                if debug_mode: self._print_(print_prefix + str(each_tag) + ':Collection index')
        for each_tag in empty_tag_list:
            result_tag_analysis.pop(each_tag,None)#Remove the empty tag
        return result_tag_analysis
    def get_text_content_from_html(self,url_path,html_content_in=None,use_selenium=False,remove_header=True,remove_footer=True,format='str'):#ALREADY A FUNCTION IS THERE IN HTML
        #https://www.adventisthealth.org/pages/news/newssearchresult.aspx?primaryorgunitid=2&amp;searchvisibility=public
        #https://www.adventisthealth.org/Pages/Doctors.aspx --date was not fetched
        #self.current_function_name='get_text_content_from_html'
        content_collected=[]
        content_collected[:]=[]
        if format.lower() not in ['str','list']: format='str' #Tuple to list () to []
        format=format.lower()
        if html_content_in:
            html_content=html_content_in
        else:
            if use_selenium:
                html_content=get_url_page_source_via_selenium(url_path)
            else:
                html_content=fetch_for_url(url_path,file_only_mode=self.work_offline)
        if not html_content: return content_collected
        if not is_html_doc(html_content): return content_collected
        formatted_output=html_massage(remove_unhealthy_tags(html_content,remove_header=remove_header,remove_footer=remove_footer))
        MINIMUM_WORDS_TO_SELECT_LINK=5
        line_index=0
        no_value_tags=0
        MAX_NO_VALUE_TAGS=5
        MAX_TAGS_WITHIN_A=5
        no_of_tags_within_a=0
        unclosed_a_tag_found=False
        tag_name_is=''
        href_is=''
        tag_content_value_is=''
        link_type_is=''
        for each_line in formatted_output.split('\n'):
            tag_details=get_html_tag_properties(each_line)
            if tag_details:
                if 'tag_content_value' not in tag_details: continue
                if len(tag_details['tag_content_value'])>2: line_index += 1
                if 'current_tag_name' in tag_details and 'tag_content_value' in tag_details:
                    if self.developer_mode: self._print_('Current Line:' + each_line + '\nBefore value:\t' + str(tag_details['tag_content_value']) + '\nAfter value:\t' + str(replace_selected_html(tag_details['tag_content_value'])))
                    content_collected.append(get_printable_string(tag_details['tag_content_value']))
            else:
                if self.developer_mode: self._print_('Current Line No Tag:' + each_line)
        if not content_collected: return ''
        #if content_collected_formatted: content_collected = content_collected_formatted
        if format == 'str':
            return '\n'.join(content_collected)
        return content_collected
    def remove_menu_like_section(self,html_content_in):
        self.current_function_name='remove_menu_like_section - pre'
        if not html_content_in: return []
        if not (isinstance(html_content_in,str) or isinstance(html_content_in,unicode)):
            self._print_('remove_menu_like_section: The input should of str or unicode type.....')
            exit()
        if 'remove_menu_like_section' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        content_collected=[]
        content_collected[:]=[]
        developer_mode=False
        html_content=html_content_in
        if not html_content: return content_collected
        self.current_function_name='remove_menu_like_section'
        formatted_output=self.split_on_end_tags(html_content)
        line_index=0
        tag_name_is=''
        href_is=''
        tag_content_value_is=''
        valid_menu_like_tags=['a','li','ul','p','div','span']#,'img']
        temp_collection_for_menu_like=[]
        temp_collection_for_menu_like[:]=[]
        menu_like_tags_stock=[]
        menu_like_tags_stock[:]=[]
        menu_like_tags_pattern=[]
        menu_like_tags_pattern[:]=[]
        menu_collection_started=False
        link_type_is=''
        formatted_output_split=formatted_output.split('\n')
        formatted_output_split_length=len(formatted_output_split)
        weightage_of_words=[0,0,0,0,0,0,0]#number of content tags,1 or 2 words, 3 to 15 words,15 + words,# of valid_menu_like_tags,# of not valid_menu_like_tags
        if self.developer_mode: self._print_('remove_menu_like_section - Length of the content:' + str(formatted_output_split_length))
        for each_line in formatted_output_split:
            if (not each_line) or len(each_line) < 1: continue
            line_index += 1
            tag_details=self.get_html_tag_properties(each_line)
            if  debug_mode: self._print_( 'Start of :'+ str(line_index) + 'content_collected len:' + str(len(content_collected)) + '\t' + str(menu_collection_started) + '\t' + str(menu_like_tags_stock) + '\tInput\t:' + repr(each_line),skip_timestamp=True)
            if tag_details:
                if 'current_tag_name' in tag_details and 'tag_content_value' in tag_details and 'find method' not in tag_details:
                    tag_content_value=str(tag_details['tag_content_value']).strip().strip("'")
                    current_tag_name=tag_details['current_tag_name']
                    if menu_collection_started:
                        if current_tag_name in valid_menu_like_tags:
                            temp_collection_for_menu_like.append(each_line)
                            weightage_of_words[4] +=1
                            if tag_content_value:
                                menu_like_tags_pattern.append((current_tag_name,len(tag_content_value),len(tag_content_value.split()),line_index,tag_content_value))
                            else:
                                menu_like_tags_pattern.append((current_tag_name,0,0))
                            if 'closing tags' in tag_details:
                                if current_tag_name in tag_details['closing tags']:
                                    pass # self closing 
                                else:
                                    menu_like_tags_stock.append(current_tag_name)
                        else:
                            temp_collection_for_menu_like.append(each_line)
                            weightage_of_words[5] +=1
                            if tag_content_value:
                                menu_like_tags_pattern.append((current_tag_name,len(tag_content_value),len(tag_content_value.split()),line_index,tag_content_value))
                            else:
                                menu_like_tags_pattern.append((current_tag_name,0,0))
                            if 'closing tags' in tag_details:
                                if current_tag_name in tag_details['closing tags']:
                                    pass # self closing 
                                else:
                                    menu_like_tags_stock.append(current_tag_name)
                        if  debug_mode: self._print_( 'EOL at :'+ str(line_index) + ' menu_collection_started is True'  + str(menu_like_tags_stock),skip_timestamp=True)
                    else:
                        if current_tag_name == 'ul':
                            if 'closing tags' in tag_details:
                                if current_tag_name in tag_details['closing tags']: continue
                            menu_collection_started=True
                            weightage_of_words[4] +=1
                            if tag_content_value:
                                menu_like_tags_pattern.append((current_tag_name,len(tag_content_value),len(tag_content_value.split()),line_index,tag_content_value))
                            else:
                                menu_like_tags_pattern.append((current_tag_name,0,0))
                            temp_collection_for_menu_like.append(each_line)
                            menu_like_tags_stock.append(current_tag_name)
                        else:
                            content_collected.append(each_line)
                        if  debug_mode: self._print_( 'EOL at :' + str(line_index) + ' menu_collection_started is False'  + str(menu_like_tags_stock),skip_timestamp=True)
                    if menu_collection_started and tag_content_value:
                        tag_content_value_length=len(tag_content_value.split())
                        weightage_of_words[0] +=1
                        if tag_content_value_length <=3:
                            weightage_of_words[1] +=1
                        elif tag_content_value_length <=15:
                            weightage_of_words[2] +=1
                        else:
                            weightage_of_words[3] +=1
                else:
                    if menu_collection_started:
                        closing_tag_details=self.get_html_closing_tags(each_line)
                        if closing_tag_details:
                            last_tag_is=menu_like_tags_stock[-1:]
                            if last_tag_is == closing_tag_details[0]: #closing the inner most tag
                                if  debug_mode: self._print_( 'Closing the inner tag at :' + str(line_index) + ' menu_collection_started is True. last tag, current tag and stock top' + '\t' + str(last_tag_is,closing_tag_details[0])+ '\t' + str(menu_like_tags_stock.pop()),skip_timestamp=True)
                                #menu_like_tags_stock.pop()
                                if (not menu_like_tags_stock) or len(menu_like_tags_stock) == 0: #closing the outer most tag -- end of menu
                                    if  debug_mode: self._print_( 'Closing Tag pattern at :' + str(line_index) + ' menu_collection_started is True. PATTERN Snap:' + '\t' + str(weightage_of_words) + '. PATTERN:'+ '\t' + str(menu_like_tags_pattern),skip_timestamp=True)
                                    menu_collection_started=False
                                    temp_collection_for_menu_like[:]=[]
                                    menu_like_tags_pattern[:]=[]
                            else:
                                if  debug_mode: self._print_( 'Logical Error at :'+ str(line_index) + ' menu_collection_started is True. Last tag and current closing tag is not matching'+ '\t' + str(last_tag_is) + '!=' + str(closing_tag_details[0]),skip_timestamp=True)
                        if menu_collection_started: temp_collection_for_menu_like.append(each_line)
                        if  debug_mode: self._print_( 'EOL at :'+ str(line_index) + ' Tag details with exception and menu_collection_started is True'  + str(menu_like_tags_stock),skip_timestamp=True)
                    else:
                        content_collected.append(each_line)
                        if  debug_mode: self._print_( 'EOL at :'+ str(line_index) + ' Tag details with exception and menu_collection_started is False'  + str(menu_like_tags_stock),skip_timestamp=True)
            else:
                #REPEATED FOR Closing tags
                if menu_collection_started and menu_like_tags_stock:
                    closing_tag_details=self.get_html_closing_tags(each_line)
                    if closing_tag_details:
                        last_tag_is=menu_like_tags_stock[-1:][0]
                        if  debug_mode: self._print_('Closing tag at :'+ str(line_index) + ' No Tag details and menu_collection_started is True'  + str(menu_like_tags_stock)+ '\t' + '\tClosing tags\t'+ '\t' + str(closing_tag_details[0]) + '\t' + '\tLast Tag\t:'+ '\t' + str(last_tag_is),skip_timestamp=True)
                        if last_tag_is == closing_tag_details[0]: #closing the inner most tag
                            if  debug_mode: self._print_('Closing the inner tag at :'+ str(line_index) + ' menu_collection_started is True. last tag, current tag and stock top'+ '\t' + str(last_tag_is) +'\t' + str(closing_tag_details[0])+ '\t' + str(menu_like_tags_stock.pop()),skip_timestamp=True)
                            #menu_like_tags_stock.pop()
                            if (not menu_like_tags_stock) or len(menu_like_tags_stock) == 0: #closing the outer most tag -- end of menu
                                exclude_menu_like=False
                                if weightage_of_words[0] == 0 or (weightage_of_words[2] ==0 and weightage_of_words[3] == 0):
                                    weightage_of_words[6]=1
                                    exclude_menu_like=True
                                if not exclude_menu_like:
                                    if (line_index - len(temp_collection_for_menu_like)) > (formatted_output_split_length/2) and line_index > (formatted_output_split_length * 0.9):
                                        weightage_of_words[6]=2
                                        exclude_menu_like=True
                                if not exclude_menu_like:
                                    if (line_index - len(temp_collection_for_menu_like)) <= (formatted_output_split_length * 0.1):
                                        weightage_of_words[6]=3
                                        exclude_menu_like=True
                                if exclude_menu_like:
                                    if  debug_mode: self._print_( 'Found a match at :'+ str(line_index) + ' with content length'+ '\t' + str(len(temp_collection_for_menu_like)) + '. PATTERN Snap:'+ '\t' + str(weightage_of_words) + '. PATTERN:'+ '\t' + str(menu_like_tags_pattern),skip_timestamp=True)
                                else:
                                    if  debug_mode: self._print_( 'Found a MISMATCH at :'+ str(line_index) + ' with content length'+ '\t' + str(len(temp_collection_for_menu_like)) +'. PATTERN Snap:'+ '\t' + str(weightage_of_words) + '. PATTERN:'+ '\t' + str(menu_like_tags_pattern),skip_timestamp=True)
                                    for each_item in temp_collection_for_menu_like:
                                        content_collected.append(each_item)
                                menu_collection_started=False
                                menu_like_tags_pattern[:]=[]
                                temp_collection_for_menu_like[:]=[]
                                for i in range(len(weightage_of_words)):
                                    weightage_of_words[i]=0
                    if menu_collection_started: temp_collection_for_menu_like.append(each_line)
                    if  debug_mode: self._print_( 'EOL at :'+ str(line_index) + ' No Tag details and menu_collection_started is True'  + str(menu_like_tags_stock),skip_timestamp=True)
                else:
                    content_collected.append(each_line)
                    if  debug_mode: self._print_( 'EOL at :'+ str(line_index) + ' No Tag details and menu_collection_started is False'  + str(menu_like_tags_stock),skip_timestamp=True)
            if len(menu_like_tags_stock) > 10:
                if debug_mode: self._print_('Item exceeded Number of item in menu_like_tags_stock exceeded 10 :' + '\t' + str(len(menu_like_tags_stock)) + '\t resetting...')
                menu_like_tags_stock[:]=[]
                menu_collection_started=False
                menu_like_tags_pattern[:]=[]
                for each_item in temp_collection_for_menu_like:
                    content_collected.append(each_item)
                for i in range(len(weightage_of_words)):
                    weightage_of_words[i]=0
                temp_collection_for_menu_like[:]=[]
        if not content_collected: 
            self.current_function_name=''
            return ''
        self.current_function_name=''
        return self.merge_on_end_tags('\n'.join(content_collected))
    def get_processed_un_ordered_list(self,data_from_tag_analysis,index_to_be_start,depth_level=0):
        self.current_function_name='get_processed_un_ordered_list'
        print_prefix='get_processed_un_ordered_list(' + str(depth_level) + '):\t'
        if 'get_processed_un_ordered_list' in self.debug_mode or self.deep_developer_mode:
            debug_mode = True
        else:
            debug_mode = False
        html_list_content=[]
        if depth_level > 25:
            if debug_mode: self._print_(print_prefix + 'Depth Level(' + str(depth_level) + ') is greater than 25')
            return html_list_content
        if not data_from_tag_analysis or (not isinstance(data_from_tag_analysis,dict)):
            if self.developer_mode: self._print_(print_prefix + 'Logical error: data_from_tag_analysis is not dictionary')
            self.current_function_name=''
            return html_list_content
        a_tag_index=self.has_child_with_tag(data_from_tag_analysis,index_to_be_start,['a'])
        if a_tag_index > 0:
            ul_ol_data_with_no_a=self.support_tag_analysis_reduce_tag(data_from_tag_analysis,index_to_be_start,process_anchors=False)
            ul_ol_data_with_a=self.support_tag_analysis_reduce_tag(data_from_tag_analysis,index_to_be_start,process_anchors=True)
            if debug_mode: self._print_(print_prefix + 'Index[' + str(index_to_be_start) + '] has an a tag :' + str(data_from_tag_analysis[a_tag_index]))
            if debug_mode: self._print_(print_prefix + 'Index[' + str(index_to_be_start) + '] : data length with a:' + str(len(ul_ol_data_with_a)))
            if debug_mode: self._print_(print_prefix + 'Index[' + str(index_to_be_start) + '] : data length with no a:' + str(len(ul_ol_data_with_no_a)) + ':' + str(len(ul_ol_data_with_a) - len(ul_ol_data_with_no_a)))
        else:
            return html_list_content
        if data_from_tag_analysis[index_to_be_start][3]:
            if debug_mode: self._print_(print_prefix + 'Starting for Index:' + str(index_to_be_start) + ' with tag :' + str(data_from_tag_analysis[index_to_be_start][0]))
            for each_child_index in data_from_tag_analysis[index_to_be_start][3]:
                if each_child_index <= index_to_be_start: continue
                if data_from_tag_analysis[each_child_index][0] in ['li']:
                    if debug_mode: self._print_(print_prefix + 'Parent Index:' + str(index_to_be_start) + '\t Child Index:' + str(each_child_index) + '\t Tag Name: ' + str(data_from_tag_analysis[each_child_index]))
                    current_menu_list=self.get_processed_html_list_tag_item(data_from_tag_analysis,each_child_index,index_to_be_start,depth_level=depth_level+1)
                    if current_menu_list:
                        html_list_content.append(current_menu_list)
                elif len(data_from_tag_analysis[each_child_index][0]) == 0 and (not data_from_tag_analysis[each_child_index][3]):
                    pass
                else:
                    if (not data_from_tag_analysis[each_child_index][3]) or data_from_tag_analysis[each_child_index][0] in ['ol','ul']:# got an ul/ol under ul/ol without intermediate li
                        pass
                    elif data_from_tag_analysis[each_child_index][0] in ['div']:#Ignoring intentionally
                        pass
                    elif ul_ol_data_with_no_a > 600:
                        pass #May be wrong content
                    else:
                        self._print_(print_prefix + 'Parent Index:' + str(index_to_be_start) + '\t Child Index:' + str(each_child_index) + '\t How to handle this tag in ul/ol:' + str(data_from_tag_analysis[each_child_index]))
                        exit()
        if debug_mode: self._print_(print_prefix + 'Parent Index:' + str(index_to_be_start) + '\t Return: ' + str(html_list_content))
        return html_list_content
    def get_processed_html_list_tag_item(self,data_from_tag_analysis,index_to_be_start,parent_index,depth_level=0):
        self.current_function_name='get_processed_html_list_tag_item'
        print_prefix='get_processed_html_list_tag_item(' + str(depth_level) + '):\t'
        if 'get_processed_html_list_tag_item' in self.debug_mode or self.deep_developer_mode:
            debug_mode = True
        else:
            debug_mode = False
        html_list_content={}
        if depth_level > 25:
            if debug_mode: self._print_(print_prefix + 'Depth Level(' + str(depth_level) + ') is greater than 25')
            return html_list_content
        if not data_from_tag_analysis or (not isinstance(data_from_tag_analysis,dict)):
            if self.developer_mode: self._print_(print_prefix + 'Logical error: data_from_tag_analysis is not dictionary')
            self.current_function_name=''
            return html_list_content
        if data_from_tag_analysis[index_to_be_start][3]:
            for each_child_index in data_from_tag_analysis[index_to_be_start][3]:
                if each_child_index <= index_to_be_start: continue
                tag_name_is=data_from_tag_analysis[each_child_index][0]
                if tag_name_is in ['ul','ol']:
                    if debug_mode: self._print_(print_prefix + 'G-Parent:' + str(parent_index) + '\t Parent Index:' + str(index_to_be_start) + '\t Child Index:' + str(each_child_index) + '\t Tag Name: ' + str(data_from_tag_analysis[each_child_index][0]))
                    current_menu_inner_loop=self.get_processed_un_ordered_list(data_from_tag_analysis,each_child_index,depth_level=depth_level+1)
                    if current_menu_inner_loop:
                        if 'inner-loop' not in html_list_content:
                            html_list_content['inner-loop']=[]
                        html_list_content['inner-loop'].append(copy.deepcopy(current_menu_inner_loop))
                        current_menu_inner_loop[:]=[]
                elif tag_name_is in ['a']:
                    if debug_mode: self._print_(print_prefix + 'G-Parent:' + str(parent_index) + '\t Parent Index:' + str(index_to_be_start) + '\t Child Index:' + str(each_child_index) + '\t A Tag Name: ' + str(data_from_tag_analysis[each_child_index]))
                    if len(data_from_tag_analysis[each_child_index][1])>0:
                        html_list_content['value']=data_from_tag_analysis[each_child_index][1]
                    else:
                        html_list_content['value']=self.support_tag_analysis_reduce_tag(data_from_tag_analysis,each_child_index,process_anchors=True,ignore_image=True)
                    if len(data_from_tag_analysis[each_child_index][5])>0:
                        html_list_content['link']=data_from_tag_analysis[each_child_index][5]
                elif len(tag_name_is) == 0 and (not data_from_tag_analysis[each_child_index][3]):
                    pass
                else:
                    if tag_name_is in self.TAG_PICTURE:
                        continue
                    elif tag_name_is in ['button','input']:
                        continue
                    elif tag_name_is in self.TAG_TEXT_CONTAINER:
                        html_list_content['desc']=self.support_tag_analysis_reduce_tag(data_from_tag_analysis,each_child_index)
                        if debug_mode: self._print_(print_prefix + 'G-Parent:' + str(parent_index) + '\t Parent Index:' + str(index_to_be_start) + '\t Child Index:' + str(each_child_index) + '\t Text Tag Name: ' + str(data_from_tag_analysis[each_child_index]))
                    else:
                        if debug_mode: self._print_(print_prefix + 'G-Parent:' + str(parent_index) + '\t Parent Index:' + str(index_to_be_start) + '\t Child Index:' + str(each_child_index) + '\t Other Tag Name: ' + str(data_from_tag_analysis[each_child_index]))
                        if tag_name_is in ['div']:
                            parent_of_list_indicator=self.has_child_with_tag(data_from_tag_analysis,each_child_index,['ul','ol'])
                            if parent_of_list_indicator>0:
                                if debug_mode: self._print_(print_prefix + 'G-Parent:' + str(parent_index) + '\t Parent Index:' + str(index_to_be_start) + '\t Child Index:' + str(each_child_index) + '\t Other Tag has either ul or ol')
                                current_menu_inner_loop=self.get_processed_html_list_tag_item(data_from_tag_analysis,each_child_index,parent_index=parent_index,depth_level=depth_level+1)
                                if current_menu_inner_loop:
                                    if 'inner-loop' not in html_list_content:
                                        html_list_content['inner-loop']=[]
                                    html_list_content['inner-loop'].append(copy.deepcopy(current_menu_inner_loop))
                                    current_menu_inner_loop.clear()
                            else:
                                if debug_mode: self._print_(print_prefix + 'G-Parent:' + str(parent_index) + '\t Parent Index:' + str(index_to_be_start) + '\t Child Index:' + str(each_child_index) + '\t div with no ul or ol \t' + str(data_from_tag_analysis[each_child_index]))
                                other_div_data=self.menu_support_all_are_hyper_or_desc(data_from_tag_analysis,each_child_index)
                                if other_div_data:
                                    if 'inner-loop' not in html_list_content:
                                        html_list_content['inner-loop']=[]
                                    html_list_content['inner-loop'].append(copy.deepcopy(other_div_data))
        if debug_mode: self._print_(print_prefix + 'G-Parent:' + str(parent_index) + '\t Parent Index:' + str(index_to_be_start) + '\t Return: ' + str(html_list_content))
        return html_list_content
    def menu_support_all_are_hyper_or_desc(self,data_from_tag_analysis,index_to_be_start):
        #first list all <a> tags alone. grouping is very complex.can be done if have time. Also return False if other than anchor tag contains data
        self.current_function_name='menu_support_all_are_hyper_or_desc'
        print_prefix='menu_support_all_are_hyper_or_desc:\t'
        if 'menu_support_all_are_hyper_or_desc' in self.debug_mode or self.deep_developer_mode:
            debug_mode = True
        else:
            debug_mode = False
        if not data_from_tag_analysis or (not isinstance(data_from_tag_analysis,dict)):
            if self.developer_mode: self._print_(print_prefix + 'Logical error: data_from_tag_analysis is not dictionary')
            self.current_function_name=''
            return current_index
        if debug_mode: self._print_(print_prefix + ' Function started for Index:' + str(index_to_be_start))
        current_list_of_childs=[]
        current_list_of_childs[:]=[]
        new_list_of_childs=[]
        new_list_of_childs[:]=[]
        output_list=[]
        output_list[:]=[]
        return_false=False
        if data_from_tag_analysis[index_to_be_start][3]:
            current_list_of_childs=copy.deepcopy(data_from_tag_analysis[index_to_be_start][3])
            while current_list_of_childs:
                if debug_mode: self._print_(print_prefix + ' New list of child:' + str(current_list_of_childs))
                for each_child in current_list_of_childs:
                    if len(data_from_tag_analysis[each_child][0])>0:
                        if data_from_tag_analysis[each_child][0] in ['a']:
                            if len(data_from_tag_analysis[each_child][5])>0:
                                if debug_mode: self._print_(print_prefix + 'Add: a tag[' + str(each_child) + '] with href:' + str(data_from_tag_analysis[each_child]))
                                if len(data_from_tag_analysis[each_child][1])>0:
                                    output_list.append({'value':data_from_tag_analysis[each_child][1],'link':data_from_tag_analysis[each_child][5]})
                                else:
                                    output_list.append({'value':self.support_tag_analysis_reduce_tag(data_from_tag_analysis,each_child,process_anchors=True,ignore_image=True),'link':data_from_tag_analysis[each_child][5]})
                            elif debug_mode:
                                self._print_(print_prefix + 'a tag[' + str(each_child) + '] with no href:' + str(data_from_tag_analysis[each_child]))
                        elif self.has_child_with_tag(data_from_tag_analysis,each_child,['a'])>0:
                            if debug_mode: self._print_(print_prefix + 'Loop: tag[' + str(each_child) + '] has a grand child node with a tag')
                            for each_child_index in data_from_tag_analysis[each_child][3]:
                                new_list_of_childs.append(each_child_index)
                        else:
                            if debug_mode: self._print_(print_prefix + 'Process: Other than a tag[' + str(each_child) + ']')
                            other_tag_text=self.support_tag_analysis_reduce_tag(data_from_tag_analysis,each_child,process_anchors=True,ignore_image=True)
                            other_tag_text=other_tag_text.strip().strip('\n').strip()
                            if len(other_tag_text) > 0:
                                return_false=True
                                if debug_mode: self._print_(print_prefix + 'Break: Other than a tag[' + str(each_child) + '] has text:' + str(data_from_tag_analysis[each_child]))
                                break
                    elif debug_mode:
                        self._print_(print_prefix + 'Record[' + str(each_child) + '] with no tag:' + str(data_from_tag_analysis[each_child]))
                if return_false:
                        break
                current_list_of_childs=copy.deepcopy(new_list_of_childs)
                new_list_of_childs[:]=[]
        if return_false: return []
        return output_list
    def has_child_with_tag(self,data_from_tag_analysis,index_to_be_start,tag_list_to_check):
        self.current_function_name='has_child_with_tag'
        print_prefix='has_child_with_tag:\t'
        if 'has_child_with_tag' in self.debug_mode or self.deep_developer_mode:
            debug_mode = True
        else:
            debug_mode = False
        current_index=0
        depth_level=0
        if not data_from_tag_analysis or (not isinstance(data_from_tag_analysis,dict)):
            if self.developer_mode: self._print_(print_prefix + 'Logical error: data_from_tag_analysis is not dictionary')
            self.current_function_name=''
            return current_index
        current_list_of_childs=[]
        current_list_of_childs[:]=[]
        new_list_of_childs=[]
        new_list_of_childs[:]=[]
        if data_from_tag_analysis[index_to_be_start][3]:
            current_list_of_childs=copy.deepcopy(data_from_tag_analysis[index_to_be_start][3])
            while current_list_of_childs:
                for each_child in current_list_of_childs:
                    if len(data_from_tag_analysis[each_child][0])>0 and data_from_tag_analysis[each_child][0] in tag_list_to_check:
                        return each_child
                    for each_grand_child in data_from_tag_analysis[each_child][3]:
                        if each_grand_child <= each_child:
                            self._print_(print_prefix + 'Grand Child (' + str(each_grand_child) + ') is less than child (' + each_child + ')')
                            exit()
                        new_list_of_childs.append(each_grand_child)
                current_list_of_childs=copy.deepcopy(new_list_of_childs)
                new_list_of_childs[:]=[]
                depth_level += 1
        return current_index
    def has_index_as_parent(self,data_from_tag_analysis,child_index,parent_index):
        self.current_function_name='has_child_with_tag'
        print_prefix='has_index_as_parent:\t'
        if 'has_index_as_parent' in self.debug_mode or self.deep_developer_mode:
            debug_mode = True
        else:
            debug_mode = False
        if not data_from_tag_analysis or (not isinstance(data_from_tag_analysis,dict)):
            if self.developer_mode: self._print_(print_prefix + 'Logical error: data_from_tag_analysis is not dictionary')
            self.current_function_name=''
            return current_index
        index_to_be_checked=[]
        if isinstance(parent_index,(int,long)):
            index_to_be_checked.append(parent_index)
        else:
            for each_index in child_index:
                index_to_be_checked.append(each_index)
        all_parents=data_from_tag_analysis[child_index][4]
        if all_parents:
            for each_parent in all_parents:
                if each_parent in index_to_be_checked:
                    return True
        return False
    def get_all_anchor_tags(self,tag_details_result,base_url,include_script_link=True,remove_footer=False,remove_header=False,no_of_words=0,filter_no_value_tags=False,use_title_for_no_value=True,restrict_domain=False,allow_social=True):
        collect_links_details=[]
        print_prefix='get_all_anchor_tags:\t'
        if 'get_all_anchor_tags' in self.debug_mode or self.deep_developer_mode:
            debug_mode=True
        else:
            debug_mode=False
        if debug_mode:
            self._print_(print_prefix + 'List of all tags')
            for each_of in tag_details_result:
                self._print_(print_prefix + str(each_of) + '\t' + str(tag_details_result[each_of]))
        if restrict_domain:
            domain_of_page=self.ins_weburlparse.get_website_parent(base_url)
            temp_ins=None
        for each_a in tag_details_result['a']:
            a_tag_display=get_printable_string(self.support_tag_analysis_reduce_tag(tag_details_result,each_a),unicode_to_entitiy_flag=False,replace_html_entities=True,replace_lt_gt_symbol=True)
            a_tag_display=a_tag_display.strip(' \n\r\t')
            a_tag_display_length=len(a_tag_display.split())
            if a_tag_display_length == 0: 
                if not filter_no_value_tags:
                    if use_title_for_no_value:
                        if tag_details_result[each_a][8]:
                            if 'title' in tag_details_result[each_a][8]:
                                a_tag_display=tag_details_result[each_a][8]['title'].strip(' \n\r\t')
                                a_tag_display_length=len(a_tag_display.split())
            if no_of_words > 0 and no_of_words < a_tag_display_length:
                continue
            if debug_mode: self._print_(print_prefix + str(each_a) + '\t Display:' + a_tag_display + '.\t' + str(tag_details_result[each_a]))
            a_tag_href=tag_details_result[each_a][5]
            a_tag_href=a_tag_href.strip(' \n\r\t')
            if not a_tag_href or (len(a_tag_href) == 0): continue
            link_type=get_html_link_type(a_tag_href,return_special_for_special=True)
            if (not include_script_link) and link_type != 'link': 
                if debug_mode: self._print_(print_prefix,str(tag_details_result[each_a]) + '\t@ a and href. include_script_link-\t' + str(include_script_link) + '\tlink_type:' + str(link_type))
                continue
            if link_type == 'Special':
                absolute_path=a_tag_href
            else:
                absolute_path=get_absolute_path(base_url,a_tag_href)
            if restrict_domain:
                link_domain=self.ins_weburlparse.get_website_parent(absolute_path)
                temp_ins=None
                if domain_of_page != link_domain:
                    if link_domain in all_social_domains and allow_social:#['twitter','facebook','linkedin','pinterest','instagram','youtube'] and allow_social: #SOCIAL
                        pass
                    elif include_script_link and link_type == 'Special':#To allow tel mail
                        pass
                    else:
                        if debug_mode: self._print_(print_prefix + 'Domain does not match' + '\t' + domain_of_page + '('+ base_url +')\t' + link_domain + '(' + absolute_path +')')
                        continue
            if debug_mode: self._print_(print_prefix + '\t' + base_url + '\t' + str(a_tag_href) + '\t' + str(absolute_path))
            collect_links_details.append({'value':a_tag_display,'href':absolute_path,'index':each_a})#Do we need details? ,'details':tag_details_result[each_a]
        if debug_mode:self._print_(print_prefix + '\tcollected all anchor tags')
        if debug_mode: 
            self._print_( '\n' + print_prefix + 'Collected LINKS Parents:' + str(len(collect_links_details)))
            for each_list in collect_links_details:
                self._print_(print_prefix + str(each_list['index']) + '\t' + str(each_list['value']) + '\t' + str(each_list['href']))
        return collect_links_details
if __name__ == '__main__':
#
    if True:
        from CustomPrint import *
        cp=CustomPrint(output_type='both',buffer_line_limit=2,file_prefix='test_html_')
        url_list=['http://www.casso.com/','http://www.capitalassoc.com/','http://fiind.com/']
        for each_url in url_list:
            url_is=each_url
            ins=HTMLHandlingNews(webpage_url=url_is,developer_mode=False,debug_mode=[],deep_developer_mode=False,print_instance=cp)
            meta_content=ins.get_meta_data()
            print meta_content
    elif not True:
        from CustomPrint import *
        cp=CustomPrint(output_type='both',buffer_line_limit=2,file_prefix='test_html_')
        url_is='https://www.eegholm.dk/'#'http://www.roedeanschool.co.za/'#http://yuehwa.com#'http://roedeanschool.co.za'#'http://crosscountry-africa.com'
        ins=HTMLHandlingNews(webpage_url=url_is,developer_mode=True,debug_mode=[],deep_developer_mode=True,print_instance=cp)#'get_all_anchor_tags'])
        page_content=ins.get_content_from_page(news_title=None,process_anchors=True,no_exclusion=True)
        print repr(page_content)
        print 'Page Content Length:' + str(len(page_content))
    elif not True:
        url_is='http://www.connerprairie.org/'
        ins=HTMLHandlingNews(webpage_url=url_is,developer_mode=True,debug_mode=[])#'get_all_anchor_tags'])
        all_links=ins.fetch_all_links_for_website(restrict_domain=True,allow_social=False)
        for each_link in all_links:
            print each_link
        exit()
    elif not True:
        ins=HTMLHandlingNews(webpage_url='http://www.fiind.com',developer_mode=True,debug_mode=['get_all_anchor_tags'])
        page_urls=ins.fetch_all_anchor(restrict_domain=True,allow_social=False)
        print page_urls
        exit()
    if not True:
        print 'and',is_date('and')
        print what_is_the_object_type('Fluoropolymers and Fluorochemicals, From the Business That Invented Them')
        exit()
    if not True:
        actual_url=r'http://www.equitiesfocus.com/equity-in-focus-deere-company-nysede/111845/' #http://www.nytimes.com/2015/03/10/business/media/hbo-streaming-to-start-in-april-on-apple-devices-only.html'
        myhtml=HTMLHandling(developer_mode=developer_mode)
        print myhtml.fetch_content_for_url(actual_url)
        print myhtml.get_html_data()
        exit()
    if not True:
        input_is=r'<DOCUMENT><TYPE>10-K<SEQUENCE>1<FILENAME>a28078e10vk.htm<DESCRIPTION>FORM 10-K<TEXT><HTML><HEAD><TITLE>Oakley, Inc.</TITLE></HEAD><BODY bgcolor="#FFFFFF"><!-- PAGEBREAK --><H5 align="left" style="page-break-before:always"><A HREF="#tocpage">Table of Contents</A></H5><P><BR class="a"/>prabu<BR/><TABLE>A</TABLE></BODY>'
        myhtml=HTMLHandling(developer_mode=developer_mode)
        myhtml.feed_data(input_is)
        myhtml.process_content()
        print myhtml.get_formatted_data()
    if not True:
        #ET
        actual_url=r'http://economictimes.indiatimes.com/industry/telecom/second-day-of-telecom-spectrum-auction-ends-bids-grow-to-rs-65000-crore/articleshow/46471353.cms'
        #Firstpost
        # NOT FOUND actual_url=r'http://tech.firstpost.com/news-analysis/apples-next-smartphone-iphone-6s-to-have-2gb-ram-12-9-inch-ipad-to-support-usb-3-0-257767.html'
        #Motorola
        actual_url=r'http://www.mobiletor.com/128119/xolo-q600-club-offers-dts-audio-and-ir-blaster-for-rs-6499/'
        #Random
        actual_url=r'http://www.ndtv.com/india-news/not-consulted-dont-approve-decision-to-release-separatist-leader-masrath-alam-says-bjp-745039'
        actual_url=r'http://www.bloomberg.com/news/articles/2015-03-07/boko-haram-pledges-allegiance-to-islamic-state-on-twitter'
        actual_url=r'http://zeenews.india.com/sports/sports/badminton/i-lost-focus-and-got-nervous-says-saina-nehwal_1558385.html'
        actual_url=r'http://www.thehindu.com/news/national/mute-spectators-more-responsible-for-violence-against-women-sneha-shekhawat/article6971870.ece'#confusing candidate
        actual_url=r'http://www.dnaindia.com/sport/report-kumar-sangakkara-set-to-retire-after-india-series-in-august-2067122'
        actual_url=r'http://www.wsj.com/articles/north-korean-carrying-1-4-million-in-gold-bars-intercepted-in-bangladesh-1425736098'
        actual_url=r'http://www.bloomberg.com/bw/articles/2014-12-17/toyota-embraces-fuel-cell-cars-for-post-gasoline-future#r=read'
        actual_url=r'http://money.cnn.com/2015/03/06/investing/abercrombie-and-fitch-stock-die/'
        actual_url=r'https://github.com/grangier/python-goose'
        actual_url=r'http://mmb.moneycontrol.com/stock-message-forum/axisbank/comments/3142'#NO PROPER Hypher link
        actual_url=r'http://seekingalpha.com/news/2310656-analysts-dig-into-the-west-coast-port-slowdown'
        actual_url=r'https://nrf.com/news/the-lure-of-luxury'
        actual_url=r'http://www.wdc.com/en/company/corporateinfo/corp_bios.aspx'
        #actual_url=r'http://www.firstpost.com/india/tmcs-derek-obrien-expresses-concern-beef-ban-maharashtra-2147681.html'
        print "URL: ",actual_url
        new_file_name=get_filename_from_url(actual_url) + '.html'#'Hindu_Art.html'
        fetch_from_net=False
        import os.path
        if not os.path.isfile(new_file_name):
            fetch_from_net=True
        print "File Name: ",new_file_name,'\t\tFile Exist:',os.path.isfile(new_file_name)
        if fetch_from_net:
            print "Fetching result for the url ",actual_url
            import requests
            import urllib2
            user_agent='Mozilla/%2F4.0'
            request = urllib2.Request(actual_url)
            request.add_header('User-Agent', user_agent)
            request_opener = urllib2.build_opener()
            response = request_opener.open(request)
            try:
                article_content = response.read()
            except httplib.IncompleteRead, e:
                article_content = e.partial
            if False:
                article_content = requests.get(actual_url).text.encode('ascii','ignore')
                article_content=article_content.replace('\n',' ').replace('\r',' ').replace('\t',' ')
            wri=open(new_file_name,'w')
            wri.write(article_content)
            wri.close()
        rea=open(new_file_name,'r')
        article_content=rea.read() 
        rea.close()
        myhtml=HTMLHandling(developer_mode=developer_mode)
        #file_content=r'<DOCUMENT><TYPE>10-K<SEQUENCE>1<FILENAME>a28078e10vk.htm<DESCRIPTION>FORM 10-K<TEXT><HTML><HEAD><TITLE>Oakley, Inc.</TITLE></HEAD><BODY bgcolor="#FFFFFF"><!-- PAGEBREAK --><H5 align="left" style="page-break-before:always"><A HREF="#tocpage">Table of Contents</A></H5><P><BR class="a"/>prabu<BR/><TABLE>A</TABLE></BODY>'
        myhtml.feed_data(article_content)
        #myhtml.set_ignore_section_tag_name('table')
        myhtml.process_content()
        formatted_output=myhtml.get_formatted_data(output_format='str')
        formatted_output_stats=myhtml.get_statement_stats()
        len_formatted_output_stats=len(formatted_output_stats)
        formatted_output_html_actual=myhtml.get_statement_html()
        len_formatted_output_html_actual=len(formatted_output_html_actual)
        if isinstance(formatted_output,str): print formatted_output
        split_chars='\t\tSPLIT\t\t'
        if isinstance(formatted_output,list):
            for each_index in range(len(formatted_output)):
                if each_index < len_formatted_output_stats:
                    if formatted_output_stats[each_index][0] > 0:
                        if each_index < len_formatted_output_html_actual:
                            if developer_mode: print formatted_output_stats[each_index],split_chars,formatted_output[each_index],split_chars,formatted_output_html_actual[each_index]
                            #if developer_mode: print '\n\n'
                        else:
                            if developer_mode: print formatted_output_stats[each_index],split_chars,formatted_output[each_index]
                            #if developer_mode: print '\n\n'
                elif len(formatted_output[each_index])>0:
                    if developer_mode: print formatted_output[each_index]
                    print '\n\n'
        print myhtml.get_statement_html()
        #print myhtml.get_statement_stats()
        print myhtml.get_beautified_html_content()
    if not True:
        url_ins=URLStatus()
        url_result=url_ins.check_url('ilink.fiind.com')
        print url_result['input_url'] + '\t' +url_result['parsed_url'] + '\t' + url_result['url_status'] + '\t' + str(url_result['status_code']) + '\t' + url_result['final_url'] + '\t' + url_result['url_redirected'] + '\t' + str(url_result['no_of_redirections']) + '\t' + str(url_result['url_redirect_list']) + '\t' + str(url_result['status_code_list']) + '\t'  + url_result['error'] + '\n' 
        url_ins=None
