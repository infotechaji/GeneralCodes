import datetime
import time
#from time import sleep

current_time=datetime.datetime.now()
print 'current time :',current_time

timeout=datetime.timedelta(minutes=1)# seconds=1
print 'datetime.timedelta(minutes=5) :',timeout
timeout_expiration = datetime.datetime.now() + timeout
print 'next time out expiration :',timeout_expiration
while True:
	current_time=datetime.datetime.now()
	print 'current time :',current_time
	print ('sleeeping 30 seconds ...............')
	time.sleep(30)
	if current_time>timeout_expiration:
		print 'time crossed :!!'
		timeout=datetime.timedelta(minutes=1)
		timeout_expiration = datetime.datetime.now() + timeout
		print 'next time out expiration :',timeout_expiration
# if elapsed > datetime.timedelta(minutes=1):
#     print "Slept for > 1 minute"

# if elapsed > datetime.timedelta(seconds=1):
#     print "Slept for > 1 second"