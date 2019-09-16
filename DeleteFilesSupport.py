"""
Funcationality  : Custom deletion of files 
Version : v1.2
History : 
		  v1.0 - 12/11/2018 - initial version 
		  v1.1 - 12/17/2018 - deletion of selected files in a directory is added to the function delete_selected_files()
		  v1.2 - 20/02/2019 - skip joining_directory is added to the function delete_selected_files()

Pending :
Issues : 

"""
import os,sys
import os.path
import datetime
from os import path

def delete_file(file_to_be_deleted):
	if path.exists(file_to_be_deleted):
		os.remove(file_to_be_deleted)
		print 'File deleted :',file_to_be_deleted.split(os.sep)[-1]
		return True
	else:
		print 'File doent\'t exists !!',file_to_be_deleted.split(os.sep)[-1]
		return True

def delete_selected_files(input_directory='',delete_extension='',skip_extension='',files_list=[],full_path_given=False,log_file_name='deleted_files.txt'):
		now = datetime.datetime.now()
		date_string=now.strftime("%d_%m_%Y")
		log_file_name=log_file_name.replace('.','_'+str(date_string)+'.')
		delete_files_count=0
		if files_list:
			for each_file in files_list:
				if full_path_given:file_to_be_deleted=each_file
				else:file_to_be_deleted=os.path.join(input_directory,each_file)
				#sys.stdout.write('Deleting File.....'+file_to_be_deleted)
				# if path.exists(file_to_be_deleted):
				# os.remove(file_to_be_deleted)
				if delete_file(file_to_be_deleted):
					final_text=str(now)+'\t'+str(file_to_be_deleted)+'\tdeleted\n'
					with open(log_file_name,'a') as w:
						try:
							w.write(final_text)
						except:
							w.write(final_text.encode('utf-8'))
		elif input_directory and not files_list:
			for root, dirs, files in os.walk(input_directory):	
					for each_file in files:
						if delete_extension:
							if each_file.endswith(delete_extension):
								delete_files_count+=1
								file_to_be_deleted=os.path.join(input_directory,each_file)
								delete_file(file_to_be_deleted)
						else:
							file_to_be_deleted=os.path.join(input_directory,each_file)
							delete_file(file_to_be_deleted)
					
if __name__=="__main__":
	#input_directory="E:\Ajith\_code\_code\Tech_instances\\Tech_code1_delete_test"
	input_directory=sys.argv[1]
	#input_directory=os.getcwd()
	#extension=sys.argv[2]
	#delete_selected_files(input_directory=input_directory,delete_extension='.json')
	#delete_selected_files(input_directory=input_directory,delete_extension='.dat')
	if True:
		#input_directory=sys.argv[1]
		extension=sys.argv[2]
		delete_selected_files(input_directory=input_directory,delete_extension=extension)
	if not True :
		files_list=['AutoOpenCommand_v1.py','AutoOpenCommand_v1.txt']
		delete_selected_files(input_directory=input_directory,files_list=files_list)