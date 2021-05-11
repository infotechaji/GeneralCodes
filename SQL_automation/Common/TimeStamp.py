"""
Time stamp 
Version  :	v1.3 

History : 
			v1.0 - 01/10/2020 - initial version 
			v1.1 - 01/10/2020 - function is added
			v1.2 - 02/10/2020 - start and end time is added 
			v1.3 - 13/10/2020 - function add_timestamp() is added 

"""
from datetime import datetime
import time
# current date and time
# now = datetime.now()
# print(now)
# print (str(datetime.now()).split('.')[0])
# timestamp = datetime.timestamp(now)
# print("timestamp =", timestamp)

def add_timestamp(input_text):
    return str(get_time_stamp()['common_timestamp'])+'\t'+input_text.strip() + '\n'

def get_time_stamp(input_time = '' , date = False, day = False , month = False , year = False , skip_seconds = False , skip_milli_seconds = True ):
	
	# print(now)
	# print (str(datetime.now()).split('.')[0])
	common_timestamp = str(datetime.now()).split('.')[0]
	# timestamp = datetime.timestamp(now)
	# print("timestamp =", timestamp)	
	return {'common_timestamp':common_timestamp}


# start = time.time()
# print('Started   time : ',start)
# time.sleep(10)
# start = time.time()
# print('completed time : ',end)
# print('Total Time taken in mins : ',(end-start)/60)

if __name__ == '__main__':
	print(get_time_stamp())
	print(get_time_stamp()['common_timestamp'])
	start = time.time()
	print('Started   time : ',start)
	time.sleep(10)
	end = time.time()
	print('completed time : ',end)
	print('Total Time taken in mins : ',(end-start)/60)
	print('Total Time taken in seconds : {:.1f}'.format(end-start))
	print('Total Time taken in Minutes : {:.2f}'.format((end-start)/60))


