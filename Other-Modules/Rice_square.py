total_values =0
temp_list=[]
for i in range(64):
	try:prev_value =temp_list[-1]
	except : prev_value = 1
	total_values=2*prev_value
	temp_list.append(total_values)
	print 'prev_value :',prev_value
	print 'Calculated total_values :',total_values
	print 'temp_list :',temp_list


	
