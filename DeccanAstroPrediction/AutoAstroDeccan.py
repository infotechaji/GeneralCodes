from webSearch import  *
from bs4 import BeautifulSoup
from Create_windows_popup import *
import argparse
class AstroDeccan():
	def __init__(self,developer_mode=True):
		self.developer_mode=developer_mode
		self.source_url='https://www.deccanchronicle.com/daily-astroguide'
		self.class_name="AstroDeccan:\t"
	def get_page_source(self):
		print_prefix=self.class_name+"get_page_source:\t"
		user_agent='Mozilla/%2F4.0'
		request = urllib2.Request(self.source_url)
		request.add_header('User-Agent', user_agent)
		request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		cj = cookielib.CookieJar()#to handle cookie
		request_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		response=None
		url_content=''
		try:
			response = request_opener.open(request)
			url_content = response.read()
			if self.developer_mode: print print_prefix+'len(url_content):',len(url_content)
			#return url_content
			#print url_content
		except Exception as e:
			#error_is=str(e)
			print  'Exception :',e
			#return url_content
		return url_content
	def get_prediction(self,my_astro,destroy_time=5):
		print_prefix=self.class_name+"get_prediction:\t"
		url_content=self.get_page_source()
		#print len(url_content)
		if my_astro[0].strip(' \t\r\n').lower()=='all':
			my_astro=['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricon','aquarius','pisces']
		soup=BeautifulSoup(url_content,"html.parser")
		div_tags=soup.findAll('div',class_='col-sm-10 col-xs-8 ')#.text.strip(' \t\n')
		#print 'div_tags :',len(div_tags)
		temp_list=[]
		#temp_dict={'astro':'','astro_prediction':''}
		if self.developer_mode : print print_prefix+'astro list :'+str(my_astro)
		for each_div in div_tags:
			for each_astro in my_astro: # input list
				temp_dict={'astro':'','astro_prediction':''}
				a_text=each_div.find('a').text.strip(' \t\n')
				if each_astro in a_text.lower():
					raw_text=each_div.text.strip(' \t\n')
					raw_text=raw_text.replace('\n',' ').replace('\t',' ').replace('	',' ').replace('  ',' ')
					#print 'raw_text:',raw_text.encode('utf-8')
					raw_text=raw_text.replace(a_text,'').strip(' \r\n\t')
					temp_dict['astro']=each_astro
					temp_dict['astro_prediction']=raw_text
					temp_list.append(temp_dict)
		return self.display_prediction(temp_list,destroy_time)
	def display_prediction(self,input_list,destroy_time=3):
		print_prefix=self.class_name+"display_prediction:\t"
		wd_obj=WindowsBalloonTip()
		self.max_display_len=160
		for each_dict in input_list:
			prediction_list=[]
			if len(each_dict['astro_prediction'].split('.'))>3 or len(each_dict['astro_prediction']) > self.max_display_len:
				prediction_list=self.get_parsed_text(each_dict['astro_prediction'].split('.'))
			else:
				sub_sentence=each_dict['astro_prediction'].strip(' \t\r\n')
				prediction_list.append(sub_sentence)
			if self.developer_mode: print print_prefix+'prediction_list :',prediction_list
			for each_line in prediction_list:
				pass
				if self.developer_mode: print print_prefix+'len(each_line):', len(each_line)
				if self.developer_mode: print print_prefix+'each_line:',each_line
				wd_obj.popup_windows(title=each_dict['astro'].upper(),msg=each_line,destroy_time=destroy_time)
			#wd_obj.OnDestroy()
	def get_parsed_text(self,input_list): # parsed list which split by .
	    print_prefix=self.class_name+"get_parsed_text:\t"
	    parsed_list=[]
	    if self.developer_mode: print print_prefix+'input_list:',input_list
	    for i in range(0,len(input_list)):
	        next_index=i+1
	        if next_index>=len(input_list):next_index=0
	        if self.developer_mode: print print_prefix+'len(input_list) :',len(input_list)
	        if self.developer_mode: print print_prefix+'next_index :',next_index
	        if not input_list[i]: #or input_list[i].strip(' \t\r\n').startswith('#'): return ''
	        	continue
	        if len(input_list[i]+','+input_list[next_index])<=self.max_display_len:
	            if input_list[i] and not input_list[i].strip(' \t\r\n').startswith('#'):
	                current_sentence=input_list[i]
	                input_list[i]=''
	            if input_list[next_index] and not input_list[next_index].strip(' \t\r\n').startswith('#'):
	                current_sentence+=','+input_list[next_index]
	                input_list[next_index]=''
	            if self.developer_mode: print print_prefix+'current_sentence first if :',current_sentence
	        elif len(input_list[i])<=self.max_display_len:
	            if not input_list[i].strip(' \t\r\n').startswith('#'):
	                current_sentence=input_list[i]
	                input_list[i]=''
	        if self.developer_mode: print print_prefix+'current sentence :',current_sentence
	        if current_sentence:
	            current_sentence=current_sentence.strip(' ,\t\r\n')
	            if current_sentence not in parsed_list:
	                parsed_list.append(current_sentence.strip(' ,\t\r\n'))
	    if self.developer_mode: print print_prefix+'parsed_list :',parsed_list
	    return parsed_list


if __name__ =='__main__':
	arg = argparse.ArgumentParser('Program to collect basic details of a company',add_help=True)
	arg.add_argument('-i','--input_list',help='Enter astros(comma separated) ',default ='scorpio,pisces',required=False)
	arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	astr_obj=AstroDeccan(developer_mode=False)
	astr_obj.get_prediction(args.input_list.split(','),args.destroy_time)
