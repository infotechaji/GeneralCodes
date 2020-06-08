"""
Funcationality  : Custom copy of files 
Version : v1.4
History : 
          v1.0 - 10/24/2018 - initial version 
          v1.1 - 12/11/2018 - function copytree() is modified to copy a single file
          v1.2 - 12/17/2018 - function replace_file() is added.
          v1.3 - 12/17/2018 - Time stamp option is added for copied file
          v1.4 - 03/18/2019 - Functions replicate_folder(),back_up_files(),replace_files() are added 
Pending :
Issues : 

"""
import os 
import shutil
# from DeleteFilesExtension import *
import os.path
from os import path
import datetime
#from TechProcessSupport import get_printable_time_stamp


def replace_files(source_directory,destination_directory,instances,files_list,folder_name="",start_index=1,sub_folder=''):
    if folder_name:
        source_folder=os.path.join(source_directory,folder_name)
    else:
        folder_name=source_directory.split(os.sep)[-1]
        print ('folder_name acquired :',folder_name)
        source_folder=source_directory
    for i in range(start_index,start_index+instances):
        print (i)
        destination_directory_temp=os.path.join(destination_directory,str(folder_name)+str(i))
        #destination_directory=os.path.join(destination_directory,"wig","classes")
        if sub_folder:destination_directory_temp=os.path.join(destination_directory_temp,sub_folder)
        print ('destination_directory :',destination_directory_temp)
        #print 'source_folder :',source_folder
        print ('source_directory :',source_directory)
        print ('files_list :',','.join(files_list))
        replace_file(source_directory=source_folder,destination_directory=destination_directory_temp,files_list=files_list)
        print ('Files replaced in :',destination_directory_temp)

def back_up_files(source_directory,destination_directory,instances,files_list=['v1_combined_tech_results.dat','v1_technical_data_header.dat'],start_index=1,folder_name='',sub_folder='combined'):
    print ('Trying to back_up_files from :',source_directory)
    print ('Files :',','.join(files_list))
    if not folder_name:
        folder_name=source_directory.split(os.sep)[-1]
    print ('folder_name : ',folder_name)
    print ('start_index :',start_index)
    print ('instances :',instances)
    for i in range(start_index,start_index+instances):
        current_folder=folder_name+str(i)
        print ('current_folder :',current_folder)
        source_folder=os.path.join(source_directory,current_folder)
        if sub_folder:
            source_folder=os.path.join(source_folder,sub_folder)
        try:
            copytree(src=source_folder,dst=destination_directory,files_list=files_list,file_suffix=current_folder,copy_all_files=False)
            print ('Files copied to :',destination_directory)
        except Exception as e:
            print ('Exception while getting backup copy !!')
            pass
def replicate_folder(source_directory,destination_directory='',instances=1,start_index=1,folder_name='',copy_in_parent=True):
    copied_list=[]
    if destination_directory=="":
        destination_directory=source_directory
    if copy_in_parent==True:
        destination_directory=destination_directory.strip(os.sep+str(destination_directory.split(os.sep)[-1]))
    if folder_name:
        source_folder=os.path.join(source_directory,folder_name)    
    else:
        folder_name=source_directory.split(os.sep)[-1]
        source_folder=source_directory
    for i in range(start_index,start_index+instances):
        #pathname = os.path.join(destination_directory,folder_name+str(i+1))
        pathname = os.path.join(destination_directory,folder_name+str(i))
        print ('replicated successfully :',pathname)
        #shutil.copy(source_folder,pathname)
        try:
            copytree(source_folder,pathname)
        except Exception as e :
            print ('Exception ',e)
            #print ('Exception while copying from '+source_folder+' to '+)
            pass
        copied_list.append(pathname)
    return {'source_directory':source_folder,
            'replicated_directory':copied_list,
            'total_folders':len(copied_list),
            }

def replace_file(source_directory,destination_directory,files_list=[]): # replaces files in the destination folders 
    #source check 
    
    delete_selected_files(input_directory=destination_directory,files_list=files_list)
    #copy the files to destination directory
    copytree(src=source_directory,dst=destination_directory,files_list=files_list,copy_all_files=False)

def copy_file(src, dst,files_list='',file_suffix='', copy_all_files=False,symlinks=False,ignore=None,add_time_stamp=False):
    if copy_all_files and not files_list: 
        for item in os.listdir(src):
            s = os.path.join(src,item)
            d = os.path.join(dst,item)
            # print ('s :',s)
            ##md
            # print ('d :',d)
            if not os.path.exists(dst): os.makedirs(dst)
            if add_time_stamp:
                if '.' in d :
                    d=d.replace('.','_'+str(get_printable_time_stamp())+'.')
                else:
                    d=str(d)+'_'+str(get_printable_time_stamp())
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s,d)
    elif files_list:# and not copy_all_files:
        for each_file_name in files_list:
            s=os.path.join(src, each_file_name)
            #file_suffix=src.split(os.sep)[-1]
            file_name_m=each_file_name.replace('.',str(file_suffix)+'.')
            d=os.path.join(dst,file_name_m)
            # print ('source file :',s)
            # print ('destination file :',d)
            if not os.path.exists(dst): os.makedirs(dst)
            if add_time_stamp:
                if '.' in d :
                    d=d.replace('.','_'+str(get_printable_time_stamp())+'.')
                else:
                    d=str(d)+'_'+str(get_printable_time_stamp())
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks,ignore)
            else:
                shutil.copy2(s,d)
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
if __name__=="__main__":
    #source_directory=os.getcwd()
    #source_directory=sys.argv[1]
    #folder_name='Tech_code'
    #folder_name=''
    if True:
        source_directory='D:\\Ajith\\_data\\Dask_test\\Server\\_data\\Combined'
        destination_directory='D:\\Ajith\\_data\\Dask_test\\Server\\result_files'
        #files_list=['_core_ui_company_attributes_Basic_Details1','_core_ui_company_attributes_Basic_Details2']
        #copytree(src=source_directory,dst=destination_directory,files_list=files_list,file_suffix='',copy_all_files=False) # copies the selected files 
        #copy_file(src=source_directory,dst=destination_directory,files_list=[],file_suffix='_'+str(get_printable_time_stamp()),copy_all_files=True) # copies the selected files 
        copy_file(src=source_directory,dst=destination_directory,files_list=[],file_suffix='',copy_all_files=True,add_time_stamp=True) # copies the selected files 
        
    if not True: # replicate script folders 
        #destination_directory=source_directory
        destination_directory=""
        instances=2
        start_index=3
        replicate_folder(source_directory=source_directory,destination_directory=source_directory,instances=instances,folder_name=folder_name,start_index=start_index,copy_in_parent=False)
    
    if not True: # getting backup of combined files 
        source_directory='D:\\Ajith\\_data\\Dask_test\\Server\\_data\\Combined'
        destination_directory='D:\\Ajith\\_data\\Dask_test\\Server\\Data_backup'
        files_list=['_core_ui_company_attributes_Basic_Details1','_core_ui_company_attributes_Basic_Details2']
        instances=0
        folder_name
        back_up_files(source_directory,destination_directory=destination_directory,instances=instances,files_list=files_list,folder_name=folder_name,sub_folder='combined',start_index=18)
        
    if not True: # replaces existing files 
        files_list=['wig.py']
        #destination_directory=D:\Ajith\_code\_code\Techinstances\Tech_code1\wig\classes
        source_directory="E:\\_code\\Ajith\\_codes\\TechInstances"
        destination_directory="E:\\_code\\Ajith\\_codes\\TechInstances"
        folder_name="Tech_code"
        instances=4
        start_index=3
        sub_folder='wig'
        replace_files(source_directory=source_directory,destination_directory=destination_directory,instances=instances,files_list=files_list,folder_name=folder_name,sub_folder=sub_folder,start_index=start_index,copy_in_parent=True)
        