import threading
import time
from threading import Thread
import time

def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop(), name='LoopThread')
t2 = threading.Thread(target=loop(), name='LoopThread2')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)

exitFlag = 0
class myThread(threading.THread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("Begin thread: {}".format(threading.current_thread().name))
        print_t