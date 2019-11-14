import sys
import os

def write_content(self,file_name,content_dict):
		if file_name=='scraped_results.txt':
			fp=open(file_name,'a')
			final_text=str(content_dict['total_accounts_count'])+'\t'
			final_text+=str(content_dict['person_name'])+'\t'+str(content_dict['person_url'])+'\t'
			final_text+=str(content_dict['linkedin_url'])+'\t'+str(content_dict['designation'])+'\t'
			final_text+=str(content_dict['company_name'])+'\t'+str(content_dict['unparsed_designation'])+'\t'
			final_text+=str(content_dict['account_count'])+'\t'+str(content_dict['page_number'])+'\t'
			final_text+='\n'
			fp.write(final_text)
			fp.close()
if __name__=="__main__":
	file_lines=open(sys.argv[1],'r').readlines()
	write_fp=open('parsed_text.txt','a')
	end_list=['inc','llc','l.l.c','ltd','llp','p.l']
	count=0
	for each_line in file_lines:
		count+=1
		splits=each_line.strip(' \t\r\n').split('\t')
		p_id=splits[0]
		person_name=splits[1]
		try:
			designation_source_test=splits[2]
		except Exception as e :
			designation_source_test=''
			pass
		designation_split=designation_source_test.split(',')
		designation=''
		company_name=''
		try:
			if len(designation_split)==2:
				designation=designation_split[0]
				company_name=designation_split[1]
				#print "case 1 :"
			elif len(designation_split)==3:
				comp_end=False
				for i in end_list:
					if i in designation_split[2].lower() and not comp_end:
						comp_end=True
					if comp_end:
						break
				if comp_end:
					designation=designation_split[0]
					company_name=','.join(designation_split[1:])
				elif not comp_end:
					designation=','.join(designation_split[0:2])
					company_name=designation_split[-1]
				#print "case 2 :"
			elif len(designation_split)>3:
				comp_end=False
				for i in  end_list:
					if i in designation_split[-1].lower() and not comp_end:
						comp_end=True
					if comp_end: break
				if comp_end:
					#print 'if case '
					#print designation_split
					designation=','.join(designation_split[:len(designation_split)-2])
					company_name=','.join(designation_split[len(designation_split)-2:])
				elif not comp_end:
					#print 'Else case :'
					designation=','.join(designation_split[len(designation_split)-1:])
					company_name=designation_split[-1]
				#print "case 3 :"#" \ndesignation",designation,'\n company_name :',company_name
		except Exception as e :
			pass
		# print 'designation_source_test:',designation_source_test
		# print 'designation :',designation
		# print 'company_name :',company_name
		#raw_input()
		print count,designation,company_name
		final_text=str(p_id)+'\t'+str(person_name)+'\t'
		final_text+=str(designation_source_test)+'\t'+str(designation.strip(' .,/'))+'\t'
		final_text+=str(company_name.strip(' .,/'))
		final_text+='\n'
		write_fp.write(final_text)
	write_fp.close()




