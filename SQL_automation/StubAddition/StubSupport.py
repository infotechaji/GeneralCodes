from CustomisedFileOperation import * 
import sys

def get_out_attributes(input_list):
	out_list=[]
	for each_line in input_list:
		
		if "null " in each_line:
			variable=each_line.split("'")[1]
			temp_variable="@"+str(variable)+'  '
			temp_line=each_line.strip('\n').replace("null ",temp_variable)
			print ('added line:',temp_line)
			out_list.append(temp_line)
	return out_list

			



if __name__=="__main__":
	file_lines=get_file_content(sys.argv[1],return_lines=True)
	temp_lst=get_out_attributes(file_lines)
	for each_line in temp_lst:
		print (each_line)