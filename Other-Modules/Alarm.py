import datetime,time
from pygame import mixer # Load the required library
import sys,os

def play_mp3(my_mp3):
	mixer.init()
	print 'mp3 initiated '
	try:
		mixer.music.load(my_mp3)
		print 'mp3 loaded '
		mixer.music.play()
		print 'mp3 played'
	except Exception as e:
		print 'Exception in playing mp3 file :',e
		return False

if __name__=="__main__":
	if True:
		mp3_path=sys.argv[1]
		play_mp3(mp3_path)
	elif not True:
		hour=11
		minute=2
		while True:
			now = datetime.datetime.now()
			#print i,now
			i+=1
			#print now.hour
			#print now.strftime("%Y-%m-%d %H:%M")
			print now.strftime("%H:%M")
			#time.sleep(1)
			if hour==now.hour and minute==now.minute:
				print 'raise_alarm()!!!!!!'
		

