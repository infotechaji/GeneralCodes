"""
Functionality : Script to help stub addition
"""
import re
import sys
import argparse

def list_difference(stub_param_list,actual_list):
	return (list(set(stub_param_list) - set(actual_list)))
def get_parameters(input_text,developer_mode=False):
	temp_text=input_text.lower().split('create '.lower())[1]
	actual_text=temp_text.split('begin')[0]
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
	arg = argparse.ArgumentParser('Program to Help stub addition !!',add_help=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	arg.add_argument('--stub_file',help='Trace file name',required=True)
	arg.add_argument('--sp',help='actual_file',required=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',default ='scorpio,pisces',required=False)
	# arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	result_set1=get_parameters(get_file_content(args.stub_file))
	result_set2=get_parameters(get_file_content(args.sp))
	print ('Stub variables :',len(result_set1['variables']))
	print ('sp variables :',len(result_set2['variables']))
	newly_added=list_difference(result_set1['variables'],result_set2['variables'])
	print ('Added variables :',newly_added)
	out_file_name='added_variables.txt'
	for i,each in enumerate(newly_added):
		index= result_set1['variables'].index(each)
		each_line=args.stub_file+'\t'+each+'\t'+result_set1['content'][index]+'\t'+str(len(newly_added))+'\t'+str(i+1)+'\n'
		fp=open(out_file_name,'a')
		fp.write(each_line)
		fp.close()