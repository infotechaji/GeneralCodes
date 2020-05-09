"""
Description : Contains all the common file operations
"""
import os.path
from os import path
import os 

def get_file_content(filename,return_lines=False):
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

def get_file_presence(file):
	return os.path.exists(file)