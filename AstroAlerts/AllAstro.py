
#--testing comming
from Generic_Scrapy import * 
from custom_mail import * 
from AutoAstroDeccan import * 

class Astro():
	def __init__(self,developer_mode=False):
		self.developer_mode=developer_mode
		self.astro_list=['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces']
		self.scrapy_obj=MasterScrape(0)
		self.full_file_list=[]
		self.ganesha_speaks_link="https://www.ganeshaspeaks.com/horoscopes/daily-horoscope/{}/"
		self.cyber_astro_link="https://www.cyberastro.com/prediction/{}_daily.asp"
		self.astro_yogi_link="https://www.astroyogi.com/horoscopes/daily/{}-free-horoscope.aspx"
		self.main_list=[
						{'website':'astro_yogi',
						'link':"https://www.astroyogi.com/horoscopes/daily/{}-free-horoscope.aspx"
						}
						,
						{'website':'cyber_astro',
						#'link':"https://www.cyberastro.com/prediction/{}_daily.asp"
						'link':"https://www.cyberastro.com/{}-prediction"
						}
						,{'website':'ganesha_speaks',
						'link':"https://www.ganeshaspeaks.com/horoscopes/daily-horoscope/{}/"
						}
						]
		self.get_deccan_prediction()
	def get_deccan_prediction(self):
		astr_obj=AstroDeccan(developer_mode=False)
		#astr_obj.get_prediction(args.input_list.split(','),args.destroy_time)
		deccan_results=astr_obj.get_prediction(desktop_notification=False)
		for each_dict in deccan_results:
			each_astro=each_dict['astro']
			prediction=each_dict['astro_prediction']
			try: final_text='Deccan\t'+str(prediction)+'\n'
			except : final_text='Deccan\t'+str(prediction.encode('utf-8'))+'\n'
			file_name=str(each_astro)+'_'+get_printable_time_stamp(get_date_only=True)+'.txt'
			with open(file_name,'a') as fp:
				fp.write(final_text)
	def __del__(object):
		pass
	
	def general_astro(self,link='',get_all_prediction=True,get_specific=[]):
		result_dict={}
		if get_specific:source_list=get_specific
		else:source_list=self.astro_list
		for each_astro in source_list:
			for each_dict in self.main_list:
				print 'Current Website  :',each_dict['website']
				temp_link=each_dict['link'].format(each_astro)
				print 'processing link :',temp_link
				page_source=self.scrapy_obj.GetPageSoure(link=temp_link,use_request=True,check_files=False,save_file=False)
				#print 'page_source :',len(page_source)
				soup=self.scrapy_obj.soup_modification(page_source)
				#print 'soup :',soup
				
				if each_dict['website']=='ganesha_speaks':
					get_div_tag=soup.find('p',{"class":"margin-top-xs-0"})
					#print 'get_div_tag :',get_div_tag.text.strip(' \r\n')
					prediction=get_div_tag.text.strip(' \r\n')
				elif each_dict['website']=='cyber_astro':
					#div_tag=soup.find('div',{"class":"prediction-coll img-prediction"})
					# p_tag=div_tag.find('p')
					# #print 'get_div_tag :',get_div_tag.text.strip(' \r\n')
					# prediction=p_tag.text.strip(' \r\n')
					#print soup
					div_tag=soup.find('div',{"class":"resp-tabs-container ver_1"})
					div_tag1=div_tag.find('div')
					#print "div_tag1 :",div_tag1
					p_tags=div_tag1.find_all('p')
					#print "p_tag :",p_tag
					#div_tag=soup.find('div',{"class":"resp-tab-content ver_1 resp-tab-content-active"})
					prediction=''
					for each_p_tag in p_tags:
						prediction+=each_p_tag.text.strip(' \r\n')
					
				elif each_dict['website']=='astro_yogi':
					#p_tags=soup.findAll('p',{"class":"top15 text-justify"})
					p_tags=soup.findAll('p',{"class":"top15 text-justify line27 top17"})
					#print 'len(p_tags):',len(p_tags)
					span=p_tags[1]
					#print 'get_div_tag :',get_div_tag.text.strip(' \r\n')
					prediction=span.text.strip(' \r\n')
					prediction=prediction.replace('Click here for a more personalised reading','')
					prediction=prediction.replace('  ',' ').strip(' ').strip(' \r\n')
				
				try:
					print each_astro, ' :',str(prediction)
				except:
					print each_astro.encode('utf-8'), ' :',str(prediction.encode('utf-8'))

				try: final_text=str(each_dict['website'])+'\t'+str(prediction)+'\n'
				except : final_text=str(each_dict['website'].encode('utf-8'))+'\t'+str(prediction.encode('utf-8'))+'\n'
				file_name=str(each_astro)+'_'+get_printable_time_stamp(get_date_only=True)+'.txt'
				
				if file_name not in self.full_file_list:self.full_file_list.append(file_name)

				with open(file_name,'a') as fp:
					fp.write(final_text)
				result_dict[each_astro]=prediction
		return result_dict

	def get_astro_yogi(self,link='',get_all_prediction=True,get_specific=[]):
		result_dict={}
		if get_specific:source_list=get_specific
		else:source_list=self.astro_list
		for each_astro in source_list:
			temp_link=self.astro_yogi_link.format(each_astro)
			print 'processing link :',temp_link
			page_source=self.scrapy_obj.GetPageSoure(link=temp_link,use_request=True,check_files=False,save_file=False)
			#print 'page_source :',len(page_source)
			soup=self.scrapy_obj.soup_modification(page_source)
			#print 'soup :',soup
			p_tags=soup.findAll('p',{"class":"top15 text-justify"})
			span=p_tags[1]
			#print 'get_div_tag :',get_div_tag.text.strip(' \r\n')
			prediction=span.text.strip(' \r\n')
			prediction=prediction.replace('Click here for a more personalised reading','')
			prediction=prediction.replace('  ',' ').strip(' ').strip(' \r\n')
			try:
				print each_astro, ' :',str(prediction)
			except:
				print each_astro.encode('utf-8'), ' :',str(prediction.encode('utf-8'))
			print 
			result_dict[each_astro]=prediction
		return result_dict

	def get_cyber_astro(self,link='',get_all_prediction=True,get_specific=[]):
		result_dict={}
		if get_specific:source_list=get_specific
		else:source_list=self.astro_list
		for each_astro in source_list:
			temp_link=self.cyber_astro_link.format(each_astro)
			print 'processing link :',temp_link
			page_source=self.scrapy_obj.GetPageSoure(link=temp_link,use_request=True,check_files=False,save_file=False)
			#print 'page_source :',len(page_source)
			soup=self.scrapy_obj.soup_modification(page_source)
			#print 'soup :',soup
			div_tag=soup.find('div',{"class":"prediction-coll img-prediction"})
			p_tag=div_tag.find('p')
			#print 'get_div_tag :',get_div_tag.text.strip(' \r\n')
			prediction=p_tag.text.strip(' \r\n')
			try:
				print each_astro, ' :',str(prediction)
			except:
				print each_astro.encode('utf-8'), ' :',str(prediction.encode('utf-8'))
			print 
			result_dict[each_astro]=prediction
		return result_dict

	def get_astro_ganesha_speaks(self,link='',get_all_prediction=True,get_specific=[]):
		result_dict={}
		if get_specific:source_list=get_specific
		else:source_list=self.astro_list
		for each_astro in source_list:
			temp_link=self.ganesha_speaks_link.format(each_astro)
			print 'processing link :',temp_link
			page_source=self.scrapy_obj.GetPageSoure(link=temp_link,use_request=True,check_files=False,save_file=False)
			#print 'page_source :',len(page_source)
			soup=self.scrapy_obj.soup_modification(page_source)
			get_div_tag=soup.find('p',{"class":"margin-top-xs-0"})
			#print 'get_div_tag :',get_div_tag.text.strip(' \r\n')
			prediction=get_div_tag.text.strip(' \r\n')
			try:
				print each_astro, ' :',str(prediction)
			except:
				print each_astro.encode('utf-8'), ' :',str(prediction.encode('utf-8'))
			print 
			result_dict[each_astro]=prediction
		return result_dict
		
if __name__=="__main__":
	# link="https://www.ganeshaspeaks.com/horoscopes/daily-horoscope/{}/"
	# #print link.format{'pises'}
	# print link.format('pises')
	get_specific=['pisces','scorpio']
	get_specific=[]
	obj=Astro()
	#obj.get_astro_ganesha_speaks(get_all_prediction=True,get_specific=get_specific)
	#obj.get_cyber_astro(get_all_prediction=True,get_specific=get_specific)
	#obj.get_astro_yogi(get_all_prediction=True,get_specific=get_specific)
	obj.general_astro(get_all_prediction=True,get_specific=get_specific)
	send_custom_mail(obj.full_file_list)
	

