"""
Description : Script to compare files and add the missing lines
Version     : v2.0
History     : 
              v1.0  - 31/03/2020 - initial version 
              v2.0  - 31/03/2020 - input from file is updated and output will be written in the sp name 

Input       :  both files to compare 
OutputComp      :  Updated input file A 

"""
import argparse
from CustomisedFileOperation import * 

class Compare():
	"""
	contains functions to do comparison operations between two same files 
	"""
	def __init__(self,developer_mode=False):
		self.developer_mode=developer_mode
		# self.stub_filename=stub_filename
		pass
	def compare_files(self,file1,file2,procedure_name='default_sp'):
		updated_list=[]
		index_a=0
		index_b=0
		# final_text_header='Procedure_Name\tUnmatchedIndex\tNextMatchedIndex\tTotal_Lines\tAdded_Lines\n'
		# write_into_file('changes_log.txt',final_text_header, 'w')     # actual sp change 
		try:
			for source_index, source_each_line in enumerate(file1):
				# temp_index=0
				# index_a=
				# index_b=
				if self.developer_mode ==True: print ('index_a:',index_a,'source_index',index_b)
				
				if file1[index_a].strip().lower()==file2[index_b].strip().lower():
					updated_list.append(file1[index_a])
					index_a+=1
					index_b+=1
					if self.developer_mode ==True: print ('updated_list :',updated_list)
					# updated_file+=source_each_line
				else:
					if self.developer_mode ==True: print ('else case called ')
					final_text=str(index_a)+'\t'
					res=self.get_changes_only(index_a,file1,file2)
					for each_line in res['modified_list']:
						updated_list.append(each_line)
					if self.developer_mode ==True: print ('index_to_check :',res['index_to_check'])
					index_a=res['index_to_check']
					final_text+=str(index_a)+'\t'+str(len(res['modified_list']))+'\t'+str(res['modified_list'])+'\n'
					write_into_file('changes_log.txt',str(procedure_name)+'\t'+final_text, 'a')     # actual sp change 
		except IndexError as e:
			for each_i in range(index_a,len(file1)):
				updated_list.append(file1[each_i])				
		return {
				'updated_list' :updated_list
				}
	def get_changes_only(self,index,file1,file2):
		if self.developer_mode ==True: print ('f:get_changes_only\t:')
		if self.developer_mode ==True: print ('index:',index)
		if self.developer_mode ==True: print ('source file line:',file1[index])
		if self.developer_mode ==True: print ('destination file line :',file2[index])
		source_index=index
		if file1[index].strip().lower() !=file2[index].strip().lower():
			dest_text=file2[index]
			modification_list=[]
			for i in range(len(file1)):
				temp_index=source_index+i
				if file1[temp_index].strip().lower()==dest_text.strip().lower(): # the next line will match 
					break
				else:
					modification_list.append(file1[temp_index])
		next_index=temp_index
		if self.developer_mode ==True: 
			print ('modification_list :',modification_list)
			print ('input index :',index)
			print ('next index to check :',next_index)
			print ('source file next line to check :',file1[next_index])
			print ('destination file next line to check :',file2[next_index])
		return {
				'modified_list':modification_list,
				'index_to_check':next_index,
				}

if __name__ == '__main__':
	arg = argparse.ArgumentParser('Program to Help stub addition !!',add_help=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	arg.add_argument('-s','--source_file',help='Source Procedure file name',required=False)
	arg.add_argument('-d','--destination_file',help='Destination Procedure file name',required=False)
	arg.add_argument('-i','--input_file',help='input file contains both the files tab separated',required=False)
	# arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	cl_obj=Compare()
	if args.source_file:
		print ('args:',args.source_file)
		print ('args:',args.destination_file)
		source_file_lines=get_file_content(args.source_file)
		dest_file_lines=get_file_content(args.destination_file)
		updated_A_file=cl_obj.compare_files(source_file_lines,dest_file_lines,procedure_name=args.source_file)['updated_list']
		total_text=''.join(updated_A_file)
		print (updated_A_file)
		up_file_name=args.source_file.replace('.','_updated.') # actual sp change 
		write_into_file(up_file_name,total_text,'w')

	elif args.input_file:
		file_lines=get_file_content(args.input_file)
		print ('Total lines in Procedure :',len(file_lines))
		for lin in file_lines:
			source_file,destination_file=lin.strip('\r\n').split('\t')
			print ('source_file :',source_file)
			print ('destination_file :',destination_file)
			source_file_lines=get_file_content(source_file)
			dest_file_lines=get_file_content(destination_file)
			updated_A_file=cl_obj.compare_files(source_file_lines,dest_file_lines,procedure_name=source_file)['updated_list']
			total_text=','.join(updated_A_file)
			up_file_name=source_file.replace('.','_updated.') # actual sp change 
			write_into_file(up_file_name,total_text, 'w')     # actual sp change 
	# print ('No of lines source :',len(source_file_lines))
	# print ('No of lines destination :',len(dest_file_lines))
	# for source_index, source_each_line in enumerate(source_file_lines):
	# 	for dest_index, dest_each_line in enumerate(dest_file_lines):
	# 		if source_each_line.strip().lower()==dest_each_line.strip().lower():
	# 			# if source_each_line.strip().lower()=dest_file_lines[source_index+1]
	# 			pass
	# 		else:
				
