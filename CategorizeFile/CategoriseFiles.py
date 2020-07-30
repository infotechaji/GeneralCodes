""""
Functionality : Script to Organize files
Description :
Version     : v2.0
History     :
			  v1.0 - 07/06/2020 - initial version
			  v2.0 - 08/06/2020 - Special option for handling image files is added
Input :
Output :
Pending cases :
				1, Getting input from user via Tinker
				2, Exe file creation and testing

Open issues : 
"""
import argparse
import os,sys,time,datetime
from copy_folder import *
import calendar
import imghdr
from ImageCreationDate import get_image_details

LOCAL_DATE_MAPPER={
							'01':'January','02':'February','03':'March','04':'April',
							'05':'May','06':'June','07':'July','08':'August',
							'09':'September','10':'October','11':'November','12':'December'
							}
IMAGE_EXTENSION=['rgb','gif','pbm','pgm','ppm','tiff','rast','xbm','jpeg','jpg','bmp','png','webp','exr','.mp4']
class CategorizeFile():
	def __init__(self,split_by_year=True,split_by_month=True,split_by_date=False,move_file=False,developer_mode=False):
		self.developer_mode=developer_mode
		self.class_name='CategorizeFile:\t'
		self.split_by_year=split_by_year
		self.split_by_month=split_by_month
		self.split_by_date=split_by_date
		self.move_file=move_file

	def get_splitted_date(self,created):
		created=int(created)
		"""
		This function accepts a time format and return the created data
		"""
		self.module_name='get_splitted_date:\t'
		if self.developer_mode :print(self.class_name,self.module_name,"Date created:\t" + time.ctime(created))
		if self.developer_mode :print(self.class_name,self.module_name,"Date created:", datetime.datetime.fromtimestamp(created))
		year, month, day, hour, minute, second = time.localtime(created)[:-3]
		if self.developer_mode :print(self.class_name,self.module_name,"Date created: %02d/%02d/%d %02d:%02d:%02d" % (day, month, year, hour, minute, second))
		try:
			month_txt=calendar.month_name[int(month)]
		except Exception as e:
			print('Error in mapping month :',e)
			try:
				month_txt=LOCAL_DATE_MAPPER[month]
			except:
				month_txt=month
		return_dict={
					'year':year,
					'month':month,
					'month_text':month_txt,
					'date':day,
					'hours':hour,
					'mins':minute,
					'seconds':second
					}
		return return_dict
	def is_image(self,image_path):
		"""

		:param image_path:
		:return True or False:
		"""
		try:
			if imghdr.what(image_path).lower() in IMAGE_EXTENSION:
				if self.developer_mode: print(self.class_name,self.module_name,'Yes it is an image ',imghdr.what(image_path))
			return True
		except:pass
		return False
	def  get_file_details(self,file_path):
		"""
		:param file_path:
		:return: fill file details
		"""
		created = os.path.getctime(file_path)
		modified = os.path.getmtime(file_path)
		# Test case
		# st = os.stat(file_path)
		# print ('full details :',st)
		# self.get_splitted_date('1051019939')
		# self.get_splitted_date('1591539065')
		# self.get_splitted_date('1570640618')
		# self.get_splitted_date('1591551755')
		# input()
		# return
		temp_dict ={'created_date':created,
				   'modified_date':modified
					}
		if self.developer_mode:
			print('get_file_details :',temp_dict)
		return temp_dict

	def categorise_file(self,input_directory,output_directory,classification_type='created_date'):
		self.module_name='categorise_file:\t'
		if self.developer_mode:
			print(self.class_name,self.module_name,'input_directory :',input_directory,'\nOutput directory :',output_directory)
		file_count = 0
		status = 'copied'
		skipped_count=0
		for root, dirs, files in os.walk(input_directory):
			for each_file in files:
				file_count+=1
				# if each_file.endswith(delete_extension):
				full_file_path=os.path.join(input_directory,each_file)
				print('Processing file :',file_count)
				if self.developer_mode:
					print(self.class_name, self.module_name,'File name : ',full_file_path)
				if self.is_image(full_file_path)==True:
					date_dict=get_image_details(full_file_path,developer_mode=self.developer_mode)
					if self.developer_mode: print(self.class_name,self.module_name,'direct image extraction :',date_dict)
				else:
					if classification_type == 'created_date':
						date_to_parse=self.get_file_details(full_file_path)['created_date']
					elif  classification_type == 'modified_date':
						date_to_parse=self.get_file_details(full_file_path)['modified_date']
						pass
					if self.developer_mode: print('categorise_file:\tdate_to_parse:\t',date_to_parse)
					date_dict=self.get_splitted_date(date_to_parse)
				if self.developer_mode:  print(self.class_name,self.module_name,'date_dict :',date_dict)
				temp_dir=''
				if not date_dict: # for default cases
					date_to_parse = self.get_file_details(full_file_path)['created_date']
					date_dict = self.get_splitted_date(date_to_parse)
					# print('Date dictionary is not found even if it is image ! Quitting !! ')
					# return  False
					# print ('skipping file as data dict is missing :',each_file)
					# input()
					# skipped_count+=1
					# continue
				if self.developer_mode: print(self.class_name,self.module_name,"\nsplit_by_year :",self.split_by_year,"\n split_by_month:",self.split_by_month,"\n split_by_date",self.split_by_date)
				if self.split_by_year == True:temp_dir = os.path.join(temp_dir, str(date_dict['year']))
				if self.split_by_month == True:temp_dir=os.path.join(temp_dir,str(date_dict['month_text'])) #date_dict['month_str']
				if self.split_by_date == True: temp_dir=os.path.join(temp_dir,str(date_dict['date']))
				if self.developer_mode: print(self.class_name, self.module_name,"temp_dir:\t",temp_dir,"\n output_directory:",output_directory)
				output_directory_temp=os.path.join(output_directory,temp_dir)
				if self.developer_mode: print('Destination directory:',output_directory_temp)
				# if not os.path.exists(output_directory_temp): os.mkdirs(output_directory_temp)
				if not os.path.exists(output_directory_temp):
					os.makedirs(output_directory_temp)
				# dest_file_name=os.path.join(output_directory_temp,each_file)
				# if self.developer_mode: print('Destination file (full path) :', dest_file_name)
				try:
					copy_file(src=input_directory, dst=output_directory_temp, files_list=[each_file])  # copies the selected files
					if self.move_file==True:
						status='moved'
						try:
							os.remove(full_file_path)
						except Exception as e:
							print('Error while deleting the file :',full_file_path)
				except Exception as e:
					print('Got the Error',str(e),' while copying file:',each_file,dest_file_name)
				# if file_count >=3:break
			break # for skipping directories
		temp_d={'Total_files':file_count,
				'status':status,
				'skipped':skipped_count}
		return temp_d






if __name__ =='__main__':
	arg = argparse.ArgumentParser('File script will help to categrise the files using timestamp by year and month wise ',add_help=True)
	arg.add_argument('-i','--input_directory',help='Input directory,  which contains all the files ',required=True)
	arg.add_argument('-out','--output_directory',help='Output directory which we need to categrise',default='',required=False)
	arg.add_argument('--dev_mode',help='To enable Developer mode , use "--dev_mode" ',nargs='?',const=True,default=False,required=False)
	arg.add_argument('--year',help='to categorise using year ',nargs='?',const=True,default=True,required=False)
	arg.add_argument('--month', help='to categorise using month ',nargs='?', const=True, default=True, required=False)
	arg.add_argument('--date', help='to categorise using year ',nargs='?',const=True, default=False,required=False)
	arg.add_argument('--move', help='Can be enabled to move the file completely  ',nargs='?',const=True, default=False,required=False)
	arg.add_argument('-ct','--classification_type', help='permitted types "modified_date","created_date" ', default="created_date" ,required=False)
	args = arg.parse_args()
	print('args :',args)
	print('Input directory :',args.input_directory)
	print('Output directory :',args.output_directory)
	if not args.output_directory:output_directory=args.input_directory
	else: output_directory=args.output_directory
	cus_obj=CategorizeFile(split_by_year=args.year,split_by_month=args.month,split_by_date=args.date,move_file=args.move,developer_mode=args.dev_mode)
	result_dict=cus_obj.categorise_file(input_directory=args.input_directory,output_directory=output_directory,classification_type=args.classification_type)
	print('Process status :',result_dict)

	# New Pattern to be added in the date classification_type
	# IMG20191105195030 

	# sample command to run  
	# python CategoriseFiles.py -i G:\Ajith\Others\MyImages\DCIM\TestCase