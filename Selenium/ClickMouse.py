import pyautogui,time,sys
#raw_input('Press Enter to make the mouse clickable ')
clicked_count=0
limit=275
while True:
	clicked_count+=1
	tublee=pyautogui.position()
	time.sleep(1)
	pyautogui.click(tublee[0],tublee[0]) 
	time.sleep(1)
	sys.stdout.write('clicked_count:'+str(clicked_count)+' \r')
	if clicked_count>=limit:
		print 'clicked_count :',clicked_count
		break
