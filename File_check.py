import os.path,sys
if __name__=="__main__":
	input_file_name=sys.argv[1]
	if os.path.isfile(input_file_name):
		print 'File Present'
	else: print 'File not present !!'
