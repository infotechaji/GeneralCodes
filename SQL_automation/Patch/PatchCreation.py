"""
Functionality  : Script to generate the patch file based on the input 
Version        : v1.0
History        : 
				 v1.0 - 26/03/2020 - initial version
Input: 
	A text file contains the below information as tab separated
	table_name \t column_name1 \t data_type1 
	table_name \t column_name2 \t data_type1
	table_name \t column_name3 \t data_type2 
	table_name \t column_name4 \t data_type1 
	
Output : 
		1.Patch file with all the attributes
"""
from CustomisedFileOperation import * 
import argparse

PATCH_HEADER="""
/*$File_version=MS4.3.0.00$*/
/********************************************************************************************/
/*	Filename				:	xxx-1111.sql											        */
/*	Author					:	AAAAAAAAA B													    */
/*	Date					:	01/01/2020														*/
/*	Component name			:																	*/
/*	DTSID					:	xxx-1111														*/
/*	Purpose of Patch		:	Table Script													*/
/********************************************************************************************/

SET NOCOUNT  ON
			"""

PATCH_QUERY="""
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'_table_name_'
		AND		b.name      =	'_column_name_'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE _table_name_ ADD _column_name_  _data_type_ null
	END
		"""

PATCH_FOOTER="""
SET NOCOUNT  OFF
			"""
def get_patch_query(table_name,column_name,data_type):
	table_name=table_name.strip('\t\r\n')
	column_name=column_name.strip('\t\r\n')
	data_type=data_type.strip('\t\r\n')
	temp=PATCH_QUERY
	temp=temp.replace('_table_name_',table_name)
	temp=temp.replace('_column_name_',column_name)
	temp=temp.replace('_data_type_',data_type)
	return {
			'patch_result':temp,
			'raw':PATCH_QUERY
			}
def get_patch_file(updated_patch_query):
	patch_file_content=str(PATCH_HEADER)+str(updated_patch_query)+str(PATCH_FOOTER)
	return {
			'patch_file_content':patch_file_content,
			'PATCH_HEADER':PATCH_HEADER,
			'PATCH_FOOTER':PATCH_FOOTER
			}



if __name__=="__main__":
	arg = argparse.ArgumentParser('Program to create Patch File !!',add_help=True)
	arg.add_argument('-i','--input_file',help='Trace file name',required=True)
	# # arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	input_filename=args.input_file
	if not True:
		table_name='wms_bin_type_hdr'
		column_name='wms_bin_typ_qty_capacity'
		data_type='udd_amount'
		res= get_patch_query(table_name,column_name,data_type)
		print ('Raw text :',res['raw'])
		print ('updated text :',res['patch_result'])
		write_into_file('Patch_file_res.sql',res['raw'],mode='w')
		write_into_file('Patch_file_res.sql',res['patch_result'],mode='a')
	if True:
		file_lines=get_file_content(input_filename)
		print ('Total Attributes:',len(file_lines))
		actual_content=''
		for index,each_line in enumerate(file_lines):
			table_name,column_name,data_type=each_line.strip('\n').split('\t')
			# print ('table_name:',table_name)
			# print ('column_name:',column_name)
			# print ('data_type:',data_type)
			print ('Lines processed :',index+1)
			updated_patch= get_patch_query(table_name,column_name,data_type)['patch_result']
			# updated_patch= get_patch_query(each_line.strip('\r\n').split('\t'))['patch_result']
			write_into_file('Patch_queries.sql',str(updated_patch),mode='a')
			actual_content+=str(updated_patch)
		patch_full_content=get_patch_file(actual_content)['patch_file_content']
		write_into_file('Full_patch_file.sql',str(patch_full_content),mode='a')