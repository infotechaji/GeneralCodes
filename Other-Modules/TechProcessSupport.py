"""
Description : Supporting script which contains the below functions
Functions   : 
            1.ListDifference()              - added on 03/13/2019 - which do List B - List B 
            2.get_all_process_id()          - added on 03/13/2019 - which returns all the active process id  from current system
            3.get_active_specific_process()  - added on 03/13/2019  - which returns all the specfic process 
            4.get_all_json()                 - added on 03/13/2019 - which returns all the json files from a given directory 
            5.get_processed_json_files()     - added on 03/13/2019 - which returns count and details of all the json files from a given directory with n directories with n suffix.
            6.get_vm_name()                  - added on 03/13/2019 - which gets and returns VM name from the table "core_stage.vm_mapping"
            7.get_vm_name()                  - added on 03/13/2019 - which gets and returns VM name from the table "core_stage.vm_mapping"
            8.get_host_details()             - added on 03/13/2019 - which gets host_name,system_name,ip_address of current user 
            9.get_printable_time_stamp()     - added on 03/13/2019 - get printable current time stamp 
            
Version    : v1.1
History    : 
             v1.0   - 03/13/2019 - initial version 
             v1.1   - 06/04/2019 - () added to print statements to work with python 3 
            
Open Issues :

Pending :           
"""
import os,sys
import time,datetime
import psutil
from SQLConnection import * 
import getpass
if str(sys.version).startswith('2'):
    from FileHandling import *
elif str(sys.version).startswith('3'):
    from FileHandling3 import *

def ListDifference(list1, list2): 
    return (list(set(list1) - set(list2))) 

def get_all_process_id(get_python_process=False,use_list=[],check_process='python'): # return all the active python process ID
    #print 'get_all_process_id called :'
    if use_list:
        total_id_list=use_list
    else:
        total_id_list=psutil.pids()
    if get_python_process:
        python_codes=[]
        for each_id in total_id_list:
            try:
                p = psutil.Process(each_id)
                process_name=p.name()
                #print 'process_name :',process_name
                if check_process.lower() in process_name:
                    if each_id not in python_codes:
                        python_codes.append(each_id)
            except Exception as e :
                print ('Exception in getting process name :',e)
                pass
        return python_codes
    return total_id_list
def get_active_specific_process(existing_processes,check_process='cmd'): # get only python process from given process 
        current_processes=get_all_process_id()
        temp_list=ListDifference(current_processes,existing_processes)
        # print 'Total Processes :',len(existing_processes)
        # print 'Total Processes after code execution :',len(current_processes)
        # print 'Process Difference :',len(temp_list)
        if temp_list:
            current_python_processes=get_all_process_id(use_list=temp_list,get_python_process=True,check_process=check_process)
            #print "key_list[0][active_instances]:",key_list[0]['active_instances']
            #print "len(current_python_processes):",current_python_processes
        else:
            print ('No Active Processes !!')
            current_python_processes=[]
        return current_python_processes
        
def get_all_json(input_directory): # returns all the json in the given directory
    f_h_ins=FileHandling()
    all_files_list=f_h_ins.get_all_files(directory_is=input_directory,pattern='*.json',full_path=True,recursive=False)
    del f_h_ins
    return all_files_list

def get_processed_json_files(source_directory,thread_count=1):
    print ('get_processed_json_files :')
    print ('source_directory :',source_directory)
    print ('thread_count :',thread_count)
    total_json_files=0
    log_list=[]
    for i in range(0,thread_count):
        temp_directory=source_directory+str(i+1)
        temp_json_files=len(get_all_json(temp_directory))
        total_json_files+=temp_json_files
        temp_dict={
            'directory':temp_directory
            ,'json_files':temp_json_files
                }
        log_list.append(temp_dict)
    result_dict={'total_json_files':total_json_files,
                   'files_list':log_list}
    #print result_dict
    return result_dict
def get_vm_name(): 
    result=''
    result_dict=get_host_details()
    result_dict['vm_name']=''
    sql_query="select vm_name from core_stage.vm_mapping where host ='"
    sql_query+=str(result_dict['host_name'])
    sql_query+="' or ip_address ='"
    sql_query+=str(result_dict['ip_address'])+"'"
    #print 'sql_query :',sql_query
    try:
        result=execute_query(sql_query)
    except Exception as e:
        print ('Exception in getting Host name get_vm_name:',e )
        pass
    if result:
        #print 'result:',result
        # print 'result[0]:',result[0]
        try:
            result_dict['vm_name']=result['vm_name']
        except Exception as e:
            result_dict['vm_name']=result[0][0]
    
    return result_dict
    
def get_host_details(): # gets current user name,host_name,ip_address 
    import socket
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    user_name=getpass.getuser()
    return {'host_name':host_name,
            'ip_address':ip_address,
            'user_name':user_name}
def get_printable_time_stamp(get_exact_time=False,skip_seconds=False):
    c_time= str(datetime.datetime.now())
    date_time=c_time.split('.')[0]
    if skip_seconds:
        date_time=date_time.split()[0]
    if get_exact_time:
        return date_time # returns 2018-05-22 12:21:22
    return get_replaced_content(date_time)

def get_replaced_content(content,characters_list=['-',':',' '],replace_by=''):
    if not content: return ''
    for each_char in characters_list:
        if each_char==' ':
            content=content.replace(each_char,'_')
        else:
            content=content.replace(each_char,replace_by)
    return content
