"""
Functionality : Script which replaces the variables with actual values in a stored procedure 
Version       : v1.0
History       :
				v1.0 - 05/03/2020 - initial version 

Input         : 
				1.Trace file 
Output 		  : 
				1.Stored Procedures with replaced values.

"""
import sys
import argparse


class SP():
	def __init__(self,trace_file,developer_mode=False):
		self.developer_mode=developer_mode

	def replace_by_value(self,file_text,to_replace_dict):
		temp_text=file_text
		for each_val in to_replace_dict:
			print (each_val, to_replace_dict['each_val'])
			temp_text=temp_text.replace(each_val,to_replace_dict['each_val'])
		return {'input_text':'','replaced_text':''}
	

def read_lines(input_filename):
	file_lines=open(input_filename).readlines()
	return file_lines
def write_into_file(file_name,file_lines,mode='w'):
	""" Function which write the input content into the file 
	"""
	fp=open(file_name,mode)
	for each_line in file_lines:
		fp.write(each_line)
	fp.close()

		
if __name__=="__main__":
	arg = argparse.ArgumentParser('Program to collect SP change details !!',add_help=True)
	arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',default ='scorpio,pisces',required=False)
	arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	input_filename=args.input_file
	print ('input_filename:',input_filename)
	print (read_lines(input_filename))
	# input_filename =sys.argv[1]
	# sp_obj=SP(trace_file=input_filename,developer_mode)
