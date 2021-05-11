import sys
sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')

# sample piece of code
# import pyttsx3

# engine = pyttsx3.init()
# engine.say("I will speak this text haha ")
# engine.runAndWait()


import pyttsx3
ENGINE = pyttsx3.init() # object creation
ENGINE.setProperty('voice', ENGINE.getProperty('voices')[1].id)   #changing index, changes voices. 1 for female
ENGINE.setProperty('rate', 150)
# engine.say('Thanks Mariyappan and lakshmi !! ')

def speak_words(input_text, engine = ENGINE):
    try:
        engine.say(input_text)
        engine.runAndWait()
        return  True
    except Exception as e:
        print('Error while speaking the text :',e)
    return False


# """ RATE"""
# rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
# engine.setProperty('rate', 125)     # setting up new voice rate
#
#
# """VOLUME"""
# volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# print (volume)                          #printing current volume level
# engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
#
# """VOICE"""
# voices = engine.getProperty('voices')       #getting details of current voice
# # #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
# engine.getProperty('voices')
# engine.setProperty('voice', engine.getProperty('voices')[1].id)   #changing index, changes voices. 1 for female
#
# engine.say("Hello World!")
# engine.say('My current speaking rate is ' + str(rate))
# engine.say('Ellam avan seyal ')
# engine.say('Thanks Mariyappan and lakshmi !! ')
# engine.runAndWait()
# engine.stop()

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
# engine.save_to_file('Hello World', 'test.mp3')
# engine.runAndWait()
# for index,temp_voice in enumerate(voices):
#     print('Processing voice :',index)
#     engine.setProperty('voice', voices[index].id)   #changing index, changes voices. 1 for female
#     engine.say("Merge requests are raised !!")
#     engine.runAndWait()


if __name__ == '__main__':
    input_text = 'TEsting this '
    input_text1 = 'Commit is done for EPE-12345'
    input_text2 = 'Merge request raised for EPE-12345'
    input_text3 = 'Error while raising the merge requests '+str('Chrome extension element is not found !')
    input_text4 = 'Total time taken : 4 minutes'
    test = [input_text1,input_text2,input_text3,input_text4]
    for i in test:
        speak_words(i)