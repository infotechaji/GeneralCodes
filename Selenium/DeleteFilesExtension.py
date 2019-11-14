"""
Funcationality  : Custom deletion of files 
Version : v1.1
History : 
          v1.0 - 12/11/2018 - initial version 
          v1.1 - 12/17/2018 - deletion of selected files in a directory is added to the function delete_selected_files()

Pending :
Issues : 

"""
import os,sys
import os.path
from os import path

def delete_selected_files(input_directory,delete_extension='',skip_extension='',files_list=[]):
        delete_files_count=0
        if files_list:
            for each_file in files_list:
                file_to_be_deleted=os.path.join(input_directory,each_file)
                if path.exists(file_to_be_deleted):
                    os.remove(file_to_be_deleted)
                    print 'File deleted ',each_file
                else: print 'File doent\'t exists !!',file_to_be_deleted
                
        elif input_directory and not files_list:
            for root, dirs, files in os.walk(input_directory):    
                    for each_file in files:
                        if each_file.endswith(delete_extension):
                            delete_files_count+=1
                            file_to_be_deleted=os.path.join(input_directory,each_file)
                            if path.exists(file_to_be_deleted):
                                os.remove(file_to_be_deleted)
                                print 'File deleted ',each_file
                            else: print 'File doent\'t exists !!',file_to_be_deleted
                    
if __name__=="__main__":
    #input_directory="E:\Ajith\_code\_code\Tech_instances\\Tech_code1_delete_test"
    #input_directory=sys.argv[1]
    #input_directory=os.getcwd()
    #extension=sys.argv[2]
    #delete_selected_files(input_directory=input_directory,delete_extension='.json')
    #delete_selected_files(input_directory=input_directory,delete_extension='.dat')
    if  True:
        input_directory=sys.argv[1]
        extension=sys.argv[2]
        delete_selected_files(input_directory=input_directory,delete_extension=extension)
    if not True :
        files_list=['AutoOpenCommand_v1.py','AutoOpenCommand_v1.txt']
        delete_selected_files(input_directory=input_directory,files_list=files_list)