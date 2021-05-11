"""
Functionlaity : Script to handle Rtrack
Version       : v1.0
History       :
                v1.0 - 28/11/2020 - initial version
                
                

Input:

Process      :
Output       :

Test Cases taken   :
Test Cases passed  :
Test Cases need
to be handled      :

Pending   items :
                    




Open issues :
Comments :

"""
import time,argparse,re
import urllib.parse,sys
sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')
from selenium import webdriver
from bs4 import BeautifulSoup
from Rtrack_config import *
from Help_print import *
from CustomisedFileOperation import *
from Datastructure_help import *
from CompareAndUpdate import *

from selenium.webdriver.common.keys import Keys


class Linkedin():
	def __init__(self,url='',use_selenium = True,developer_mode = False,login = True):
		self.use_selenium = use_selenium
		self.developer_mode = developer_mode
		if not url:
			url = 'https://www.linkedin.com/mynetwork/'
		if self.use_selenium == True:
			self.browser = webdriver.Chrome()
			developer_print('Browser started...')
			self.browser.get(url)
			time.sleep(3)
			# if login:
				
			# 	self.login()
			# 	time.sleep(5)
				
	def make_connections(self,invite_count = 30):
		pass

	def login(self):
		user_name = 'ajithkumar0511@gmail.com'
		password = ''
		try:
			print('Logging in with username {} ..............'.format(USERNAME))
			# time.sleep(1)
			self.browser.find_element_by_id('username').send_keys(USERNAME)
			# time.sleep(1)
			password_elem = self.browser.find_element_by_id('password')
			password_elem.send_keys(PASSWORD)
			# time.sleep(1)
			password_elem.send_keys(Keys.ENTER)

			print('Login success ! ')
		except Exception as e:
			print('Error while loggin in ..',e)
			return False
		return True

	



if __name__ == "__main__":
	link_obj = Linkedin()
	link_obj.make_connections(invite_count = 30)
	# start = time.time()

	# arg = argparse.ArgumentParser('Program to handle Rtrack details !!', add_help=True)
	# # arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	# # arg.add_argument('--sp_name', help='single sp file', required=False)
	# arg.add_argument('-i', '--input_file', help='File contains list of procedures', required=False)
	# # arg.add_argument('-dir', '--directory', help='Directory to save the file.', required=False)
	# arg.add_argument('-dev_mode', '--developer_mode',help='This will enable the developer mode which helps the developer', nargs='?', const=True,default=False, required=False)
	# # arg.add_argument('--validate_sp', help='This option helps you to verify the fixes present in procedure  ',nargs='?', const=True, default=False, required=False)
	# # arg.add_argument('--check_missing_defects',help='This option helps to find the missing defects between different version', nargs='?',const=True, default=False, required=False)
	# # arg.add_argument('--save_files', help='This option helps to save the sps for future refereces', nargs='?',const=True, default=False, required=False)
	# # arg.add_argument('--use_local_files', help='This option helps to ignore the extraction of sps from SERVER',nargs='?', const=True, default=False, required=False)

	# args = arg.parse_args()
	# print('Input arguments :', args)
	# input("Enter to proceed ?")
	# input_file = args.input_file
	# developer_mode = args.developer_mode

	# ramco_obj = Rtrack(url='')
	# input_data = get_input_excel(input_file, developer_mode=developer_mode)['excel_data']
	# # print ('input_data[0] :',input_data[0])
	# if input_file:
	# 	t_dic = handle_extension(input_file)
	# 	temp_file_name = str(t_dic['no_extension']) + '_Rtrack_results.txt'
	# 	DIRECTORY = t_dic['directory']
	# 	if not DIRECTORY:
	# 		DIRECTORY = os.getcwd()
	# 	output_file_name = os.path.join(DIRECTORY,temp_file_name)
	# 	write_into_file(file_name=output_file_name, contents=RTRACK_HEADERS, mode='w')
	# for index,each_line in enumerate(input_data):
	# 	if index==0:
	# 		print('Skipping headers :',each_line)
	# 		continue
	# 	defect_id = each_line[0][0].strip()
	# 	# formalizing to LME-123_12 to LME-123
	# 	# print ('Defect ID before formalization : ',defect_id)
	# 	defect_id = get_all_fix_id(file_content = str(defect_id),extract_from_header = False,developer_mode=developer_mode,get_rtrack_id = True)['valid_fixes'][0]
	# 	# print ('Defect ID after formalization : ',defect_id)
	# 	if index ==0:
	# 		print('Ignoring index :',defect_id)
	# 		continue
	# 	print('Processing line : {0}/{1} , Defect id : {2}'.format(index,len(input_data),defect_id))
	# 	res_dict = ramco_obj.get_defect_details(defect_id = defect_id,developer_mode = developer_mode)
	# 	#print('Results :',res_dict)

	# 	# res_dict ={'defect_status': '\nFix Sent ',
	# 	# 		   'defect_id': 'LLE-930',
	# 	# 		   'dependency_list':
	# 	# 			   	[
	# 	# 					{'status': 'Sent For Review',
	# 	# 					 'priority': '',
	# 	# 					 'defect_id': 'EPE-25625',
	# 	# 					 'defect_desc': 'LBC FIX object  movement to UT'
	# 	# 					 }
	# 	# 				]
	# 	# 		   }
	# 	# input('Proceed ?')
	# 	if res_dict:
			
	# 		final_text = [len(res_dict['dependency_list'])]
	# 		final_text.append(res_dict['defect_id'])
	# 		final_text.append(res_dict['defect_status'])
	# 		final_text.append(res_dict['assignee'])
	# 		final_text.append(res_dict['priority_value'])
	# 		final_text.append(res_dict['issue_title'])
	# 		final_text.append(res_dict['comments'])
	# 		for dep_index,each_item in enumerate(res_dict['dependency_list']):
	# 			final_text.append(each_item['defect_id'])
	# 			final_text.append(each_item['status'])
			
	# 		temp_str = str('\t'.join(apply_to_list(final_text,make_string=True))).strip()+'\n'
	# 		write_into_file(file_name=output_file_name, contents=str(temp_str), mode='a')
	# 		write_into_file(file_name=RTRACK_LOG_FILE, contents=add_timestamp(str(temp_str)), mode='a')
	# print('Results are written in :',output_file_name)

	# end = time.time()

	# print()
	# print('Total Time taken in seconds : {:.1f}'.format(end - start))
	# print('Total Time taken in Minutes : {:.2f}'.format((end - start) / 60))


