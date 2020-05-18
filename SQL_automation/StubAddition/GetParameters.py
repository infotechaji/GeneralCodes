import sys
from Stub import *
from CustomisedFileOperation import * 

def get_maximum_length(input_list):
	max_len=1
	for each_item in input_list:
		temp_len=len(each_item.strip('\r\t\n'))
		if temp_len>max_len:
			max_len=temp_len
	return max_len
def fill_by_space(input_str,char_to_fill=' ',max_legth=10):
	max_legth=int(max_legth)
	input_str=input_str.strip('\t\r\n')
	print ('max_legth :',max_legth)
	print ('String lenght :',len(input_str))
	if max_legth<=len(input_str):
		print ('Input string '+str(input_str)+' is greater than or equal to max lenght : '+str(max_legth))
		return input_str
	else:
		to_be_filled=max_legth-len(input_str)
		print ('to_be_filled :',to_be_filled)
		temp_string=str(char_to_fill)*int(to_be_filled)
		print ('temp_string :',temp_string)
		return str(input_str)+str(temp_string)
		



file_name=sys.argv[1]
result_dict=get_parameters(get_file_content(file_name),developer_mode=False,check_full_text=True)
# print (result_dict)
var=result_dict['variables']
print ('Total variables ',len(var))
mx_len=get_maximum_length(var)
# fill_by_space(input_str=input_str,char_to_fill=' ',max_legth=mx_len2)
# print (fill_by_space(input_str='Ajith',char_to_fill='*',max_legth=12))
final_text=''
for each_var in var:
	print (each_var)
	final_text+=str(fill_by_space(input_str=each_var,char_to_fill=' ',max_legth=mx_len))+"\t'"+str(each_var)+"' ,\n"
file_name_out=file_name.replace('.','_EXTRACTED_PARAMETERS_OUTPUT.')
write_into_file(file_name_out,final_text,'w')