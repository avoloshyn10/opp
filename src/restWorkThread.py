import time, threading
from Queue import Queue
from opp import updateUnit

REQ_NONE = 1
REQ_UPDATE_UNIT = 2
REQ_UPDATE_ALL = 3
REQ_EXPORT_ALL = 4

reqs = Queue()
in_update_all = False

def work(eq, rdfdb):
    print "START WORK THREAD"
    while True:
        if reqs.empty():
            dummy = 1
        else:
            func, args, kwargs = reqs.get()
            print "REQ:", func.__name__
            func(*args, **kwargs)
            print "END REQ:", func.__name__
