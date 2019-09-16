# # u_limit=input()
# u_limit=5
# # # print 
# # # for i in range(1,u_limit):
# # print 
# for i in range(1,u_limit): 
#     #print 'i :',i
    #print (str(i)* i)
#     #print ("b%s"*i,% (num,))
#     print ("%s*%d" %(i,i))
#     #print('{0} and {0}'.format(i,i))
    #"b%s" % (num,)

def u(input):
	for i in range(input):
		exec('a=str(i)*i')	
		print a
    #a=2
    #print(a)
    #print(locals())
    #print(locals()['a'])
input=5
u(input)