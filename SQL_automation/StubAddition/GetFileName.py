"""
File to get the filenames from in the diven directory
Version :v2.0
History :
		v1.0 -08/05/2020 - initial version 
		v2.0 -08/05/2020 - name is added as input and few inputs are changed

Pending actions : 
				1, Header data need to be added - DONE
				2, All Variables needs to be checked and form an testing  - DONE
				3, alter the modifed sp in _187 server and check it whether it is working fine ?
				4, Need to cross check the out data 
"""
import os,sys
import os.path
from os import path
from CustomisedFileOperation import * 
from Stub import * 
import datetime




# sys.path.insert(0,"G:\Ajith\OtherFiles\HelpText_from_sp")
# from HelpText_sp import *

global comments_starts
global comments_ends
global rtrack_id

def get_today_date():
	current_date = datetime.date.today()
	current_date = current_date.strftime("%d-%m-%Y")
	return current_date

def get_all_files(rtrack_id,name,input_directory,server_directory='files_from_server',get_help_text=False,developer_mode=False,strict_mode=False):
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
			try:
				print ('--------------------------------------------------------------------------------------------')
				print (count,each_file)
				# write_into_file(file_name='sps_list.txt',contents=str(each_file).strip()+'\n',mode='a')
				stub_file_name=os.path.join(root,each_file)
				total_files.append(each_file)
				# getting text from the server 
				if get_help_text==True:
					help_text=get_sptext(each_file)['help_text']
					if developer_mode==True: print ('help_text :',help_text)
					write_into_file(file_name=server_file_name,contents=str(help_text).strip(),mode='w')
				server_file_name=os.path.join(server_directory,each_file)
				# stub file comparison for both modes
				print ('stub_file_name:',stub_file_name)
				if developer_mode==True : print ('get_all_files:\t stub_file_name presence:',get_file_presence(stub_file_name))
				print ('sp file name :',server_file_name)
				if developer_mode==True : print ('get_all_files:\t sp file name presence :',get_file_presence(server_file_name))
				up_directory=os.path.join(input_directory,'updated_procedures')
				if not os.path.exists(up_directory): os.makedirs(up_directory)
				updated_file=os.path.join(up_directory,each_file)
				if os.path.exists(updated_file) and strict_mode==False:
					print ('Skipping file .....',each_file,'as it exists ',updated_file)
					continue # if the updated file exists then the file will be skipped 
				# continue # added for getting href 
				
				stub_dict=stub_comparison(stub_file_name=stub_file_name,server_version_name=server_file_name,developer_mode=developer_mode)
				# print (stub_dict)
			
		# updating changes here !!
				file_contents=get_file_content(server_file_name,True)
				index_dict=get_variable_index(file_contents)
				if index_dict['variable_index']!=0:
					file_contents2=file_contents
					# print ('file_contents2 copied')
					if stub_dict['variables']['list']:
						file_contents2.insert(index_dict['header_index'],get_merged_content(rtrack_id=rtrack_id,name=name,header=True))
						file_contents2.insert(index_dict['variable_index'],get_merged_content(rtrack_id=rtrack_id,temp_list=stub_dict['variables']['list']).replace('\t','udd_'))
						file_contents2.insert(index_dict['null_index'],get_merged_content(rtrack_id=rtrack_id,temp_list=stub_dict['null_checks']['list']))
						file_contents2.insert(index_dict['space_index'],get_merged_content(rtrack_id=rtrack_id,temp_list=stub_dict['space_checks']['list']))
						print ('updated file name :',updated_file)
						write_into_file(file_name=updated_file,contents=str(' '.join(file_contents2)).strip(),mode='w')
				else:
					print ('Issue in getting index',index_dict)
				# file_contents2.insert(index_dict['out_index'],stub_dict['outs']['list'])
				before_addition=len(get_file_content(server_file_name,return_lines=True))
				if index_dict['variable_index']!=0:
					after_addition=len(get_file_content(updated_file,return_lines=True))
				print ('Lines before addition :',before_addition)
				print ('Lines After addition :',after_addition)
				log_data=str(str(datetime.datetime.now()).split('.')[0])+'\t'+str(each_file)+'\t'+str(stub_file_name)+'\t'
				log_data+=str(server_file_name)+'\t'+str(updated_file)+'\t'
				log_data+=str(len(stub_dict['stub_variables']))+'\t'+str(len(stub_dict['sp_variables']))+'\t'+str(len(stub_dict['added_variables']))+'\t'+str(before_addition)+'\t'+str(after_addition)+'\n'
				write_into_file(file_name='logs.txt',contents=log_data,mode='a')
				# if count>=3:break # for processing certain limits
			except Exception as e :
				print ('Error  while reading file',e)
				e_log_data=str(get_today_date())+'\t'+str(each_file)+'\t'+str('Error')+'\t'+str(e)+'\n'
				write_into_file(file_name='Error_logs.txt',contents=e_log_data,mode='a')
				
				print ('--------------------------------------------------------------------------------------------')

				pass
		break # to end this current directory 
	
	return True
def get_merged_content(rtrack_id,temp_list=[],name="Ajithkumar",header=False):
	# rtrack_id='EPE-20094'
	if header==True:
		comments_header='/*'+str(name)+'\t\t\t'+str(get_today_date())+'\t\t\t\t'+str(rtrack_id)+'\t\t\t\t*/\n'
		return comments_header
	comments_starts='/*code added for '+str(rtrack_id)+' starts    */'
	comments_ends='/*code added for '+str(rtrack_id)+'   ends        */'

	temp_content=str(comments_starts)+'\n'
	temp_content+='\n'.join(temp_list)+'\n'
	temp_content+=str(comments_ends)+'\n'
	return temp_content
#List.insert(2, '@new')
def ensure_space_check(index,file_lines,depth=5):
	for i in range(1,depth+1):
		if "rtrim" in  file_lines[index+i].lower() and "ltrim" in file_lines[index+i].lower():
			return False
	return True

def ensure_null_check(index,file_lines,depth=5):
	# print ("Ensure null check :",index,file_lines[index])

	for i in range(1,depth+1):
		if "'~#~'" in  file_lines[index+i] or "-915" in file_lines[index+i]:# or "-915" in file_lines[index+i]:
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
	header_index=0
	for index,each_line in enumerate(file_lines):
		# if 'begins' not in each_line.lower() and 'begin' in each_line.lower():
		# 	print ('begin index:',index,each_line)
		# 	temp_index=index
		# 	break
		if header_index==0:
			if 'create ' in each_line.lower():
				if '********' in file_lines[index-1]:
					header_index=index-1
				elif '********' in file_lines[index-2]:
					header_index=index-2
				else:
					header_index=index-1
		if var_index==0:
			if '@m_errorid' in each_line.lower() and not each_line.strip().startswith('--'):
			# if '@m_errorid' in each_line.lower() and "udd_int" in each_line.lower() and  not each_line.strip().startswith('--'):
				# print ('Variable id index ',index,each_line)
				var_index=index+1
		if space_index==0:
			if  "rtrim" in each_line.lower()  and  "ltrim" in each_line.lower():# or "set " in each_line.lower()
				if ensure_space_check(index,file_lines)==True:
						# print ('Space check is over :',index,each_line)
						space_index=index+4
		if null_index==0:
			if " = null" in each_line:
				if ensure_null_check(index,file_lines,7)==True:
						# print ('null checking is over :',index+1,file_lines[index+1])
						null_index=index+4
						break
		# if out_index==0:
		# 	# pass
		# 	top_len-=1

	return {
			'variable_index':var_index,
			'space_index':space_index,
			'null_index':null_index,
			'out_index':out_index,
			'header_index':header_index
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
	try:
		input_directory=sys.argv[1]
	except:
		print ('Give the valid Stub files directory ')
	# input_directory='G:\\Ajith\\Issues\\Logistics\\2020\\STUB-Addition\\April\\PICK&BIN\\PICK&BIN'
	# input_directory='G:\\Ajith\\Issues\\Logistics\\2020\\STUB-Addition\\April\\Bin\\Bin'
	#input_directory='G:\\Ajith\\Issues\\Logistics\\2020\\STUB-Addition\\April\\Bin_Plan\\Bin_Plan'
	# rtrack_id='EPE-20094'
	rtrack_id='EPE-20343'
	name='Kasimaharajan T'
	print (get_all_files(rtrack_id=rtrack_id,name=name,input_directory=input_directory,get_help_text=False,developer_mode=False))


	# sp_name ='WMM_picpln_Sp_cmpimg_hrf.sql'
	# sp_name_full=os.path.join(input_directory,'files_from_server',sp_name)
	# sp_name_full='G:\\Ajith\\OtherFiles\\HelpText_from_sp\\wms_bin_sp_cmn_pln_dtl.sql'
	# print (get_indexes(sp_name_full))



# read the stub file 
# get the text from the server file and store it in given directory 
# run the stub file difference for all the sps.