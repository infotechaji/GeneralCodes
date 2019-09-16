import os,sys

def get_all_files(input_directory):
	for root, dirs, files in os.walk(input_directory):	
		for each_file in files:
			# print 'dirs :',dirs
			# print 'root :',root
			# print 'each_file',each_file
			file_full_path=os.path.join(root,each_file)
			print 'file_full_path :',file_full_path

if __name__=="__main__":
	input_directory=sys.argv[1]
	get_all_files(input_directory)