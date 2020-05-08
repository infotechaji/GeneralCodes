import filecmp 
import sys,os
import os,sys
import os.path
from os import path
from CustomisedFileOperation import *

sys.path.insert(0,"G:\\Ajith\\OtherFiles\\FileCopy_and_update")
from copy_folder import *

def compare_files(file1,file2):
	"""
	Input   : gets two files are input 
	Process : compares both the files
	Output  : returns true if they are same 
	"""
	# comp = filecmp.cmp(file1, file2)
	# print("Using shallow = True :",comp) 
	comp=False
	try:
		comp = filecmp.cmp(file1, file2, shallow = False)
		print("Using shallow = False :",comp) 
	except Exception as e:
		print ('Error while comparing file :',e)
		return comp
	return comp

def each_line_compare(file1,file2):
	file_lines1=get_file_content(file1)
	file_lines2=get_file_content(file2)
	for index1,each_line in enumerate(file_lines1):
		if each_line.strip()==file_lines2[index1]:
			pass
		else:
			print ('Line mismatch !',each_line,file_lines2[index1])
			return

  
if __name__=="__main__":

	if not True:
		file1 = sys.argv[1]
		file2 = sys.argv[2]
	# comp = filecmp.cmp(file1, file2)
	# print("Using shallow = True :",comp)
	# comp = filecmp.cmp(file1, file2, shallow = False)
	# print("Using shallow = False :",comp)
		print (compare_files(file1,file2))
	
	file_lines=get_file_content(sys.argv[1],True)
	directory1='G:\\Ajith\\Issues\\Logistics\\2020\\LRT-5244\\PICK_and_BIN_updated\\Mail_version'
	directory2='G:\\Ajith\\Issues\\Logistics\\2020\\LRT-5244\\PICK_and_BIN_updated\\188_version'
	for index,each_line in enumerate(file_lines):
		each_line=each_line.strip('\\r').strip('\\n').strip('\\t')
		file1=os.path.join(directory1,each_line)
		file2=os.path.join(directory2,each_line)
		print ('1:',file1)
		print ('2:',file2)
		print ('Get1 :',get_file_presence(file1))
		print ('Get2 :',get_file_presence(file2))
		if True:#get_file_presence(file1)==True and get_file_presence(file2)==True:
			print ('IF SATISFIED')
			file_presence =compare_files(file1,file2)
			final_text=str(each_line)+'\\t'+str(file1)+'\\t'+str(file2)+'\\t'
			final_text+=str(file_presence)+'\\n'
			write_into_file(file_name='File_cmp.txt',contents=final_text,mode='a')
			if file_presence==False:
				files_list=[each_line]
				copytree(src=directory1,dst=os.path.join(directory1,'not_matched'),files_list=files_list)
				copytree(src=directory2,dst=os.path.join(directory2,'not_matched'),files_list=files_list)
			elif file_presence==True:
				files_list=[each_line]
				copytree(src=directory1,dst=os.path.join(directory1,'matched'),files_list=files_list)
				copytree(src=directory2,dst=os.path.join(directory2,'matched'),files_list=files_list)
			else:
				print ('File presence status is not True/False :')

