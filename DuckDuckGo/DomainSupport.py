"""
    Version    : v1.4
    History    :
                1.0 - 07/31/2015 - Initial Version
                1.1 - 11/24/2015 - Moved to one version logic
                1.2 - 11/30/2015 - Add get_url_health function
                1.3 - 12/23/2015 - change get_url_health
                1.4 - 01/05/2016 - Set timeout in requests.head
"""
import requests,socket
def get_domain_details(in_domain_name):
    common_www_list=['www','www2','www3','www4','www5','www6','www7','www8','www9']
    common_second_level_sub_domains=['co','com','net','edu','gov']
    www_type=''
    domain_name=in_domain_name
    schema=''
    sub_domain_name=''
    path=''
    param=''
    if '//' in domain_name:
        domain_name=domain_name.split('//')[1]
        schema=in_domain_name.split('//')[0].strip(':')
        #print 'schema for ' + in_domain_name + ' is - ' + str(schema)
    if '/' in domain_name:
        domain_name_fs_list=domain_name.split('/')
        domain_name=domain_name_fs_list[0]
        #print in_domain_name,'\tInside domain name',domain_name,domain_name_fs_list,len(domain_name_fs_list)
        if len(domain_name_fs_list)>1:
            path='/'.join(domain_name_fs_list[1:])
            #print in_domain_name,'\tInside after/',domain_name_fs_list,path,'\tParam\t',domain_name_fs_list[-1:]
            if '?' in str(domain_name_fs_list[-1:]):
                #print in_domain_name,'\tInside Param/',path,'\tParam\t',domain_name_fs_list[-1:]
                param=''.join('/'.join(domain_name_fs_list[-1:]).split('?')[1:])
            path=path.strip('/')
    domain_name_split=domain_name.split('.')
    filtered_domain_list=[]
    filtered_domain_list[:]=[]
    domain_name_split_length=len(domain_name_split)
    adjusted_domain_split_length=domain_name_split_length
    www_found=0
    domain_suffix='' #.in,.com,.us
    for iter_i in range(domain_name_split_length):
        if iter_i ==0:
            if domain_name_split[iter_i].lower() in common_www_list:
                www_type=domain_name_split[iter_i]
                www_found=1
                adjusted_domain_split_length = adjusted_domain_split_length - 1
            else:
                filtered_domain_list.append(domain_name_split[iter_i])
        elif iter_i == (domain_name_split_length - 2):
            if domain_name_split_length - (2 + www_found) > 0:
                if domain_name_split[iter_i] in common_second_level_sub_domains:
                    domain_suffix=domain_name_split[iter_i]
                else:
                    filtered_domain_list.append(domain_name_split[iter_i])
            else:
                filtered_domain_list.append(domain_name_split[iter_i])# need to handle somehow co.us
        elif iter_i == (domain_name_split_length - 1):
            if len(domain_suffix)>0:
                domain_suffix = domain_suffix + '.' + domain_name_split[iter_i]
            else:
                domain_suffix=domain_name_split[iter_i]
            adjusted_domain_split_length = adjusted_domain_split_length - 1
        else:
            filtered_domain_list.append(domain_name_split[iter_i])
    domain_name=''
    if len(filtered_domain_list) == 1:
        sub_domain_name=''
        domain_name_alone=str(filtered_domain_list[0])
        domain_name=domain_name_alone + '.' + domain_suffix
    else:
        sub_domain_name='.'.join(filtered_domain_list[:-1])
        domain_name_alone = ''.join(filtered_domain_list[-1:])
        if len(domain_name_alone)>0: domain_name= domain_name_alone + '.' + domain_suffix
    return {'schema':schema,'input':in_domain_name,'www_type':www_type,'sub_domain':sub_domain_name,'domain_name':domain_name,'domain_alone':domain_name_alone,'path':path,'param':param}
def get_url_health(request_url,iteration_no=1,time_out_in=10):
    #print 'DomainSupport.py:get_url_health:' + str(request_url) + ':' + str(iteration_no) + ':' + str(time_out_in)
    if 'http://' not in request_url and 'https://' not in request_url:
        request_url='http://' + str(request_url)
    try:
        #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        #head_result=requests.head(request_url,headers=headers)
        if time_out_in <= 0 or time_out_in > 25: 
            timeout = 25
        else:
            timeout=time_out_in
        socket.setdefaulttimeout(timeout)
        head_result=requests.head(request_url,verify=False,timeout=timeout)
        head_status_code=head_result.status_code
        if head_status_code >= 200 and head_status_code <=307:
            return True
        return False
    except Exception as e:
        print 'get_url_health: Error for url:' + str(request_url) + '. Error : ' + str(e)
        if iteration_no > 1:
            return False
        else:
            if 'https://' in request_url:
                print 'get_url_health: requesting http:// content for :' + str(request_url)
                return get_url_health(request_url.replace('https://','http://'),iteration_no=iteration_no+1,time_out_in=timeout+2)
            else:
                if 'Connection aborted.' in str(e) and '10060' in str(e): #not responding
                    return False
                elif 'Connection aborted.' in str(e) and '11001' in str(e): #getaddrinfo failed
                    return False
                elif 'Connection aborted.' in str(e) and '10054' in str(e): #An existing connection was forcibly closed by the remote host
                    return False
                elif 'Connection aborted.' in str(e) and '10061' in str(e): #target machine actively refused
                    return False
                #exit()
                return False
if __name__ == '__main__':
    if True:
        print 'http://www.colliersparrish.com/html/en/us/index.asp?ptype=1',get_domain_details('http://www.colliersparrish.com/html/en/us/index.asp?ptype=1')
        print 'http://www.macraesbluebook.com/search/company.cfm?company=867549',get_domain_details('http://www.macraesbluebook.com/search/company.cfm?company=867549')
        exit()