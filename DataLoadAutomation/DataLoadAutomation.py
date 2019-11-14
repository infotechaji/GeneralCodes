"""
Description : Downloads Blob,Combines the downloaded files,Creates Bat file and executes it to fetch data to the table.
Version : v1.9
History : 
            v1.1 - 03/20/2018 - Initial version 
            v1.2 - 03/21/2018 - Sending status mail is added and enable using variable "send_mail"
            v1.3 - 03/21/2018 - Variables disable_DownloadBlob,disable_CreateBatFile,disable_CombineFiles are added to disable the respective task
            v1.4 - 04/18/2018 - option "encode" enabled in the command prompt.
            v1.5 - 08/21/2018 - Table support dependency is removed
            v1.6 - 09/05/2018 - option "use_source_only" added to Ignore dependency for 'staging/data' directory - helps while  not download the blobs
            v1.7 - 09/05/2018 - option "wd" is used to give the directory to create luigi(Output files )
            v1.8 - 09/05/2018 - option "table_suffix" added to give the table suffix while loading data (added in class CreateBatFile,RunBatFile)
            v1.9 - 09/06/2018 - option 'use_table_support' is added to get the table details (to load ) from file "TableSuppport.txt" - older method
            
Pending : To enable 'TableSuppport.txt' file dependency as a additional feature 
            
            
"""
#code_list=['basic_details','indeed_jobs','career_jobs','home_page_scrap','newscode','chatbot','hiring_page_classified',
    #'pr_classification','facebook_post','twitter_post','facebook_activity','twitter_activity','govt_contracts',
    # 'facebook_search','twitter_search'

import luigi
import time,os,pyodbc
from luigi.contrib.external_program import ExternalProgramTask
from BatchSupport_new import *
from BCPSupport_v2 import *
from StatusMail import *
import datetime
import logging
from TableSupport import *
# try:
    # logging.basicConfig(filename='DataLoadAutomation.log') # for logging luigi commands 
# except: 

logging.basicConfig(filename='DataLoadAutomation.log') # for logging luigi commands 
# DB_HOST="fiimynt.database.windows.net"
# DB_USERNAME="fiinduser@fiimynt"#@fiimynt.database.windows.net
# DB_PASSWORD="myntraF!!nd"
# DB_DATABASE="fiimynt"

# DB_HOST="minicusdb.fiindlabs.com"
# DB_USERNAME="mini_select"
# DB_PASSWORD="select@123"
# DB_DATABASE="minicus_prod_0116"


# DB_HOST="13.84.135.176"
# DB_USERNAME="fiinduser"
# DB_PASSWORD="Welcome$11nd"
# DB_DATABASE="minicus_prod_0213"
# DEVELOPER_MODE=False

# DB_HOST="clds1.fiindlabs.com"
# DB_USERNAME="fluke"
# DB_PASSWORD="fluke$@1234"
# DB_DATABASE="Fluke"

# DB_HOST="clds1.fiindlabs.com"
# DB_USERNAME="sa"
# DB_PASSWORD="Welcome$11nd"
# DB_DATABASE="fiidge"

# DB_HOST="minicus.database.windows.net"
# DB_USERNAME="fiinduser"
# DB_PASSWORD="Welcome$11nd"
# DB_DATABASE="minicus_prod"
# TABLE_SCHEMA='unicode'

DB_HOST="xxxxxxxx"
DB_USERNAME="xxxx"
DB_PASSWORD="xxxx"
DB_DATABASE="xcxcxc"
TABLE_SCHEMA='xcxc'
#TABLE_SCHEMA='core_automation'
DEVELOPER_MODE=False
#send_mail=False

class DownloadBlob(luigi.Task): # get blob name and downloads the blob using azcommand 
    blob_name=luigi.Parameter(default='')
    code_key=luigi.Parameter(default='')
    source_directory=luigi.Parameter(default=os.getcwd())
    journal_directory=luigi.Parameter(default=os.path.join(os.getcwd(),'_journal')) # default it takes journal directory as the output directory
    result_dict={}
    receivers=luigi.Parameter(default='')
    send_mail=luigi.BoolParameter(default=False)
    wd=luigi.Parameter(default='')
    def output(self):
        if DEVELOPER_MODE : print 'DownloadBlob output started'
        local_target='DownloadBlob_started'+self.code_key+'.txt'
        if self.wd:# if working_directory means , the output files will be created 
            local_target=os.path.join(self.wd,local_target)
        return luigi.LocalTarget(local_target)
        if DEVELOPER_MODE : print 'DownloadBlob output completed'
    def run(self):
        if DEVELOPER_MODE : print 'DownloadBlob run started '
        if self.blob_name:
            print 'Blob Name:' ,self.blob_name
            result_dict= download_blob_usingAzcopy(blobname=self.blob_name,destination_path=self.source_directory,journal_path=self.journal_directory,use_local_exe_path=False)
            if result_dict:
                print 'Blob'+str(self.blob_name)+' is  downloaded to :'+str(self.source_directory)
            self.output().open('w').close()
    def on_success(self):
        print 'DownloadBlob : On success called !!'
        if self.send_mail : send_status_email(task=DownloadBlob(),receivers=self.receivers,success=True,test_mail=True)
    def on_failure(self,exception):
        print 'DownloadBlob Failure  called ' 
        print 'Exception in DownloadBlob :',exception
        if self.send_mail : send_status_email(task=DownloadBlob(),receivers=self.receivers,success=False,test_mail=True,exception=exception)

class CombineFiles(luigi.Task): # get blob name and run azcommand to blob date
    blob_name=luigi.Parameter(default='')
    code_key=luigi.Parameter(default='') #* # Use  any one of code_key or file_details . for more code_key refer code_list give above
    source_directory=luigi.Parameter(default=os.getcwd()) #*
    journal_directory=luigi.Parameter(default='')
    destination_directory=luigi.Parameter(default='')
    file_details=luigi.Parameter(default='')
    file_details_dict={}
    file_extension=luigi.Parameter(default='')
    encode=luigi.Parameter(default=True)
    combine_files_dict={}
    receivers=luigi.Parameter(default='')
    disable_DownloadBlob=luigi.BoolParameter(default=False)
    send_mail=luigi.BoolParameter(default=False)
    use_source_only=luigi.BoolParameter(default=False)
    wd=luigi.Parameter(default='')
    def requires(self): # the given blob will be downloaded
        if DEVELOPER_MODE : print 'CombineFiles requires started'
        if self.disable_DownloadBlob:
            return None
        else:
            return DownloadBlob(blob_name=self.blob_name,journal_directory=self.journal_directory,source_directory=self.source_directory,receivers=self.receivers,send_mail=self.send_mail,code_key=self.code_key,wd=self.wd) #  downloads the blob to the given input path
        if DEVELOPER_MODE : print 'CombineFiles requires completed'
    def output(self):   
        if DEVELOPER_MODE : print 'CombineFiles output started'
        local_target='CombineFiles_started'+self.code_key+'.txt'
        if self.wd:# if working_directory means , the output files will be created 
            local_target=os.path.join(self.wd,local_target)
        return luigi.LocalTarget(local_target)
    def run(self):
        if DEVELOPER_MODE: print 'CombineFiles run started'
        print 'self.use_source_only :',self.use_source_only
        if self.use_source_only:
            downloaded_path=self.source_directory
        else:
            if os.sep+'data' not in self.source_directory and os.sep+'staging' not in self.source_directory:
                if DEVELOPER_MODE: print 'The downloaded path is created now!!!'
                downloaded_path=os.path.join(self.source_directory,'staging'+os.sep+'data')
            else:
                if DEVELOPER_MODE: print 'Downloaded path is given already !!!'
                downloaded_path=self.source_directory
        print 'downloaded_path :',downloaded_path
        self.destination_directory=os.path.join(self.source_directory,'combined') # Combined files will be saved in this path
        if DEVELOPER_MODE: print 'self.destination_directory :',self.destination_directory
        if DEVELOPER_MODE:  print 'downloaded path :',downloaded_path
        if self.file_details:
            for i in self.file_details.split(','):
                self.file_details_dict[i]=i
            if DEVELOPER_MODE: print 'self.file_details_dict:',self.file_details_dict 
        input_dict={'source_directory':downloaded_path, # path contains the downloaded files.
                    'destination_directory':self.destination_directory, # path where the combined files will be created 
                    'code_key':self.code_key,
                    'file_details':self.file_details_dict,
                    'file_extension':self.file_extension,
                    'encode':self.encode}
        print 'Input Dict:', input_dict
        if DEVELOPER_MODE:  print 'input_dict in (Before calling combine files ) CombineFiles:',input_dict
        combine_files_dict=combine_files(input_dict)
        if combine_files_dict:
            if DEVELOPER_MODE:  print 'combine_files_dict : after combining files  result dict :',combine_files_dict
        self.output().open('w').close()
        if DEVELOPER_MODE: print 'CombineFiles run completed'
    def on_success(self):
        print 'CombineFiles : On success called !!'
        if self.send_mail : send_status_email(task=CombineFiles(),receivers=self.receivers,success=True,test_mail=True)
    def on_failure(self,exception):
        print 'CombineFiles Failure  called ' 
        print 'Exception in CombineFiles :',exception
        if self.send_mail : send_status_email(task=CombineFiles(),receivers=self.receivers,success=False,test_mail=True,exception=exception)

class CreateBatFile(luigi.Task): # get blob name and run azcommand to blob date
    blob_name=luigi.Parameter(default='')
    code_key=luigi.Parameter(default='')  # can be used for getting the key values
    source_directory=luigi.Parameter(default=os.getcwd())
    destination_directory=luigi.Parameter(default='')
    journal_directory=luigi.Parameter(default='')
    file_details=luigi.Parameter(default='')
    file_extension=luigi.Parameter(default='')
    encode=luigi.Parameter(default=True)
    batfilename=luigi.Parameter(default='default.bat') # *
    disable_DownloadBlob=luigi.BoolParameter(default=False)
    disable_CombineFiles=luigi.BoolParameter(default=False)
    receivers=luigi.Parameter(default='')
    bcp_out_file=luigi.Parameter(default='')
    send_mail=luigi.BoolParameter(default=False)
    encode=luigi.BoolParameter(default=True)
    use_source_only=luigi.BoolParameter(default=False)
    table_suffix=luigi.Parameter(default='')
    wd=luigi.Parameter()
    use_table_support=luigi.BoolParameter(default=False)
    def requires(self):
        if DEVELOPER_MODE: print 'CreateBatFile requires started '
        if self.disable_CombineFiles:
            return None
        else:
            return CombineFiles(blob_name=self.blob_name,source_directory=self.source_directory,code_key=self.code_key,file_details=self.file_details,receivers=self.receivers,disable_DownloadBlob=self.disable_DownloadBlob,send_mail=self.send_mail,encode=self.encode,use_source_only=self.use_source_only,wd=self.wd) 
        if DEVELOPER_MODE: print 'CreateBatFile requires completed '
    def output(self):
        if DEVELOPER_MODE: print 'CreateBatFile output started '
        local_target='CreateBatFile_started'+self.code_key +'.txt'
        if self.wd:# if working_directory means , the output files will be created 
            local_target=os.path.join(self.wd,local_target)
        return luigi.LocalTarget(local_target)
    def run(self):
        if DEVELOPER_MODE:  print 'CreateBatFile run started '
        if '.bat' not in self.batfilename:
            print '.bat added to the given filename '
            self.batfilename=self.batfilename+'.bat'
        self.batfilename=self.batfilename.replace('.bat','_'+str(self.code_key)+'.bat')   
        destination_directory=os.path.join(self.source_directory,'temp_files') # encoded files will be saved in this  folder
        combined_directory=os.path.join(self.source_directory,'combined') # combined files in this folder
        batfilename_updated=os.path.join(self.source_directory,self.batfilename)
        if DEVELOPER_MODE: print 'input directory :',self.source_directory
        if DEVELOPER_MODE: print 'destination_directory :',destination_directory
        if DEVELOPER_MODE: print 'combined directory:',combined_directory
        if DEVELOPER_MODE: print 'batfilename_updated :',batfilename_updated
        bcp_ins=BCPSupport(developer_mode=True)
        success_flag=''
        print 'use_table_support Status : ',self.use_table_support
        if self.use_table_support:
            TABLE_SUPPORT=open('TableSupport.txt').readlines()
        else:
            TABLE_SUPPORT=getTablesList(code_key=self.code_key,schema=TABLE_SCHEMA,table_suffix=self.table_suffix) # Table suffix can be given using variable "table_suffix"
        print 'Total files in to be loaded :',len(TABLE_SUPPORT)
        countt=0
        for each_line  in TABLE_SUPPORT:
            countt+=1
            splits=each_line.strip(' \n\r\t').split('\t')
            file_pattern=splits[0]
            schema=splits[1]
            table_name=splits[2]
            if DEVELOPER_MODE: print countt,file_pattern
            self.bcp_out_file='bcp_details_'+str(self.blob_name)+'_'+str(get_printable_time_stamp())+'.txt'
            bcp_path=os.path.join(os.getcwd(),'bcp_files')
            if not os.path.exists(bcp_path):
                try:
                    os.makedirs(bcp_path)
                    print 'Folder created : bcp_files'
                except Exception as exc: 
                    print 'Exception in making directory !!'
            self.bcp_out_file=os.path.join(bcp_path,self.bcp_out_file)
            print self.bcp_out_file
            bcp_ins.set_configuration(input_directory=combined_directory,file_pattern='*'+file_pattern+'*',output_directory=destination_directory,target_schema_name=schema,target_table_name=table_name,database=DB_DATABASE,server=DB_HOST,user=DB_USERNAME,password=DB_PASSWORD,bcp_out=self.bcp_out_file) # bcp_details.txt
            success_flag=bcp_ins.construct_bcp_commands(batfilename=batfilename_updated,convert_file=False)
        self.output().open('w').close()
        if DEVELOPER_MODE: print 'CreateBatFile run completed '
    def on_success(self):
        print 'CombineFiles : On success called !!'
        if self.send_mail : send_status_email(task=CreateBatFile(),receivers=self.receivers,success=True,test_mail=True)
    def on_failure(self,exception):
        print 'CombineFiles Failure  called ' 
        print 'exception in CombineFiles :',exception
        if self.send_mail : send_status_email(task=CreateBatFile(),receivers=self.receivers,success=False,test_mail=True,exception=exception)

class RunBatFile(luigi.Task): # get blob name and run azcommand to blob date
    blob_name=luigi.Parameter(default='')
    code_key=luigi.Parameter(default='') 
    source_directory=luigi.Parameter(default=os.getcwd())
    destination_directory=luigi.Parameter(default='')
    journal_directory=luigi.Parameter(default='')
    file_details=luigi.Parameter(default='')
    file_extension=luigi.Parameter(default='')
    encode=luigi.Parameter(default=True)
    batfilename=luigi.Parameter(default='default.bat') # 
    receivers=luigi.Parameter(default='')
    disable_DownloadBlob=luigi.BoolParameter(default=False)
    disable_CombineFiles=luigi.BoolParameter(default=False)
    disable_CreateBatFile=luigi.BoolParameter(default=False)
    send_mail=luigi.BoolParameter(default=False)
    encode=luigi.BoolParameter(default=True)
    use_source_only=luigi.BoolParameter(default=False)
    wd=luigi.Parameter(default='')# working_directory - In which the luigi files are created.
    table_suffix=luigi.Parameter(default='') # can be loaded into another tables using suffix
    use_table_support=luigi.BoolParameter(default=False)
    def requires(self):
        if DEVELOPER_MODE: print 'RunBatFile requires started '
        print 'self.disable_CreateBatFile :',self.disable_CreateBatFile
        if self.disable_CreateBatFile:
            print 'disable_CreateBatFile satisfied !!'
            return None
        else:
            return CreateBatFile(blob_name=self.blob_name,code_key=self.code_key,source_directory=self.source_directory,batfilename=self.batfilename,file_details=self.file_details,receivers=self.receivers,disable_DownloadBlob=self.disable_DownloadBlob,disable_CombineFiles=self.disable_CombineFiles,send_mail=self.send_mail,encode=self.encode,use_source_only=self.use_source_only,wd=self.wd,table_suffix=self.table_suffix,use_table_support=self.use_table_support)
        if DEVELOPER_MODE: print 'RunBatFile requires completed'
    def output(self):
        if DEVELOPER_MODE: print 'RunBatFile output started '
        local_target='RunBatFile_started'+self.code_key+'.txt'
        if self.wd:# if working_directory means , the output files will be created 
            local_target=os.path.join(self.wd,local_target)
        return luigi.LocalTarget(local_target)
    def run(self):
        if DEVELOPER_MODE: print 'RunBatFile run started '
        if DEVELOPER_MODE: print 'Before Changing Directory:',os.getcwd()
        if '.bat' not in self.batfilename: # appending 
            print 'bat added to the given filename '
            self.batfilename=self.batfilename+'.bat'
        self.batfilename=self.batfilename.replace('.bat','_'+str(self.code_key)+'.bat')  
        try:
            bat_file_full_path=os.path.join(self.source_directory,self.batfilename)
            print 'bat_file_full_path :',bat_file_full_path
            try:
                os.system(bat_file_full_path)
            except:
                os.chdir(self.source_directory)
                os.system(self.batfilename)
            self.output().open('w').close()
            print 'RunBatFile run completed '
        except Exception as e :
            print 'Exception in Execution of batfile ',e
    def on_success(self):
        print 'RunBatFile : On success called !!'
        if self.send_mail : send_status_email(task=RunBatFile(),receivers=self.receivers,success=True,test_mail=True)
    def on_failure(self,exception):
        print 'RunBatFile Failure  called ' 
        print 'exception in RunBatFile :',exception
        if self.send_mail : send_status_email(task=RunBatFile(),receivers=self.receivers,success=False,test_mail=True,exception=exception)

def get_replaced_content(content,characters_list=['-',':',' '],replace_by=''):
    if not content: return ''
    for each_char in characters_list:
        if each_char==' ':
            content=content.replace(each_char,'_')
        else:
            content=content.replace(each_char,replace_by)
    return content

def get_printable_time_stamp(get_exact_time=False):
    c_time= str(datetime.datetime.now())
    date_time=c_time.split('.')[0]
    if get_exact_time:
        return date_time # returns 2018-05-22 12:21:22
    return get_replaced_content(date_time)

if __name__=="__main__":
    luigi.run()
#Sample Commands:

#python DataLoadAutomation.py CreateBatFile --blob-name basicdetailssmbindi4 --source-directory D:\Ajith\Luigi\BatchCode\_code\forVM\BasicFinalTest\fulltest\ --journal-directory D:\Ajith\ --code-key basic_details
#python DataLoadAutomation.py RunBatFile --blob-name basicdetailssmbindi4 --source-directory D:\Ajith\Luigi\BatchCode\_code\forVM\BasicFinalTest\successtest\ --file-details company_attributes,company_info 
# python DataLoadAutomation.py RunBatFile --blob-name basic312 --source-directory E:\Ajith\bulkEnhancement\basic_details_test --file-details company_info

#code_keys --
# Basic details          : basic_details
# Indeed jobs            : indeed_jobs
# Career Jobs            : career_jobs
# News                   : newscode
# Hiring page classified : hpc
# Tec - mx               : mx
# PR classification      : pr_classification
# Social handling        : fb_posts,tw_posts,fb_activity,tw_activity

#Additional options 