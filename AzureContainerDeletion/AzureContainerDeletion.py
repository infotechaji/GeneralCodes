"""
Description : code which deleted containers and blob in azure account
Version     : v1.1
History     : 
              v1.0 - 06/18/2018 - initial version
              v1.1 - 08/22/2018 - Function delete_old_blobs() is added to delete selected blobs in a container

Pending     : None
Issues      : None
"""
from __future__ import division
import azure.storage.blob as azureblob
import datetime
import argparse
import sys,os
import azure.batch as batch


class AzureAccess():
    def __init__(self,account_name,account_key,developer_mode=False):
        self.account_name=account_name
        self.account_key=account_key
        self.developer_mode=developer_mode
        try:
            self.blob_client = azureblob.BlockBlobService(account_name=self.account_name,account_key=self.account_key)
        except Exception as e :
            self.blob_client = azureblob.BlobService(account_name=self.account_name,account_key=self.account_key)
            pass
    def get_containers_list(self):
        return self.blob_client.list_containers() 
    def delete_container(self,container_name):
        try:
            self.blob_client.delete_container(container_name)
            return True
        except Exception as e:
            print ('Container \"'+str(container_name)+'\" does not excist ')
            return False
    def get_all_blobs(self,container_name,marker=None):
        blobs = []
        marker = None
        while True:
            batch = self.blob_client.list_blobs(container_name, marker=marker)
            blobs.extend(batch)
            if not batch.next_marker:
                break
            marker = batch.next_marker
        if blobs:
            return blobs
        else: 
            return ''
    def log_deletion_details(self,final_text):
        date_suffix=str(datetime.date.today()).strip(' \t\r\n').replace('-','_')
        file_name='deletion_log_'+str(date_suffix)+'.txt'
        directory='Deletion_log'
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path=os.path.join(directory,file_name)
        with open(file_path,'a') as fp:
            fp.write(final_text)
            fp.close()
    def get_blob_details(self,container_name,blob):
        final_text=str(datetime.datetime.now())+'\t'+str(container_name)+'\t'+str(blob.name)+'\t'
        final_text+=str(blob.properties.last_modified)+'\t'+str(blob.properties.content_length)+'\t'+str("{:.1f}")
        final_text+='\n'
        size_in_mb=blob.properties.content_length/1048576
        if self.developer_mode : print 'get_blob_details:\t size_in_mb:',size_in_mb
        final_text=final_text.format(size_in_mb)
        if final_text:
            return final_text
        else: return ''
    
    def delete_blobs(self,container_name,from_date='',to_date=datetime.datetime.now(),include_from_date=False):
        blobs=self.get_all_blobs(container_name)
        deleted_blobs_count=0
        for each_blob in blobs :
            if self.developer_mode : print 'delete_blobs:\t each_blob :',each_blob.name
            if self.developer_mode : print 'delete_blobs:\t each_blob :',each_blob.properties.content_length
            last_modified=str(each_blob.properties.last_modified)
            #print 'last modified :',last_modified
            temp_date_string=last_modified.replace(' GMT','')
            blob_dt = datetime.datetime.strptime(temp_date_string, '%a, %d %b %Y %H:%M:%S')
            blob_date=blob_dt.date()
            if self.developer_mode : print 'delete_blobs:\t blob_date :',blob_date
            if self.developer_mode : print 'delete_blobs:\t from_date :',from_date
            if self.developer_mode : print 'delete_blobs:\t to date :',to_date.date()
            
            if not from_date <= blob_date <=to_date.date():
                deleted_blobs_count+=1
                if self.developer_mode : print 'delete_blobs:\t Yes !! blob :"'+str(each_blob.name)+'" is in deletion range , date :'+str(blob_date)
                final_text=self.get_blob_details(container_name=container_name,blob=each_blob)
                try:
                    self.blob_client.delete_blob(container_name,each_blob.name)
                    print 'Blob deleted successfully !!: ',each_blob.name
                    self.log_deletion_details(final_text)
                except Exception as e:
                    print 'delete_blobs:\tException in deleting blob :',each_blob.name
        if not deleted_blobs_count>0:print 'No blobs found in the given criteria!!'
                
    
    def delete_old_blobs(self,container_name,delete_before_days='',delete_before_date=''): # date format yyyy/mm/dd
        if delete_before_days and not delete_before_date:
            print 'delete_before_days :',delete_before_days
            temp_date_time = datetime.datetime.now() - datetime.timedelta(days=delete_before_days)
            from_date=temp_date_time.date()
            self.delete_blobs(container_name=container_name,from_date=from_date)
        elif not delete_before_days and delete_before_date:
            print 'delete_before_date:',delete_before_date
            splits=delete_before_date.strip(' \t\r\n').split('-')
            if len(splits)==3:
                year=int(splits[0])
                month=int(splits[1])
                date=int(splits[2])
                if self.developer_mode:print "delete_old_blobs:\t",year,month,date
                from_date= datetime.date(year,month,date)
                self.delete_blobs(container_name=container_name,from_date=from_date)
            else:
                print 'please enter the date in valid format YYYY/MM/DD '
        else:
            print "please specify either delete_before_days or  delete_before_date not the both "
            exit()

if __name__=="__main__":
    account_name='xxxxxxxx'
    account_key='xxxxxxxxx'
    container_name='exceltest'
    marker='ns534636_testingMango.txt'
    azure_obj=AzureAccess(account_name=account_name,account_key=account_key)
    blobs= azure_obj.get_all_blobs(container_name=container_name,marker='ns534636_testingMango.txt')
    #blobs=self.get_all_blobs(container_name)
    deleted_blobs_count=0
    for each_blob in blobs :
        print each_blob
        # for each in each_blob.properties:
            # print each
        print each_blob.properties.
        print each_blob.name
        print each_blob.properties.last_modified
    