from bs4 import BeautifulSoup
from domain_name_test import *
import sys,os

def soup_modification(page_source,remove_tags=[]):
		try:
			soup = BeautifulSoup(page_source, "html.parser")
		except Exception as e:
			#print 'except :',e
			soup=page_source
			pass
		if not remove_tags : remove_tags=['script','style']
		for tag in remove_tags:
			for each_tag in soup.select(tag):
				each_tag.decompose()
		#soup = BeautifulSoup(soup, "html.parser")
		return soup
def get_person_details(page_source):
	# result_dict ={
		# 'linkedin':linkedin,
		# 'twitter':twitter,
		# 'website':website,
		# 'job_category':job_category,
		# 'country':country,
		# 'industry_focus':industry_focus,
		# 'business_focus':business_focus,
		# 'customer_segment':customer_segment,
		# 'solution_area':solution_area
		# 'person_name':'',
		# 'designation':designation,
		# 'company_name':company_name 
		# }
	soup=soup_modification(page_source)	
	#print soup
	result_dict={}
	try:
		each_tag=soup.find("div",{"class":"attendee-detail__info"})
		#print 'each_tag :',each_tag
		#person name
		#try:
		temp_person_name=each_tag.find('div',{"class":"attendee-detail__info--heading"})
		person_name=temp_person_name.find('h3').text
		#except: person_name=''
		#print 'person_name :',person_name
		# designation and company
		try:
			temp_p_tag=each_tag.find('p',{"class":"c-paragraph-2 f-lean"})
			temp_designation=temp_p_tag.text
			try:company_name=temp_p_tag.find('a').text.strip()
			except:company_name=''
			if company_name:
				designation=temp_designation.replace(company_name,'').strip()
			else:
				designation=temp_p_tag.find('span').text.strip()
		except:pass
		# try:
		# 	print 'person_name :',person_name
		# 	print 'designation :',designation
		# 	print 'company_name :',company_name
		# except: pass
		result_dict ={
			'person_name':person_name.strip(),
			'designation':designation.strip(),
			'company_name':company_name.strip()
			}
		#handling left side details 
		left_divs=soup.find_all("div",{"class":"metadata__property"})
		total_list=[]
		for each_element in left_divs:
			header=each_element.find('h5').text.strip()
			a_tags=each_element.find_all('a')
			a_text=[]
			for each_tag in a_tags:
				temp_text=each_tag.text.strip()
				if temp_text:a_text.append(temp_text)
			temp_dict={'header':header,'divisions':a_text}
			total_list.append(temp_dict)
		result_temp_dict=get_mapped_dictionary(total_list)
		result_dict.update(result_temp_dict)
	except Exception as e:
		#print "Exception in getting data ",e
		pass
	#print "result_dict:\t get_person_details:\t",result_dict
	return result_dict
	
def get_mapped_dictionary(input_list):
	result_dict ={
		'linkedin':'',
		'twitter':'',
		'website':'',
		'job_category':'',
		'country':'',
		'industry_focus':'',
		'business_focus':'',
		'customer_segment':'',
		'solution_area':''
	}
	for dictt in input_list:
		if dictt['header'].lower()=='LinkedIn'.lower():
			result_dict['linkedin']=','.join(dictt['divisions']).strip(',')
		elif dictt['header'].lower()=='Twitter'.lower():
			result_dict['twitter']=','.join(dictt['divisions']).strip(',')
		elif dictt['header'].lower()=='Website'.lower():
			result_dict['website']=','.join(dictt['divisions']).strip(',')
		elif dictt['header'].lower()=='Job Category'.lower():
			result_dict['job_category']=','.join(dictt['divisions']).strip(',')
		elif dictt['header'].lower()=='Country'.lower():
			result_dict['country']=','.join(dictt['divisions']).strip(',')
		elif dictt['header'].lower()=='Industry Focus'.lower():
			result_dict['industry_focus']=','.join(dictt['divisions']).strip(',')
		elif dictt['header'].lower()=='Business Focus'.lower():
			result_dict['business_focus']=','.join(dictt['divisions']).strip(',')
		elif dictt['header'].lower()=='Customer Segment'.lower():
			result_dict['customer_segment']=','.join(dictt['divisions']).strip(',')
		elif dictt['header'].lower()=='Solution Area'.lower():
			result_dict['solution_area']=','.join(dictt['divisions']).strip(',')

	#print 'result_dict :',result_dict
	return result_dict
def write_into_file(file_name,content='',mode='a'):
		try:
			with open(file_name,mode) as fp:
				try:fp.write(content)
				except:fp.write(content.encode('utf-8'))
			return True
		except Exception as e :
			print('Exception in writing write_into_file :',file_name,e)
			return False
if __name__=="__main__":
	if not True:
		file_name=sys.argv[1]
		file_content=open(file_name).read()
		result_dict=get_person_details(file_content)
		if result_dict :
			final_text=str(result_dict['person_name'])+'\t'+str(result_dict['designation'])+'\t'+str(result_dict['company_name'])+'\t'
			final_text+=str(result_dict['linkedin'])+'\t'+str(result_dict['twitter'])+'\t'+str(result_dict['website'])+'\t'
			final_text+=str(result_dict['job_category'])+'\t'+str(result_dict['country'])+'\t'+str(result_dict['industry_focus'])+'\t'
			final_text+=str(result_dict['business_focus'])+'\t'+str(result_dict['customer_segment'])+'\t'+str(result_dict['solution_area'])
			final_text+="\n"
			write_into_file(file_name='result_files.txt',content=final_text)
	if True:
		import os
		input_directory=sys.argv[1]
		try:
			for root, dirs, files in os.walk(input_directory):
				file_count=0
				for file in files:
					file_count+=1
					write_into_file(file_name='file_names_test.txt',content=file+'\n')
					if False:continue
					file_full_path=os.path.join(root, file)
					try: file_content=open(file_full_path).read()
					except: continue
					#print 'Processig file ',file_count,file
					sys.stdout.write('count:'+str(file_count)+' \r')
					result_dict=get_person_details(file_content)
					if result_dict :
						final_text=''
						try:final_text+=str(result_dict['person_name'])+'\t'
						except :final_text+=result_dict['person_name']+'\t'
						try:final_text+=str(result_dict['designation'].strip(','))+'\t'
						except :final_text+=result_dict['designation'].strip(',')+'\t'
						try:final_text+=str(result_dict['company_name'])+'\t'
						except :final_text+=result_dict['company_name']+'\t'
						#str(result_dict['designation'])+'\t'+str(result_dict['company_name'])+'\t'
						try:final_text+=str(result_dict['linkedin'])+'\t'
						except :final_text+=result_dict['linkedin']+'\t'
						try:final_text+=str(result_dict['twitter'])+'\t'
						except :final_text+=result_dict['twitter']+'\t'
						try:final_text+=str(result_dict['website'])+'\t'
						except :final_text+=result_dict['website']+'\t'
						if result_dict['website']:
							temp_domain_name=get_domain_name(result_dict['website'])['domain_name']
							if len(temp_domain_name)>1:domain_name=temp_domain_name
							else:domain_name=''
						else:domain_name=''
						try:final_text+=str(domain_name)+'\t'
						except :final_text+=domain_name+'\t'
						#final_text+=str(result_dict['linkedin'])+'\t'+str(result_dict['twitter'])+'\t'+str(result_dict['website'])+'\t'
						try:final_text+=str(result_dict['job_category'])+'\t'
						except :final_text+=result_dict['job_category']+'\t'
						try:final_text+=str(result_dict['country'])+'\t'
						except :final_text+=result_dict['country']+'\t'
						try:final_text+=str(result_dict['industry_focus'])+'\t'
						except :final_text+=result_dict['industry_focus']+'\t'
						#final_text+=str(result_dict['job_category'])+'\t'+str(result_dict['country'])+'\t'+str(result_dict['industry_focus'])+'\t'
						try:final_text+=str(result_dict['business_focus'])+'\t'
						except :final_text+=result_dict['business_focus']+'\t'
						try:final_text+=str(result_dict['customer_segment'])+'\t'
						except :final_text+=result_dict['customer_segment']+'\t'
						try:final_text+=str(result_dict['solution_area'])
						except :final_text+=result_dict['solution_area']
						#final_text+=str(result_dict['business_focus'])+'\t'+str(result_dict['customer_segment'])+'\t'+str(result_dict['solution_area'])
						final_text+="\n"
						write_into_file(file_name='result_files.txt',content=final_text)
		except Exception as e:
			print 'Exception in reading file content ',e
		print ('processed files ',file_count)

# {
# 'linkedin':linkedin,
# 'twitter':twitter,
# 'website':website,

# 'job_category':job_category,
# 'country':country,

# 'industry_focus':industry_focus,
# 'business_focus':business_focus,
# 'customer_segment':customer_segment,
# 'solution_area':solution_area

# 'person_name':person_name
# 'designation':designation
# 'website':website
# }