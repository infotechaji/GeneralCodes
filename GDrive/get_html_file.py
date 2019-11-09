#-*-coding: utf-8 -*-
import codecs
import sys
import os
import chardet
from file_to_utf8 import * 
class HtmlActivites():
	def __init__(self,file_path):
		self.file_path=file_path
		self.output_file_encoding="UTF-8"
		result_dict=any_to_any_encoding(input_file=file_path,get_encoding_only=True)
		print 'result_dict:',result_dict
		with codecs.open(file_path, "r",result_dict['encoding']) as sourceFile:
			#file_lines_act=sourceFile.read()
			self.file_lines=sourceFile.read().split('\n')
		#self.file_lines=open(self.file_path,'r').readlines()
		self.get_html_file_name()
		pass
	def get_page_number(self):
		line_count=0
		self.page_number=''
		for each_line in self.file_lines:
			line_count+=1
			#print line_count,each_line
			if each_line.startswith('Page'):
				temp_page_number=each_line.split()[0:2]
				self.page_number=' '.join(temp_page_number).strip(' \t\n')
				print 'page number :',self.page_number
				self.content=' '.join(self.file_lines[line_count-1:])
				self.content_only=self.content.replace(self.page_number,'').replace('\r\n',' ').replace('  ',' ').strip(' \r\n\t')
				#print self.content_only
				break
			else:
				self.content=' '.join(self.file_lines[line_count-1:])
				self.content_only=self.content.replace(self.page_number,'').replace('\r\n',' ').replace('  ',' ').strip(' \r\n\t')
				print 'self.content_only :',self.content_only.encode('utf-8')
		return self.page_number



	def get_html_file_name(self,extension='.html'):
		self.file_name=self.file_path.split(os.sep)[-1]
		print 'text file_name :',self.file_name
		self.path_only=self.file_path.replace(self.file_name,'')
		print 'self.path_only :',self.path_only
		temp_html_file_name=self.file_name.split('.')[0]
		self.html_file_name=temp_html_file_name+extension
		self.title=temp_html_file_name
		self.get_page_number()
		return self.html_file_name
	def write_headers(self):
		#self.write_content="<START>\r\n<TITLE>"+self.title+"</TITLE>\r\n<BODY>\r\n<P>"+self.page_number+"</P>\r\n<P>"
		self.write_content="<START>\r\n<TITLE>"+self.title+"</TITLE>\r\n<BODY>\r\n"
		if self.page_number:
			self.write_content+="<P>"+str(self.page_number)+"</P>\r\n"
		self.write_content+='<P>'+str(self.content_only)+'</P>\r\n</BODY>\r\n<END>'
		# print 'html_file_name modified :',self.html_file_name
		# self.html_file_name=os.path.join('html_files',self.html_file_name)
		# print 'html_file_name modified :',self.html_file_name
		temp_output_directory=os.path.join(self.path_only,'html_files')
		try: 
			os.makedirs(temp_output_directory)
		except OSError:
			    #if not os.path.isdir(path):
			    pass
		html_path=os.path.join(temp_output_directory,self.html_file_name)
		print 'html_path:',html_path
		with codecs.open(html_path, "a",self.output_file_encoding) as targetFile:
			targetFile.write(self.write_content)
		# fp=open(self.html_file_name,'a')
		# fp.write(self.write_content)
		targetFile.close()

		
	
if __name__=="__main__":
	file_path='D:\\Ajith\\_code\\GoogleDrive\\sample_output\\testingOutput\\UAE0b15600.txt'
	ht=HtmlActivites(file_path)
	print 'object created!!!!'
	#ht.get_page_number()
	#print ht.get_html_file_name()
	ht.write_headers()