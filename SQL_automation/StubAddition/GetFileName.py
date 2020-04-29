"""
File to get the filenames from in the diven directory
"""
import os,sys
import os.path
from os import path
from CustomisedFileOperation import * 
from Stub import * 

sys.path.insert(0,"G:\Ajith\OtherFiles\HelpText_from_sp")
from HelpText_sp import *

comments_starts =''
comments_ends=''
def get_all_files(R_track_id,input_directory,server_directory='files_from_server',get_help_text=True,developer_mode=False):
	"""
	Input : A directory
	Process : get all the file names present in that directory
	Output  : returns all the filenames as output and writes in a file 
	"""
	
	total_files=[]
	count=0
	if server_directory.lower()=='files_from_server':
		server_directory=os.path.join(input_directory,server_directory)
		if not os.path.exists(server_directory): os.makedirs(server_directory)
	for root, dirs, files in os.walk(input_directory):
		for each_file in files:
			count+=1
			# if each_file.endswith(delete_extension):
			print (count,each_file)
			write_into_file(file_name='sps_list.txt',contents=str(each_file).strip()+'\n',mode='a')
			total_files.append(each_file)
			# getting text from the server 
			if get_help_text==True:
				help_text=get_sptext(each_file)['help_text']
				if developer_mode==True: print ('help_text :',help_text)
			server_file_name=os.path.join(server_directory,each_file)
			write_into_file(file_name=server_file_name,contents=str(help_text).strip(),mode='w')
			# stub file comparison for both modes
			print ('stub_file_name:',os.path.join(root,each_file))
			print ('sp file name :',server_file_name)

			stub_dict=stub_comparison(stub_file_name=os.path.join(root,each_file),server_version_name=server_file_name)
			# print (stub_dict)
		
	# updating changes here !!
			file_contents=get_file_content(server_file_name,True)
			index_dict=get_variable_index(file_contents)
			if index_dict['variable_index']!=0:
				file_contents2=file_contents
				file_contents2.insert(index_dict['variable_index'],get_merged_content(stub_dict['variables']['list']))
				file_contents2.insert(index_dict['null_index'],get_merged_content(stub_dict['null_checks']['list']))
				file_contents2.insert(index_dict['space_index'],get_merged_content(stub_dict['space_checks']['list']))
				up_directory=os.path.join(input_directory,'updated_procedures')
				if not os.path.exists(up_directory): os.makedirs(up_directory)
				write_into_file(file_name=os.path.join(up_directory,each_file).replace('.sql','_output.sql'),contents=str(' '.join(file_contents2)).strip(),mode='w')
			else:
				print ('Issue in getting index',index_dict)
			# file_contents2.insert(index_dict['out_index'],stub_dict['outs']['list'])
			print ('Lines before addition :',len(file_contents))
			print ('Lines After addition :',len(file_contents2))
			break # to end with single file 
		break # to end this current directory 
	
	return True
def get_merged_content(temp_list,rtrack):
	comments_header='/*Ajithkumar       29-04-2020    '+str(rtrack)+'  *\\'
	comments_starts='/*code added for '+str(rtrack)+' starts *\\'
	comments_ends='/*code added for '+str(rtrack)+' ends *\\'

	temp_content=str(comments_starts)+'\n'
	temp_content+='\n'.join(temp_list)+'\n'
	temp_content+=str(comments_ends)+'\n'
	return temp_content
#List.insert(2, '@new')
def ensure_space_check(index,file_lines,depth=5):
	t_index=index
	for i in range(1,depth+1):
		if "rtrim" in  file_lines[index+i].lower() and "ltrim" in file_lines[index+i].lower():
			return False
	return True

def ensure_null_check(index,file_lines,depth=5):
	t_index=index
	# print ("Ensure null check :",index,file_lines[index])

	for i in range(1,depth+1):
		if "= '~#~'" in  file_lines[index+i] or "= -915" in file_lines[index+i]:
			# print ('Inside null checking  condition satisfied',file_lines[index+i])
			return False
	
	return True
def get_variable_index(file_lines):
	# temp_text=input_text.lower().split('create '.lower())[1]
	# begin_split=''
	print(len(file_lines))
	temp_index=0
	var_index=0
	space_index=0
	out_index=0
	null_index=0
	top_len=len(file_lines)
	for index,each_line in enumerate(file_lines):
		# if 'begins' not in each_line.lower() and 'begin' in each_line.lower():
		# 	print ('begin index:',index,each_line)
		# 	temp_index=index
		# 	break
		if var_index==0:
			if '@m_errorid ' in each_line.lower() and not each_line.strip().startswith('--'):
				# print ('Error id index ',index,each_line)
				var_index=index
		if space_index==0:
			if  "rtrim" in each_line.lower()  and  "ltrim" in each_line.lower():# or "set " in each_line.lower()
				if ensure_space_check(index,file_lines)==True:
						# print ('Space check is over :',index+1,file_lines[index+1])
						space_index=index+1
		if null_index==0:
			if " = null" in each_line:
				if ensure_null_check(index,file_lines)==True:
						# print ('null checking is over :',index+1,file_lines[index+1])
						null_index=index+1
						break
		# if out_index==0:
		# 	# pass
		# 	top_len-=1

	return {
			'variable_index':var_index,
			'space_index':space_index,
			'null_index':null_index,
			'out_index':out_index
			}

	# print ('Before begins:',file_lines[temp_index])
	# if not begin_split:begin_split='begin '


# def get_indexes(sp_name):
# 	file_contents=get_file_content(sp_name,True)
# 	print ('total_lines:',len(file_contents))
# 	# result_set=get_parameters(file_contents)
# 	# print (result_set)
# 	return get_variable_index(file_contents)
	
	
	

if __name__=="__main__":
	input_directory='G:\\Ajith\\Issues\\Logistics\\2020\\STUB-Addition\\April\\PICK&BIN\\PICK&BIN'
	R_track_id='EPE-001'
	print (get_all_files(R_track_id,input_directory))

	# sp_name ='WMM_picpln_Sp_cmpimg_hrf.sql'
	# sp_name_full=os.path.join(input_directory,'files_from_server',sp_name)
	# sp_name_full='G:\\Ajith\\OtherFiles\\HelpText_from_sp\\wms_bin_sp_cmn_pln_dtl.sql'
	# print (get_indexes(sp_name_full))



# read the stub file 
# get the text from the server file and store it in given directory 
# run the stub file difference for all the sps.