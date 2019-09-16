import sys

def get_entered_arguments():
	count=0
	command='python'
	for i in sys.argv:
		count+=1
		print 'count :',count,i
		command=command+' '+str(i)
	return command
if __name__=="__main__":
	print get_entered_arguments()