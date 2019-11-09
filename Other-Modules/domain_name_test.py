from WebsiteCodesSupport import *

def get_domain_name(input_link):
	web_ins=WebURLParse(input_link,ignore_errors=False,developer_mode=False)
	domain_name =web_ins.get_website_parent()+'.'+web_ins.get_website_suffix()
	if domain_name:
		return {'domain_name': domain_name}
	else: return {}

if __name__=="__main__":
	sample_text='306 W Michigan St'
	print get_domain_name()