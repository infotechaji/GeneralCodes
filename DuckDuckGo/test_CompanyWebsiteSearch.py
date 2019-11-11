# -*- coding: utf-8 -*-
"""
    Content Type: Code
    Description: This python file will test the functionalities of Company Website search module
    Version       : v1.0
    History       :
                v1.0 - 07/11/2016 - Initial version.
                v1.1 - 07/20/2016 - Using base class
    Procedure to use: TBD
    Open Issues: None.
    Pending :     None.
"""
import sys
sys.path.insert(0,'..\\common')
from InputOutput import *
from CompanyWebsite import *
from azure.storage.queue import QueueService
import os
import base64
import time
import requests
import argparse
from Utilities import *
from datetime import datetime
data_directory=os.getcwd()

def read_input_queue(queue_name):
    number_of_retry=10#10minutes
    retry_count=0
    while True:
        try:
            queue_service = QueueService(account_name='fiindmllabs', account_key='odsS8z/XCVaE+ccTHaaLULfvHfnDS/3tNmd/Otf99CFR7P5ckqEeFKzxPE08p5auBNQZ04GZ7vC1jxY2QCc6IQ==')
            q_messages=queue_service.get_messages(queue_name, numofmessages = 1) #,visibility_timeout=5*60
            break
        except Exception as e:
            error_msg=str(e).lower()
            
            print '-------------',error_msg,'--------------'
            if '10060' in error_msg and ('connection attempt failed' in error_msg or  'connected host has failed to respond' in error_msg):
                retry_count += 1
                if retry_count <  number_of_retry:
                    continue
            break
    q_status=False
    input_company_list=[]
    for each_message in q_messages:
        message_text=base64.b64decode(str(each_message.message_text))
        ins_read=InputOutput('Feed')
        ins_read.open(message_text)
        input_company=ins_read.read(output_format='dict',column_structure=['company_name','country','company_id'])[0]
        input_company['q_pop_receipt']=each_message.pop_receipt
        input_company['q_message_id']=each_message.message_id
        input_company_list.append(input_company)
        if input_company_list:
            q_status=True
        ins_read.close()
        return input_company_list
    return q_status

def mark_input_queue_consumed(q_message_id,q_pop_receipt,queue_name):      
    if len(q_message_id) > 0:
        queue_service = QueueService(account_name='fiindmllabs', account_key='odsS8z/XCVaE+ccTHaaLULfvHfnDS/3tNmd/Otf99CFR7P5ckqEeFKzxPE08p5auBNQZ04GZ7vC1jxY2QCc6IQ==')
        queue_service.delete_message(queue_name,q_message_id,q_pop_receipt)
        if True:
            print ('Message with id=' + q_message_id + ' deleted from queue:' + queue_name)
        q_message_id=''
        q_pop_receipt=''
    return True
        

def this_azure_upload(local_file_name,target_filename_in=None,local_data_directory=data_directory,timestamp=None):
    # return True
    if not target_filename_in:
        target_filename=local_file_name
    else:
        target_filename=target_filename_in
    local_file_name=os.path.join(local_data_directory,target_filename)
    if os.path.isfile(local_file_name):
        try:
            import socket
            hostname=str(socket.gethostbyname(socket.gethostname()))
        except:
            hostname='NoHostName'
        if timestamp:
            hostname+='_'+str(timestamp).strip(":\t")
        target_filename=hostname + '_' + target_filename
        # target_filename=get_file_name_with_time_stamp(target_filename,check_file_existence=False)
        from StorageAzure import *
        azure=PythonAZURE('fiindmllabs','odsS8z/XCVaE+ccTHaaLULfvHfnDS/3tNmd/Otf99CFR7P5ckqEeFKzxPE08p5auBNQZ04GZ7vC1jxY2QCc6IQ==')
        print 'args.blob inside blob upload function :',args.blob
        azure.create_bucket(args.blob)# args.blobname
        azure.set_bucket_name(args.blob)# args.blobname
        azure.set_environment('staging')
        azure.upload_file( 'data', local_file_name, filename_to_save=target_filename,new_extension=None)
        print azure.list_file()
    

if __name__ == '__main__':
    arg = argparse.ArgumentParser('Program to collect basic details of a company',add_help=True)
    arg.add_argument('-i','--input_file','--file',help='Input type(ms-queue) or File name', required=False)#dest='somename', somename is the name by which to access the value from NameSpace
    arg.add_argument('-q','--queue', nargs='?',help='Queue name to fetch input data', const='tpoctaskq',required=False)
    arg.add_argument('-f','--format', help='Output format(bcp, postgres)', default='bcp',required=False)
    arg.add_argument('-b','--blob', help='Blob to upload',nargs='?',const='automatedtesting',required=False)
    arg.add_argument('-a','--azure_account', nargs='?',help='Azure account name for queue and blob',const='fiindmllabs',required=False)
    arg.add_argument('-k','--azure_key', nargs='?',help='Azure account key for queue and blob',const='odsS8z/XCVaE+ccTHaaLULfvHfnDS/3tNmd/Otf99CFR7P5ckqEeFKzxPE08p5auBNQZ04GZ7vC1jxY2QCc6IQ==',required=False)
    arg.add_argument('-t','--test',nargs='?',const=True,default=False,required=False)
    arg.add_argument('-p','--process_name', help='Identifier for the Module', default='Basic_Details',required=False)
    arg.add_argument('--restart', help='Restart the process. Take precedence over force_start',nargs='?',const=True,default=False,required=False)
    arg.add_argument('--force_start', help='Ignore previous run and start from the beginning',nargs='?',const=True,default=False,required=False)
    arg.add_argument('-d','--developer_mode', help='Developer Mode Flag',nargs='?',const=True,default=False,required=False)
    arg.add_argument('--deep_developer_mode', help='Deep Developer Mode Flag',nargs='?',const=True,default=False,required=False)
    arg.add_argument('--company_count', help='Number of companies to be processed',type=int,default=0,required=False)
    arg.add_argument('--blob_upload_count', help='Number of companies once the blob needs to be uploaded',type=int,default=1,required=False)
    arg.add_argument('--skip_count', help='Number of companies to be skipped from start',type=int,default=0,required=False)
    arg.add_argument('--url_status', dest='url_status_only',help='Check for only url status',nargs='?',const=True,default=False,required=False)
    arg.add_argument('--process_home_page', dest='process_home_page',help='Flag to process data from home with url_status is set',nargs='?',const=True,default=False,required=False)
    arg.add_argument('--disable', dest='disable_tasks',help='Flag to disable task from getting executed.',default='',required=False)
    arg.add_argument('--instance_identifier', help='Identifier to differentiate multiple instances running in same machine',type=int,default=0,required=False)
    arg.add_argument('--queue_test', help='Test Queue Execution',nargs='?',const=True,default=False,required=False)
    #parser.add_argument('--feature', dest='feature', action='store_true')
    #parser.add_argument('--no-feature', dest='feature', action='store_false')
    #parser.set_defaults(feature=True)
    #ap.add_argument('-f','--format', nargs='?',help='Output format(bcp, postgres)', const='bcp',required=False)
    #ap.add_argument('-f','--format', nargs=1,help='Output format(bcp, postgres)', required=True)
    args = arg.parse_args()
    valid_output_types=['bcp','postgres']
    print 'args :',args
    print args.queue
    print args.blob
    input_from_file=[]
    if args.input_file:
        filename=args.input_file
        input_from_file=[each_company.strip('\r\n\t ') for each_company in open(filename,'r').readlines()]
        
    driver_timestamp=log_time_stamp()
    browser=webdriver.Chrome()
    # browser=webdriver.Firefox()
    webhooks='https://hooks.slack.com/services/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'    
    output_json={
        "attachments": [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#808080",
            "pretext": "Company Search Code",
            "author_name": str(socket.gethostbyname(socket.gethostname())),
            "text": "",
            "fields": [
                {
                    "title": "Priority",
                    "value": "High",
                    "short": True
                }
            ],
            "ts": 123456789
        }
        ]
    }
    search_ins=CompanyWebsiteSearch(developer_mode=False,re_run_mode=False,use_deeper_analysis=True,search_method='DuckDuckGo',financial_domains_to_check=['wikipedia'],browser_instance=browser)
    # search_ins=CompanyWebsiteSearch(developer_mode=False,re_run_mode=False,use_deeper_analysis=True,search_method='DuckDuckGo',financial_domains_to_check=['wikipedia'])
    item_count =0 
    # for each_line in ins_r:
    company_processed=0
    start_time = datetime.now()
    while True:
        # ins_io.open(each_line.strip('\\n '))
        # each_item=ins_io.read(output_format='dict',column_structure=['company_name','country','company_id'])
        # each_item=each_item[0]
        each_item=''
        if input_from_file:
            # print 'Input from file : Yes',input_from_file
            try:
                ins_read=InputOutput('Feed')
                ins_read.open(input_from_file[item_count])
                each_item=ins_read.read(output_format='dict',column_structure=['company_name','country','company_id'])[0]                 
            except Exception as e :
                print 'error in getting input file',e
                each_item=''
        elif args.queue:
            print 'Input from queue',args.queue
            each_item=read_input_queue(args.queue)[0]
            
        if not each_item: 
            print 'no more companies to process'
            print 'Took {} time to process {} companies'.format(datetime.now()-start_time,item_count)
            exit()
        if True and each_item:#len(each_item) > 2:
            item_count += 1
            # if item_count<=160: continue
            #print each_item
            #exit()
            try:
                print str(item_count) + '\\t Processing:\\t' + each_item['company_name']
            except:
                print str(item_count) + '\\t Processing:\\t' + repr(each_item['company_name'])
                
            if len(each_item['country']) == 0: each_item['country']=None
            if args.queue:
                mark_input_queue_consumed(each_item['q_message_id'],each_item['q_pop_receipt'],args.queue)
            try:
                func_result=search_ins.get_company_website(each_item['company_name'],country_name=each_item['country'],record_identifier=each_item['company_id'])                 
            except Exception as e:
                print str(e)
                date_string='<!date^'+str(int(time.time()))+'^{date_num} {time} - |Error occured in date>'
                output_json['attachments'][0]['text']=date_string+' '+str(e)
                requests.post(webhooks,json=output_json)
                
                # print str(item_count) + '. WEBSITE IDENTIFIED:\\t' + str(each_item) + ':\\t' + str(func_result)
            # try:
                # this_azure_upload('CompanyWebsites.stat.txt',timestamp=driver_timestamp)
            # except Exception as e:
                # print str(e)
                # date_string='<!date^'+str(int(time.time()))+'^{date_num} {time} - |Error occured in date>'
                # output_json['attachments'][0]['text']=date_string+' '+str(e)
                # requests.post(webhooks,json=output_json)
            # try:    
                # this_azure_upload('ddg_company_search_result.txt',timestamp=driver_timestamp)
            # except Exception as e:
                # print str(e)
                # date_string='<!date^'+str(int(time.time()))+'^{date_num} {time} - |Error occured in date>'
                # output_json['attachments'][0]['text']=date_string+' '+str(e)
                # requests.post(webhooks,json=output_json)
            company_processed+=1
        time.sleep(2)
            #break
        # if item_count >= 100000: break
    print 'Process completed'
    print 'Took {} time to process {} companies'.format(datetime.now()-start_time,item_count)
    # ins_r.close()