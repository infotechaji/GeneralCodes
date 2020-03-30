"""
Description : Script which get help text of all the procedures for single and multi input 
Version     : 
				v1.0
History     :
				v1.0  - 30/03/2020 - initial version

Input       : --sp_name sp_name 
			  -i input_filename which contains the list of sps

Output      : Stored procedure as new file which can be extracted from DB

"""
import pyodbc 
import argparse
from serverdetails import * 
from CustomisedFileOperation import * 
# conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=172.16.17.168,50196;DATABASE=AVNAPPDB_TEMPDB;UID=rvwuser;PWD=rvw;Trusted_Connection=no;')
# conn = pyodbc.connect('''DRIVER={ODBC Driver 13 for SQL Server};
# 						SERVER=172.16.10.68;
# 						DATABASE=scmdb;
# 						UID=Sa;
# 						PWD=war3sa*;
# 						Trusted_Connection=no;''')
global cursor
CONNECTION_STRING='DRIVER={ODBC Driver 13 for SQL Server};SERVER='+str(SERVER)
CONNECTION_STRING+=';DATABASE='+str(DB)
CONNECTION_STRING+=';UID='+str(UID)
CONNECTION_STRING+=';PWD='+str(PWD)
CONNECTION_STRING+=';Trusted_Connection=no;'
print ('CONNECTION_STRING :',CONNECTION_STRING)
def connect():
	try:
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
	print ('file_name :',file_name)
	return file_name

def get_sptext(sp_name):
	sp_name=sp_name.strip()
	full_text=''
	try:
		cursor.execute("sp_helptext '"+sp_name+"'")
		for row in cursor.fetchall():
			# print (row)
			full_text+=str(row[0]).replace('\r\n','\n')
		return {'help_text':full_text}
	except Exception as e :
		print ('Error while getting procedure text :',e)
		return {'help_text':full_text}


if __name__ == '__main__':
	arg = argparse.ArgumentParser('Program to Help stub addition !!',add_help=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	arg.add_argument('--sp_name',help='single sp file',required=False)
	arg.add_argument('-i','--input_file',help='list of procedures',required=False)
	# arg.add_argument('-i','--input_file',help='Trace file name',default ='scorpio,pisces',required=False)
	# arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	if args.sp_name:
		cursor=connect()# connects to the server
		file_name =get_file_name(args.sp_name)
		help_text=get_sptext(args.sp_name)['help_text']
		write_into_file(file_name=file_name,contents=help_text,mode='w')
	elif args.input_file:
		cursor=connect()# connects to the server
		file_lines=get_file_content(args.input_file)
		for index,each_line in enumerate(file_lines):
			each_line=each_line.strip('\t\r\n')
			print ('processing :',index)
			file_name =get_file_name(each_line)
			help_text=get_sptext(each_line)['help_text']
			write_into_file(file_name=file_name,contents=help_text,mode='w')
	else:
		print ('Please provide --sp_name procedure_name or -i input_filename ')


