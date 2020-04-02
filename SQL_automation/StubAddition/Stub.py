"""
Functionality : Script to help stub addition
version : v2.1

History :
		  v1.0  - 01/03/2020 - initial version
		  v2.0  - 02/04/2020 - trim and null check functions are also added 
		  v2.1  - 02/04/2020 - splitting logic is enhanced

"""
import re
import sys
import argparse

def list_difference(stub_param_list,actual_list):
	# print ('Stublist len:',len(stub_param_list))
	# print ('actual_list len:',len(actual_list))
	return (list(set(stub_param_list) - set(actual_list)))
def get_parameters(input_text,developer_mode=False):
	temp_text=input_text.lower().split('create '.lower())[1]
	begin_split=''
	for each_line in input_text.split('\n'):
		if 'begins' not in each_line.lower() and 'begin' in each_line.lower():
			begin_split=each_line
			break
	if not begin_split:begin_split='begin '
	actual_text=temp_text.split(begin_split)[0]
	# print (actual_text.split('\n'))
	if developer_mode==True : print ('actual_text :',actual_text)
	actual_list=actual_text.split('\n')
	# print ('actual_list :',actual_list)
	variables=[]
	index_to_be_deleted=[]
	if developer_mode==True : print ('Actual list :',len(actual_list))
	for i,val in enumerate(actual_list):
		if developer_mode==True : print ('i and val :',i,val)
		temp=''
		if val.strip(' \t\r\n').startswith('--'):
			if developer_mode==True : print ('deleted:',actual_list[i])
			actual_list[i]=''
		else:
			try:
				if developer_mode==True : print ('val before regex :',val)
				temp=re.findall("@\w+", val)[0]
				# print (re.search("@\w+", val).group())
				if developer_mode==True : print ('temp :',temp)
				if developer_mode==True : print (temp)
				if temp not in variables and len(temp)>1:
					if developer_mode==True : print ('added to variables :',temp)
					variables.append(temp)
				else:
					actual_list[i]=''
			except Exception as e :
				if developer_mode==True : print ('Error :',e) 
				actual_list[i]=''
				pass
	for i,each_val in enumerate(actual_list):
		if len(each_val)<2 or not each_val:
			del actual_list[i]
	if developer_mode==True : print ('Total variables :',len(variables))
	if developer_mode==True : print ('Total variables :',variables)
	return {'content':actual_list,
			'variables':variables
			}
def get_sp_help_text():
	conn = pyodbc.connect('''DRIVER={ODBC Driver 13 for SQL Server};
							 SERVER=172.16.17.168,50196;
							 DATABASE=AVNAPPDB_TEMPDB;
							 UID=rvwuser;
							 PWD=rvw;
							 Trusted_Connection=no;''')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM test_emp')
	pass
def get_file_content(filename):
	try:
		return open(filename).read()
	except Exception as e:
		print ('Error while getting content from file :',e)
		return ''
def write_into_file(file_name,file_lines,mode='w'):
		""" Function which write the input content into the file 
		"""
		fp=open(file_name,mode)
		for each_line in file_lines:
			fp.write(each_line)
		fp.close()

if __name__ == '__main__':
	arg = argparse.ArgumentParser('Program to Help stub addition!!',add_help=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	arg.add_argument('--stub_file',help='Trace file name',required=True)
	arg.add_argument('--sp',help='actual_file',required=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',default ='scorpio,pisces',required=False)
	# arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	stub_file_contents=get_file_content(args.stub_file)
	result_set1=get_parameters(stub_file_contents)
	result_set2=get_parameters(get_file_content(args.sp))
	print ('Stub variables :',len(result_set1['variables']))
	print ('sp variables :',len(result_set2['variables']))
	newly_added=list_difference(result_set1['variables'],result_set2['variables'])
	print ('Total added variables :',len(newly_added))
	print ('Added variables :',newly_added)
	out_file_name='added_variables.txt'
	for i,each in enumerate(newly_added):
		index= result_set1['variables'].index(each)
		each_line=args.stub_file+'\t'+each+'\t'+(result_set1['content'][index].replace('\t','    ').replace(' --input/output','').strip())+'\t'+str(len(newly_added))+'\t'+str(i+1)+'\n'
		fp=open(out_file_name,'a')
		fp.write(each_line)
		fp.close()
	# print ('Variables are written ')
	for index,each_line in enumerate(stub_file_contents.split('\n')):
		for var_index,each_var in enumerate(newly_added):
			# print ('var :',each_var)
			# print (index,each_line)
			if each_var.strip().lower() in each_line.lower():
				# print ('if matched - last')
				# input('test')
				final_text=args.stub_file+'\t'+each_var.strip()+'\t'+str(each_line.replace('\t',' ').strip())+'\t'+str(var_index+1)+'\t'+str(index+1)+'\n'
				write_into_file('SpaceAndNull_checks.sql',final_text,'a')
	print ('Trim and null checkings are added in file :SpaceAndNull_checks.sql')
