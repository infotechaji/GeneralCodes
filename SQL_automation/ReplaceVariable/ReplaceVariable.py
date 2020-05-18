"""
Functionality :Script to replace the variables by the corresponding values
Version :	v2.0
History :
			v1.0 - 18/05/2020 initial version - 
			v2.0 - 18/05/2020 Logic for input set 2 is updated
Input:
Process:
Output :

Pending :
Open issues :
Comments :
"""

import os,argparse,sys
sys.path.insert(0,'G:\Ajith\OtherFiles\HelpText_from_sp')
from CustomisedFileOperation import * 


def split_my_line(input_line,split_by='\t'):
	return input_line.split(split_by)

def get_var_values(input_list,developer_mode=True):
	list1=split_my_line(str(input_list[0]).strip('\t\r\n'))
	list2=split_my_line(str(input_list[1]).strip('\t\r\n'))
	print ('list1 :',list1)
	print ('list2 :',list2)
	res_dict={}
	if len(list1)==len(list2):
		for index,each_var in enumerate(list1):
			value=list2[index]
			if '_ouinstance' in each_var.lower() or '_language' in each_var.lower() or value.lower().strip('\t\r\n')=='null':
				res_dict[each_var]=value
			else :
				res_dict[each_var]="'"+str(value)+"'"
	print ('Case 2 Input detected :\nres_dict :',res_dict)
	return res_dict

def extract_variables_and_values(variables,developer_mode=True):
	var_dict={}	
	# {variable1: value1 , variable1: value1 }
	print ('Type :',type(variables))
	# if type(variables)!=list:

	if len(variables)==2:
		print ('Length is 2')
		print ('1:',len(split_my_line(variables[0])))
		print ('2:',len(split_my_line(variables[1])))
		if len(split_my_line(variables[0]))==len(split_my_line(variables[1])):
			print ('Case 2 Input is found !\n Variable and Values in separate lines !')
			return get_var_values(variables,developer_mode=developer_mode)
	else:
		var_text=' '.join(variables)
		var_text=var_text.strip('\r\n\t')
		var_text=var_text.replace("N'","'")
		variables_list=var_text.split(',')
		for index,each_line in enumerate(variables_list):
			if index==0:
				temp_var=each_line.split('@')[1]
				temp_var='@'+str(temp_var)
			elif '@' in each_line: temp_var=each_line
			else:continue

			if developer_mode==True:
				print('extract_variables_and_values\t Variable before dividing:',temp_var)
			temp_var=temp_var.strip('\t\r\n')
			variable,value=temp_var.split('=')
			var_dict[variable.strip('\t ')]=value.strip('\t ')
		if developer_mode==True:
			print('extract_variables_and_values\t Results before returning:',var_dict)
	return var_dict
def get_replaced_text(variables,sp_text,developer_mode=True):
	"""
	Input : variables,sp_text,developer_mode=True
	Process: replaces the variables with the corresponding values 
	Output : replaced contents 
	Comments :
	"""
	if developer_mode==True:
		print('get_replaced_text\tvariables:',variables)
		print('get_replaced_text\tsp_text:',sp_text)
	var_dict=extract_variables_and_values(variables,developer_mode=developer_mode)
	actual_text=' '.join(sp_text) # if it is a list this will make this as a single line 
	temp_text=actual_text
	print ("Total Variables ",len(var_dict))
	count=0
	for each_variable in var_dict:
		count+=1
		if developer_mode==True:
			print('get_replaced_text\t Processing variables :'+str(count),each_variable)
		temp_text=temp_text.replace(each_variable,var_dict[each_variable]) # replacing each variable by its value 
		temp_text=temp_text.replace(each_variable.lower(),var_dict[each_variable]) # replacing each variable by its value 

	if actual_text.lower()==temp_text.lower():
		temp_text=''
	return {
			'content':sp_text,
			'replaced_content':temp_text
	}


if __name__=="__main__":
	arg = argparse.ArgumentParser('Program to create Patch File !!',add_help=True)
	arg.add_argument('-q','--input_file',help='File should contains Variable name and values in the format "@sample_variable=123,@sample_variable2=N\'123\',"',required=True)
	arg.add_argument('-sp','--select_query',help='SQL file contains the select statements in which the variables can be replaced',required=True)
	# # arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	variables_text=get_file_content(args.input_file,return_lines=True) # returns a single line 
	select_statement_text=get_file_content(args.select_query) # returns all the file content as a single line 
	result=get_replaced_text(variables_text,select_statement_text,False)
	if result['replaced_content']:
		out_file_name=args.select_query.replace('.','_REPLACED_VARIABLES_OUTPUT.')
		write_into_file(out_file_name,str(result['replaced_content']),'w')
