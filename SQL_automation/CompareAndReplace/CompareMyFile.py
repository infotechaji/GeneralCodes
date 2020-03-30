"""
Description : Script to compare files and add the missing lines

Pending  :
List needs to be compared and added 

"""





def get_file_content(filename,return_lines=True):
	try:
		if return_lines==True:
			return open(filename).readlines()
		else:
			return open(filename).read()
	except Exception as e:
		print ('Error while getting content from file :',e)
		return ''
def write_into_file(file_name,contents,mode='w'):
		""" Function which write the input content into the file 
		"""
		fp=open(file_name,mode)
		fp.write(contents)
		fp.close()
if __name__ == '__main__':
	arg = argparse.ArgumentParser('Program to Help stub addition !!',add_help=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	arg.add_argument('--source_file',help='Source Procedure file name',required=True)
	arg.add_argument('--destination_file',help='Destination Procedure file name',required=True)
	# arg.add_argument('-i','--input_file',help='Trace file name',default ='scorpio,pisces',required=False)
	# arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	print ('args:'args.source_file)
	print ('args:'args.destination_file)
	source_file_lines=get_file_content(args.source_file)
	dest_file_lines=get_file_content(args.destination_file)
	print ('No of lines source :',len(source_file_lines))
	print ('No of lines destination :',len(dest_file_lines))
	for source_index, source_each_line in enumerate(source_file_lines):
		for dest_index, dest_each_line in enumerate(dest_file_lines):
			if source_each_line.strip().lower()==dest_each_line.strip().lower():
				# if source_each_line.strip().lower()=dest_file_lines[source_index+1]
				pass
			else:
				
