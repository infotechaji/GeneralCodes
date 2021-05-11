"""
Description : Contains all the common file operations
Version :	v2.4
History :
			v1.0 - 25/09/2020 - initial version
			v2.0 - 25/09/2020 - Function get_input_excel() is added
			v2.1 - 01/10/2020 - Function write_in_excel() is just added and not tested
			v2.2 - 03/10/2020 - ignore errors options is added in the funcion write_into_file()
			v2.3 - 14/10/2020 - function write_results_and_logs() is added
			v2.4 - 15/10/2020 - function handle_extension() )is added to handle the extensions easily

Cases to handle :
			1, Reading all the sheet in excel 
"""
import os.path
from os import path
import os,sys
from datetime import datetime, timezone
from TimeStamp import * 
import openpyxl

def get_file_content(filename,return_lines=True,trim_spaces=False):

	try:
		if return_lines == True:
			if trim_spaces:
				file_lines = []
				for each_line in open(filename).readlines():
					# file_lines.append(each_line.strip(''))
					# print('len(each_line) :',len(each_line))
					# print('each_line.rstrip :',len(each_line.rstrip('\t\r\n ')))
					# input()
					each_line = each_line.rstrip('\t\r\n ')+'\n'
					file_lines.append(each_line)
				return file_lines

			else:
				return open(filename).readlines()
		else:
			return open(filename).read()
	except Exception as e:
		print ('Error while getting content from file :',e)
		return ''
def write_into_file(file_name,contents,mode='w',errors='ignore'):
		""" Function which write the input content into the file 
		"""
		fp=open(file_name,mode,errors = 'replace')
		fp.write(str(contents))
		fp.close()

def get_file_presence(file):
	return os.path.exists(file)

def check_and_make_path(directory):
	try:
		if not os.path.exists(directory):
			os.mkdir(directory)
		status = True
	except:
		status = False
	return {
			'directory':directory,
			'status':status
			}

def delete_file(file_full_path):
	try:
		os.remove(full_file_path)
	except Exception as e:
		print('Error while deleting the file :',file_full_path)
		return False
	return True


def get_input_excel(excel_file_name, developer_mode=False):
	"""

     :param excel_file_name: name of the uploaded excel file
     :return: names along with the defect IDS
     """
	import xlrd
	loc = excel_file_name
	# To open Workbook
	wb = xlrd.open_workbook(loc)
	sheet = wb.sheet_by_index(0)
	# For row 0 and column 0
	sheet.cell_value(0, 0)
	rows = sheet.nrows
	cols = sheet.ncols
	if developer_mode:
		print('get_input_excel:\tSheet Name :{0}\tRows:{1}\tColumns:{2}'.format(excel_file_name, rows, cols))
	rows_data = []
	# if cols == 2:
	for i in range(0, rows):
		# print(i, sheet.row_values(i))
		if developer_mode:
			sys.stdout.write('Reading row ..... ' + str(i) + ',' + str(sheet.row_values(i)))
			sys.stdout.write('\r')
		col_data = []
		for col in range(0,cols):
			# col_value = sheet.row_values(i)[col].strip()
			col_value = str(sheet.row_values(i)[col]).strip()
			if developer_mode:
				print('get_input_excel:\tColumn value :',col_value)
			col_data.append(col_value)
		if col_data:
			rows_data.append([col_data])

	# print(rows_data)

	return {
		'rows': rows,
		'cols': cols,
		'excel_data': rows_data
	}

def write_int_excel(file_name , content_list ,mode ):
	# Basic code is added but needs updates
	import xlwt
	from xlwt import Workbook

	# Workbook is created
	wb = Workbook()

	# add_sheet is used to create sheet.
	sheet1 = wb.add_sheet('Sheet 1')

	sheet1.write(1, 0, 'ISBT DEHRADUN')
	sheet1.write(2, 0, 'SHASTRADHARA')
	sheet1.write(3, 0, 'CLEMEN TOWN')
	sheet1.write(4, 0, 'RAJPUR ROAD')
	sheet1.write(5, 0, 'CLOCK TOWER')
	sheet1.write(0, 1, 'ISBT DEHRADUN')
	sheet1.write(0, 2, 'SHASTRADHARA')
	sheet1.write(0, 3, 'CLEMEN TOWN')
	sheet1.write(0, 4, 'RAJPUR ROAD')
	sheet1.write(0, 5, 'CLOCK TOWER')

	wb.save('xlwt example.xls')

def file_mtime(path):
    t = datetime.fromtimestamp(os.stat(path).st_mtime,
                               timezone.utc)
    return t.astimezone().isoformat()

def write_results_and_logs(file_name,log_name, content, header_data=False,file_mode = 'a', log_mode = 'a'):

	# VALIDATION_LOG = 'defect_validation_log.txt'
	# VALIDATION_FILE_MODE = VALIDATION_LOG_MODE = 'a'
	if header_data:
		file_mode = 'w'
	write_into_file(file_name = file_name, contents = content, mode = file_mode)
	write_into_file(file_name = log_name , contents = add_timestamp(content), mode = log_mode)

def handle_extension(input_sp, extension_to_add='.sql',developer_mode = False):
	status = False
	DIRECTORY, extracted_file_name = os.path.split(input_sp)
	sp_name = None
	file_name = None
	try:
		sp_name = str(extracted_file_name).split('.')[0]
		file_name = str(sp_name) + str(extension_to_add)
		status = True
	except Exception as e:
		developer_print('Error in handling name :',e)
		status = False
	return {
            'no_extension': sp_name
            , 'new_extension': file_name
            , 'directory': DIRECTORY
            , 'file_name': extracted_file_name
            }

def write_excel(work_book_name, rows=[]):
	book = openpyxl.load_workbook(work_book_name)
	sheet = book.active
	for row in rows:
		sheet.append(row)
		book.save(work_book_name)
	return True


if __name__ == "__main__":
	excel_data = get_input_excel(sys.argv[1],developer_mode=False)['excel_data']
	# print(excel_data)
	for i,d in enumerate(excel_data):
		print(i,d)