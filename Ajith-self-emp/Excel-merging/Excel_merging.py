# import xlrd
import  os,sys
import pandas as pd

def get_input_excel(excel_file_name, developer_mode=False):
	"""

     :param excel_file_name: name of the uploaded excel file
     :return: names along with the defect IDS
     """

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
def read_excel_file(excel_name,developer_mode = False):
	status = False

	return_list = []
	try:
		xls = pd.ExcelFile(excel_name)
		total_sheets = xls.sheet_names
		if developer_mode:
			print('Total_sheets :',total_sheets)

		for sheet_index,each_sheet in enumerate(total_sheets):
			if developer_mode:
				print('Processing sheet :', each_sheet)
			df = pd.read_excel(excel_name, sheet_name = each_sheet)
			products_list = [df.columns.values.tolist()] + df.values.tolist()
			if developer_mode:
				print(type(products_list))
			return_list.append({
						'sheet_index':sheet_index
						,'sheet_name':each_sheet
						,'sheet_values':products_list
							})
		status = True
	except Exception as e:
		print('Error in reading excel ',e)
		status = 'Error'
	return {
			'status':status
			,'excel_data':return_list
	}

def get_files_from_directory(input_directory , file_extension = '.sql',developer_mode = False):
	if not os.path.exists(input_directory):
		print('Input directory doesn''t exits')
	if developer_mode:
		print('input directory exists !:',input_directory)
	selected_files = []
	all_files = []
	for root, dirs, files in os.walk(input_directory):
		for each_file in files:
			if each_file.endswith(file_extension):
				selected_files.append(each_file)

			all_files.append(each_file)
		break
	return {
		'all_files':all_files
		,'selected_files':selected_files
		,'input_directory':input_directory
			}


if __name__ == "__main__":
	excel1 = 'G:\\Ajith\\Others\\Ajith-self-emp\\Excel-merging\\Excel_file1.xlsx'
	excel2 = 'G:\\Ajith\\Others\\Ajith-self-emp\\Excel-merging\\Excel_file2.xlsx'
	# input_dir ='G:\\Ajith\\Others\\Ajith-self-emp\\Excel-merging'
	input_dir =sys.argv[1]
	print('Input directory :', input_dir)
	# all_excel_files = get_files_from_directory(input_directory = input_dir, file_extension = '.xlsx')['all_files']
	all_excel_files = get_files_from_directory(input_directory = input_dir, file_extension = '.xlsx')['selected_files']
	# files_list  = [excel1,excel2]
	files_list  = all_excel_files

	input('total files found in the directory :'+str(len(files_list)))
	for files_index,each_excel in enumerate(files_list):
		file_full_path = os.path.join(input_dir,each_excel)
		# print('Each file:', each_excel)
		if not os.path.exists(file_full_path):
			print('Excel file does not exists :',file_full_path)
			continue
		res = read_excel_file(file_full_path,developer_mode = False)
		total_lists  = res['excel_data']
		for res_index,each_dict in enumerate(total_lists):
			print('Processing file : {0}/{1},Sheets :{5}/{6} , File:{2} Sheet : {3} ( Lines:{4} ) '.format(files_index+1,len(files_list),str(each_excel).split(os.sep)[-1],each_dict['sheet_name'],len(each_dict['sheet_values']),res_index+1,len(total_lists)))
			excel_data   = each_dict['sheet_values']
			# print('Excel data :',len(excel_data))
			for line_index,temp_line in enumerate(excel_data):
				# print('Excel data :',excel_data[1])
				temp = ['' if str(i).lower().strip() == 'nan' else i for i in temp_line]
				temp = ['' if 'unnamed:' in str(i).lower().strip() else i for i in temp]
				temp = [str(i) for i in temp]
				# print('Excel data :',temp)

				contents = str('\t'.join([str(each_excel),str(each_dict['sheet_index']+1),str(each_dict['sheet_name']),str(line_index+1)])) + '\t' + '\t'.join(temp) + '\n'
				fp = open('Combined_results.txt', mode='a')
				fp.write(str(contents))
				fp.close()

	# 	print('df.keys() :',df.keys())
	# 	print('df.values() :',df.values())
	# 	# for index,each_line in enumerate(df):
	# 	# 	print('each_line :',each_line)
	# 	# 	print('df[index] :',df[each_line][index])
	# 	# print('Dataframe :',df)
	# 	break

	# total_excel_list = [excel1,excel2]
	# for each_file_index,each_excel in enumerate(total_excel_list):
	#
	# 	excel_data = get_input_excel(excel_file_name=each_excel)['excel_data']
	# 	# print('Total rows :',len(excel_data))
	# 	print('Processing files :{0}/{1}, File name : {2}'.format(each_file_index,len(total_excel_list),each_excel))
	# 	for index,each_line in enumerate(excel_data):
	# 		# print(index,':',len(each_line[0]))
	# 		contents = str(each_excel)+'\t'+'\t'.join(each_line[0])+'\n'
	# 		fp = open('Combined_results.txt', mode = 'a')
	# 		fp.write(str(contents))
	# 		fp.close()