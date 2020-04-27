"""
Code to generate nxn matrix 
and will print the diagonal 

History : 
			v1.0 - 27/04/2020 - initial version  ( written for MapleLabs input )

"""
import random,sys

def create_matrix(row,colum):
	"""
	returns a matrix based on the inputs
	"""
	col_list=[]
	row_list=[]
	for i in range(row):
		for j in range(colum):
			r_num=random.randint(0,99)
			if r_num<10:r_num+=10
				# print ('single digit r num :',r_num)
				# r_num=str(r_num)*2
				# print ('updated:',r_num)

			col_list.append(r_num)
		row_list.append(col_list)
		col_list=[]
	for each in row_list:
		print (each)
	
	return row_list




def get_diagonal(matrix,dev_mode=False):
	diag_list=[]
	diag_no=1

	for row_index,each_row in enumerate(matrix):
		if dev_mode==True: print ('Row :',row_index ,'each_row :',each_row)
		for col_index,each_col in enumerate(each_row):
			if dev_mode==True: print ('col_index :',col_index ,'each_col :',each_col)
			if col_index+1==diag_no:
				if dev_mode==True: print ('row No  :''diagonals :',each_col)
				diag_list.append(each_col)
				diag_no+=1
				break
	if dev_mode==True: print ('diagonals :',diag_list)
	return diag_list



	



if __name__=="__main__":
	# Test inputs 
	try:
		cross=int(sys.argv[1])
	except:cross=random.randint(1,9)
	row,colum=10,2
	matrix=create_matrix(row,colum)
	# print(matrix)

	if not True:
		matrix=[
				[1,2,3],
				[4,5,6],
				[7,8,9]
				]
		print(matrix)
	if not True:
	
		matrix=[
				[1,2,3,11,22],
				[4,5,6,44,55],
				[7,8,9,77,88],
				[47,48,49,47,48],
				[57,58,59,57,58]
				]
	if not True:
		print('Input matrix:')
		for ind,mat in enumerate(matrix):
			print('Row No:',ind+1,'Values :',mat)
		print ('Diagonals',get_diagonal(matrix,dev_mode=False))
