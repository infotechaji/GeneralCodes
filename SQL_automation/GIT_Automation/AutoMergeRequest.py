"""
Functionlaity : Script to generate merge request
Version       : v1.4
History       :
                v1.0 - 15/10/2020 - initial version
                v1.1 - 15/10/2020 - Log in successful , new merge page is clicked correcly.
                v1.2 - 30/10/2020 - Perfect working version is added , Validation of merge requests using the commit message is added.
                v1.3 - 31/10/2020 - Text to speech intimation is added
                v1.4 - 19/01/2021 - Source prefix added. 

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


import sys
sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')
from CompareAndUpdate import get_all_fix_id
from CustomisedFileOperation import *
from TimeStamp import *
from Help_print import *
from Datastructure_help import *
from Text_to_speech import *

from AutoMergeRequest_config import *

import time,argparse
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup


class RamcoGIT():
	def __init__(self,url = '',use_selenium = True,developer_mode = False,login = True):
		if not url:
			url = GIT_SOURCE_LINK
		self.use_selenium = use_selenium
		self.developer_mode = developer_mode
		if self.use_selenium == True:
			self.browser = webdriver.Chrome()
			developer_print('Browser started...')
			self.browser.get(url)
			if login:
				time.sleep(2)
				self.login()
				time.sleep(2)


	def login(self):
		user_name = USER_NAME
		password = PASSWORD
		try:
			print('Logging in with username {} ..............'.format(USER_NAME))
			time.sleep(1)
			self.browser.find_element_by_id('user_login').send_keys(USER_NAME)
			time.sleep(1)
			password_elem = self.browser.find_element_by_id('user_password')
			password_elem.send_keys(PASSWORD)
			time.sleep(1)
			password_elem.send_keys(Keys.ENTER)

			print('Login success ! ')
		except Exception as e:
			print('Error while loggin in ..',e)
			return False
		return True

	def raise_merge_request(self,epe_id ,ut_branch_name,source_prefix ='dev-',source_suffix ='',developer_mode = False,voice_mode = False):

		status = False
		branch_presence = False
		merge_request_id = 0
		commit_match = False
		epe_id = epe_id.strip()
		ut_branch_name = ut_branch_name.strip()
		comments = ''

		source_branch = str(source_prefix)+str(epe_id)+str(source_suffix)
		destination_branch = ut_branch_name
		temp_req = NEW_MERGE_REQUEST_PATTERN
		expected_commit_message = COMMIT_MESSAGE_PATTERN.replace('<epe_id>',epe_id)
		if developer_mode:
			developer_print('Source branch :',source_branch)
			developer_print('Destination branch :',destination_branch)
		# new_merge_req = temp_req.replace('<source_branch>',source_branch).replace('<destination_branch>',destination_branch)
		# source_branch = 'dev-'+str(epe_id)
		new_merge_req = temp_req.replace('<source_branch>',str(source_branch)).replace('<destination_branch>',destination_branch)
		if developer_mode:
			developer_print('New merge request created :',new_merge_req)
		# developer_print('New merge request created :',new_merge_req)
		# input()
		developer_print('Creating new merge request for S:', source_branch,' D:',destination_branch)
		self.browser.get(new_merge_req)

		time.sleep(5)
		try:
			# checking the commit message
			commmit_elem = self.browser.find_element_by_id("merge_request_title")
			commit_msg_tmp = str(commmit_elem.get_attribute("value")).strip()
			if developer_mode:
				developer_print('Extracted commmit message :',commit_msg_tmp)
				developer_print('expected_commit_message :',expected_commit_message)
			if commit_msg_tmp.lower() == expected_commit_message.lower():
				commit_match = True
				if developer_mode:
					developer_print('Commit messages are matched  :', commit_msg_tmp)
			else:
				raise Exception("Commit message does not matches")

			suspect_element = self.browser.find_element_by_name("commit")
			suspect_text = str(suspect_element.get_attribute("value")).strip()
			if developer_mode:
				developer_print('Suspect element Text :',suspect_text)
			if suspect_text.lower() in SUBMIT_TEXTS :
				branch_presence = True
				try:
					# input('Check to proceed for creation ??')
					suspect_element.click()
					time.sleep(3)
					status = True
					developer_print('Merge request is created !')
					if voice_mode:
						speak_words('Merge request is created for '+str(epe_id))
					merge_request_id = str(self.browser.find_element_by_class_name("breadcrumbs-sub-title").text).strip()
				except Exception as e :
					developer_print('Error in clicking the submit button !:',e)
			elif suspect_text.lower() in CASES_TO_IGNORE :
				developer_print('No submit button is available  :')

			else:
				developer_print('Undefined text is found in the buttons:')


		except Exception as e:
			if developer_mode:
				developer_print('Error while Submitting request :',e)
			developer_print('Request not raised for :',epe_id)
			if voice_mode:
				speak_words('Request is not raised for :'+str(epe_id))
			comments = str(e).replace('\t',' ').replace('\n',' ').replace('  ',' ')


		res =  {
				'status':status
				,'branch_presence':branch_presence
				,'source_branch':source_branch
				,'destination_branch':destination_branch
				,'merge_request_link':new_merge_req
				,'merge_request_id':merge_request_id
				,'commit_match':commit_match
				,'comments':comments
		}
		full_log = [res['source_branch'], res['destination_branch'], res['branch_presence'], res['commit_match'],res['status'], res['merge_request_id'], res['comments']]
		full_log_text = '\t'.join(apply_to_list(full_log, make_string=True)) + '\n'
		write_into_file(file_name=AUTO_MERGE_REQUEST_LOG, contents=add_timestamp(full_log_text), mode='a')
		return res



	def get_page_source(self):
		if self.use_selenium:
			page_content=self.browser.page_source
			return {'page_content':page_content,'page_content_length':len(page_content)}
	def click_next_page(self):
		module_name=_class_name+'click_next_page\t'
		print_statement=module_name
		try:
			click_next_button()
			'Next ›'
			print()
		except Exception as e:
			print('Next page not available !')
			return  False
		return True

	def fiind_elements():
		# div_tags=self.browser.find_elements_by_class_name('attendee-metadata__property')
			# div_tags=self.browser.find_element_by_class_name('attendee-metadata__property')
			# div_tags=self.browser.find_element_by_class_name('attendee-metadata__property')
			# 					find_element_by_id
			# 					find_element_by_name
			# 					find_element_by_xpath
			# 					find_element_by_link_text
			# 					find_element_by_partial_link_text
			# 					find_element_by_tag_name
			# 					find_element_by_class_name
			# 					find_element_by_css_selector
		pass
	def switch_browser_window():
		"""
		which switch to new tab and gets the page source and then roll backs to the start page !!!
		"""
		self.browser.execute_script("window.open('');")
		time.sleep(1)
		self.browser.switch_to.window(self.browser.window_handles[1])
		#print 'New page Opened'
		self.browser.get(combined_url)
		time.sleep(2)
		temp_page_source=self.browser.page_source
		try:
			print ('Page source collected !',person_name)
		except:print ('Page source collected !')
		self.write_into_file(file_name=full_file_name,content=temp_page_source,mode='w')
		self.browser.close()
		time.sleep(1)
		# Switch back to the first tab
		self.browser.switch_to.window(self.browser.window_handles[0])
	def soup_functions(self,page_source):
		"""
		This function handles the pagesource using Beautiful Soup
		"""
		soup = BeautifulSoup(page_source, "html.parser")
		
		# removing styles and script
		if not remove_tags : remove_tags=['script','style']
		for tag in remove_tags:
			for each_tag in soup.select(tag):
				each_tag.decompose()
		each_tag=soup.find("div",{"class":"attendee-detail__info"})
		each_tag=soup.find_all("div",{"class":"attendee-detail__info"})
		header=each_element.find('h5').text.strip()


	def get_epe_trace(self,epe_id, ut_branch_name ='',developer_mode=False,voice_mode = False):
		status = True
		new_epe_link = EPE_TRACE_PATTERN.replace('<epe_id>',epe_id)
		if developer_mode:
			developer_print('EPE Trace link : ',new_epe_link)

		self.browser.get(new_epe_link)
		time.sleep(3)

		temp_soup = BeautifulSoup(self.browser.page_source, "html.parser")
		write_into_file(file_name='temp_epe_trace.txt', contents=str(temp_soup), mode='w')

		# full_list = str((temp_soup.find("ul", {"class": "content-list mr-list issuable-list"})).get_text()).strip()
		unmerged_list_elem = []
		merged_list_elem = []
		try:
			unmerged_list_elem = temp_soup.find_all("li", {"class": "merge-request"})
		except Exception as e:
			developer_print('Error in getting unmerged_list ',e)
		# try:
		# 	merged_list_elem = temp_soup.find_all("li", {"class": "merge-request merged"})
		# except Exception as e:
		# 	developer_print('Error in getting merged_list ',e)


		both_lists = merged_list_elem+unmerged_list_elem
		both_lists = merged_list_elem+unmerged_list_elem
		if developer_mode:
			developer_print('len(both_lists) :',len(both_lists))

		if not both_lists:
			status =False
		total_records = []
		for mer_index,each_elem in enumerate(both_lists):
			temp_epe_title = ''
			temp_merge_req_id =''
			temp_author =''
			temp_target_branch =''
			temp_period =''
			temp_status =''


			try:
				temp_epe_title = str((each_elem.find("span", {"class": "merge-request-title-text"})).get_text()).strip()
			except Exception as e:
				temp_epe_title = ''

			try:
				temp_merge_req_id = str((each_elem.find("span", {"class": "issuable-reference"})).get_text()).strip()
			except Exception as e:
				temp_merge_req_id = ''

			try:
				temp_author = str((each_elem.find("span", {"class": "author"})).get_text()).strip()
			except Exception as e:
				temp_author = ''

			try:
				temp_target_branch = str((each_elem.find("a", {"class": "ref-name"})).get_text()).strip()
			except Exception as e:
				temp_target_branch = ''
			temp_period = str((each_elem.find("div", {"class": "float-right issuable-updated-at d-none d-sm-inline-block"})).get_text()).strip().replace('"','')
			try:
				temp_status = str((each_elem.find("li", {"class": "issuable-status d-none d-sm-inline-block"})).get_text()).strip()
			except Exception as e:
				temp_status = 'UNMERGED'

			each_dict = {
						'epe_id':epe_id
						,'epe_title':temp_epe_title
						,'merge_req_id':temp_merge_req_id
						,'author':temp_author
						,'target_branch':temp_target_branch
						,'status':temp_status
						,'period':temp_period
						}


			full_log =[mer_index+1,len(both_lists)]
			full_log.append(each_dict['epe_id'])
			full_log.append(each_dict['epe_title'])
			full_log.append(each_dict['merge_req_id'])
			full_log.append(each_dict['author'])
			full_log.append(each_dict['target_branch'])
			full_log.append(each_dict['status'])
			full_log.append(each_dict['period'])
			full_log_text = str('\t'.join(apply_to_list(full_log, make_string=True))).strip() + '\n'
			write_into_file(file_name=AUTO_EPE_TRACE_LOG, contents=add_timestamp(full_log_text), mode='a')
			if developer_mode:
				developer_print(mer_index,'temp_dict :',each_dict)
			total_records.append(each_dict)




		if developer_mode:
			developer_print('Total unmerged list element found  : ', len(unmerged_list_elem))
			developer_print('Total  merged list element found  : ', merged_list_elem)
		if voice_mode:
			speak_words('Traces taken for '+str(each_dict['epe_id']))

		res = {
			'status': status
			, 'total_records': total_records
		}


			# , 'source_branch': source_branch
			# , 'destination_branch': destination_branch
			# , 'merge_request_link': new_merge_req
			# , 'merge_request_id': merge_request_id
			# , 'commit_match': commit_match
			# , 'comments': comments
		# }
		# full_log = [res['source_branch'], res['destination_branch'], res['branch_presence'], res['commit_match'],
		# 			res['status'], res['merge_request_id'], res['comments']]

		return res

def create_merge_request_object(): # added on oct-30
	ramco_obj = RamcoGIT()
	return {'object' :ramco_obj}

if __name__ == "__main__":
	start = time.time()
	# ramco_obj = RamcoGIT()
	# epe_id = 'EPE-24397'
	# branch_name = 'ut-WMS_Merge_o48090_102020'
	if False:
		epe_id = 'EPE-24397'
		speak_words('Merge request is created for ' + str(epe_id))
	if True:
		arg = argparse.ArgumentParser('Program to Raise merge request !!', add_help=True)
		arg.add_argument('-i', '--input_excel', help='Input excel which contains ', required=True)
		arg.add_argument('-dev_mode', '--developer_mode',help='This will enable the developer mode which helps the developer', nargs='?', const=True,default=False, required=False)
		arg.add_argument('-b', '--branch', help='Destination branch', required=False, default='ut-189-mergeO48090')
		arg.add_argument('--branch_from_file', help='This will be enabled for Branches from file', required=False,default=False, const=True, nargs='?')
		arg.add_argument('--get_trace', help='This will be enabled for Branches from file', required=False,default=False, const=True, nargs='?')
		arg.add_argument('--voice_mode', help='This option will mute the voice help', required=False,default=False, const=True, nargs='?')

		args = arg.parse_args()
		print('/nUser inputs :', args)
		input('Check the deployment branch ID  and press Enter')
		developer_mode = args.developer_mode
		input_excel = args.input_excel
		branch = args.branch
		branch_from_file = args.branch_from_file
		get_trace = args.get_trace
		voice_mode = args.voice_mode
		input_data = get_input_excel(input_excel, developer_mode=developer_mode)['excel_data']
		# print (input_data)

		DIRECTORY = ''
		if input_excel:
			t_dic = handle_extension(input_excel)
			if get_trace:
				temp_file_name = str(t_dic['no_extension']) + '_AUTO_EPE_TRACE.txt'
			else:
				temp_file_name = str(t_dic['no_extension']) + '_AUTO_MERGE_REQUEST.txt'

			DIRECTORY = t_dic['directory']
			result_file_name = temp_file_name
		else:
			if get_trace:
				result_file_name = AUTO_EPE_TRACE_FILE
			else:
				result_file_name = AUTO_MERGE_REQUEST_FILE
		if not DIRECTORY: DIRECTORY = os.getcwd()

		result_file_name = os.path.join(DIRECTORY, result_file_name)
		if get_trace:
			headers = EPE_TRACE_HEADERS
		else:
			headers = MERGE_REQUEST_HEADERS
		write_into_file(file_name=result_file_name, contents=headers, mode='w')
		ramco_obj = RamcoGIT()

		for file_count, each_line in enumerate(input_data):
			try:
				each_line = each_line[0]
				# print('each_line :',each_line)
				# input()
				epe_id = each_line[0].strip()
				if branch_from_file:
					branch_name = each_line[3].strip()  # incase the branch is given in the file
				elif branch:
					branch_name = branch.strip()
				else:
					print('Branch name is missing !!\tQuitting code ')
					exit()
			except Exception as e:
				print('Please provide valid inputs !')
				continue
			# print('Processing file: {0}/{1}, Source-branch :{2} \t Destination-branch:{3}'.format(file_count + 1,len(input_data),epe_id, branch_name))
			# input('Proceed ??')
			if get_trace:
				print('EPE-Tracing: Processing file : {0}/{1}, EPE- ID :{2} '.format(file_count + 1,len(input_data),epe_id))

				res = ramco_obj.get_epe_trace(epe_id=epe_id, ut_branch_name=branch_name,developer_mode=developer_mode,voice_mode = voice_mode)
				for res_index,each_dict in enumerate(res['total_records']):
					full_log = [res_index +1, len(res['total_records'])]
					full_log.append(each_dict['epe_id'])
					full_log.append(each_dict['epe_title'])
					full_log.append(each_dict['merge_req_id'])
					full_log.append(each_dict['author'])
					full_log.append(each_dict['target_branch'])
					full_log.append(each_dict['status'])
					full_log.append(each_dict['period'])
					full_log_text = str('\t'.join(apply_to_list(full_log, make_string=True))).strip() + '\n'
					write_into_file(file_name=result_file_name, contents=full_log_text, mode='a')
			else:
				print('Merge request: Processing file: {0}/{1}, Source-branch :{2} \t Destination-branch:{3}'.format(file_count + 1,len(input_data),epe_id,branch_name))

				res = ramco_obj.raise_merge_request(epe_id = epe_id, ut_branch_name = branch_name,developer_mode=developer_mode,voice_mode=voice_mode)
				if res:
					full_log = [res['source_branch'],res['destination_branch'],res['branch_presence'],res['commit_match'],res['status'],res['merge_request_id'],res['comments']]
					full_log_text = '\t'.join(apply_to_list(full_log, make_string=True))+'\n'
					write_into_file(file_name=result_file_name, contents=full_log_text, mode='a')

		print('result_file_name :',result_file_name)
		end = time.time()

		print()
		print('Total Time taken in seconds : {:.1f}'.format(end - start))
		print('Total Time taken in Minutes : {:.2f}'.format((end - start) / 60))
