import weakref
 
class TestClass(object):
    def check(self):
        print ("object is alive!")
    def __del__(self):
        print ("object deleted")
 
a = TestClass()
 
b = weakref.proxy(a)
 
print a.check()

 
#del a
#object deleted
 
print b.check()
