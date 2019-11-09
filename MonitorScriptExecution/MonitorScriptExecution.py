"""
Description : Script Which monitors code execution and will send periodic mail update 
History : v1.1
Version : 
          v1.0 - 05/09/2019 - initial version 
          v1.1 - 05/09/2019 - Function write_data_in_file() is updated with random waiting time 
Pending :
Open issues :
"""
from TechProcessSupport import * 
from SQLConnection import * 
from MasterGmail import * 
import random
def get_entered_arguments():
    count=0
    command='python'
    for i in sys.argv:
        count+=1
        #print 'count :',count,i
        command=command+' '+str(i)
    command=command.strip('\n')
    command+='\n'
    return command       

def execute_batch_file(batch_file_name): # executes batch file
    os.system("start cmd /c"+batch_file_name)
def write_data_in_file(file_name='processed_accounts.txt',content='',mode='a'):
    written=True
    try_count=0
    while written:
        try_count+=1
        try:
            with open(file_name,mode) as fp:
                if content:
                    try:fp.write(content+'\n')
                    except:fp.write(str(content)+'\n')
            written='yes'
            # print 'planning to rise exception !'
            # raise_exception('some error arises')
        except Exception as e :
            print 'Exception in writing processed_accounts.txt ',e
            time_seconds=random.randint(1,5)
            print 'waiting time :',time_seconds
            time.sleep(time_seconds)
        if written=='yes' or try_count>4:
            print 'File written successfully'
            break
    return True

def get_processed_accounts(file_name):
    accounts_processed=len(open(file_name).readlines())
    return accounts_processed

class MonitorScript():
    def __init__(self,mail_attributes,additional_attributes,developer_mode=False):
        self.code_started_time=datetime.datetime.now()
        self.processed_accounts_log='processed_accounts.txt'
        self.class_name='MonitorScript'
        self.developer_mode=developer_mode
        self.mail_attributes=mail_attributes
        self.additional_attributes=additional_attributes
        self.existing_processes=self.additional_attributes['existing_processes']
        self.update_vm_details()
        self.update_total_accounts()
        if self.check_record_presence(): # checks the table based on primary_key .
            exit()
    def __del__(object):
        print 'MonitorScript object deleted'
    
    def set_time_to_mail(self,time_to_mail=False):
        self.time_to_mail=time_to_mail
        timeout=datetime.timedelta(minutes=self.periodic_mail_update)# seconds=1
        self.timeout_expiration = datetime.datetime.now() + timeout
    def update_vm_details(self): # getting system details 
        vm_results=get_vm_name()
        self.mail_attributes['vm_name']=vm_results['vm_name']
        self.mail_attributes['host_name']=vm_results['host_name']
        self.mail_attributes['ip_address']=vm_results['ip_address']
        self.mail_attributes['user_name']=vm_results['user_name']
    def update_total_accounts(self): # update code_execution_status,data_loading_status,error comments will be updated 
        input_file=self.additional_attributes['input_file']
        if input_file:
            total_accounts=len(open(input_file).readlines())
            if total_accounts<1: 
                print 'Input File "'+str(input_file)+'" has no data to process  !!'
                exit()
            # if self.mail_attributes['total_instances']>1:
                # result_dict=split_files(input_file,no_of_files=self.mail_attributes['total_instances'])
                # self.splitted_file_names=result_dict['splitted_file_names']
            self.mail_attributes['input_type']='File'
        elif self.mail_attributes['queue']:
            queue=self.mail_attributes['queue']
            self.queue_obj=CheckQueue()
            queue_count= self.queue_obj.get_queue_length(queue)
            if queue_count<1: 
                print 'Input Queue "'+str(queue)+' has no messages !!'
                exit()
            total_accounts=queue_count
            self.mail_attributes['input_type']='Queue'
            self.splitted_file_names=[]
        self.mail_attributes['total_accounts']=total_accounts
        self.mail_attributes['pending_accounts']=total_accounts
        self.mail_attributes['processed_accounts']=0
        self.mail_attributes['code_execution_status']='Running'
        self.mail_attributes['data_loading_status']='Running'
        
    def log_details(self,module_name,input_text=''): # prints time stamp with the given content.
        time_stamp=get_printable_time_stamp()
        final_text=str(time_stamp)+':\t'+str(self.class_name)+'\t'+str(module_name)+'\t'+str(input_text)
        print final_text
        
    def check_record_presence(self,scrip_check=False): # checks wheather the input record is already present or not ?
        record_check_dict={
                    'code':self.mail_attributes['code']
                    ,'project':self.mail_attributes['project']
                    ,'ip_address':self.mail_attributes['ip_address']
                    ,'owner':self.mail_attributes['owner']
                    ,'try_count':self.mail_attributes['try_count']
                    }
        module_name='check_record_presence:'
        presence=False
        select_command=get_select_command(record_check_dict)
        results=execute_query(select_command)
        presence_count=int(results[0][0])
        if self.developer_mode :
            self.log_details(module_name,'presence_count :'+str(presence_count))
        if presence_count>0: 
            presence=True
            temp_dict=record_check_dict.copy()
            temp_dict.pop('try_count')
            select_command=get_select_command(temp_dict,what_to_select='max(try_count)')
            results=execute_query(select_command)
            if self.developer_mode :
                self.log_details(module_name,'results :'+str(results))
            old_instance_count=int(results[0][0])
            new_instance_count=old_instance_count+1
            print 'Record Already exists !! and Instance count is changed  from '+str(record_check_dict['try_count'])+' to '+str(new_instance_count)
            self.mail_attributes['try_count']=new_instance_count
            presence=False
        elif presence_count==0:
            presence=False
            print 'Eligible to run with the given details !!'
            if scrip_check:
                print 'Checking Script presence...'
                script_dict=get_script_details(record_check_dict['code']) # gets all the Python script name 
                if not script_dict:
                    print 'Script "'+str(record_check_dict['code'])+'" is not found ! please check "ScriptConfig.py"\n Quiting code .'
                    exit()
                else:
                    print 'Matching script Found !!'
                    self.script_dict=script_dict
        return presence
    def update_code_execution_status(self,error=''):
        values={'active_instances':self.mail_attributes['active_instances']
                ,'pending_accounts':self.mail_attributes['pending_accounts']
                ,'processed_accounts':self.mail_attributes['processed_accounts']
                ,'data_loading_status':self.mail_attributes['data_loading_status']
                ,'code_execution_status':self.mail_attributes['code_execution_status']
                }
        if error:
            formatted_error=str(error).replace("'",'')
            values['comments']=str(formatted_error)
        #conditions={'project':self.project,'code':self.code,'try_count':self.try_count,'owner':self.owner,'ip_address':self.ip_address,'user_name':self.user_name}
        conditions={'project':self.mail_attributes['project'],'code':self.mail_attributes['code'],'try_count':self.mail_attributes['try_count'],'owner':self.mail_attributes['owner'],'ip_address':self.mail_attributes['ip_address'],'user_name':self.mail_attributes['user_name']}
        #update_command=get_update_command(values=values,conditions=conditions)
        try:
            update_command=execute_query(get_update_command(values=values,conditions=conditions))
            return True
        except Exception as  e:
            print 'Exception in update_code_execution_status() :',str(e)
        return False
    def monitor_script_execution(self,delete_current_process_id=False): # Monitors the Entire Script 
            module_name='monitor_script_execution'
            #current_python_processes=get_active_specific_process(self.existing_processes,check_process='cmd') # may change to python
            current_python_processes=self.additional_attributes['current_python_processes']
            print 'current_python_processes :',current_python_processes
            if current_python_processes or self.mail_attributes['pending_accounts']==self.mail_attributes['total_accounts']:
                if not current_python_processes:
                    current_python_processes=[0]
                #else:
                self.mail_attributes['active_instances']=len(current_python_processes)
                # Inserting new record into the table 
                #print 'Mail attributes before insertion :',self.mail_attributes
                result = execute_query(get_insert_command(self.mail_attributes))
                if self.developer_mode :
                    self.log_details(module_name,'len(current_python_processes) :'+str(len(current_python_processes)))
                process_id=os.getpid()
                print 'current process_id :',process_id
                if delete_current_process_id:
                    if process_id in current_python_processes:
                        current_python_processes.remove(process_id)
                print 'Total New Instances :',len(current_python_processes)
                self.periodic_mail_update=self.additional_attributes['periodic_mail_update']
                self.set_time_to_mail()
                while True:
                    for i in range(10):
                        sys.stdout.write(str(get_printable_time_stamp())+':  Total Active Process :'+str(len(current_python_processes)))
                        time.sleep(1)
                        sys.stdout.write('\r')
                    #time.sleep(20)
                    active_instance_changed=False
                    current_time=datetime.datetime.now()
                    if current_time>=self.timeout_expiration:
                        print 'Now the time is to send update Database Log in core_stage.  !!'
                        self.set_time_to_mail(time_to_mail=True)
                    try:
                        for index,each_process_id in enumerate(current_python_processes):
                            if not psutil.pid_exists(int(each_process_id)):
                                print "Process :",each_process_id,"Not Exists !! so removed "
                                current_python_processes.remove(int(each_process_id))
                                active_instance_changed=True
                        if active_instance_changed or self.time_to_mail :
                            if self.time_to_mail:self.time_to_mail=False
                            if self.mail_attributes['code']=='tech':
                                json_result_dict=get_processed_json_files(self.main_script_directory,args.threads)
                                temp_processed_count=json_result_dict['total_json_files']
                            else:
                                temp_processed_count=get_processed_accounts(self.processed_accounts_log)
                            self.mail_attributes['processed_accounts']=temp_processed_count
                            if len(current_python_processes)==0 or self.mail_attributes['processed_accounts']==self.mail_attributes['total_accounts']:
                                print datetime.datetime.now(),'All process are completed'
                                self.mail_attributes['code_execution_status']='Completed'
                                self.mail_attributes['data_loading_status']='Completed'
                            if self.mail_attributes['queue']:
                                self.mail_attributes['pending_accounts']=self.queue_obj.get_queue_length(self.queue)
                            elif self.additional_attributes['input_file']:
                                self.mail_attributes['pending_accounts']=self.mail_attributes['total_accounts']-self.mail_attributes['processed_accounts']
                            self.mail_attributes['active_instances']=len(current_python_processes)
                            self.update_code_execution_status()
                        if self.mail_attributes['code_execution_status'].lower()=='completed' or len(current_python_processes)==0:
                            break
                    except Exception as e:
                        print 'Exception in code exeution  :',str(e)
                        self.mail_attributes['code_execution_status']='Error'
                        self.mail_attributes['data_loading_status']='Error'
                        self.mail_attributes['active_instances']=len(current_python_processes)
                        self.update_code_execution_status(error=str(e))
                        break
                if not self.additional_attributes['disable_mail']:
                    self.send_completion_mail() 
    def send_completion_mail(self):
        gm_obj=Gmail()
        receivers=self.additional_attributes['receivers']
        type_receivers=type(receivers)
        if type_receivers==str:
            receivers=receivers.split(',')
        input_dict={}
        input_dict['subject']=str(self.mail_attributes['code'].capitalize())+' Execution completed in VM :"'+str(self.mail_attributes['vm_name'])+'" with the CodeExecutionStatus : '+str(self.mail_attributes['code_execution_status'])+'!!'
        input_dict['body']={
                            'greetings':'Hi All ,',
                            'content':'Code execution status are given below !',
                            'bottom_content':'',
                            'table_input':{
                                            'headers':{'Title':'Value'},
                                            'table_content':[
                                                                 {'vm_name':self.mail_attributes['vm_name']}
                                                                ,{'ip_address':self.mail_attributes['ip_address']}
                                                                ,{'project':self.mail_attributes['project']}
                                                                ,{'code':self.mail_attributes['code']}
                                                                ,{'owner':self.mail_attributes['owner']}
                                                                ,{'code_execution_status':self.mail_attributes['code_execution_status']}
                                                                ,{'data_loading_status':self.mail_attributes['data_loading_status']}
                                                                ,{'total_instances':self.mail_attributes['total_instances']}
                                                                ,{'total_accounts':self.mail_attributes['total_accounts']}
                                                                ,{'processed_accounts':self.mail_attributes['processed_accounts']}
                                                                ,{'pending_accounts':self.mail_attributes['pending_accounts']}
                                                                ,{'input_type':self.mail_attributes['input_type']}
                                                                ,{'queue':self.mail_attributes['queue']}
                                                                ,{'blob':self.mail_attributes['blob']}
                                                                ,{'azure_account_name':self.mail_attributes['azure_account_name']}
                                                                ,{'code_started_time':self.code_started_time}
                                                                ,{'code_completed_time':str(datetime.datetime.now())}

                                                            ]
                                            }
                            }
        input_dict['attachment']=[
                                    # {
                                    # 'file_name':'Dummy_textFile.txt',# file 1 
                                    # 'full_file_path':'D:\\Ajith\\_code\\GeneralCodes\\Mail\\Dummy_textFile.txt'
                                    # }
                                  ]
        gm_obj.send_mail(input_dict=input_dict,receivers=receivers)
if __name__=="__main__":
    write_data_in_file(content='dummy')
    raw_input('raw input')
    #get_processed_accounts(sys.argv[1])
    #raw_input('Monitor batch')
    existing_processes=get_all_process_id()
    print 'existing processes :',len(existing_processes)
    #os.system('start python test.py')
    #process_id=os.getpid()
    print 'current process_id :',process_id
    print 'current process_id type :',type(process_id)
    current_python_processes=get_active_specific_process(existing_processes,check_process='python')
    print 'current_python_processes :',current_python_processes
    print 'type(current_python_processes):',type(current_python_processes)
    if not current_python_processes:
        current_python_processes=[process_id]
    #required details 
    total_instances=1
    project='test'
    owner='ajith'
    code='indeed_jobs'
    queue=''
    blob=''
    file_name=''
    try_count=0
    azure_account_name='testing'
    mail_attributes={
            'total_instances':total_instances
            ,'project':project
            ,'code':code
            ,'owner':owner
            ,'queue':queue
            ,'blob':blob
            ,'try_count':try_count
            ,'azure_account_name':azure_account_name
            }
    additional_attributes={
                     'disable_mail':False
                    ,'periodic_mail_update':2 # minutes
                    ,'start_index':0
                    ,'receivers':'ajith@fiind.com'
                    ,'existing_processes':existing_processes
                    ,'current_python_processes':current_python_processes
                    ,'input_file':'single_domains.txt'
                }
    #less priority additonal attributes 
    #,'disable_delete_results':args.disable_delete_results
    #,'disable_load_results':args.disable_load_results
    #,'code_directory':args.code_directory
    #,'folder_suffix':args.folder_suffix
    #,'python2_path':args.python2_path
    #,'python3_path':args.python3_path
    #,'tech_header_table_name':args.tech_header_table_name
    #,'tech_data_table_name':args.tech_data_table_name
    #,'skip_backup':args.skip_backup
    #,'input_file':args.input_file
    m_obj=MonitorScript(mail_attributes,additional_attributes,True)
    m_obj.monitor_script_execution()
