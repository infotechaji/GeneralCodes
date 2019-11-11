"""
    Version    : v2.1
    History    :
                1.0 - 01/01/2016 - Initial Version
                1.1 - 03/29/2016 - Updated download_file and added download_all_files
                2.0 - 08/29/2016 - Publishing as new version.
                2.1 - 03/21/2017 - Bucket creation functionality is added
"""

from azure.storage.blob import BlobService
import os
import sys
class PythonAZURE():
    def __init__(self, account_name, access_key, bucket = '', environment_name = 'test', secondary_folder_name= '',developer_mode=True,print_instance=None):
        self.account_name = account_name
        self.access_key = access_key
        self.bucket = bucket
        self.environment_name = environment_name
        self.sub_folder = secondary_folder_name
        self.current_folder=None
        self.connection_status=False
        self.bucket_status=False
        self.developer_mode=developer_mode
        self.my_delimiter='_'
        self.my_name='azure'
        self.current_function_name=''
        self.initiate_print_instance(print_instance)
        self.connect(account_name, access_key)
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True):
        input_string=input_string_in
        if len(self.current_function_name) > 1: 
            #input_string='HTMLHandling_New:' + self.current_function_name + ':' + input_string
            input_string='PythonAZURE:' + input_string
        else:
            input_string='PythonAZURE:' + input_string
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
    def connect(self, account_name, access_key):
        self.conn = BlobService(account_name=account_name, account_key=access_key)
        try:
            self.conn.list_containers()
            self.connection_status=True
            self.bucket_status=False
            if self.developer_mode: self._print_ ( 'Connected to ' + self.my_name + '. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return self.connection_status
        except:
            self.connection_status=False
            if self.developer_mode: self._print_ ( 'Connection is failed with error ' + str(sys.exc_info())  + '\t' + '. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return self.connection_status
    def set_bucket_name(self, bucket_name,create_if_not_exist=True,try_once_on_failure=True):
        try:
            buck_properties= self.conn.get_container_acl(bucket_name)
            self.bucket=bucket_name
            self.bucket_status=True
            if self.developer_mode: self._print_ ( 'Bucket is set to ' + bucket_name + '. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return self.bucket_status
        except:
            self.bucket_status=False
            if self.developer_mode: self._print_ ( 'Bucket(' + bucket_name + ') set is failed with error ' + str(sys.exc_info())  + '\t' + '. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            if 'container does not exist' in str(sys.exc_info()) and create_if_not_exist:
                if self.create_bucket(bucket_name) and try_once_on_failure:
                    return self.set_bucket_name(bucket_name,create_if_not_exist=False,try_once_on_failure=False)#This will exactly loop once
            return self.bucket_status
    def create_bucket(self,bucket_name):
        if self.developer_mode: self._print_('Bucket Creation script for ' + bucket_name)
        return self.conn.create_container(bucket_name)
    def set_environment(self, environment_name):
        try:
            primary_folder_name = environment_name.strip('/').strip('\\')
            self.environment_name = primary_folder_name
            if self.developer_mode: self._print_ ( 'Environment is set to ' + self.environment_name + '. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))               
            return True
        except:
            if self.developer_mode: self._print_ ( 'Environment set up is failed with error ' + str(sys.exc_info())  + '\t. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))        
            return False
    def create_folder(self, sub_folder,environment_name=None):#dont use
        try:
            return True
            if not environment_name:
                primary_folder=self.environment_name
            else:
                primary_folder=environment_name
            self.sub_folder = sub_folder
            if self.sub_folder[-1:] == '/':
                pass
            else:
                self.sub_folder = self.sub_folder + '/'
            primary_key = primary_folder + self.sub_folder
            full_key = os.path.join(primary_key)
            self.current_folder = self.bucket.new_key(full_key)
            self.current_folder.set_contents_from_string('')
            if self.developer_mode: self._print_ ( 'Created folder \' ' + primary_key + '\'. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return True
        except:
            if self.developer_mode: self._print_ ( 'Error while creating folder \' ' + primary_key + '\'.' + '. Error is '  + str(sys.exc_info())  + '\t.  Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return False

    def delete_environment(self, environment_name):#yet to use
        return True
        if environment_name[-1:] == '/':
                pass
        else:
            environment_name = environment_name + '/'
        list_data = self.list_file()
        if self.developer_mode: self._print_ ( 'Deleting file and folders in the environment ' + environment_name.strip('/') + '. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
        for data in list_data:
            if environment_name in data:  
                self.delete_folder(data)
        if self.developer_mode: self._print_ ( 'Deleted file and folders in the environment ' + environment_name.strip('/') + '. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
    def delete_folder(self, object_path):#yet to use#need to include the environment name
        return True
        try:
            object_key = self.bucket.get_key(object_path)
            object_key.delete()
            if self.developer_mode: self._print_ ( 'Deleted folder \'' + str(object_path) + '\'. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return True
        except:
            if self.developer_mode: self._print_ ( 'Error while deleting folder \'' +  str(keyname)  + '\'.' + '. Error is '  + str(sys.exc_info())  + '\t.  Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return False
    def __rename_file__(self,existing_key_name,new_key_name): #yet to use
        try:
            return True
            if existing_key_name == new_key_name:
                if self.developer_mode: self._print_ ( 'Rename is not processed. Current name and new name is same. Current: \'' +  existing_key_name  + '\'. New: \'' + new_key_name + '\'. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
                return True
            key_is=Key(self.bucket)
            key_is.key=existing_key_name
            key_is.copy(self.bucket,new_key_name)
            key_is.delete()
            if self.developer_mode: self._print_ ( 'Renamed object \'' +  existing_key_name  + '\' to \'' + new_key_name + '\'. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return True
        except:
            if self.developer_mode: self._print_ ( 'Error while renaming object \'' +  existing_key_name  + '\' to \'' + new_key_name + '\'. Error is '  + str(sys.exc_info())  + '\t.  Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return False
    def upload_file(self, sub_folder, file_path, filename_to_save=None,new_extension=None):
        try:
            if os.path.isfile(file_path):
                file_name=os.path.basename(file_path)
            else:
                if self.developer_mode: self._print_ ( 'Error while uploading the file \''+ file_path + '\'. File does not exist' +'. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))            
                return False
            if new_extension and (not filename_to_save):
                base_file_name=os.path.splitext(file_name)[0]
                current_extension=os.path.splitext(file_name)[1]
                file_name = base_file_name + '.' + new_extension
            if not filename_to_save:
                filename_to_save=file_name.replace(' ','')
            folder_key = os.path.join(self.environment_name , sub_folder)
            full_key = os.path.join(folder_key, filename_to_save)
            full_key=full_key.strip('\\')
            if self.developer_mode: self._print_ ( 'Uploading the file \''+ file_path + '\' to folder \'' + self.bucket + '\' with file name \'' + full_key +'\'. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))            
            self.conn.put_block_blob_from_path(self.bucket, full_key, file_path)
            if self.developer_mode: self._print_ ( 'Uploaded the file \''+ file_path + '\' to folder \'' + self.bucket + '\' with file name \'' + full_key +'\'. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return True
        except:
            if self.developer_mode: self._print_ ( 'Error while uploading the file \'' +  file_path  + '\' to \'' + self.environment_name + '\\' + sub_folder + '\'. Error is '  + str(sys.exc_info())  + '\t.  Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return False
    def download_file(self, azure_file_path,path):##yet to test
        try:
            #return True
            if self.developer_mode: self._print_('download_file: downloading -' + str(azure_file_path))
            self.conn.get_blob_to_path(self.bucket,azure_file_path,path)
            return True
        except:
            if self.developer_mode: self._print_ ( 'Error while list all the files from the bucket \''+ str(self.bucket) + '\'. Error is '  + str(sys.exc_info())  + '\t. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return False
    def download_all_files(self,target_folder,filter_by=None):
        try:
            all_file_name=self.list_file(filter_by=filter_by)
            if not all_file_name:
                if self.developer_mode: self._print_ ( 'Downloading files from the bucket \''+ str(self.bucket) + '\'. No file is available ')
            for each_file in all_file_name:
                target_file_name=each_file.replace('\\','/')
                if '/' in target_file_name:
                    target_file_name=target_file_name.split('/')[-1]
                else:
                    pass
                self.download_file(each_file,os.path.join(target_folder,target_file_name))
            return True
        except:
            if self.developer_mode: self._print_ ( 'Error while Downloading all the files from the bucket \''+ str(self.bucket) + '\'. Error is '  + str(sys.exc_info())  + '\t. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return False
    def list_file(self,filter_by=None):
        try:
            list_of_files=[]        
            if filter_by:
                if len(filter_by.strip()) <3:
                    if self.developer_mode: self._print_ ( 'Breaking List all files module. filter_by(' +filter_by +'), if given, should contain minimum 3 character. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))            
                    return list_of_files
            list_of_keys = self.conn.list_blobs(self.bucket)
            for each_result in list_of_keys:
                if filter_by:
                    if each_result.name.startswith(filter_by):
                        list_of_files.append(each_result.name)
                else:
                    list_of_files.append(each_result.name)
            return list_of_files
        except:
            if self.developer_mode: self._print_ ( 'Error while list all the files from the bucket \''+ str(self.bucket) + '\'. Error is '  + str(sys.exc_info())  + '\t. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return False
    def list_file_size(self,filter_by=None):#size need to be added
        try:
            list_of_files=''
            if filter_by:
                if len(filter_by.strip()) <3:
                    if self.developer_mode: self._print_ ( 'Breaking List all files size module. filter_by(' +filter_by +'), if given, should contain minimum 3 character. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))            
                    return list_of_files
            list_of_keys = self.conn.list_blobs(self.bucket)
            for each_result in list_of_keys:
                #self.conn.get_blob_properties(self.bucket,each_result.name) content-length            
                if filter_by:
                    if each_result.name.startswith(filter_by):
                        list_of_files = list_of_files + each_result.name + '\n'
                else:
                    list_of_files = list_of_files + each_result.name + '\n'
            return list_of_files
        except:
            if self.developer_mode: self._print_ ( 'Error while list all the files size from the bucket \''+ str(self.bucket) + '\'. Error is '  + str(sys.exc_info())  + '\t. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return False
    def file_size(self,key_name):
        try:    
            props=self.conn.get_blob_properties(self.bucket,key_name)
            props_size= int(props['content-length'])
            return props_size
        except:
            if self.developer_mode: self._print_ ( 'Error while fetching size for  \'' + key_name + '\' from bucket \''+ str(self.bucket) + '\'. Error is '  + str(sys.exc_info())  + '\t. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
    def set_current_folder(self, sub_folder):#yet to form
        try:
            if sub_folder[-1:] == '/':
                pass
            else:
                sub_folder = sub_folder + '/'        
            folder_path= os.path.join(self.environment_name , sub_folder)
            self.current_folder = self.bucket.get_key(folder_path)
            if self.developer_mode: self._print_ ( 'Current folder is set to \''+ sub_folder + '\'. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))                        
            return True
        except:
            if self.developer_mode: self._print_ ( 'exception while setting current folder as \''+ sub_folder + '\'. Error is '  + str(sys.exc_info())  + '\t. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
            return False
    def get_current_folder(self):#yet to form
        if self.developer_mode: self._print_ ( 'In get_current_folder function. Current folder is \'' + str(self.current_folder) + '\'. Connection status is ' + str(self.connection_status) + '. Bucket set status is ' + str(self.bucket_status))
        return self.current_folder
    def copy_file(self, destination_bucket, destination_key):##yet to test
        try:
            return True
            self.current_folder.copy(destination_key, destination_key)
            """
            def copy_blob(self, container_name, blob_name, x_ms_copy_source,
                          x_ms_meta_name_values=None,
                          x_ms_source_if_modified_since=None,
                          x_ms_source_if_unmodified_since=None,
                          x_ms_source_if_match=None, x_ms_source_if_none_match=None,
                          if_modified_since=None, if_unmodified_since=None,
                          if_match=None, if_none_match=None, x_ms_lease_id=None,
                          x_ms_source_lease_id=None):
            """
            return True
        except:
            return False
if __name__ == '__main__':
    if True:
        azure=PythonAZURE('fiindhdinsight','DV5LBbma0JAekanA3OuUCol6c3EoULWD9sp08IPBzBNmwu7o3lvbjRONxBvL9qxRWFPO+Tmkz6VjWDExVvz0XQ==')
        azure.set_bucket_name('aaaaaaaa')
    elif not True:
        #scenario_no=1 #<INPUT>
        #load_count=0 #<INPUT>
        #file_prefix_is='test_scenario_' + str(scenario_no) + '_' + str(load_count) + '_'
        azure=PythonAZURE('fiindhdinsight','DV5LBbma0JAekanA3OuUCol6c3EoULWD9sp08IPBzBNmwu7o3lvbjRONxBvL9qxRWFPO+Tmkz6VjWDExVvz0XQ==')
        azure.set_bucket_name('aaaaaaaa')
        azure.set_environment('staging')
        available_file_list=azure.list_file()
        #azure.download_file(available_file_list[0],'ThisIs.txt')
        azure.download_all_files(target_folder='_download')
        # import socket
        # azure.upload_file( 'data', 'E:\\_data\\CleanUp\\CompanyWebsites_20160127\\CompPage_core_stage_company_attributes.psql', filename_to_save=str(socket.gethostname()) + '_' + 'CompPage_core_stage_company_attributes.psql',new_extension=None)
        # print azure.list_file()
        # #print azure.get_blob_properties('dev','staging/data/DataLoadStats_20141113.dat')    
        exit()    