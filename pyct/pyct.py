#coding=utf-8



"""python版本的crontab实现思路
"""

import threading 
import time
from b2 import thread2 
import re





class CTCondition(object):

    

    def __init__(self, condition , ):
        self.condition_type = self._get_condition_type(condition)
        self.judge = None # ct时间判断方法
        self.condition_string = condition

    def _get_condition_type(self.condition):
        pass


    def return_true(object):
        return True

    def every(self , time_value , value):
        if value % time_value == 0:
            return True 
        return False

    def time_range(self , start_time , end_time , value):
        if value >= start_time and end_time >= value:
            return False
        return False
   
   def time_range_every(self , start_time , end_time , time_diff , value):
       if self.time_range(start_time , end_time , value) is True:
           return self.every(time_diff , value)
       return False
        
class CTItem(object):



    def __init__(self , condition ):
        self.conditions = self.parse(condition)

    def __eq__(self , obj):
        if isinstance(obj , int):
            for condition in self.conditions:
                if condition.judge(obj) is True:
                    return True
            return False
    def __ne__(self , obj):
        return not self.__eq__(obj)

    def parse(self , condition):
        params = condition.split(",")
        return [CTCondition(param) for param in params]
            
class TimeObject(object):
    """ct 字符串保存结构；方便后面去判断，隐藏解析
        * * * * *
        - - - - -
        | | | | |
        | | | | |___ week 
        | | | |_____ month 
        | | |_______ day 
        | |_________ hour 
        |___________ minute 
    """


    def __init__(self , ct_string = None , week = None , month = None , day = None , hour = None , minute = None ):
        if ct_string is None and (week is None or month is None or day is None or hour is None or minute is None ):
            raise ValueError
        if ct_string is not None:
            self.week , self.month , self.day , self.hour , self.minute = self.parser(ct_string)
        else:
            self.week , self.month , self.day , self.hour , self.minute = week , month , day , hour , minute 

    def parser(self , ct_string):
        params = ct_string.split()
        if len(params) != 5:
            raise ValueError
        week , month , day , hour , minute = params
        return week , month , day , hour , minute 

    def __eq__(self , obj):
        if obj and isinstance(obj,(list , tuple)):
            if len(obj) == 5:
                if self.week != obj[4]:
                    return False
                if self.day != obj[3]:
                    return False
                if self.hour != obj[2]:
                    return False
                if self.minute != obj[1]:
                    return False
                if self.minute != obj[0]:
                    return False
            return True
        return False


    
class Ticker(threading.Thread):


    def __init__(self , pool_size = 100):
        super(Ticker , self).__init__()
        self._run_flag = True
        self.crontabs = []
        self.workers = thread2.ThreadPool(pool_size) 
        
    def add(self , ctstring , command , *argv , **kw ):
        pass 

    def run(self):

        while self._run_flag:
            time.sleep(1)




if __name__ == "__main__":


    Ticker().start()
