import sys, time, msvcrt

def readInput(timeout = 5):
    start_time = time.time()
    #sys.stdout.write('%s(%s):'%(caption, default));
    input = ''
    total_seconds=5
    loop_count=1
    print 'time.time():',time.time()
    print 'start_time:',start_time
    print '(time.time() - start_time) :',(time.time() - start_time)
    print 'timeout:',timeout
    sys.stdout.write('Enter the Option deletion :\t')
    while True:
        #sys.stdout.write('Getting deletion option from user {0} seconds remaining :\r'.format(int(total_seconds)-int(loop_count)))
        if msvcrt.kbhit():
            chr = msvcrt.getche()
            if ord(chr) == 13: # enter_key
                    break
            elif ord(chr) >= 32: #space_char
                input += chr
        if len(input) == 0 and (time.time() - start_time) > timeout:
            break
    if len(input) > 0:
        if input.lower()=='--kill':
            print 'All process will be killed '
        elif input.lower()=='--load_all':
            print 'Data will be loaded in all instances !!'
        else:
            print 'Entered option is not available'
# and some examples of usage
ans = readInput(15) 

#ans = readInput('Please enter a number', 10 ) 
