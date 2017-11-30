#coding=utf-8

from pyct import pyct  
from pyct.pyct import cron
import time

if __name__ == "__main__":
    @cron("* * * * *",*[],**{})
    def p(*argv,**kw):
        print "hi"
    time.sleep(10)
