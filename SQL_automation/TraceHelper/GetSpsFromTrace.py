import re
import sys,os





if __name__=="__main__":
	filelines = open(sys.argv[1]).read()
	modified_pattern = 'exec (\w+)'
	total_ids = re.findall(modified_pattern, str(filelines),re.IGNORECASE)
	# print ('total_ids :',total_ids)
	output_file = sys.argv[1].replace('.','_ExtractedSps.')
	total_ids = list(set(total_ids))
	print (' Total sps:',len(total_ids))
	print (' Output file :',output_file)
	with open (output_file,'a') as fp:
		fp.write('\n'.join(total_ids)+str('\n'))

