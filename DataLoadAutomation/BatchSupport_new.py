"""
    Version    : v1.1
    History    :
                v1.0 - 01/01/2016 - Initial Version
                v1.1 - 03/29/2016 - Updated download_file and added download_all_files
                v1.2 - 03/19/2018 - Function download_blob_usingAzcopy is updated to work with local directory
                v1.2.1 - 03/19/2018 - Function combine_parallel is added to execute combining files in parallel 
                v1.2.2 - 03/19/2018 -Function get_files_dictionary is added to get the details of result files in a dictionary

Issues :
    if encode=True in combine_files(), there is a chance for code termination.

"""
import sys,os
import subprocess
#sys.path.insert(0,'D:\\_code\\productjobs\\productjobs\\python\\common')
#sys.path.insert(0,os.path.join(os.getcwd(),'TechJsonFlatten'))
import multiprocessing 
from datetime import datetime
from StorageAzure import *
from Utilities import *

#from TechDataJson2Csv import *


class BatchSupport():
    def __init__(self,download_folder_name,developer_mode=False,print_instance=None):
        self.download_folder_name=download_folder_name
        self.developer_mode=developer_mode
        self.current_function_name=''
        self.initiate_print_instance(print_instance)
        self.defaults_()
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True):
        input_string=input_string_in
        if len(self.current_function_name) > 1:
            input_string='BatchSupport:' + input_string
        else:
            input_string='BatchSupport:' + input_string
        if self.print_instance:
            self.print_instance.customPrint(input_string,skip_timestamp=skip_timestamp,add_leading_space=add_leading_space)
        else:
            print (input_string)
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
    def defaults_(self):
        if not os.path.isdir(self.download_folder_name):
            self._print_('Directory does not exist:' + str(self.download_folder_name))            
    def encode_to_ucs2le(self,each_line):
        current_line=each_line
        if len(current_line.strip('\r\n\t'))>0:
            if '|^|' not in current_line and '\t' in current_line:
                current_line=current_line.replace('\t','|^|')
            if current_line.endswith('\r\n'):
                return current_line.decode('utf-8').encode('utf-16le')#.replace('\r\n','\n')
            elif current_line.endswith('\n'):
                current_line=current_line.replace('\n','\r\n')
                return current_line.decode('utf-8').encode('utf-16le')#.replace('\r\n','\n')
            else: return current_line.decode('utf-8').encode('utf-16le')#.replace('\r\n','\n')
        
    def get_files_details(self,input_file_parts,file_extension='.psql'):
        files_dict={}
        all_files=os.listdir(self.download_folder_name)
        for each_file in all_files:
            # print each_file
            # raw_input()
            key_parts=filter(lambda key : key.lower() in each_file.lower(), input_file_parts.keys())
            if len(key_parts)>0 and each_file.endswith(file_extension):
                files_dict.setdefault(key_parts[0],[])
                files_dict[key_parts[0]].append(os.path.join(self.download_folder_name,each_file))        
                
        #print 'get_files_details :\t files_dict :',files_dict
        return files_dict    
            
    def combine_all_files(self,target_folder_name,input_file_parts,file_prefix='combined',file_extension='.psql',create_target_folder=True,encode=False):
        print_prefix='combine_all_files \t'
        if not os.path.isdir(target_folder_name):
            if create_target_folder:
                create_directory(target_folder_name)
                self._print_(print_prefix + ' target folder name is created:' + str(target_folder_name))
            if not os.path.isdir(target_folder_name):
                self._print_(print_prefix + ' target folder name does not exist:' + str(target_folder_name))
                return False
        if not isinstance(input_file_parts,dict):
            self._print_(print_prefix + ' input_file_parts should be a dict but received:' + type(target_folder_name))
            return False
        # current_file_list=get_all_files('*' + file_extension,self.download_folder_name)
        current_file_list=self.get_files_details(input_file_parts,file_extension)
        print 'Total Files :',len(current_file_list)
        if not current_file_list:
            self._print_(print_prefix + ' No file available in directory:' + self.download_folder_name)
            return False
        print 
        for each_key in current_file_list:
            if len(input_file_parts[each_key])>1:
                target_file_name=re.sub(r'[^\w]*','',input_file_parts[each_key])
            else:
                target_file_name=re.sub(r'[^\w]*','',each_key)
            target_file_name=file_prefix + '_' + target_file_name
            if file_extension.lower() not in target_file_name.lower():
                target_file_name=target_file_name + '.' + file_extension
            target_file_name=os.path.join(target_folder_name,target_file_name)
            input_file_parts[each_key]=target_file_name  
                
            print ('Processing Files patttern :' + each_key)
            if encode:
                file_object=open(target_file_name,'ab')
            else:    
                file_object=open(target_file_name,'a')
            count=0    
            for index,each_file in enumerate(current_file_list[each_key]):
                count+=1
                #print count 
                input_h=open(each_file,'r')
                output_string=''
                start_collecting_lines=False
                line_no=0
                #print (count , 'Processing File:' + each_file)
                sys.stdout.write('Processing File count:'+str(count)+' \r')
                #print 'Processing File count:',count,each_file
                #print 'Processing File count:',counteach_file
                format_type=''
                for each_line in input_h:
                    #print 'each_line :',each_line
                    line_no += 1
                    if line_no == 1:
                        #print 'line_no==1 satisfied '
                        # if '--' in each_line:
                            # format_type='postgres'
                        if '|^|' in each_line:
                            format_type='bcp'
                            start_collecting_lines=True
                        elif '\t' in each_line:
                            format_type='tab format'
                            start_collecting_lines=True
                        if (not format_type) or len(format_type) == 0:
                            print ('Format is not decided:' + each_file,repr(each_line))
                            # custom_exit()
                            continue
                    if format_type == 'postgres' and (not start_collecting_lines) and each_line.startswith('COPY ') and each_line.strip('\n').endswith(') FROM stdin;') and each_line.count('(') == 1:
                        start_collecting_lines=True
                        continue
                    elif format_type == 'postgres' and start_collecting_lines and each_line.strip('\n') == '\\.':
                        #print 'Elif condition satisfied'
                        start_collecting_lines=False
                        continue
                    #print 'start_collecting_lines ',start_collecting_lines
                    if start_collecting_lines:
                        #print 'start_collecting_lines satisfied',start_collecting_lines
                        if encode:
                            #print 'encode satisfied  '
                            encoded_String=self.encode_to_ucs2le(each_line)
                            #print 'encoded_String :',encoded_String
                            if not encoded_String: 
                                print 'encoded_String not found '
                                continue
                            
                            output_string=output_string + encoded_String
                        else:
                            output_string=output_string + each_line# + '\n'
                    #print line_no,start_collecting_lines,len(output_string),each_line
                input_h.close()
                #exit()
                # self._print_(print_prefix + ' Processing file:' + each_file + ' with length:' + str(len(output_string)))
                #print 'output_string :',output_string
                self.push_content_to_file(content=output_string,encode=encode,target_file_name=input_file_parts[each_key],file_object=file_object)
                if index==(len(current_file_list[each_key])-1):
                    file_object.close()
                    print ('Finished Processing: ',each_key,'Files processed :',count)
                # print print_prefix + 'First Line',output_string.split('\n')[0]
                # for each_key in input_file_parts:
                    # if each_key.lower() in each_file.lower():
                        # self._print_(print_prefix + ' file sub part matches for file:' + each_file + ' with sub part:' + str(each_key))
                        # self.push_content_to_file(target_file_name=input_file_parts[each_key],content=output_string,encode=encode)
                        
    def push_content_to_file(self,content,encode=False,target_file_name=None,file_object=None):
        if not (target_file_name,file_object): return False
        print_prefix='push_content_to_file \t'
        if not file_object:        
            if os.path.isfile(target_file_name):
                if encode:
                    output_h=open(target_file_name,'ab')
                else:
                    output_h=open(target_file_name,'a')
            else:
                print 'File opened in write mode '
                if encode:
                    output_h=open(target_file_name,'wb')
                else:
                    output_h=open(target_file_name,'w')
            output_h.write(content)
            output_h.close()
            # print print_prefix + 'First Line',content.split('\n')[0]
            if self.developer_mode:
                self._print_(print_prefix + ' Adding content(' + str(len(content)) + ') to file:' + target_file_name )
        else:
            file_object.write(content)
            if self.developer_mode:
                self._print_(print_prefix + ' Adding content(' + str(len(content)) + ') to file:' + target_file_name )
            
def download_blob_usingAzcopy(blobname,destination_path,journal_path='',use_journal_path=True,local_exe_path='c:\\Program Files (x86)\\Microsoft SDKs\\Azure\\AzCopy',use_local_exe_path=False): # download the given blob in given directory
    result_dict={}
    source_path='https://fiindmllabs.blob.core.windows.net/'+blobname
    source_key='odsS8z/XCVaE+ccTHaaLULfvHfnDS/3tNmd/Otf99CFR7P5ckqEeFKzxPE08p5auBNQZ04GZ7vC1jxY2QCc6IQ=='
    Azcommand='Azcopy /Source:'+source_path+' /Dest:'+destination_path
    Azcommand+=' /SourceKey:'+source_key+' /S '
    if not journal_path and use_journal_path:
        Azcommand+='/Z:'+destination_path # journal path 
    if journal_path:
        Azcommand+='/Z:'+journal_path # journal path 
    if use_local_exe_path:
        os.chdir(local_exe_path) # path will be changed to execute azcopy.exe 
        print 'current working directory changed :',os.getcwd()
    cmdCommand =Azcommand
    print 'cmdCommand:',cmdCommand
    print 'Blob',blobname,'is being downloaded'
    #method1
    # process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE) #
    # output, error = process.communicate()
    #method2
    #os.popen(cmdCommand)
    if os.system(cmdCommand):
        print 'Azcopy command executed successfully'
        result_dict={'downloaded_path':destination_path,
                  'blobname':blobname}
    else:
        print  'Error in downloading the blob '
    return result_dict

# code_keys --
# Basic details          : basic_details
# Indeed jobs            : indeed_jobs
# Career Jobs            : career_jobs
# News                   : newscode
# Hiring page classified : hpc
# Tec - mx               : mx
# PR classification      : pr_classification
# Social handling        : fb_posts,tw_posts,fb_activity,tw_activity
    
def get_files_dictionary(code_key): # returns output files of a code as a dictionary 
    files_index={
                'basic_details':{'core_ui_company_attributes':'core_ui_company_attributes'
                                ,'core_ui_company_info':'core_ui_company_info'
                                ,'core_ui_company_location_details':'core_ui_company_location_details'
                                ,'core_ui_company_reference_links':'core_ui_company_reference_links'
                                ,'core_ui_people_data':'core_ui_people_data'
                                ,'core_ui_post_feed':'core_ui_post_feed'
                                }
                ,'indeed_jobs':{'core_ui_job_info':'core_ui_job_info'
                                ,'core_ui_job_classification':'core_ui_job_classification'
                                }
                ,'career_jobs':{'careerpage_with_links_1':'careerpage_with_links_1'
                                ,'jobs_results':'jobs_results'
                                ,'job_not_found':'job_not_found'
                                }
                ,'home_page_scrap':{'core_ui_company_attributes':'core_ui_company_attributes'
                                    ,'core_ui_company_info':'core_ui_company_info'
                                    }
                ,'newscode':{'core_stage_post_feed':'core_stage_post_feed'
                            }
                ,'chatbot':{'website_designed':'website_designed'
                            ,'domains_list':'domains_list'
                            ,'interesting_picks':'interesting_picks'
                            ,'mobileapps':'mobileapps'
                            ,'output_chat_window':'output_chat_window'
                            ,'sign_in':'sign_in'
                           ,'ajax_request':'ajax_request'}
                ,'hpc':{'home_page_db_match':'home_page_db_match' }
                ,'mx':{'mx':'mx' }
                ,'pr_classification':{'feeds_classified':'feeds_classified'}
                ,'fb_posts':{'core_ui_facebook_posts':'core_ui_facebook_posts'}
                ,'tw_posts':{'core_ui_twitter_posts':'core_ui_twitter_posts'}
                ,'fb_activity':{'core_ui_facebook_activity':'core_ui_facebook_activity'}
                ,'tw_activity':{'core_ui_twitter_activity':'core_ui_twitter_activity'}
                ,'govt_contracts':{'contracts_output':'contracts_output'}
                ,'facebook_search':{'core_ui_facebook_search':'core_ui_facebook_search'}
                ,'twitter_search':{'core_ui_twitter_search_':'core_ui_twitter_search_'}
            }
    return files_index[code_key]

def combine_files(input_dict,execute_parallel=False):
    res_dict={}
    start_time=str(datetime.datetime.now())
    print 'BatchSupport_new:\tcombine_parallel: \t'
    print 'input_dict :',input_dict
    file_details_updated=''
    total_processes=[]
    if not input_dict['file_details'] and not input_dict['code_key']:
            print 'Please provide code_key=\'some_key\' or file_details{} '
            exit()
    if input_dict['file_details']: pass
    elif input_dict['code_key']:
        if str(input_dict['code_key']).lower()=='tech':
            results =JsonToFile(input_directory=input_dict['source_directory'],output_directory=input_dict['destination_directory'])
            return True
        else:
            file_details_updated=get_files_dictionary(input_dict['code_key']) # get all the file patterns for the code 
            print '\nfile_details:',input_dict['file_details']
    if not file_details_updated:
        file_details_updated=input_dict['file_details']
    bs=BatchSupport(download_folder_name=input_dict['source_directory'])
    try:
        if execute_parallel: # each file will be combined in separate threads
            file_count=0
            for each_file in file_details_updated:
                file_count+=1
                print file_count, each_file
                p_file_details={each_file:file_details_updated[each_file]}
                p=multiprocessing.Process(target=bs.combine_all_files,args=(input_dict['destination_directory'],p_file_details,'combined',input_dict['file_extension'],True,input_dict['encode']))
                total_processes.append(p) # all process will be appended here
                p.start()
        else:
            bs.combine_all_files(target_folder_name=input_dict['destination_directory'],input_file_parts=file_details_updated,file_prefix='combined',file_extension=input_dict['file_extension'],encode=input_dict['encode'])
        if execute_parallel:
            for each_process in total_processes: # to achive dependency of all the threads
                each_process.join()
        print "All files are combined successfully !!!"
        print 'code started :',start_time
        print 'code completed :',datetime.datetime.now()
        res_dict={'output_directory':input_dict['destination_directory']}
    except Exception as e:
        print 'Exception in combining files : ',e
        pass
    return res_dict
             


if __name__ == '__main__':
    if not  True:
        bs=BatchSupport(download_folder_name='E:\\Ajith\\_data\\PublicCompanies\\Public_1118\\Output\\Basicdetails_missing\\staging\\data') # directory should be changed
        file_details={
        
        # 'News_Process_core_stage_post_feed':'News_Process_core_stage_post_feed'
        # 'HG_Microsoft_DUNS_Location_2017-10-08_distinct_domain_output':'HG_Microsoft_DUNS_Location_2017-10-08_distinct_domain_output'
        #'company_search_result':'company_search_result'
        #'core_ui_job_info':'core_ui_job_info'
        #'CompanyWebsites':'CompanyWebsites'
        # 'ddg_company_search_result':'ddg_company_search_result'
        #fb posts/twt posts
        # 'job_info_class_output_output':'job_info_class_output_output'
        # 'core_ui_twitter_posts':'core_ui_twitter_posts'
        # ,'core_ui_twitter_activity':'core_ui_twitter_activity'
        # ,'core_ui_twitter_search':'core_ui_twitter_search'
        #  'core_ui_facebook_posts':'core_ui_facebook_posts'
        #'core_ui_facebook_activity':'core_ui_facebook_activity'
         #'core_ui_facebook_search':'core_ui_facebook_search'
        #gov contracts
        #'contracts_output':'contracts_output'
        #job title classification
        #'profoundJobtitleClassification_output':'profoundJobtitleClassification_output'
        #home page scrape
        #'core_ui_company_attributes':'core_ui_company_attributes'
        #,'core_ui_company_info':'core_ui_company_info'
        #ajax
        # 'website_designed':'website_designed'
        # ,'domains_list':'domains_list'
        # ,'interesting_picks':'interesting_picks'
        # ,'mobileapps':'mobileapps'
        # ,'output_chat_window':'output_chat_window'
        # ,'sign_in':'sign_in'
       # ,'ajax_request':'ajax_request'
        # ,'contracts_output':'contracts_output'
        # jobs scrapy
        #'home_page_db_match':'home_page_db_match'
        #'core_ui_twitter_search_':'core_ui_twitter_search_'
        #jobs career
        #'careerpage_with_links_1':'careerpage_with_links_1'
        #'jobs_results':'jobs_results'
        # ,'job_not_found':'job_not_found'
        # facebook posts
        #'core_ui_facebook_posts':'core_ui_facebook_posts'
        #'core_ui_twitter_posts':'core_ui_twitter_posts'
        #news
        #'core_stage_post_feed':'core_stage_post_feed'
        #'core_stage_post_feed':'core_stage_post_feed'
        #PR classification parallel
        #'feeds_classified':'feeds_classified'
        # #basic details
        # 'core_ui_company_attributes':'core_ui_company_attributes'
        # ,'core_ui_company_info':'core_ui_company_info'
        # ,'core_ui_company_location_details':'core_ui_company_location_details'
        # ,'core_ui_company_reference_links':'core_ui_company_reference_links'
        # ,'core_ui_people_data':'core_ui_people_data'
        # ,'core_ui_post_feed':'core_ui_post_feed'
        #jobs indeed
         #'core_ui_job_info':'core_ui_job_info' 
        # ,'search_results':'search_results'
        #,'core_ui_job_info_classification_pre_calcualtion':'core_ui_job_info_classification_pre_calcualtion'
        # 'core_stage_post_feed':'core_stage_post_feed'
         # 'patents_output':'patents_output'
        # 'core_stage_mob':'core_stage_comp_social_links'
        #,'core_stage_company_info_details':'core_stage_company_info_details'
        # 'core_stage_company_info':'core_stage_company_info'
        #'core_ui_company_info':'core_ui_company_info'
        # ,'core_stage_company_reference_links':'core_stage_company_reference_links'
        #,'core_ui_company_reference_links':'core_ui_company_reference_links'
        # 'core_ui_company_attributes':'core_ui_company_attributes'
        #,'core_ui_company_attributes':'core_ui_company_attributes'
        # #,'core_stage_key_initiatives':'core_stage_key_initiatives'
        #,'core_ui_location_details':'core_ui_location_details'
        #,'core_ui_company_location_details':'core_ui_company_location_details'
        #,'core_ui_people_data':'core_ui_people_data'
        #,'process_stats':'process_stats'
        #'core_ui_post_feed':'core_ui_post_feed'
        #,'core_ui_web_page_details':'core_ui_web_page_details'
        # 'CompanyWebsites':'CompanyWebsites'
        # ,'ddg_company_search_result':'core_stage_.ddg_company_search_results'
        # 'process_stats.log':'process_stats.log'
        # 'core_stage.Location':'core_stage.Location',
        # 'core_stage.Error':'core_stage.Error'
        # 'ajax_request':'ajax_request'
        # ,'domains_list':'domains_list'
        # ,'interesting_picks':'interesting_picks'
        # 'mobileapps':'mobileapps'
        # ,'output_chat_window':'output_chat_window'
        # ,'sign_in':'sign_in'
        # ,'website_designed':'website_designed'
        # 'core_ui_people_data':'core_ui_people_data'
        # 'sign_in':'sign_in'
        # 'home_page_db_match':'home_page_db_match'
            'company_info':'company_info'
        }
        bs.combine_all_files(target_folder_name='E:\\Ajith\\_data\\PublicCompanies\\Public_1118\\Output\\Basicdetails_missing\\staging\\data\\combined',input_file_parts=file_details,file_prefix='combined',file_extension='',encode=True)

    if not True:
        blobname="basicdetailssmbindi4"
        output_directory='D:\\Ajith\\Luigi\\BatchCode\\_code\\forVM\\BasicFinalTest\\set6'
        print 'line before download_blob_usingAzcopy call'
        journal_directory=os.path.join(os.getcwd(),'_journal')
        download_blob_usingAzcopy(blobname,output_directory,journal_path=journal_directory,use_local_exe_path=False)
    if True:
        source_directory='E:\\Ajith\\_code\\Basic_details_april_test\\_data'
        destination_directory=os.path.join(source_directory,'combined')
        #destination_directory=os.path.join(source_directory,'combined')
        code_key='basic_details'
        #file_details={'company_info':'company_info'}
        file_details={}
        file_extension=''
        encode=True
        input_dict= {'source_directory':source_directory,
                    'destination_directory':destination_directory,
                    'code_key':code_key,
                    'file_details':file_details,
                    'file_extension':file_extension,
                    'encode':encode}
        print 'input_dict before calling :',input_dict
        combine_files(input_dict,execute_parallel=False)

        
        input_dict= {'source_directory':source_directory,'destination_directory':os.path.join(source_directory,'combined'),
                    'code_key':'basic_details','file_details':{},'file_extension':'','encode':True}
        #print 'input_dict before calling :',input_dict
        combine_files(input_dict,execute_parallel=False)