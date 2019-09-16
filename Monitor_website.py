import requests

class MonitorWebsite():
	def __init__(self):
		pass
	def __del__(object):
		print 'MonitorWebsite object deleted !'
	def check_website_content(url,content_size=0):
		res_body = requests.get(url).text
		print 'len(res_body) :',len(res_body)

if __name__=="__main__":
	url='https://www.fiind.com/'
	monitor_obj=MonitorWebsite()
	monitor_obj.check_website_content()

