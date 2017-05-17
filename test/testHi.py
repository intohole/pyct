#coding=utf-8

from pyct import pyct  
import time

if __name__ == "__main__":
    c = pyct.PyCt()
    def p(*argv , **kw):
        print "hi"
    for _ in range(2):
        c.add("* * * * *", p , *[] , **{}) 
    
    _now = time.gmtime(time.time())
    print c.crontabs[0] == (_now.tm_min , _now.tm_hour , _now.tm_mday, _now.tm_mon , _now.tm_wday)
    time.sleep(100)
    print c.crontabs
    print c == (3 , 12 , 13 ,14 ,15)
