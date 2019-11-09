#PGM 1:
# #!/usr/bin/env python2
# import sys, select, time
# while True:
#     print "Looping until ENTER pressed"
#     time.sleep(1)
#     i,o,e = select.select([sys.stdin],[],[],0.0001)
#     if i == [sys.stdin]: break
# print "Goodbye"

# import sys ,time

# text = ""
# count=0
# while 1:
# 	count+=1
# 	c = sys.stdin.read(2)
# 	text = text + c
# 	if c == '\n':
# 		break	
# 	print count,text



# try:
# 	input = raw_input
# 	print 'input :',input
# except NameError as n:
# 	print 'Name error : ',n
# 	pass



# def prompt(message, errormessage, isvalid):
#     """Prompt for input given a message and return that value after verifying the input.

#     Keyword arguments:
#     message -- the message to display when asking the user for the value
#     errormessage -- the message to display when the value fails validation
#     isvalid -- a function that returns True if the value given by the user is valid
#     """
#     res = None
#     while res is None:
#         res = input(str(message)+': ')
#         if not isvalid(res):
#             print str(errormessage)
#             res = None
import sys, time, msvcrt

def readInput( caption, default, timeout = 5):
    start_time = time.time()
    sys.stdout.write('%s(%s):'%(caption, default));
    input = ''
    while True:
        if msvcrt.kbhit():
            chr = msvcrt.getche()
            if ord(chr) == 13: # enter_key
                break
            elif ord(chr) >= 32: #space_char
                input += chr
        if len(input) == 0 and (time.time() - start_time) > timeout:
            break

    print ''  # needed to move to next line
    if len(input) > 0:
        return input
    else:
        return default

# and some examples of usage
ans = readInput('Please type a name', 'john') 
print 'The name is %s' % ans
ans = readInput('Please enter a number', 10 ) 
print 'The number is %s' % ans 
