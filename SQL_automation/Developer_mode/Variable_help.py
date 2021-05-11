"""
Functionlaity : Debugging Helper to handle variables 
Version	   : v1.0
History	   :
				v1.0 - 09/11/2020 - initial version
				


Input:

Process	  :
Output	   :

Test Cases taken   :
Test Cases passed  :
Test Cases need
to be handled	  : 

Pending   items :
			1, get total valid variables from the definition , handle the commented lines using the defect id mapping
			2, detect the type of variables


			# print(isnull(OBJECT_NAME(@@PROCID),'NA')+':	<variable_name> : '+cast(isnull(<variable_name>,'NULL') as nvarchar(max)))'
					



Open issues :
Comments :

"""

import re,argparse,filecmp,sys
sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')
from subprocess import Popen, PIPE
from os import path
from CustomisedFileOperation import *
from copy_folder import *
from Git_config import *
from Help_print import *
from CompareAndUpdate import get_all_fix_id
from Datastructure_help import *

from Variable_config import *


# import logging
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='GITAutomation.log')

def prepare_bat_file(template_no, GIT_path, modified_objects=[]):
	# future use
	pass

def change_case(input_list):
	# change the case
	return [x.lower() for x in input_list]

def get_modified_files(files_list,git_path, developer_mode = False):
	current_path = os.getcwd()
	# changing to GIT MASTER PATH
	os.chdir(git_path)
	git_command = 'git status'
	# git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
	git_query = Popen(git_command, stdout=PIPE, stderr=PIPE)
	(git_status, error) = git_query.communicate()
	if developer_mode:
		developer_print('GIT Status query executed :',(git_status, error))

	str_git_status = str(git_status, 'utf-8')
	if developer_mode:
		developer_print('str_git_status :',(git_status))
	# modified_pattern = '(modified:\s+)(\w+.*.sql)'
	# modified_pattern = '()(\w+.*.sql)'
	modified_pattern = '(modified:\s+|\t+|\s+|\n+)(\w+.*.sql)'
	# patches = '(01-Source\/Patches\/Patches_Mandatory\/Appln\/)(\w+.sql)'
	total_ids = re.findall(modified_pattern, str(str_git_status))
	if developer_mode:
		developer_print(' total_ids:',total_ids)

	modified_list = []
	add_commands = []
	missing_files =[]
	for each_obj in total_ids:
		try:
			if developer_mode:
				developer_print(' inside total ids:',each_obj)
			# current_obj = each_obj[1]
			current_obj = str(each_obj[1]).strip().split()[-1]
			if developer_mode:
				developer_print('current_obj :',current_obj)
			if current_obj not in modified_list and [i.lower() in current_obj.lower() for i in files_list ]:
				temp_add_cmd = 'git add '+str(current_obj).strip('\t\r\n ')+'\n'
				if temp_add_cmd not in add_commands: add_commands.append(temp_add_cmd) # "git add file1" this command will be added in a separate list
				modified_list.append(current_obj)
		except:
			missing_files.append(current_obj)
			pass
	# os.chdir(current_path)
	if developer_mode:
		print('get_modified_files:\t modified_list :',modified_list)
		print('get_modified_files:\t add_commands :',add_commands)
	return {
		'modified_list': modified_list,
		'missing_files': missing_files,
		'git_add_commands': add_commands
	}

def copy_modified_files(files_directory,files_list,git_path, developer_mode = False):
	for each_file in files_list:
		# if not each_file.lower().endswith('.sql'): each_file += '.sql'
		if developer_mode :developer_print('Processing file :',each_file)
		each_file = handle_extension(each_file)['new_extension']
		target_paths = []
		patch_file = False
		if len(get_all_fix_id(file_content=each_file, extract_from_header=False, developer_mode=developer_mode)['valid_fixes'])>0:  # patch file is handled here
			if developer_mode :developer_print('Detected as patch file :', each_file)
			target_paths.append(GIT_DEPLOYMENT_MANDATORY_PATCH_PATH) # added on 21/10/2020 - In future cases non mandatory patches can be added

			patch_file = True
		else:
			detected_folder = get_deployment_folder(each_file)['matched_folder']
			if developer_mode:
				developer_print(' detected_folder:',detected_folder)
			if detected_folder:
				for each_dir in detected_folder:
					target_paths.append(GIT_DEPLOYMENT_DEFAULT_PATH.replace('<DEPLOYMENT_FOLDER>', each_dir).replace('<SUB_FOLDER>', SP_PATH))
					target_paths.append(GIT_DEPLOYMENT_DEFAULT_PATH.replace('<DEPLOYMENT_FOLDER>', each_dir).replace('<SUB_FOLDER>', VIEW_PATH)) # added f

			else:
				developer_print('Target folder not found ')
				# return False # commeneted to handle to patch file execution

		try:
			for each_mapped_path in target_paths:
				mod_file = os.path.join(files_directory, each_file)
				tar_file = os.path.join(each_mapped_path, each_file)
				if not os.path.exists(tar_file) and patch_file == True:
					if developer_mode: developer_print('Trying to copy the patch file  :', tar_file)
					copy_status = copy_file(src=files_directory, dst=each_mapped_path, files_list=[each_file],developer_mode=developer_mode)['status']  # copies the selected files
					if developer_mode: developer_print('copy_status  :', copy_status)
				# elif (os.path.exists(tar_file) or os.path.exists(str(tar_file).replace('.sql','.SQL')) ) and filecmp.cmp(tar_file, mod_file) == False: # #1001 added on 29-oct-2020 to handle the .SQL missing cases
				elif os.path.exists(tar_file) and filecmp.cmp(tar_file, mod_file) == False: # #1001 added on 29-oct-2020 to handle the .SQL missing cases
					if developer_mode: developer_print('copying file  :', tar_file)
					copy_status = copy_file(src = files_directory, dst = each_mapped_path, files_list=[each_file],developer_mode = developer_mode)['status']  # copies the selected files
					if developer_mode: developer_print('copy_status  :', copy_status)
				else:
					if developer_mode: developer_print('File is skipped ',tar_file)
					pass

			# log can be written in future cases  25/09/2020
		except Exception as e:
			developer_print('Error while copying ',each_file)
			developer_print('Error :',e)

			return  False # commented to handle the patch
			# pass

	return True

def write_log(branch_id,epe_id,copy_status,batch_1_status,batch_2_status,git_add_files): # added on 13/10/2020
	final_text = str(branch_id) + '\t' + str(epe_id) + '\t' + str(copy_status) + '\t'
	final_text += str(batch_1_status) + '\t'+ str(batch_2_status) +'\t'
	if type(git_add_files) == list:
		final_text += str(','.join(git_add_files))
	else:
		final_text+=str(git_add_files)

	final_text += '\n'
	# logging.info(final_text)
	write_into_file(file_name = 'GIT_Automation_log.txt', contents=add_timestamp(final_text), mode='a')
	# print('Logs are written : GIT_Automation_log.txt ')

def git_auto_deploy(epe_id  ,branch_id , files_directory , files_list ,developer_mode = False,testing = False,raise_merge_request = False,ramco_obj = '',skip_git_commit = False):
	"""
	Date		  : 25/sep/2020
	:param epe_id : Source ID
	:param branch_id: destination Branch ID
	:param files_directory: Directory contains the modified fies
	:param files_list: All the file names
	:return: Status of deployment
	"""
	# developer_mode = True
	# logging_prefix = (str(epe_id)+'\t'+str(branch_id)
	# logging.info)
	merge_request_id = 0
	merge_request_status = False
	status = False

	file_1_content = get_file_content(filename = GIT_DEPLOYMENT_PATTERN_1 , return_lines = False)
	file_2_content = get_file_content(filename = GIT_DEPLOYMENT_PATTERN_2 , return_lines = False)
	# if developer_mode:
	#	 developer_print('GIT File pattern - 01 ',file_1_content)
	#	 developer_print('GIT File content - 02 ',file_2_content)
	current_path = os.getcwd()  # added here for future cases

	# bat_file_name1 = build_bat_file(pattern_code = 01,file_content = file_1_content, epe_id = epe_id,branch_id = branch_id,current_path = current_path, git_path = GIT_PATH)['bat_file_name']
	# execute_bat_file(bat_file_name1)
	# bat_file_name2 = build_bat_file(pattern_code = 02, file_content = file_2_content, epe_id = epe_id,branch_id = branch_id,current_path = current_path, git_path = GIT_PATH, modified_files = modified_files)['bat_file_name']
	# execute_bat_file(bat_file_name2)

	bat_file_1 = os.path.join(GIT_MASTER_PATH,DEPLOYMENT_PATTERN_01)
	bat_file_2 = os.path.join(GIT_MASTER_PATH,DEPLOYMENT_PATTERN_02)

	file_1_content = file_1_content.replace('<ut_main_branch>',branch_id)  # replacing the ur branch id "ut-189-mergeO48090"
	file_1_content = file_1_content.replace('<epe_id>', epe_id)  # replacing the ur branch id for file 01
	file_1_content = file_1_content.replace('<git_master_path>', GIT_MASTER_PATH)  # replacing the ur branch id for file 01

	file_2_content = file_2_content.replace('<epe_id>', epe_id)  # replacing the ur branch id for file 02
	# file_2_content = file_2_content.replace('<git_master_path>', GIT_MASTER_PATH)  # replacing the ur branch id for file 02
	# file_2_content = file_2_content.replace('<current_working_directory>', current_path)  # replacing the ur branch id for file 02 # FUTURE cases

	batch_1_status = ''
	batch_2_status = ''
	copy_status = ''
	git_add_files = ''

	write_into_file(file_name = bat_file_1, contents =file_1_content, mode='w')
	if developer_mode:
		developer_print(' batch file 01 is ready for execution ',bat_file_1)
	# Codes to handle errors in executing batch file  can be added here
	if skip_git_commit == False:
		try:
			if testing == False:
				os.system(bat_file_1) # preparing the branch environment
				if developer_mode : developer_print('Batch file 1 executed successfully ')
			batch_1_status = 'success'
		except Exception as e:
			developer_print('Error while executing Batch file 1 : {0}\n Quitting code......'.format(bat_file_1))
			batch_1_status = 'errored'
			write_log(branch_id, epe_id, copy_status, batch_1_status, batch_2_status, git_add_files)
			exit()
		if developer_mode:
			developer_print('Batch file 01 is executed ! ')
			# input('Batch file 1 is executed :  Copy path if you have any ')
		if testing == False:
			cpy_sts = copy_modified_files(files_directory,files_list,git_path = GIT_MASTER_PATH,developer_mode= developer_mode)
			if cpy_sts:
				copy_status = 'success'
			else:
				developer_print('Copy failed ! Quitting code ....')
				copy_status = 'failed'
				# write_log(branch_id, epe_id, copy_status, batch_1_status, batch_2_status, git_add_files)
				# exit()

		if copy_status == 'success':
			git_add_files = get_modified_files(files_list =  files_list,git_path = GIT_MASTER_PATH )['git_add_commands'] # runs git status files

			developer_print('modified_files :','\n'.join(git_add_files))

		if git_add_files:
			directory_change_to_file2 ='cd '+str(GIT_MASTER_PATH)+'\n'
			write_into_file(file_name = bat_file_2, contents = directory_change_to_file2 , mode = 'w')
			write_into_file(file_name = bat_file_2, contents = ''.join(git_add_files) , mode = 'a')
			write_into_file(file_name = bat_file_2, contents = file_2_content, mode='a')
			if developer_mode:
				developer_print(' Batch file 02 is ready for execution ',bat_file_2)
			# Codes to handle errors in executing batch file  can be added here

			try:
				if testing == False:
					os.system(bat_file_2)  # preparing the branch environment
				developer_print('Batch file 2 is executed successfully')
				batch_2_status = 'success'
			except Exception as e:
				developer_print('Error while executing Batch file 2 : {0}\n Quitting code......'.format(bat_file_2))
				batch_2_status = 'errored'

		else:
			developer_print('Skipping current DEFECT ID  ... because not match is found :',epe_id)

		if copy_status and batch_1_status and batch_2_status and git_add_files:
			status = True
	else:
		status = 'git_commit_skipped'

	if status and raise_merge_request:
		try:
			if not ramco_obj:
				ramco_obj =RamcoGIT()
			merge_res = ramco_obj.raise_merge_request(epe_id = epe_id, ut_branch_name = branch_id,developer_mode=developer_mode)
			merge_request_status = merge_res['status']
			merge_request_id = merge_res['merge_request_id']
		except Exception as e:
			merge_request_status = 'errored'

	#logging added on 12/10/2020

	res =  {
			'branch_id':branch_id
			,'epe_id':epe_id
			,'copy_status':copy_status
			,'batch_1_status':batch_1_status
			,'batch_2_status':batch_2_status
			,'modified_files':git_add_files
			,'merge_request_status':merge_request_status
			,'merge_request_id':merge_request_id
			,'status':status
			}
	full_log = [res['status'],res['epe_id'], res['branch_id'], res['batch_1_status'], res['copy_status'],res['batch_2_status'],res['merge_request_status'], res['merge_request_id']]
	full_log_text = '\t'.join(apply_to_list(full_log, make_string=True)) + '\n'
	write_into_file(file_name=GIT_AUTOMATION_LOG, contents=add_timestamp(full_log_text), mode='a')

	return res


def get_deployment_folder(sp_name): #added on 13/10/2020 from the config file.

	try:
		if developer_mode:
			developer_print('Given sp-name : ', sp_name)
			developer_print('Given looking term : ',sp_name.lower()[:3])
		matched_folder = GIT_FILE_LOOKUP[sp_name.lower()[:3]]
		# print('matched_folder',matched_folder)
		return {'matched_folder' : matched_folder}
	except Exception as e:
		developer_print('Keywords does not match ',e)
		return {'matched_folder' : ''}


def get_string_from_list(input_list):
	if type(input_list) == list:
		sp_calling_list = input_list
		sp_calling_str = '\n'.join(input_list)
	elif type(input_list) == str:
		sp_calling_list = input_list.split('\n')
		sp_calling_str = input_list

	return {
		'as_string': sp_calling_str
		, 'as_list': sp_calling_list
	}


def prepare_developer_statement(input_list):
	print_list = []
	for each_var in input_list:
		print_list.append(DEVELOPER_PRINT_PATTERN.replace('<variable_name>', each_var))
	return {
		'print_statements': print_list}

if __name__ == "__main__":
	if True:
		sp_calling_file = get_file_content(sys.argv[1],return_lines = True)
		sp_definition_file = get_file_content(sys.argv[2],return_lines = True)
		variables_to_check = []
		res = get_mapped_sp_variables(sp_calling = sp_calling_file,sp_definition = sp_definition_file)
		def get_mapped_sp_variables(sp_calling, sp_definition,developer_mode = False):
			sp_calling_str = ''
			sp_calling_list = ''

			sp_definition_str = ''
			sp_definition_list = ''
			res1 = get_string_from_list(sp_calling)
			sp_calling_str = res1['as_string']
			sp_calling_list = res1['as_list']
			res2 = get_string_from_list(sp_definition)
			sp_definition_str = res2['as_string']
			sp_definition_list = res2['as_list']

			defenition_tmp = sp_definition_str.split(',')
			calling_tmp = sp_calling_str.split(',')
			defenition_variables = get_valid_variables_definition(sp_definition_str.split(',')) # list of dict [{'variable':@ouinstance 'value':'0.0','type':'variable/int/string'   }
			calling_variables = get_valid_variables_calling(sp_calling_str.split(','))

				# mis_var_pattern = "@\w+"
				# missing_variables = re.findall(mis_var_pattern, str(temp_text))
			l1 = '\n'.join(apply_to_list(prepare_developer_mode_statement(calling_variables,developer_mode = developer_mode)['print_statements'],make_string = True))
			l2 = '\n'.join(apply_to_list(prepare_developer_mode_statement(defenition_variables,developer_mode = developer_mode)['print_statements'],make_string = True))
			write_into_file(file_name='DEVMODE_calling_variables.txt', contents=l1, mode='w')
			write_into_file(file_name='DEVMODE_sp_definition_variables.txt', contents=l2, mode='w')


			if len(valid_variables) == len(calling_variables):
				map_variable_and_values()












	
# 	# if False:exit()	
# 	start = time.time()
# 
# 	arg = argparse.ArgumentParser('Program to GIT AutoDeployment  !!', add_help=True)
# 	arg.add_argument('-i', '--input_excel', help='Input excel which contains ', required=True)
# 	# arg.add_argument('-o', '--output_directory', help='Output directory for the modified files', required=False)
# 	# arg.add_argument('--defects_file',
# 	#				  help='An excel or text file which contains Defect IDs SP_NAME<tab>DEFECT_ID1,DEFECT_ID2,DEFECT_ID3 ',
# 	#				  required=False)
# 	# arg.add_argument('--get_help_text', help='If the keyword is mentioned, then the text will be extracted from DB',
# 	#				  nargs='?', const=True, default=False, required=False)
# 	arg.add_argument('-dev_mode', '--developer_mode', help='This will enable the developer mode which helps the developer', nargs='?', const=True, default=False, required=False)
# 	# arg.add_argument('--skip_batch1', help='to skip the execution of Batch file 1', nargs='?', const=True, default=False, required=False)
# 	arg.add_argument('-b','--branch', help = 'Destination branch',required = False ,default='ut-189-mergeO48090')
# 	arg.add_argument('--testing', help = 'Enabled for testing purpose',required = False ,default= False , const= True,nargs='?')
# 	arg.add_argument('--branch_from_file', help = 'This will be enabled for Branches from file',required = False ,default= False , const= True,nargs='?')
# 	arg.add_argument('--raise_merge_request', help = 'Option to raise the merge request',required = False ,default= False , const= True,nargs='?')
# 	arg.add_argument('--skip_git_commit', help = 'This option skips the GIT commit',required = False ,default= False , const= True,nargs='?')
# 
# 	args = arg.parse_args()
# 	print('/nUser inputs :', args)
# 	input('Check the deployment branch ID  and press Enter')
# 	input('Check Raise merge request option !!!!')
# 	developer_mode = args.developer_mode
# 	input_excel  = args.input_excel
# 	branch = args.branch
# 	testing = args.testing
# 	branch_from_file = args.branch_from_file
# 	raise_merge_request = args.raise_merge_request
# 	skip_git_commit = args.skip_git_commit
# 
# 	input_data = get_input_excel(input_excel,developer_mode = developer_mode)['excel_data']
# 	# print (input_data)
# 	DIRECTORY = ''
# 	if input_excel:
# 		t_dic = handle_extension(input_excel)
# 		temp_file_name = str(t_dic['no_extension']) + '_AUTO_GIT_COMMITS_STATUS.txt'
# 		DIRECTORY = t_dic['directory']
# 		result_file_name = temp_file_name
# 	else:
# 		result_file_name = GIT_AUTOMATION_FILE
# 	if not DIRECTORY: DIRECTORY = os.getcwd()
# 	result_file_name = os.path.join(DIRECTORY, result_file_name)
# 
# 	headers = 'STATUS\tEPE_ID\tBRANCH_ID	BATCH_FILE_01_STATUS  COPY_STATUS BATCH_FILE_02_STATUS	MERGE_REQUEST_STATUS	MERGE_REQUEST_ID\n'
# 	write_into_file(file_name=result_file_name, contents=headers, mode='w')
# 
# 	if raise_merge_request:
# 		ramco_obj = RamcoGIT()
# 	else:
# 		ramco_obj = ''
# 
# 	for file_count, each_line in enumerate(input_data):
# 		if file_count ==0:
# 			print('Skipping headers !!',each_line)
# 			continue
# 		try:
# 			each_line = each_line[0]
# 			# print('each_line :',each_line)
# 			# input()
# 			epe_id = each_line[0].strip()
# 			if branch_from_file:
# 				branch_id = each_line[3].strip() # incase the branch is given in the file 
# 			elif branch:
# 				branch_id = branch.strip()
# 			else:
# 				print('Branch name is missing !!\tQuitting code ')
# 				exit()
# 			files_directory = each_line[1].strip()
# 			files_list = each_line[2].split(',')
# 		except Exception as e:
# 			print('Please give all the inputs..!! \n All the inputs are mandatory ,\n Skipping File no {0} \n Error : {1}'.format(file_count+1,e))
# 			continue
# 
# 		# print('Processing file : {3}....\n Source ID : {0}\t Dest ID : {1},\t Total Files : {2} \n Files : {4}'.format(epe_id,branch_id,len(files_list),file_count+1,files_list))
# 		print('Processing file : {0}/{1} ... Source ID : {2} Dest ID : {3} \n Files : {4}'.format(file_count+1,len(files_list),epe_id,branch_id,files_list))
# 		# input('Proceed ??')
# 		res = git_auto_deploy(epe_id = epe_id ,branch_id = branch_id, files_directory = files_directory, files_list =  files_list, developer_mode = developer_mode , testing = testing,raise_merge_request = raise_merge_request,ramco_obj= ramco_obj,skip_git_commit = skip_git_commit)
# 		if res:
# 			full_log = [res['status'], res['epe_id'], res['branch_id'], res['batch_1_status'], res['copy_status'],res['batch_2_status'], res['merge_request_status'], res['merge_request_id']]
# 			full_log_text = '\t'.join(apply_to_list(full_log, make_string=True)) + '\n'
# 			write_into_file(file_name=result_file_name, contents=full_log_text, mode='a')
# 
# 	end = time.time()
# 
# 	print()
# 	print('Total Time taken in seconds : {:.1f}'.format(end - start))
# 	print('Total Time taken in Minutes : {:.2f}'.format((end - start) / 60))
# 
#   # sample command to execute : python GITAutomation.py -i G:\Ajith\Excel\GIT_Automation_input.xlsx
# # python GITAutomation.py -i G:\Ajith\Excel\GIT_Automation_input.xlsx -b ut-189-mergeO48090
# # python GITAutomation.py -i g:\Ajith\Excel\GIT_Automation_input.xlsx -b ut-WMS_merge_o48090_102020
# # python GITAutomation.py -i GIT_Automation_input.xlsx -b ut-WMS_merge_o48090_102020