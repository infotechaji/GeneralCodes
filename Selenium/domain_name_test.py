from WebsiteCodesSupport import *
import sys,os

def get_domain_name(input_link):
	web_ins=WebURLParse(input_link,ignore_errors=True,developer_mode=False)
	domain_name =web_ins.get_website_parent()+'.'+web_ins.get_website_suffix()
	if domain_name:
		return {'domain_name': domain_name}
	else: return {}

if __name__=="__main__":
	if not True:
		sample_text='306 W Michigan St'
		print get_domain_name(sample_text)
	if True:
		input_file_name=sys.argv[1]
		output_file_name=input_file_name.replace('.','_output.')
		file_lines=open(input_file_name).readlines()
		count=0
		for each_line in file_lines:
			count+=1
			#if True:
			try:
				record_identifier,input_link=each_line.strip(' \t\r\n').split('\t')
				#print  count#,input_link
				sys.stdout.write(' count:'+str(count)+' \r')
				parsed_domain=get_domain_name(input_link)['domain_name']
				#print 'parsed_domain :',parsed_domain
				if len(parsed_domain)>2:
					final_text =str(record_identifier) +'\t'+str(input_link)+'\t'
					try:final_text +=str(parsed_domain)
					except:final_text +=parsed_domain
					#final_text +=str(parsed_domain)
					final_text+='\n'
					with open(output_file_name,'a') as fp :
						try:fp.write(final_text)
						except:fp.write(final_text.encode('utf-8'))
						#fp.write(final_text)
			except Exception as e:
				print  count
				print 'Error while processing ',input_link
				pass
		print  count



