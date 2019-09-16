import os.path,sys
def trim_list(input_list):
	output_list=[]
	for i in input_list:
		pass
if __name__=="__main__":
	input_file_name=sys.argv[1]
	output_file_name=input_file_name.replace('.','_output.')
	file_lines=open(input_file_name).readlines()
	count=0
	for each_line in file_lines:
		count+=1
		splits=each_line.strip(' \t\r\n').split('\t')
		key=splits[0]
		value=splits[1:]
		#print 'key:',key
		#print 'value:',value
		final_text=",'"+key+"'"+":"+str(value)+'\n'
		with open(output_file_name,'a') as fp:
			fp.write(final_text)
		print count,key