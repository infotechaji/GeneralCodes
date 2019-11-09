"""
Version  : v1.1 
History  : 
			v1.0 - 05/24/2019 - initial version 
			v1.1 - 05/24/2019 - script is modified as function move_files()

Open Issues : 

"""
import shutil
import os,sys

def move_files(source_directory,destination_directory,no_of_files=-1):
	if not os.path.exists(destination_directory):
		os.makedirs(destination_directory)
	files = os.listdir(source_directory)
	count=0
	print "source_directory:",source_directory
	print "destination_directory:",destination_directory
	print 'limit :',no_of_files
	if no_of_files<=0:no_of_files=len(files)+1
	for each_file in files:
		count+=1
		if count>no_of_files:
			print 'Count exceeds !!'
			break
		else:
			shutil.move(os.path.join(source_directory,each_file), destination_directory)
			print 'Files moved :',count

if __name__=="__main__":
	source_directory = 'D:\\Ajith\\_code\\GeneralCodes\\sourcefolder'
	destination_directory = 'D:\\Ajith\\_code\\GeneralCodes\\movedFolder'
	limit =int(sys.argv[1])
	repeat_times=int(sys.argv[2])
	if True:
		for i in range(1,repeat_times+1):
			temp_directory=os.path.join(str(destination_directory)+str(i))
			print 'writing_directory :',temp_directory
			move_files(source_directory,temp_directory,limit)
	elif True:
		move_files(source_directory,destination_directory,limit)