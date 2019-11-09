import sys,os

if __name__=='__main__':
	file_name=sys.argv[1]
	output_filename=file_name.replace('.','_output.')
	file_lines=open(file_name).readlines()
	print 'len(file_lines) :',len(file_lines)
	fp=open(output_filename,'a')
	for each_line in file_lines:
		company_id,line=each_line.strip(' \t\r\n').split('\t')
		line_splits=line.split(',')
		country_temp=line_splits[-1]
		if country_temp:
			try:
				country,zip_code=country_temp.split()
				address=str(line.replace(country_temp,'')).strip(' \r\n\t,')
			except:
				country=''
				zip_code=''
			#address=str(line.replace(country_temp,'')).strip(' \r\n\t')
		else:
			country=''
			zip_code=0
			address=each_line
		final_text=str(company_id)+'\t'+line.strip(' \t\r\n')+'\t'
		final_text+=str(address)+'\t'+str(country)+'\t'
		final_text+=str(zip_code)
		final_text+='\n'
		fp.write(final_text)
	fp.close()