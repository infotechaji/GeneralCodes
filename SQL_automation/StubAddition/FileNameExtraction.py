import os,sys
import os.path
from os import path
from CustomisedFileOperation import * 

if __name__=="__main__":
	input_directory=sys.argv[1]
	for root, dirs, files in os.walk(input_directory):
		count=0
		for each_file in files:
			count+=1
			temp_file=str(each_file)+'\n'
			print (count,each_file)
			write_into_file(file_name='file_names.txt',contents=temp_file,mode='a')
		break		
