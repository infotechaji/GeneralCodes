from pygame import mixer  # Load the popular external library
import sys,time,os
sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')
from Text_to_speech import * 


def alert_for_user_creation():
	mixer.init()

	mixer.music.load(sys.argv[1])
	
	for i in range(5):
		mixer.music.play()
		time.sleep(2)
		speak_words('New user is created !')

def get_total_folders(input_dir='C:\\Users'):
	files = 0
	folders = 0
	for _, dirnames, filenames in os.walk(input_dir):
		files += len(filenames)
		folders += len(dirnames)
		break
	return {
	  	'total_folders':folders
	  	,'folder_names':dirnames
	  	,'file_names':filenames
	  	,'total_files':files
	  }

if __name__ =='__main__':
	user_directory ='C:\\Users'
	# print (get_total_folders(user_directory)['total_folders'])
	# alert_for_user_creation()
	# 
	while True:
		no_of_folders = 5
		if no_of_folders != get_total_folders(user_directory)['total_folders']:
			alert_for_user_creation()
		time.sleep(20)
	

