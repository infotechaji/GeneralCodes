import os,sys,time

main_dir={'01.iRIS':['01.Proxy','02.API','03.Local Entries','04.XSLT','MessageStores','05.Sample'],
			'02.RM':{'01.AVNAPPDB':['01.UDD','02.Synonyms','03.Tables','04.Indexes','05.Metadata','06.Views','07.Functions','08.Sprocs']
					,'02.Integdb':['01.UDD','02.Synonyms','03.Tables','04.Indexes','05.Metadata','06.Views','07.Functions','08.Sprocs']}
					
			}
def create_directory(source_dir,sub_folders=[],files=[]):
	success =[]
	errored =[]
	try:
		for each_folder in sub_folders:
			if not os.path.exists(os.path.join(source_dir,each_folder)):
				os.makedirs(os.path.join(source_dir,each_folder))
				success.append(os.path.join(source_dir,each_folder))
	except Exception as e:
		print('Error while creating the directory :',e)
		errored.append(os.path.join(source_dir,each_folder))
	return {
		'success':success
		,'errored':errored
		}






if __name__=="__main__":
	cwd = os.getcwd()
	# lamda x,y : os.path.join(x,y)
	# x = lambda a, b : a * b
	x = lambda a, b : os.path.join(a,b)
	print (x(cwd,'yahoo'))
	print(list(map(x,[cwd],['yahoo','testing'])))

	for i in ['1','2']
	for i in main_dir:
		print(i,type(i),type(main_dir[i]))
		
		if type(type(main_dir[i]))==list:
			print ('Directories to create:',)
			create_directory(os.path.join(cwd,i),list)

