"""
Description : Script which get help text of all the procedures for single and multi input 
Version     : 
				v3.4
History     :
				v1.0  - 30/03/2020 - initial Version
				v1.1  - 29/04/2020 - Global cursor is added to the function
				v1.2  - 17/09/2020 - get_connection_string is added to use it in Web application for object merge.
				v1.3  - 23/09/2020 - Function get_connection_string() is updated to work for the input db-credentials
				v1.4  - 26/09/2020 - Function get_connection_string() is updated to get the missing details from locally ,
									 like if we give different db then it will add it respectively
				v2.0  - 01/10/2020 - Functions get_validated_sps(),check_id_presence are added to automate the validation of defect IDS after deployment
				v2.1  - 01/10/2020 - VALIDATION_LOG is added in the function  get_validated_sps() imported "TimeStamp.py"
				v2.2  - 01/10/2020 - Logic is improved to work for more than two servers in the function  get_validated_sps() - Testing pending
				v2.3  - 02/10/2020 - additional information from the input file is added to the result file in function "get_validated_sps()"
				v2.4  - 02/10/2020 - input excel pattern is changed in validation sp defect id column is changed from 2 to 1 and sp name changed from 1 to 2
				v2.5  - 02/10/2020 - Standard tested version of validation sp , works for 1 to n servers
				v2.6  - 02/10/2020 - validation logic improved to handle if multiple sps in single line Handled cases ( "\n" and "," ) to work for
									  n servers n defects n sps
				v2.7  - 14/10/2020 -  function write_results_and_logs() is created to write logs and results
				v2.8  - 15/10/2020 -  save_files option is added to save the files locally. and tested.
				v2.9  - 16/10/2020 -  MISSING_IDS_FILE_NAME and DIRECTORY is updated to provide results on the respective directory, Validation log file name changed
				v3.1  - 22/10/2020 -  comma separated sp_name can be handled.
				v3.2  - 02/11/2020 -  Validation minor logic change with consolidated sps
				v3.3  - 23/12/2020 -  Looping is added for the cursors to save connection time.
				v3.4  - 26/04/2021 -  File input is upgraded and server choosing options is centralised.


Input       : --sp_name sp_name 
			  -i input_filename which contains the list of sps ( Validation input should be an excel )
			Text file format :
								sp_name_1
								sp_name_3
								sp_name_3
			Excel format :
							Defect_id | sp_name | EPE_ID | other n data

Output      : Stored procedure as new file which can be extracted from DB

Pending cases : 
				1, use_local_files needs to be handled in validate_sps()
				1, File name and log name to be handle in separate config file



"""
import pyodbc 
import argparse
import os,sys,re,time,sys
sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')
from serverdetails import * 
from CustomisedFileOperation import * 
from CompareAndUpdate import *
from TimeStamp import *
from Help_print import *
from Datastructure_help import *

from ObjectMerge import *

# conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=172.16.17.168,50196;DATABASE=AVNAPPDB_TEMPDB;UID=rvwuser;PWD=rvw;Trusted_Connection=no;')
# conn = pyodbc.connect('''DRIVER={ODBC Driver 13 for SQL Server};
# 						SERVER=172.16.10.68;
# 						DATABASE=scmdb;
# 						UID=Sa;
# 						PWD=war3sa*;
# 						Trusted_Connection=no;''')
global cursor

# Sample Patter
# db_details={
#             'hostname':SERVER,
#             'username':UID,
#             'password':PWD,
#             'database':DB,
#             'timeout':60
#         }


def get_connection_string(db_details = {},developer_mode = False):
	'''
	Returns the connection string based on the Database details
	'''
	local_db_details ={
						'hostname': SERVER,
						'username': UID,
						'password': PWD,
						'database': DB,
						# 'timeout': 60
						'timeout': 300
						}
	if not db_details:
		db_details = local_db_details
	for each_key in local_db_details:
		if each_key not in db_details.keys():
			# print ('Updating missing credentials... :',each_key)
			db_details[each_key] = local_db_details[each_key]
	if developer_mode:
		print ('get_connection_string:\t db_details( raw_input )',db_details)

	# db_details ={'hostname'=SERVER,'username':UID,'password':PWD,'database':DB,'timeout':60}

	# print('HelpText_sp:\tget_connection_string\t:db_details :',db_details)
	connection_string='DRIVER={ODBC Driver 13 for SQL Server};SERVER='+str(db_details['hostname'])
	connection_string+=';DATABASE='+str(db_details['database'])
	connection_string+=';UID='+str(db_details['username'])
	connection_string+=';PWD='+str(db_details['password'])
	connection_string+=';Trusted_Connection=no;'
	# for time out 
	connection_string+=' timeout='+str(db_details['timeout'])
	if developer_mode:
		print ('get_connection_string:\t built CONNECTION_STRING:',connection_string)
	return connection_string


# print ('CONNECTION_STRING :',CONNECTION_STRING)
# CONNECTION_STRING='DRIVER={ODBC Driver 13 for SQL Server};SERVER='+str(SERVER)
# CONNECTION_STRING+=';DATABASE='+str(DB)
# CONNECTION_STRING+=';UID='+str(UID)
# CONNECTION_STRING+=';PWD='+str(PWD)
# CONNECTION_STRING+=';Trusted_Connection=no;'
# # for time out 
# CONNECTION_STRING+=' timeout=60' # in seconds




def connect(CONNECTION_STRING=''):
	if not CONNECTION_STRING:
		CONNECTION_STRING=get_connection_string()
	try:
		# print ('Server information :',CONNECTION_STRING)
		print ('Connecting to the server.................',re.search("(SERVER=)(\d+.\d+.\d+.\d+)",CONNECTION_STRING,re.I).group(2))
		conn = pyodbc.connect(CONNECTION_STRING)
		cursor = conn.cursor()
		print ('Connection sucess !')
		return cursor
	except Exception as e:
		print ('Error while connecting :',e)
		return False

# cursor.execute('SELECT top 10 * FROM wms_bin_dtl')
def get_file_name(sp_name):
	file_name=sp_name.replace('.','_')
	if '.sql' in sp_name.lower():
		file_name=file_name.replace('_sql','.sql')
	else:
		file_name=file_name+'.sql'
	# print ('file_name :',file_name)
	return file_name

def get_sptext(sp_name,cursor):
	
	sp_name=sp_name.strip()
	hd_dict =handle_extension(sp_name)
	file_name = hd_dict['new_extension']
	sp_name = hd_dict['no_extension']

	full_text=''
	# global cursor
	try:
		sys.stdout.write('\r')
		sys.stdout.write('Extracting help text....'+sp_name+'')
		
		cursor.execute("sp_helptext '"+sp_name+"'")
		# sys.stdout.write('Extracting help text...."'+sp_name+'"\r\r\r')
		sys.stdout.write('\r')
		for row in cursor.fetchall():
			# print (row)
			full_text+=str(row[0]).replace('\r\n','\n')
		return {'help_text':full_text}
	except Exception as e :
		print ('Error while getting procedure text :',e)
	return {'help_text':full_text,
			'file_name':file_name}

# cursor=connect(CONNECTION_STRING)# connects to the server

# def get_help_text(CONNECTION_STRING=get_connection_string(host,username,password,),file_output_directory):
# 	file_directory=file_output_directory
# 	# file_directory='G:\\Ajith\\Issues\\Logistics\\2020\\Pss-Enhancement-Merge\\Objects-Enhancement'
# 	cursor=connect()# connects to the server
# 	file_lines=get_file_content(args.input_file)
# 	for index,each_line in enumerate(file_lines):
# 		each_line=each_line.strip('\t\r\n')
# 		print ('processing :',index)
# 		file_name =get_file_name(each_line)
# 		if file_directory:
# 			file_name=os.path.join(file_directory,file_name)
# 			print ('file_name :',)
# 		help_text=get_sptext(each_line)['help_text']
# 		write_into_file(file_name=file_name,contents=help_text,mode='w')

def check_id_presence(help_text , defects_list,extract_from_header,developer_mode = False):
	extracted_fix_ids = get_all_fix_id(file_content = help_text, extract_from_header = extract_from_header, developer_mode = developer_mode)['valid_fixes']
	if developer_mode:
		developer_print('"look_in_header status"  :',extract_from_header)
		developer_print('Extracted fix ids :',extracted_fix_ids)

	extracted_fix_ids_lower = [i.lower() for i in extracted_fix_ids]
	if developer_mode:
		developer_print(' extracted_fix_ids_lower :',extracted_fix_ids_lower)
		# input('input')

	result_dict = {}
	for each_look_defect in defects_list:
		status = 'No'
		if each_look_defect.strip().lower() in extracted_fix_ids_lower:
			if developer_mode:
				developer_print('Defect {0} is present in input list {1} :'.format(each_look_defect,extracted_fix_ids))
			status = 'Yes'
		if each_look_defect not in result_dict.keys():
			result_dict[each_look_defect] = status
	if developer_mode:
		developer_print(' Result list  :',result_dict)
	return {
			'defect_validation_status': result_dict,
			'extracted_fix_ids': extracted_fix_ids # added on 14/10/2020 for getting the missing defects list
			}

def get_validated_sps(file_lines ,host_list,extract_from_header ,developer_mode = False,file_name = '',save_files = False,use_local_files = False):
	VALIDATION_LOG_NAME = 'HELPTEXT_DEFECT_VALIDATION_LOG.txt'
	DIRECTORY = ''
	if file_name:

		t_dic = handle_extension(file_name)
		temp_file_name = str(t_dic['no_extension']) + '_validation_results.txt'
		DIRECTORY = t_dic['directory']
		VALIDATION_FILE_NAME = temp_file_name
	else:
		VALIDATION_FILE_NAME = 'validation_results.txt'
	if not DIRECTORY: DIRECTORY = os.getcwd()
	VALIDATION_FILE_NAME = os.path.join(DIRECTORY, VALIDATION_FILE_NAME)


	cursors = []
	header_mid_term = []
	master_validation_list = []
	for index, host_dict in enumerate(host_list):  # looping servers
		cursors.append(connect(get_connection_string(db_details=host_dict)))
		# header_mid_term += '\t' + str(host_dict['hostname']) + '_presence'
		header_mid_term.append(str(host_dict['hostname']) + '_presence')
	print('Total cursors :', len(cursors))

	header_text = '\t'.join(['DEFECT ID','OBJECT NAME','EPE ID'] + header_mid_term )+'\n'
	write_into_file(file_name=VALIDATION_FILE_NAME, contents=header_text, mode='w')
	# write_results_and_logs(file_name=VALIDATION_FILE_NAME, log_name=VALIDATION_LOG_NAME, content=header_text,header_data=True)
	# print('Ignoring headers for processing...', each_line)

	def_res_dict = prepare_input_from_defects_file(file_name, developer_mode=False)
	# epe_id_and_sps = def_res_dict['epe_id_and_sps']  # for GIT Input preparation
	sp_and_defects = def_res_dict['sp_and_defects']
	defect_status_list = {}
	for index, each_dict in enumerate(sp_and_defects):  # processed inputs
		temp_list = []
		defects_list = sp_and_defects[each_dict]['defects']
		epe_id = sp_and_defects[each_dict]['epe_id']
		each_sp = each_dict
		print('Processing sp {0}/{1} : {2}'.format(index+1,len(sp_and_defects),each_sp))
		for cur_index, each_cursor in enumerate(cursors):
			help_text = str(get_sptext(handle_extension(each_sp)['no_extension'], each_cursor)['help_text'])
			if save_files == True:
				file_directory_temp = os.path.join(DIRECTORY, str(
					host_list[cur_index]['hostname'].replace('.', '_')) + '_Extracted_objects')
				check_and_make_path(file_directory_temp)
				if developer_mode:
					developer_print('file_directory_temp :', file_directory_temp)
					developer_print('each_sp :', each_sp)
				file_name_temp = os.path.join(file_directory_temp, handle_extension(each_sp)['new_extension'])
				if developer_mode:
					developer_print('handle_extension(each_sp)[new_extension] :',
									handle_extension(each_sp)['new_extension'])
					developer_print('file_name_temp :', file_name_temp)
				# input()
				write_into_file(file_name=file_name_temp, contents=help_text, mode='w')
			results_dict = check_id_presence(help_text=help_text, extract_from_header=extract_from_header, defects_list=defects_list,developer_mode=developer_mode)['defect_validation_status']
			temp_list.append(results_dict)
			if developer_mode:
				developer_print('Temp list : ',temp_list)
		# defect_status_list.append(results_dict)
		defect_status_list[each_sp] = temp_list
		if developer_mode:
			developer_print('defect_status_list : ', defect_status_list)

		if developer_mode:
			developer_print('DEFECT_STATUS_LIST :', defect_status_list)
			# input()
		if developer_mode:
			developer_print(' defects_list ', defects_list)
			developer_print(' defect_status_list ', defect_status_list)
		for each_defect in defects_list:
			if developer_mode:
				developer_print(' each defect :', each_defect)
			temp_dict = {'sp_name': each_sp, each_defect: []}
			# final_text = str(each_defect) + '\t' + str(each_sp)
			final_text = [each_defect,each_sp,epe_id]
			for each_res_dict in defect_status_list[each_sp]:
				if developer_mode:
					developer_print('each_res_dict :', each_res_dict)
					developer_print('each_res_dict[each_defect] :', each_res_dict[each_defect])
					input()

				# final_text += '\t' + str(each_res_dict[each_defect])
				final_text.append(each_res_dict[each_defect])
				temp_dict[each_defect].append(each_res_dict[each_defect])
			if developer_mode:
				developer_print(' Final text to write :', final_text)
				input()
			# write_validation_results(VALIDATION_FILE_NAME = VALIDATION_FILE_NAME, content = final_text+'\n',header_data=False)
			full_log_text = '\t'.join(apply_to_list(final_text, make_string=True))+'\n'
			write_into_file(file_name=VALIDATION_FILE_NAME, contents=full_log_text, mode='a')
			write_into_file(file_name=VALIDATION_LOG_NAME, contents=add_timestamp(full_log_text), mode='a')
			master_validation_list.append(temp_dict)

	return {
		'validation_list': master_validation_list
		, 'file_name': VALIDATION_FILE_NAME
		, 'log_name': VALIDATION_LOG_NAME
	}


def get_validated_sps_old(file_lines ,host_list,extract_from_header ,developer_mode = False,file_name = '',save_files = False):
	"""
	:date : 01/10/2020 
	:param file_lines: input lines returned from excel 
	:param developer_mode: 
	:return: defect id presence : True or False
	future update  : should work for all the host_names in the list : Done Already
	"""
	VALIDATION_LOG_NAME ='HELPTEXT_DEFECT_VALIDATION_LOG.txt'
	DIRECTORY = ''
	if file_name:

		t_dic = handle_extension(file_name)
		temp_file_name = str(t_dic['no_extension']) +'_validation_results.txt'
		DIRECTORY = t_dic['directory']
		VALIDATION_FILE_NAME = temp_file_name
	else:
		VALIDATION_FILE_NAME = 'validation_results.txt'
	if not DIRECTORY: DIRECTORY = os.getcwd()
	VALIDATION_FILE_NAME = os.path.join(DIRECTORY,VALIDATION_FILE_NAME)

	# db_detail1 = {'hostname': '172.27.4.198'} # UT
	# db_detail2 = {'hostname': '172.27.5.174'} # ST
	# new logic starts here

	cursors = []
	header_mid_term = ''
	for index,host_dict in enumerate(host_list): # looping servers
		cursors.append(connect(get_connection_string(db_details = host_dict)))
		header_mid_term += '\t'+str(host_dict['hostname'])+'_presence'
	print('Total cursors :',len(cursors))

	master_validation_list =[]
	for index, temp_line in enumerate(file_lines): # looping sps
		each_line = temp_line[0]  # copying the row 01
		if index == 0:
			header_text = str('\t'.join(each_line)) +str(header_mid_term) + '\n'
			# write_validation_results(VALIDATION_FILE_NAME = VALIDATION_FILE_NAME, content = header_text,header_data = True)
			write_results_and_logs(file_name=VALIDATION_FILE_NAME, log_name=VALIDATION_LOG_NAME, content=header_text,header_data=True)
			print('Ignoring headers for processing...', each_line)
			continue
		print('Processing  line : {0} \t sp_name : {1} :'.format(index, each_line[1]))
		# input('Proceed ?')
		try:
			sp_names = check_suspects(each_line[1])['result']
			defects_list = check_suspects(each_line[0])['result']


			print('Total sps     : {0}, SPS        : {1}'.format(len(sp_names),sp_names))
			print('Total Defects : {0}, Defect IDs : {1}'.format(len(defects_list),defects_list))
			# input()
		# print('defects_list :',defects_list)
		except Exception as e:
			print('Error while processing input data :', e)
			print('Skipping the line ....', each_line)
			continue

		defect_status_list ={}
		for each_sp in sp_names:
			temp_list =[]
			if developer_mode:
				developer_print('each_sp :',each_sp)
			for cur_index,each_cursor in enumerate(cursors):

				help_text = str(get_sptext(handle_extension(each_sp)['no_extension'], each_cursor)['help_text'])
				if save_files == True:
					file_directory_temp = os.path.join(DIRECTORY, str(host_list[cur_index]['hostname'].replace('.','_'))+'_Extracted_objects')
					check_and_make_path(file_directory_temp)
					if developer_mode:
						developer_print('file_directory_temp :',file_directory_temp)
						developer_print('each_sp :',each_sp)
					file_name_temp = os.path.join(file_directory_temp,handle_extension(each_sp)['new_extension'])
					if developer_mode:
						developer_print('handle_extension(each_sp)[new_extension] :', handle_extension(each_sp)['new_extension'])
						developer_print('file_name_temp :', file_name_temp)
					# input()
					write_into_file(file_name=file_name_temp, contents=help_text, mode='w')

				results_dict = check_id_presence(help_text=help_text, extract_from_header=extract_from_header,defects_list=defects_list, developer_mode=developer_mode)['defect_validation_status']
				temp_list.append(results_dict)
				# defect_status_list.append(results_dict)
			defect_status_list[each_sp] = temp_list

			# defect_status_list.append(
			# 					{
			# 						'sp_name':each_sp
			# 						,'defects_status':results_dict
			# 					}
			# 	)

		if developer_mode:
			print('HelpText_sp:\tget_validated_sps:\t DEFECT_STATUS_LIST :',defect_status_list)
			input()
		for each_defect in defects_list:
			if developer_mode:
				print('HelpText_sp:\tget_validated_sps:\t each defect :', each_defect)
			for each_sp in sp_names:
				temp_dict = {'sp_name':each_sp.strip() , each_defect : []}
				final_text = str(each_defect).strip('\r\n\t,') + '\t' +str(each_sp).strip('\r\n\t,')
				try:
					final_text += '\t'+str('\t'.join(each_line[2:])) # additional lines from the input line
				except Exception as e:
					print('Error while adding additional details from the SP :',e)
					input()
					final_text += ''
				for each_res_dict in defect_status_list[each_sp]:
					if developer_mode:
						print('HelpText_sp:\tget_validated_sps:\t each_res_dict :',each_res_dict)
						print('HelpText_sp:\tget_validated_sps:\t each_res_dict[each_defect] :',each_res_dict[each_defect])
						input()

					final_text += '\t' + str(each_res_dict[each_defect])
					temp_dict[each_defect].append(each_res_dict[each_defect])
				if developer_mode:
					print ('HelpText_sp:\tget_validated_sps:\t Final text to write :',final_text)
					input()
				# write_validation_results(VALIDATION_FILE_NAME = VALIDATION_FILE_NAME, content = final_text+'\n',header_data=False)
				write_results_and_logs(file_name=VALIDATION_FILE_NAME, log_name=VALIDATION_LOG_NAME,content=final_text+'\n', header_data=False)
				master_validation_list.append(temp_dict)

	return {
		'validation_list': master_validation_list
		,'file_name': VALIDATION_FILE_NAME
		,'log_name': VALIDATION_LOG_NAME
	}

# def write_validation_results(VALIDATION_FILE_NAME ,content, header_data = False):
#
# 	VALIDATION_LOG = 'defect_validation_log.txt'
# 	VALIDATION_FILE_MODE = VALIDATION_LOG_MODE = 'a'
# 	if header_data:
# 		VALIDATION_FILE_MODE = 'w'
# 	write_into_file(file_name = VALIDATION_FILE_NAME, contents = content, mode = VALIDATION_FILE_MODE)
# 	write_into_file(file_name = VALIDATION_LOG , contents = str(get_time_stamp()['common_timestamp'])+'\t'+str(content), mode = VALIDATION_LOG_MODE)

# def write_results_and_logs(file_name,log_name, content, header_data=False,file_mode = 'a', log_mode = 'a')
#
# 	# VALIDATION_LOG = 'defect_validation_log.txt'
# 	# VALIDATION_FILE_MODE = VALIDATION_LOG_MODE = 'a'
# 	if header_data:
# 		file_mode = 'w'
# 	write_into_file(file_name = file_name, contents = content, mode = file_mode)
# 	write_into_file(file_name = log_name , contents = add_timestamp(content), mode = log_mode)


def check_suspects(sp_names):
	sp_names = sp_names.strip('\r\n\t,')
	SUSPECT_SPLITTERS = [',', '\n']
	status = 'no_change'
	splitter = ''
	for each_suspect in SUSPECT_SPLITTERS:
		if each_suspect in sp_names:
			splits = sp_names.split(each_suspect)
			if len(splits) > 1:
				sp_names = splits
				status = 'splitted'
				splitter = each_suspect
				break
	if type(sp_names) == str: sp_names = [sp_names]
	# print('sp_names WITH .sql :', sp_names)
	for index,eac_sp in enumerate(sp_names):
		if eac_sp.strip().lower().endswith('.sql'):
			eac_sp_tmp=eac_sp.strip()
			eac_sp_tmp=eac_sp_tmp.split('.')[0]
			# print('eac_sp :',eac_sp)
			# print('.sql removed')
			# print('eac_sp_tmp :',eac_sp_tmp)
			sp_names[index] = eac_sp_tmp
	# print('sp_names after removed .sql :',sp_names)
	# input()
	return {
		'result': sp_names
		, 'status': status
		, 'splitter': splitter
	}

def get_missing_defects(file_lines ,host_list,extract_from_header = True,developer_mode = False,file_name = '',save_files = False, use_local_files = False,input_directory = '',output_directory = ''):
	"""
		:date : 14/10/2020
		:param file_lines: input lines returned from excel
		:param developer_mode:
		:return: missing defects

		"""
	MISSING_IDS_LOG_NAME ='missing_ids_log.txt'
	DIRECTORY =''
	if file_name:
		# temp_file_name = str(file_name.split(os.sep)[-1].split('.')[0]) +'.txt'
		t_dic = handle_extension(file_name)
		temp_file_name = str(t_dic['no_extension']) + '_missing_defects.txt'
		DIRECTORY = t_dic['directory']

		MISSING_IDS_FILE_NAME = temp_file_name
	else:
		MISSING_IDS_FILE_NAME = 'missing_defects.txt'
	if not DIRECTORY: DIRECTORY = os.getcwd()
	MISSING_IDS_FILE_NAME = os.path.join(DIRECTORY,MISSING_IDS_FILE_NAME)




	# db_detail1 = {'hostname': '172.27.4.198'} # UT
	# db_detail2 = {'hostname': '172.27.5.174'} # ST
	# new logic starts here

	cursors = []
	header_mid_term = ''
	for index, host_dict in enumerate(host_list):  # looping servers
		if use_local_files:
			cursors.append(1)
		else:
			cursors.append(connect(get_connection_string(db_details=host_dict)))
	print('Total cursors :', len(cursors))

	missing_master_list = []
	for index, temp_line in enumerate(file_lines):  # looping sps
		each_line = temp_line[0]  # copying the row 01
		if index == 0:
			header_text ='SP \t HOST_NAME \t NO_OF_TOTAL_DEFECTS \t NO_OF_MISSING_DEFECTS \t NO_OF_DEFECTS_PRESENT \t'
			header_text +='MISSING_DEFECT \t TOTAL_DEFECTS \t DEFECTS_PRESENT \n'
			write_results_and_logs(file_name=MISSING_IDS_FILE_NAME,log_name =  MISSING_IDS_LOG_NAME, content=header_text, header_data=True)
			developer_print('Ignoring headers for processing...', each_line)
			continue
		developer_print('Processing  line : ',index+1,'\t sp_name : ',each_line[1])
		try:
			sp_names = check_suspects(each_line[1])['result']
			if developer_mode:
				developer_print('Total sps     :',len(sp_names), ' SPS        : ',sp_names)
		except Exception as e:
			developer_print('Error while processing input data :', e)
			developer_print('Skipping the line ....', each_line)


		for each_sp in sp_names:
			temp_list = []
			for cur_index, each_cursor in enumerate(cursors):
				file_directory_temp = os.path.join(DIRECTORY, str(host_list[cur_index]['hostname'].replace('.', '_')) + '_Extracted_objects')
				if use_local_files:
					if cur_index == 0 and input_directory:
						file_name_temp = os.path.join(input_directory, handle_extension(each_sp)['new_extension'])
					elif cur_index ==1  and output_directory:
						file_name_temp = os.path.join(output_directory, handle_extension(each_sp)['new_extension'])
					else:
						file_name_temp = os.path.join(file_directory_temp, handle_extension(each_sp)['new_extension'])
					try:
						help_text = get_file_content(file_name_temp,return_lines=False)
					except Exception as e:
						developer_print('Error while reading local files directory :',file_directory_temp)
						developer_print('Error while reading local files file :',file_name_temp)

				else:

					help_text = str(get_sptext(handle_extension(each_sp)['no_extension'], each_cursor)['help_text'])
					if save_files == True:
						# file_directory_temp = os.path.join(DIRECTORY, str(host_list[cur_index]['hostname'].replace('.', '_')) + '_Extracted_objects')
						check_and_make_path(file_directory_temp)
						if developer_mode:
							developer_print('file_directory_temp :',file_directory_temp)
							developer_print('each_sp :',each_sp)
						file_name_temp = os.path.join(file_directory_temp,handle_extension(each_sp)['new_extension'])
						if developer_mode:
							developer_print('handle_extension(each_sp)[new_extension] :', handle_extension(each_sp)['new_extension'])
							developer_print('file_name_temp :', file_name_temp)
						# input()
						write_into_file(file_name=file_name_temp, contents=help_text, mode='w')
				if not help_text:
					developer_print('Help_text is not extracted !')
					continue
				defects = check_id_presence(help_text=help_text,extract_from_header=extract_from_header, defects_list=[], developer_mode=developer_mode)['extracted_fix_ids']
				temp_list.append(defects)
			if len(temp_list) != 2:
				developer_print('Two cursors are (only) required !\n Quitting code...')
				exit()

			total_defects_a = temp_list[0]
			total_defects_b = temp_list[1]
			if developer_mode:
				developer_print('Total defects extracted from Server 01 :',len(total_defects_a))
				developer_print('Total defects extracted from Server 02 :',len(total_defects_b))
			difference_dict = get_list_difference(total_defects_a,total_defects_b)
			if developer_mode:
				developer_print('difference_dict[list1_missing] : ',difference_dict['list1_missing'])
				developer_print('difference_dict[list1_presence] : ',difference_dict['list1_presence'])
				developer_print('difference_dict[list2_missing] : ',difference_dict['list2_missing'])
				developer_print('difference_dict[list2_presence] : ',difference_dict['list2_presence'])

			final_text1 = [each_sp.strip(),host_list[0]['hostname']
						, len(total_defects_a)
						, len(difference_dict['list1_missing'])
						, len(difference_dict['list1_presence'])
						, ','.join(apply_to_list(difference_dict['list1_missing'], make_upper=True))
						, ','.join(total_defects_a )
						, ','.join( apply_to_list( difference_dict['list1_presence'],make_upper = True ))
					   , '\n']

			final_text2 = [each_sp.strip(), host_list[1]['hostname']
				, len(total_defects_b)
				, len(difference_dict['list2_missing'])
				, len(difference_dict['list2_presence'])
				, ','.join(apply_to_list(difference_dict['list2_missing'], make_upper=True))
				, ','.join(total_defects_b)
				, ','.join(apply_to_list(difference_dict['list2_presence'], make_upper=True))
				, '\n']


			final_text  = str( '\t'.join( apply_to_list( final_text1 , make_string = True) ) )
			final_text += str( '\t'.join( apply_to_list( final_text2 , make_string = True) ))

			write_results_and_logs(file_name = MISSING_IDS_FILE_NAME, log_name = MISSING_IDS_LOG_NAME,content = final_text, header_data = False)

	return  {
			'missing_list': missing_master_list
			,'file_name': MISSING_IDS_FILE_NAME
			,'log_name': MISSING_IDS_LOG_NAME
	}







	# extracted_fix_ids = get_all_fix_id(file_content=help_text, extract_from_header=extract_from_header, developer_mode=developer_mode)['valid_fixes']
	# extracted_fix_ids = get_all_fix_id(file_content=help_text, extract_from_header=extract_from_header, developer_mode=developer_mode)['valid_fixes']


if __name__ == '__main__':
	start = time.time()
	#
	
	if True:
		arg = argparse.ArgumentParser('Program to Help stub addition !!',add_help=True)
		# arg.add_argument('-i','--input_file',help='Trace file name',required=True)
		arg.add_argument('--sp_name',help='single sp file',required=False)
		arg.add_argument('-i','--input_file',help='File contains list of procedures',required=False)
		arg.add_argument('-dir','--directory',help='Directory to save the file.',required=False)
		arg.add_argument('-dev_mode', '--developer_mode',help='This will enable the developer mode which helps the developer', nargs='?', const=True,default=False, required=False)
		arg.add_argument('--validate_sp',help='This option helps you to verify the fixes present in procedure  ', nargs='?', const=True,default=False, required=False)
		arg.add_argument('--check_missing_defects',help='This option helps to find the missing defects between different version', nargs='?', const=True,default=False, required=False)
		arg.add_argument('--save_files',help='This option helps to save the sps for future refereces', nargs='?', const=True,default=False, required=False)
		arg.add_argument('--use_local_files',help='This option helps to ignore the extraction of sps from SERVER', nargs='?', const=True,default=False, required=False)
		# arg.add_argument('-i','--input_file',help='Trace file name',default ='scorpio,pisces',required=False)
		# arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
		args = arg.parse_args()
		print('Input arguments :',args)
		# input("Enter to proceed ?")
		input_file = args.input_file
		developer_mode = args.developer_mode
		validate_sp = args.validate_sp
		check_missing_defects = args.check_missing_defects
		save_files = args.save_files
		use_local_files = args.use_local_files
		directory = args.directory
		sp_name = args.sp_name


		# --certrali
		servers_list = [
							# {'hostname': '172.27.4.198'}, # ST-188 
							# # # {'hostname': '172.27.5.174'}  # 189 
							# # # {'hostname': '172.27.4.77'} # UT
							# {'hostname': '172.27.7.94'} # UT
							# {'hostname': '172.27.7.93'} # UT
							# {'hostname': '172.27.5.100,50196','username': 'haecologin','password': 'AvnH@ec0Dev12$','database': 'AVNAPPDB'} # Haeco  AVNAPPDB   Integdb
							# {'hostname': '172.27.5.100,52183','username': 'ericksonlogin','password': 'AvnEr!kDev12$','database': 'Integdb'} # Eriksonm 
							{'hostname': '172.27.5.100,54986','username': 'ramcoadmin','password': 'password12$','database': 'AVNAPPDB'} # AACL  AVNAPPDB   Integdb
							# ,{'hostname': '172.27.5.100,54986','username': 'ramcoadmin','password': 'password12$','database': 'Integdb'} # AACL  AVNAPPDB   Integdb

							]
			# 			'username': 'select',
			# 			'password': 'select',
			# 			'database': 'scmdb',
			# 			'timeout': 60
			# 			}
		cursors =[]
		for each_server in servers_list:
			CONNECTION_STRING = get_connection_string(db_details = each_server)
			cursor=connect(CONNECTION_STRING)# connects to the server
			cursors.append(cursor)




		if validate_sp or check_missing_defects:
			if not input_file.lower().endswith('.xlsx'):
				print('For validation process , Inputs from Excel files are only accepted patterns "sp_name | defect1,defect2,defect3"\n Quitting code..')
				exit()
			input_data = get_input_excel(input_file, developer_mode = developer_mode)['excel_data']
			print('Total lines in input file :',len(input_data))

			file_name = input_file
			extract_from_header = True
			host_list =[{'hostname': '172.27.4.198'}
					,{'hostname': '172.27.4.77'} # UT - 189 
				,{'hostname': '172.27.5.174'} # ST - 189
				# ,{'hostname': '172.27.4.198'}
				# ,{'hostname': '172.27.5.174'}
			]
			if validate_sp  == True:
				print('Total servers to check : ',len(host_list))
				print('Servers : ',[i['hostname'] for i in host_list])
				result = get_validated_sps(file_lines = input_data,host_list = host_list,extract_from_header = extract_from_header,file_name = file_name ,developer_mode = developer_mode, save_files = save_files,use_local_files = use_local_files)
				# result
				# full_log = [input_directory, sp_file_name,','.join(apply_to_list(defects_to_be_added, make_string=True)), len(FilelinesA),len(FilelinesB), len(correct_list)]
				# full_log_text = '\t'.join(apply_to_list(full_log, make_string=True))
				# write_into_file(file_name=OBJECT_MERGE_FULL_LOG, contents=add_timestamp(full_log_text), mode='a')
				print('Validation compeleted\n Please check the result file : ',result['file_name'])
			if check_missing_defects == True:
				missing = get_missing_defects(file_lines=input_data, host_list=host_list,extract_from_header = extract_from_header, file_name=file_name,developer_mode=developer_mode , save_files = save_files, use_local_files = use_local_files,input_directory=input_directory,output_directory=output_directory)
				print('Missing defects are found !\n Please check the result file : ', missing['file_name'])


			# db_details = {}
		elif sp_name:
			loop_count = 0
			while True:
				loop_count+=1
				if loop_count>1:
					directory = str(input('Enter the directory:\t')).strip()
					sp_name = str(input('Enter the sp names :\t')).strip()
				total_sps = str(sp_name).strip().split(',')
				# print ('Total sps :',','.join(total_sps))
				print ('Total sps :',len(total_sps))
				print ('Entered directory :',directory)	
				for cur_index,cursor in enumerate(cursors):
					
					
					if not cursor: 
						print('No active Cursor ! \n Quitting code .')
						exit()
					for ind,each_sp in enumerate(total_sps):
						if not each_sp: continue
						res = handle_extension(each_sp)
						temp_sp = res['no_extension']
						file_name = res['new_extension']
						print('Processing {3}: {0}/{1}, {2} '.format(ind+1,len(total_sps),each_sp,servers_list[cur_index]['hostname']))
						help_text=str(get_sptext(temp_sp,cursor)['help_text'])
						if directory:
							file_directory = check_and_make_path(directory)['directory']
						else:
							file_directory = check_and_make_path(os.path.join(os.getcwd(), 'Extracted_objects'))['directory']
						if len(servers_list)>1:
							# server_prefix = str(each_server['hostname']).replace('.','_')
							server_prefix = str(servers_list[cur_index]['hostname']).replace('.','_').replace(',','_')
							host_dir = os.path.join(file_directory,server_prefix)
							file_directory = check_and_make_path(host_dir)['directory']
						write_into_file(file_name=os.path.join(file_directory,file_name),contents=help_text,mode='w')
				print('--------------------------------------------------------------------------------')
				if 'exit' in str(input('Press enter to continue! and type exit to quit :')).lower():
					break
		elif args.input_file:
			sp_name = args.input_file
			


			loop_count = 0
			while True:
				loop_count+=1
				if loop_count>1:
					directory = str(input('Enter the directory:\t')).strip()
					sp_name = str(input('Enter the sp names or input file path  :\t')).strip()

				try:
					total_sps=get_file_content(sp_name)
				except Exception as e:
					print('Error while reading as file  :',e)
					total_sps = str(sp_name).strip().split(',')

				print (' total_sps  :',len(total_sps))#,file_lines)

				for cur_index,cursor in enumerate(cursors):
					if not cursor: 
						print('No active Cursor ! \n Quitting code .')
						exit()
					for ind,each_sp in enumerate(total_sps):
						if not each_sp: continue
						each_sp = each_sp.strip()
						res = handle_extension(each_sp)
						temp_sp = res['no_extension']
						file_name = res['new_extension']
						print('Processing {3}: {0}/{1}, {2} '.format(ind+1,len(total_sps),each_sp,servers_list[cur_index]['hostname']))
						help_text=str(get_sptext(temp_sp,cursor)['help_text'])
						if directory:
							file_directory = check_and_make_path(directory)['directory']
						else:
							file_directory = check_and_make_path(os.path.join(os.getcwd(), 'Extracted_objects'))['directory']
						if len(servers_list)>1:
							# server_prefix = str(each_server['hostname']).replace('.','_')
							server_prefix = str(servers_list[cur_index]['hostname']).replace('.','_').replace(',','_')
							host_dir = os.path.join(file_directory,server_prefix)
							file_directory = check_and_make_path(host_dir)['directory']
						write_into_file(file_name=os.path.join(file_directory,file_name),contents=help_text,mode='w')
					print('--------------------------------------------------------------------------------')
				if 'exit' in str(input('Press enter to continue! and type exit to quit :')).lower():
					break
		else:
			print ('Please provide --sp_name procedure_name or -i input_filename ')
	end = time.time()
	print('Total Time taken in seconds : {:.1f}'.format(end - start))
	print('Total Time taken in Minutes : {:.2f}"'.format((end - start) / 60))
	exit()


#  command to run : python HelpText_sp.py -i g:\Ajith\text_files\input_test.txt
#  command to run validations  : python HelpText_sp.py -i g:\Ajith\Excel\Real_time_test_1_prasath.xlsx --validate_sp