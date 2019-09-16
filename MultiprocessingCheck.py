from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    #print('parent process:', os.getpid())
    #print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    #info('main line')
    for i in ['test1','test2','test3']:
        p = Process(target=f, args=(i,))
        p.start()
        p.join()
        print 'i:',os.getpid()
