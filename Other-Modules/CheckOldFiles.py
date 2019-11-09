"""
Functionality : Code which check for the old files and delete the files with permission from the mail 
Version 	  : v1.2
History 	  : 
				v1.0   - 02/16/2019 - intial version 
				v1.1   - 02/19/2019 - Separate File size cheking is skipped
				v1.1.1 - 02/19/2019 - Giga bytes calculation is changed.
				v1.2   - 02/19/2019 - Fucntion CheckSizeAndLogDirectory() is modified to log files.


Issues 		  :
Pending	   : 
				1.Sending mail to recepients with the files list attached 
				2.With confirmation from the mail - delete all the content.
"""
import os,sys
import time
from decimal import Decimal
import shutil
import datetime
#current_time = time.time()
from DeleteFilesSupport import *
from MasterGmail import * 

class CheckOldFiles():
	def __init__(self,vm_name,input_directory,check_sub_directory=True,check_directory_only=False,day_limit=1,size_limit=20,size_measure='kb',skip_size=False,skip_extension=['.py','.pyc','.sql','.exe','.mp3','.mp4'],write_headers=True,output_file_name='DoubtfulDirectories.txt',delete_files=False,write_file_log=True,file_log_name='FileLog.txt'):
		self.input_directory=input_directory
		self.day_limit=day_limit
		self.size_limit=float(size_limit)
		self.size_measure=size_measure.strip().lower()
		self.skip_extension=skip_extension
		self.skip_size=skip_size
		self.output_file_name=os.path.join(os.getcwd(),output_file_name)
		self.delete_files=delete_files
		self.universal_directory_count=0
		self.check_sub_directory=check_sub_directory
		self.now = datetime.datetime.now()
		self.date_string=self.now.strftime("%d_%m_%Y")
		self.write_file_log=os.path.join(os.getcwd(),write_file_log)
		self.output_file_name=self.output_file_name.replace('.','_'+self.date_string+str('.'))
		print 'Output_file_name :',self.output_file_name
		print 'size_measure :',self.size_measure
		print 'size_limit :',self.size_limit
		print 'day_limit :',self.day_limit
		self.doubtful_files=[]
		headers='Directory\tParent_directory\tFull_Directory\tfile_created_time\tlast_modified_on\tdays_difference\tsize_in_kb\tsize_in_mb\tsize_in_gb\ttotal_files\ttotal_folders\tfolder_status\n'
		self.file_log=os.path.join(os.getcwd(),file_log_name)
		self.file_log=self.file_log.replace('.','_'+self.date_string+str('.'))
		self.vm_name=vm_name
		#self.file_log='FileLog_'+str(self.date_string)+'.txt'
		if write_headers:
			for file_name in [self.output_file_name,self.file_log]:
				with open(file_name,'w') as w:
					try:
						w.write(headers)
					except:
						w.write(headers.encode('utf-8'))
		#total_size=get_files_log(input_directory=full_file_path,check_sub_directory=check_sub_directory,delete_files=delete_files,check_directory_only=check_directory_only,day_limit=day_limit,size_limit=self.size_limit,size_measure=self.size_measure,skip_size=skip_size)
	def get_folder_details(self,input_directory=''):
		self.universal_directory_count+=1
		if input_directory =='':
			input_directory=self.input_directory
		#print 'Current Directory......:',input_directory
		sys.stdout.write('Checking....... '+input_directory)
		total_size=0
		sum_kb=0
		sum_mb=0
		sum_gb=0
		total_folders=0
		total_files=0
		for each_item in os.listdir(input_directory):
			print 'File name  :',each_item
			#raw_input('File name ')
			input_directory_temp=input_directory.split(os.sep)[-1]
			full_file_path=os.path.join(input_directory,each_item)
			if os.path.isdir(full_file_path) and self.check_sub_directory:
				#get_files_log(full_file_path)
				total_folders+=1
				try:
					result_sub_dict=self.get_folder_details(input_directory=full_file_path)
					sum_kb+=result_sub_dict['total_size_kb']
					sum_mb+=result_sub_dict['total_size_mb']
					sum_gb+=result_sub_dict['total_size_gb']
					total_folders+=result_sub_dict['total_folders']
					total_files+=result_sub_dict['total_files']
				except Exception as e :
					print 'Exception in getting this directory :',e
					pass
			else:
				extension_match=[True for each_extension in self.skip_extension if each_item.endswith(each_extension)]
				print 'extension_match :',extension_match
				if extension_match:continue
				total_files+=1
				b_ytes=os.path.getsize(full_file_path)
				# kb=round(Decimal(b_ytes/1024.0),2)
				# mb=round(Decimal(kb/1024.0),2)
				# gb=round(Decimal(mb/1024.0),2)
				kb=b_ytes/1024.0
				mb=kb/1024
				gb=mb/1024
				# mb=round(Decimal(kb/1024.0),2)
				# gb=round(Decimal(mb/1024.0),2)
				#print 'gb:',gb
				# print 'size of file in kb',kb
				# print 'size of file in mb',mb
				# print 'size of file in gb',gb
				sum_kb+=kb
				sum_mb+=mb
				sum_gb+=gb
				# Writing File Log
				if self.write_file_log :
					kb=round(Decimal(kb),2)
					mb=round(Decimal(mb),2)
					gb=round(Decimal(gb),2)
					file_created_time = os.path.getctime(full_file_path)
					file_modified_time = os.path.getmtime(full_file_path)
					p_file_created_time=time.ctime(file_created_time)
					p_file_modified_time=time.ctime(file_modified_time)
					file_dict={
						'total_size_kb':kb,
						'total_size_mb':mb,
						'total_size_gb':gb,
						'input_directory':full_file_path,
						'total_folders':0,
						'total_files':0,
						'created_time':p_file_created_time, # printable time 
						'modified_time':p_file_modified_time, # printable time 
						'c_created_time':file_created_time,
						'c_modified_time':file_modified_time
							}
					print 'doubtful_files - full_file_path :',full_file_path
					self.doubtful_files.append(file_dict)
					# self.skip_size=True
					# self.CheckSizeAndLogDirectory(file_dict,output_file_name=self.file_log)
					# self.skip_size=False
				# if sum_gb>0:
				# 	#print 'sum_gb :',sum_gb
				# 	raw_input()
		sum_kb=round(Decimal(sum_kb),2)
		sum_mb=round(Decimal(sum_mb),2)
		sum_gb=round(Decimal(sum_gb),2)
		# sys.stdout.write(' Size:'+str(sum_kb)+'KB \n')
		# sys.stdout.write('Size:'+str(sum_mb)+'MB \n')
		# sys.stdout.write('Size mb/1024 :'+str(sum_mb/1024)+'GB \n')
		if self.write_file_log:
			match=self.check_size_only(sum_kb,sum_mb,sum_gb)
			if match:
				self.skip_size=True
				for each_dict in self.doubtful_files:
					self.CheckSizeAndLogDirectory(each_dict,output_file_name=self.file_log)
				self.skip_size=False
		self.doubtful_files=[]
		sys.stdout.write('\r '+str(self.universal_directory_count)+',Processed Directory : '+str(input_directory)+' Size:'+str(sum_gb)+'GB \n')
		c_created_time = os.path.getctime(input_directory)
		c_modified_time = os.path.getmtime(input_directory)
		created_time=time.ctime(c_created_time)
		modified_time=time.ctime(c_modified_time)
		result_dict={
				'total_size_kb':sum_kb,
				'total_size_mb':sum_mb,
				'total_size_gb':sum_gb,
				'input_directory':input_directory,
				'total_folders':total_folders,
				'total_files':total_files,
				'created_time':created_time,
				'modified_time':modified_time,
				'c_created_time':c_created_time,
				'c_modified_time':c_modified_time
					}
		self.CheckSizeAndLogDirectory(result_dict)
		#raw_input('rw')
		return result_dict

	def check_size_only(self,total_size_kb,total_size_mb,total_size_gb):
			if self.skip_size:
				match=True
			else:
				match=False
				if self.size_limit:
					if self.size_measure=='mb':
						#print 'MB matched size measure'
						if total_size_mb>=self.size_limit:
							match=True
					elif self.size_measure=='gb':
						#print 'GB matched size measure'
						if total_size_gb>=self.size_limit:
							match=True
							#print 'match status changed'
					elif self.size_measure=='kb':
						#print 'KB matched size measure'
						if total_size_kb>=self.size_limit:
							match=True
			return match	
	def CheckSizeAndLogDirectory(self,result_dict,delete_files=False,output_file_name=''): # Which checks the size and delete if exceeds the size
		if not output_file_name:
			output_file_name=self.output_file_name
		total_size_kb=result_dict['total_size_kb']
		total_size_mb=result_dict['total_size_mb']
		total_size_gb=result_dict['total_size_gb']
		c_created_time=result_dict['c_created_time']
		c_modified_time=result_dict['c_modified_time']
		input_directory=result_dict['input_directory']
		created_time=result_dict['created_time']
		modified_time=result_dict['modified_time']
		total_files=result_dict['total_files']
		total_folders=result_dict['total_folders']
		folder_name=input_directory.split(os.sep)[-1]
		parent_folder_name=input_directory.split(os.sep)[-2]
		current_time = time.time()
		# print 'total_size_mb :',total_size_mb
		#print 'total_size_gb :',total_size_gb
		# print 'self.size_measure :',self.size_measure
		#if self.size_measure
		if self.skip_size: # we need to check the folder size we need condition 
			match=True
		else:
			match=self.check_size_only(total_size_kb,total_size_mb,total_size_gb)
		# print 'self.day_limit :',self.day_limit
		days_difference=((current_time - c_modified_time) // (24 * 3600))
		#print 'days_difference :',days_difference
		#print 'match :',match
		if  days_difference>= self.day_limit and match:
			#print('{} removed'.format(input_directory))
			#print 'Written in file !!'
			status='Not deleted'
			if delete_files:
				#os.unlink(f)
				#shutil.rmtree(input_directory)
				pass
			final_text=str(folder_name)+'\t'+str(parent_folder_name)+'\t'+str(input_directory)+'\t'+str(created_time)+'\t'
			final_text+=str(modified_time)+'\t'+str(days_difference)+'\t'+str(total_size_kb)+'\t'+str(total_size_mb)+'\t'+str(total_size_gb)+'\t'
			final_text+=str(total_files)+'\t'+str(total_folders)+'\t'
			final_text+=str(status)
			final_text+='\n'
			with open(output_file_name,'a') as w:
				try:
					w.write(final_text)
				except:
					w.write(final_text.encode('utf-8'))
		return True
	def SendstatusMail(self,input_dict,receivers=['ajith@fiind.com']):
		total_size_mb=input_dict['total_size_mb']
		total_size_gb=input_dict['total_size_gb']
		input_directory=input_dict['input_directory']
		total_files=input_dict['total_files']
		total_folders=input_dict['total_folders']
		full_output_file_path=self.output_file_name
		output_file_name=self.output_file_name.split(os.sep)[-1]
		file_split_details=self.file_log
		body_content ="Checked "
		gm_obj=Gmail()
		#gm_obj.read_email_from_gmail()
		receivers=receivers
		input_dict={}
		subject='Periodic Memory Check done in the VM "'+str(self.vm_name)+'" on '+str(self.now.strftime("%m-%d-%Y"))
		input_dict['subject']=subject
		input_dict['body']={
							'greetings':'Hi All ,',
							'bottom_content':'',
							'content':'Below are the storage summary of directory :, \n Note: Please respond "Yes" (within 30 mins) to this mail to auto-delete all the suspected files ! , Otherwise Files wo'+str(input_directory),
							'table_input':{
											'headers':{'Title':'Value'},
											'table_content':{
															'Total_files':total_files,
															'Total_folders':total_folders,
															'Size_in_GB':total_size_gb,
															'Size_in_MB':total_size_mb,
															'Directory':input_directory,
															'File_details':file_split_details,
															'Directory_details':full_output_file_path,
															'Checked_size': self.size_limit+' '+self.size_measure,

															}
											}
							}
		input_dict['attachment']=[{'file_name':output_file_name,
									'full_file_path':full_output_file_path}]
		gm_obj.send_mail(input_dict=input_dict,receivers=receivers)
		status = gm_obj.wait_for_reply(input_dict={'subject':subject,'sensitive_data':'yes'},time_out_minutes=0.1,receivers=receivers) 
		print 'status of Reply :',status
		if status:
			for index,each_line in enumerate(open(self.file_log).readlines()):
				line_split=each_line.split('\t')			
				full_file_path=line_split[2]
				if full_file_path=='Full_Directory':continue
				sys.stdout.write("\rCurrently processing ..."+full_file_path)
				#delete_selected_files(input_directory=input_directory,files_list=full_file_path.split('\t'),full_path_given=True)
		pass

if __name__=="__main__":
	#input_directory="D:\\Ajith\\_data\\hiringPageClassified"
	#input_directory="D:\\Ajith\\_data\\MarketingData"
	input_directory=sys.argv[1]
	#input_directory=''
	if True:
		day_limit=60
		size_limit='100'
		size_measure='mb'
		vm_name='Ajith-Local-Machine'
		del_obj=CheckOldFiles(vm_name=vm_name,input_directory=input_directory,size_measure=size_measure,size_limit=size_limit,day_limit=day_limit,check_sub_directory=True)
		result_dict=del_obj.get_folder_details()
		#send status mail 
		print 'result_dict:',result_dict
		# SendstatusMail(result_dict)
		# wait_for_response (30)# minutes 
		# delete_files()
	if not True:
		file_name='FileLog_19_02_2019_test.txt'
		file_lines=open(file_name).readlines()
		for index,each_line in enumerate(file_lines):
			line_split=each_line.split('\t')			
			full_file_path=line_split[2]
			if full_file_path=='Full_Directory':continue
			sys.stdout.write("\rCurrently processing ..."+full_file_path)
			delete_selected_files(input_directory=input_directory,files_list=full_file_path.split('\t'),full_path_given=True)
			# except Exception as e:
			# 	print 'Exception in deleting files :',e
			# 	pass
			# raw_input('2')
		# day_limit=10
		# size_measure='kb'
		# size_limit=10
		# skip_extension=['.py','.sql']
		# result_dict=get_files_log(input_directory=input_directory,day_limit=day_limit,size_measure=self.size_measure,size_limit=self.size_limit,skip_size=False,skip_extension=skip_extension)
		# print 'result_dict :',result_dict

