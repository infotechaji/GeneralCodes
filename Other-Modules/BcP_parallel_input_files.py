import sys,os

if "__name__"=="__main__":
	file_name =sys.argv[1]
	file_lines = open(file_lines).readlines()
	for each_line in file_lines:
		print 'bcp line :',each_line
		try:
			os.system(each_line)
		except Exception as e :
			print 'Exception while executing bcp command ',e
			pass
			exit()
