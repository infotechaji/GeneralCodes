import os
import re,sys
import lib  

#this is the latest version

# Function to rename multiple files
def rename_files(input_dir,source_text,text_to_replace='sample',replace_file_content= True,ignore_sub_dir= True):
	print('Input directory:',input_dir)
	# for count, filename in enumerate(os.listdir(input_dir)):
	if source_text == text_to_replace:
		print ('No change!')
		return -1
	try:
		for path, subdirs, files in os.walk(input_dir):
			print ('\nCurrent directory :',os.path.join(path))
			for filename in files:
				try:
					src =filename
					# print ('Before condition :',src)
					# print (open(os.path.join(path,src),'r').read())
					if (source_text.lower() in filename.lower()) or (source_text.lower() in (open(os.path.join(path,src),'r').read()).lower()):
						print ('Condition passed for :',filename)
						src_str  = re.compile(source_text, re.IGNORECASE)
						dst  = src_str.sub(text_to_replace,filename)
						# print('filename :',filename)
						src_path = os.path.join(input_dir,path,src)
						dst_path = os.path.join(input_dir,path,dst)
						if os.path.exists(src_path):
							os.rename(src_path, dst_path)
							print('File renamed :',src,';',dst)
							if replace_file_content == True:
								try:
									fin = open(dst_path, "r")
									# fin = open(dst_path, "r")
									data = fin.read()
									data = src_str.sub(text_to_replace, data)
									fin.close()
								except Exception as e:
									print('Error while reading and replacing contens of the file :',e)

								try:
									# reload(sys)  # Reload does the trick!
									# sys.setdefaultencoding('UTF8')
									finw = open(dst_path, "w")
									# finw = open(dst_path, "w")
									finw.write(data)
									finw.close()
								except Exception as e:
									print('Error while writing [replaced] contents to the file :',e)
						else:
							print('File does not exist to rename !',src_path)
				except Exception as ee:
					print ('Error while reading the file :',ee)
					pass
			if ignore_sub_dir==True:
				break
	except Exception as e:
		print('Error while renaming ..',e)
		pass

  

if __name__ == '__main__':

	# Calling main() function
	rename_files(sys.argv[1],sys.argv[2],sys.argv[3],replace_file_content= True,ignore_sub_dir= False)
	# src_str  = re.compile("this", re.IGNORECASE)
	# str_replaced  = src_str.sub("that", "THiS is a test sentence. this is a test sentence. THIS is a test sentence.")
	# print (str_replaced)
