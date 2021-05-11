"""
Version : v2.6
History :

		v1.0 - 21/09/2020 - Initial version
		v2.0 - 21/09/2020 - To catch these patterns "PROCPSS-1203_01" the regex patterns are upgraded
		v2.1 - 22/09/2020 - ID-1001  - defect-id pattern is added to detect without space
		v2.2 - 22/09/2020 - ID-1002  - function get_all_fix_id() is upgraded to detect more than one defect fix ID
		v2.3 - 26/09/2020 - ID-1003  - "get all the defect IDS from the headers" is added in the function get_all_fix_id()
		v2.4 - 01/10/2020 - ID-1004  - In function get_all_fix_id() , "extract_from_header" option is added to handle
		v2.5 - 15/10/2020 - 		   Core logic for the function get_all_fix_id()  is upgraded, extract_from_header option is upgraded
		v2.6 - 12/11/2020 - 		   Option  "get_rtrack_id" is added to detect the Rtrack IDs

"""
import argparse
import os,sys,re
from CustomisedFileOperation import * 
from Help_print import * 


def get_all_fix_id(file_content,extract_from_header = False,developer_mode=False,get_rtrack_id = False):
	"""
	Date : 18-sep-2020
	:param file_content: Gets total file content / line of code
	:param developer_mode:
	process : extract the defect ID from the given input text
	:return: extraced IDS
	"""
	if developer_mode: 
		developer_print(' Type of input file content :',type(file_content))
	file_string = ''
	if type(file_content)==list:
		
		file_string='\n'.join(file_content)
	elif type(file_content)==str:
		file_string=file_content
	# print (file_string)
	if developer_mode: 
		developer_print('Type of file_sting:',type(file_string),'len(file_string):',len(file_string))
	# first_section=file_string.lower().split('create ')
	# ID-1004 - option added to handle header fixes starts here
	if extract_from_header:
		if developer_mode : developer_print(' extract_from_header : ',extract_from_header)
		splitss = re.split('create\s+procedure',str(file_string).lower())
		if developer_mode : developer_print(' len(splitss) : ',len(splitss))
		first_section = splitss[0]
	else:
		first_section = file_string
	if developer_mode :
		developer_print('first section : ',first_section)
		# input()
	# ID-1004 - option added to handle header fixes ends here
		
	if developer_mode:
		if extract_from_header:
			developer_print('len(splitss):',len(splitss))
			developer_print('len(first_section):',len(first_section),'First section  last 100 words:',first_section[-100:])
	

	#  To catch these patterns "PROCPSS-1203_01" the below regex patterns are commented


	#  To catch these patterns "PROCPSS-1203_01" the regex patterns are upgraded

	# total_ids=re.search(pattern,first_section)
	if get_rtrack_id:
		suspectful_patterns2=[]
	else:
		suspectful_patterns2 =['(\s+)(\w+-\d+_\d+)'		#  To catch these patterns "PROCPSS-1203_01"
								,'()(\w+-\d+_\d+)'		#  To catch these patterns "PROCPSS-1203_01"
							]

	suspectful_patterns=[
						'(\d{4}\s+)(\w+-\d+)'      # Ids in the header section
						,'(\s+)(\w+-\d+)'           # simple defect ID
						,'()(\w+-\d+)'                # ID-1001 simple defect ID without space
	]

	total_ids=[]
	fixes=[] 
	for each_pattern in suspectful_patterns2+suspectful_patterns:

		total_ids=re.findall(each_pattern,str(first_section)) # finding defect-ids in header section
		if developer_mode: 
			developer_print ('Pattern :',each_pattern,total_ids)
		# print(total_ids)
		if total_ids:
			if developer_mode: 
				developer_print(' Breaking here ...')
			for i in total_ids:
				new_id=i[1]
				if new_id not in fixes:
					fixes.append(new_id)
			# break  # commented with respect to "ID-1002" to add more fixes

	if developer_mode: 
		developer_print('total_ids header section :',total_ids)

	# line_pattern='(\s+)(\w+-\d+)' # pattern to match the defect ID and al
	# pattern_title='(\d{4}\s+)(\w+-\d+)' # pattern which matches along with the date pattern # commented because it is not getting defect ids in the commented lines

	# if not total_ids:
	# 	total_ids=re.findall(line_pattern,str(first_section)) # finding defect-ids except in header section
	# 	if developer_mode: print ('get_all_fix_id:\t total_ids other section :', total_ids)

	# fixes=[]
	# for i in total_ids:
	# 	if developer_mode:
	# 		developer_print(' Total list i[0]',i[0])
	# 		developer_print(' Total list i[1]',i[1])
	# 	new_id=i[1]

	# 	if new_id not in fixes:
	# 		fixes.append(new_id)
	if developer_mode: 
		developer_print(' Total detected fixes :',len(fixes))

	# total_ids=re.match(pattern,str(first_section))
	# total_ids=re.findall(pattern,first_section)
	# print(total_ids)
	# print('Matched sections :',total_ids.group(2))
	if developer_mode:
		developer_print(' Finally extracted IDS :', fixes)
		
	return {'valid_fixes':fixes}

def get_missing_id(ids_a,ids_b):
	missings_a=ids_a-ids_b
	missings_b=ids_b-ids_a
	return {'missing_ids_a':missings_a,
			'missing_ids_b': missings_b
			}
def get_updated_file(file_a,file_b,each_id_miss):

	"""
	Function which finds the respective fixes added in the File A and adds them to the file B
	:param file_a:
	:param file_b:
	:param each_id_miss:
	:return:
	"""
	status = 'not_changed'
	fix_lines=get_all_fix_lines(file_a,each_id_miss) # detects all the fixes which are done against that ID
	updated_file_b=add_fix_lines(file_b,each_id_miss,fix_lines)     # finds the correct place to add the fixes.
	if file_b!=updated_file_b:
		status='changed'
	return  {
			'updated_file_b':updated_file_b,
			'status':status
			 }





def compare_and_update_missing_values(file_lines1,file_lines2,ids=[],developer_mode=False):
	"""
	This function updates the missing fixes from File A to File B and returns the updated File B content as output
	:param file_lines1:
	:param file_lines2:
	:param ids:
	:param developer_mode:
	:return:
	"""
	file_a=file_lines1
	file_b=file_lines2
	ids_a=get_all_fix_id(file_a,developer_mode=developer_mode)['valid_fixes']
	ids_b=get_all_fix_id(file_b)['valid_fixes']
	print ('Valid fixes count \n File A:',len(ids_a),'\n File B :',len(ids_b))
	status='NoUpdate'
	if ids_a==ids_b:
		status='Matching'
		print('Fix Ids are exactly matching :')
	else:
		print('Fixes count is not matching !')
	input('Test :')
	missing_ids_a=get_missing_id(ids_a,ids_b)['missing_ids_a']
	updated_file_b=[]
	for each_id_miss in missing_ids_a:
		if ids:
			if each_id_miss not in ids: continue# checking for the user requirement
		updated_file_A=get_updated_file(file_a,file_b,each_id_miss)

	return {
			'updated_file_b':updated_file_b,
			'missing_ids_a':missing_ids_a,
			'missing_ids_b':missing_ids_b

			}











if __name__ == '__main__':
	file_contents=get_file_content(sys.argv[1],return_lines=True)
	# file_contents2=get_file_content(sys.argv[1],return_lines=True)
	# # print(str(file_contents)+"\nfile_contents :")
	# print(len(file_contents))
	# file_contents ='--@stk_con_tqty			=	sum(wms_stk_con_mas_to_qty)--Code Added for LRT-1204 --VLVI-418'
	# file_contents ='@stk_con_tqty			=	sum(isnull(wms_stk_con_mas_to_qty,wms_stk_con_to_qty))--Code Added for VLVI-418'
	res = get_all_fix_id(file_contents,extract_from_header = True, developer_mode = False)
	res2 = get_all_fix_id(file_contents,extract_from_header = False, developer_mode = False)
	
	# print(res['valid_fixes'])
	print('Total fixess :',len(res['valid_fixes']))
	print('Total fixess :',len(res2['valid_fixes']))


	# arg = argparse.ArgumentParser('Program to add the missing Fixes  !!',add_help=True)
	# # arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	# arg.add_argument('--sp1',help='single sp file1',required=False)
	# arg.add_argument('--sp2',help='single sp file2',required=False)
	# arg.add_argument('--ids',help='IDs to merge the script',required=False,nargs='?')
	# # arg.add_argument('-i1','--input_dir1',help='list of procedures',required=False)
	# # arg.add_argument('-i2','--input_dir2',help='list of procedures',required=False)
	# # arg.add_argument('-i','--input_file',help='Trace file name',default ='scorpio,pisces',required=False)
	# arg.add_argument('--dev_mode',help='To enable developer_mode ',type=bool,default =False,const=True,required=False,nargs='?')
	# args = arg.parse_args()
	# print ('User inputs :',args)
	# if args.sp1 and args.sp2:
	# 	file_lines1=get_file_content(args.sp1)
	# 	file_lines2=get_file_content(args.sp2)
	# 	res=compare_and_update_missing_values(file_lines1,file_lines2,args.ids,developer_mode=args.dev_mode)
	#
	#
	# else:
	# 	print('Please specify two input files ')
	# 	cursor=connect()# connects to the server
	# 	file_name =get_file_name(args.sp_name)
	# 	help_text=get_sptext(args.sp_name)['help_text']
	# 	write_into_file(file_name=file_name,contents=help_text,mode='w')
	# elif args.input_file:
	# 	# file_directory='G:\\Ajith\\Issues\\Logistics\\2020\\LRT-5244\\Bin_Plan_updated\\Bin_Plan_updated\\188_server_latest_version'
	# 	# file_directory='G:\\Ajith\\Issues\\Logistics\\2020\\LRT-5244\\Bin_updated\\MailVersion'
	# 	# file_directory='G:\\Ajith\\Issues\\Logistics\\2020\\LRT-5244\\PICK_and_BIN_updated\\188_version'
	# 	# file_directory='G:\\Ajith\\Issues\\Logistics\\2020\\Pss-Enhancement-Merge\\Extracted_objects_188'
	# 	file_directory='G:\\Ajith\\Issues\\Logistics\\2020\\Pss-Enhancement-Merge\\Objects-Enhancement'
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
	# else:
	# 	print ('Please provide --sp_name procedure_name or -i input_filename ')