import time, threading
from Queue import Queue
from opp import updateUnit

REQ_NONE = 1
REQ_UPDATE_UNIT = 2
REQ_UPDATE_ALL = 3
REQ_EXPORT_ALL = 4

reqs = Queue()

def work():
    print "START WORK THREAD"
    while True:
        (code, obj1, obj2, obj3) = reqs.get()
        print "REQ:", code, obj1, obj2, obj3
        if code == REQ_UPDATE_UNIT:
            print "Start updateUnit", obj1.id
            updateUnit(obj1.id, obj2, eqlist=obj3)
            print "End updateUnit", obj1.id
