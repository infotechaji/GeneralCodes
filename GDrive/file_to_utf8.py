#-*- coding: utf-8 -*-
import codecs
import sys
import os
import chardet
import time
def any_to_any_encoding(input_file,get_encoding_only=False,output_file_encoding="UTF-8",use_underscore=True,delete_source=False):
	source_file_presence=True
	fp_read=open(input_file,'r')
	file_lines=fp_read.read()
	fp_read.close()
	input_file_encoding=chardet.detect(file_lines)['encoding']
	print 'Detected Encoding  \"%s\" from file \"%s\"'%(input_file_encoding,input_file)
	if get_encoding_only:
		return {'encoding':input_file_encoding,
				'input_file':input_file}
	with codecs.open(input_file, "r",input_file_encoding) as sourceFile:
		file_lines_act=sourceFile.read()
	sourceFile.close()
	if delete_source:
		os.remove(input_file)
		source_file_presence=False
		print "file \"%s\"deleted!!"%(input_file)
	time.sleep(1)
	if use_underscore:
		output_file=input_file.replace('.','_.')
	else:
		output_file=input_file
	with codecs.open(output_file, "w", output_file_encoding) as targetFile:
		targetFile.write(file_lines_act)
	targetFile.close()
	print 'file created with \"%s\" created with encoding \"%s\"'%(input_file,output_file_encoding)
	result_dict={'input_file':input_file,
				'output_file':output_file,
				'input_file_encoding':input_file_encoding,
				'output_file_encoding':output_file_encoding,
				'source_file_presence':source_file_presence}
	return result_dict

if __name__=="__main__":
	input_file=sys.argv[1]
	print any_to_any_encoding(input_file,get_encoding_only=True)
	#print any_to_any_encoding(input_file,delete_source=True)
	# fp_read=open(input_file,'r')
	# file_lines=fp_read.read()
	# fp_read.close()
	# encoding=chardet.detect(file_lines)['encoding']
	# print 'Encoding :',encoding
	# # fp_write=open('encoded_file.txt','w')
	# # fp_write.write(file_lines.encode('utf-8'))
	# # fp_write.close()
	
	# with codecs.open(input_file, "r",encoding) as sourceFile:
	# 	file_lines_act=sourceFile.read()
	# sourceFile.close()
	# os.remove(input_file)
	# print "file deleted!!"
	# time.sleep(1)
	# m_input_file=input_file.replace('.','_.')
	# with codecs.open(m_input_file, "w", ) as targetFile:
	# 	targetFile.write(file_lines_act)
	# targetFile.close()
	# print 'file created with encoding utf-8'



