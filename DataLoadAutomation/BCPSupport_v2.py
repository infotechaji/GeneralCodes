"""
    Description: This python file is used to convert files to bcp format and also create a .bat file to upload the files using bcp command
    Version    : v1.0
    History    :
                v1.0 - 01/11/2017 - Initial version
    Pending :  database name, username, password, servername to be passed as arguments
"""
import sys,os
sys.path.insert(0,os.path.join("D:\_code\productjobs\productjobs\python",'\common'))
from Utilities import *
from FileHandling import *
import pyodbc
class BCPSupport():
    def __init__(self,developer_mode=True,print_instance=None,log_process_status=True):
        self.company_name_list = []
        self.description_list = []
        self.other_language_check = False
        self.developer_mode = developer_mode
        self.log_process_status=log_process_status
        self.initiate_print_instance(print_instance)
        self.ins_fh=FileHandling(developer_mode=self.developer_mode,log_process_status=self.log_process_status,print_instance=self.print_instance)
        self.valid_configuration=False
        if self.log_process_status:
            self._print_('__init__:\t' + ' Instance created with developer_mode:' + str(self.developer_mode) + ' \t Log Process:' + str(self.log_process_status))
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='BCPSupport'
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
    def set_configuration(self,input_directory,file_pattern,database,server,user,password,target_schema_name,target_table_name,bcp_out,output_directory=None,recursive_search=False,include_timestamp=False):
        self.input_directory=input_directory
        self.file_pattern=file_pattern
        self.output_directory=output_directory
        self.recursive_search=recursive_search
        self.include_timestamp=include_timestamp
        self.database=database
        self.server=server
        self.user=user
        self.password=password
        self.target_schema_name=target_schema_name
        self.target_table_name=target_table_name
        self.bcp_out=bcp_out
        self.valid_configuration=True
        self.fetch_table_columns()
    def validate_bcp_file(self,file_name):
        file_content=''
        try:
            file_handle=open(file_name,'rb')
            file_content=file_handle.read()
            file_handle.close()
        except Exception as e:
            print "exception in validate_bcp_file : ",e
            if 'memoryerror' in (str(e).lower()):
                print 'Memory Error in opening the file ',e
                return True
            else:
                return False
            pass
        # file_first_line_org=file_first_line
        
        if file_content:
            if '\x00' in file_content:
                file_content=file_content.replace('\x00','')
                file_first_line=file_content.split('\r\n')[0]
                if '|^|' in file_first_line:
                    file_column_count=len(file_first_line.split('|^|'))
                    if file_column_count==self.column_count:
                        return True
                    else:
                        # self._print_(repr(file_first_line_org))
                        self._print_(repr(file_first_line))
                        self._print_('No of Table Columns: '+str(self.column_count)+'\t'+'No of File Columns: '+str(file_column_count)+'\t'+'Number of Columns does not match')
                        # self._print_('No of Table Columns: '+str(self.column_count))
                        # self._print_('No of File Columns: '+str(file_column_count))
                        # self._print_('Number of Columns does not match')
                        return False
            # elif '\t' in file_first_line:
                # file_column_count=len(file_first_line.split('\t'))
                # if file_column_count==self.column_count:
                    # return True
                # else:
                    # self._print_('No of Table Columns:'+self.column_count)
                    # self._print_('No of File Columns:'+file_column_count)
                    # self._print_('Number of Columns does not match')
                    # return False
            else:
                self._print_('File is not encoded to ucs2le format')
                return False
        #raw_input()
    def fetch_table_columns(self):
        # conn=pymssql.connect(database=self.database,server=self.server,user=self.user,password=self.password)
        conn_string = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.user+';PWD='+self.password
        print conn_string
        conn = pyodbc.connect(conn_string)
        cursor=conn.cursor()
        query="select count(*) from information_schema.columns where table_schema='"+self.target_schema_name+"'and table_name='"+self.target_table_name+"'"
        cursor.execute(query)
        column_count=cursor.fetchone()
        if column_count:
            self.column_count=column_count[0]
        else:
            self.column_count=0        
        conn.close()
        print self.column_count
        # self.column_count = 18
    def convert_file_to_bcp_format(self,file_name,target_file_name):
        print_prefix='convert_file_to_bcp_format:\t'
        if len(file_name) > 0  and file_name == target_file_name:
            if self.developer_mode:
                self._print_(print_prefix + 'Both source and target file names are same.' + 'Source:' + file_name + '\t Target:' + target_file_name)
                return False
        if len(file_name) == 0 or len(target_file_name) == 0:
            if self.developer_mode:
                self._print_(print_prefix + 'Either source and target file names is blank.' + 'Source:' + file_name + '\t Target:' + target_file_name)
                return False
        if not os.path.isfile(file_name):
            if self.developer_mode:
                self._print_(print_prefix + 'File does not exists.' + 'Source:' + file_name)
                return False
        if self.developer_mode:
            self._print_(print_prefix + 'Processing:' + file_name)
        input_h=open(file_name,'rb')
        output_w=open(target_file_name,'wb')
        output_string=''
        start_collecting_lines=False
        line_no=0
        format_type=''
        for each_line in input_h:
            line_no += 1
            #print format_type,start_collecting_lines,each_line
            if line_no == 1:                
                if '|^|' in each_line:
                    format_type='bcp'
                    start_collecting_lines=True
                    if self.developer_mode:
                        self._print_(print_prefix + ' Format is bcp')
                elif '\t' in each_line:
                    format_type = 'tab-delimited'
                    start_collecting_lines=True
                    if self.developer_mode:
                        self._print_(print_prefix + ' Format is tab delimited')
                elif '--' in each_line:
                    format_type='postgres'
                    if self.developer_mode:
                        self._print_(print_prefix + ' Format is postgres')        
                if (not format_type) or len(format_type) == 0:
                    print 'Format is not decided:' + file_name,repr(each_line)
                    custom_exit()
            if format_type == 'postgres' and (not start_collecting_lines) and each_line.startswith('COPY ') and each_line.count('(') == 1 and each_line.strip('\n\r').endswith(') FROM stdin;'):
                start_collecting_lines=True
                continue
            elif format_type == 'postgres' and start_collecting_lines and each_line.strip('\n\r') == '\\.':
                start_collecting_lines=False
                continue
            if start_collecting_lines:
                current_line=each_line
                if len(current_line.strip('\r\n\t'))>0:
                    if '|^|' not in current_line and '\t' in current_line:
                        current_line=current_line.replace('\t','|^|')
                    if current_line.endswith('\r\n'):
                        output_w.write(current_line.decode('utf-8').encode('utf-16le'))#.replace('\r\n','\n')
                    elif current_line.endswith('\n'):
                        current_line=current_line.replace('\n','\r\n')
                        output_w.write(current_line.decode('utf-8').encode('utf-16le'))#.replace('\r\n','\n')
        #output_w.write("\r\n".decode('utf-8').encode('utf-16le'))
        output_w.close()
    def construct_bcp_commands(self,batfilename='default.bat',convert_file=True):
        try:
            input_files_list=self.ins_fh.get_all_files(directory_is=self.input_directory,pattern=self.file_pattern,full_path=True,recursive=self.recursive_search)
            if self.output_directory:
                self.ins_fh.create_directory(self.output_directory)
            batch_h=open(batfilename,'a') # writes the content in to the bat file , will be executed to fetch data into the table
            bcp_prefix='bcp '+ self.database + '.' + self.target_schema_name + '.' + self.target_table_name + ' in ' 
            bcp_suffix=' -w -t "|^|" -S '+ self.server +' -U '+ self.user +' -P '+ self.password +' >>'+self.bcp_out
            for each_file in input_files_list:
                file_base_name=os.path.basename(each_file)
                if convert_file:
                    output_file_name=os.path.join(self.output_directory,file_base_name)
                    # self.validate_bcp_file(output_file_name)
                    print 'Output File Name',output_file_name
                    self.convert_file_to_bcp_format(each_file,output_file_name)                                
                    validity=self.validate_bcp_file(output_file_name)
                    if not validity:
                        with open('LoadingFilesError.txt','a') as target:
                            target.write(each_file+'\n')    
                        continue
                    # command_line=bcp_prefix + ' "' + output_file_name + '"' + bcp_suffix + '\n'
                else:
                    output_file_name=os.path.join(self.input_directory,file_base_name)
                    #try:
                    validity=self.validate_bcp_file(output_file_name) # 
                    # except Exception as e :
                        # print 'Exception in validating BCP file  :',e
                        # pass
                    if not validity:
                        with open('LoadingFilesError.txt','a') as target:
                            target.write(output_file_name+'\n')
                        continue
                command_line=bcp_prefix + ' "' + output_file_name + '"' + bcp_suffix + '\n'
                batch_h.write(re.sub(r' +' ,' ',command_line))
                #custom_exit()
            batch_h.close() # batch file closed 
            return True
        except Exception as e :
            print 'Exception  in creating Bat file :',e
            return False
if __name__ =='__main__':
    bcp_ins=BCPSupport(developer_mode=True)
    # bcp_ins.set_configuration(input_directory='E:\\_data\\contracts_20170815\\staging\\data\\',file_pattern='*_contracts_output*.txt',output_directory='E:\\_data\\contracts_20170815\\staging\\target\\',target_schema_name='unicode',target_table_name='govt_contracts_selfbi',database='minicus_prod',server='minicusdb.southcentralus.cloudapp.azure.com,1743',user='mini_select',password='select@123',bcp_out='cnt')
    # bcp_ins.set_configuration(input_directory='D:\_data\smbrefershc3\smbrefnewsfeedref3\staging\data',file_pattern='*core_ui_facebook_posts*.psql',output_directory='D:\\_data\\fbpostsoutput6k\\staging\\data_\\',target_schema_name='unicode',target_table_name='post_feed_social_media',database='Fluke',server='clds1.fiindlabs.com',user='Fluke',password='fluke$@1234',bcp_out='fbposts')
    bcp_ins.set_configuration(input_directory='D:\\kema\\SMB\\renewal_set2\\staging_ddg_new\\data\\',file_pattern='*CompanyWebsites.stat*',output_directory='D:\\kema\\SMB\\renewal_set2\\staging_ddg_new\\target\\',target_schema_name='unicode',target_table_name='ddg_results_renew_set2',database='minicus_prod_0213',server='13.84.135.176',user='fiinduser',password='Welcome$11nd',bcp_out='renewalddgsearch')
    # bcp_ins.set_configuration(input_directory='C:\\Users\\Gopi\\Downloads\\october_order_detaiils\\',file_pattern='october_order_detaiils',output_directory='C:\\Users\\Gopi\\Downloads\\october_order_detaiils\\bcp_support\\',target_schema_name='core_stage',target_table_name='fact_core_item_sample_data_1',database='fiimynt',server='fiimynt.database.windows.net',user='fiinduser',password='myntraF!!nd',bcp_out='fiimynt')
    bcp_ins.construct_bcp_commands(convert_file=True)
# -Umini_select -Pselect@123 -Sminicusdb.southcentralus.cloudapp.azure.com,1743