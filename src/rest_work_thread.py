import time, threading
from Queue import Queue

reqs = Queue()

def work():
    print "START DOING NOTHING"
    while True:
        i = reqs.get()
        print "REQ:", i
