#coding=utf-8



"""python版本的crontab实现思路
"""

import threading 
import time
from b2 import thread2 
from b2 import exceptions2
import re
import collections


_CONDITION_TYPES =[
                    ("ALL", "^\\*$"),
                    ("TIME_RANGE" , "^(\d+)-(\d+)$"),
                    ("EVERY" , "^\\*/(\d+)$"),
                    ("TIME_RANGE_EVERY" , "^(\d+)-(\d+)/(\d+)$"),
                    ("NUM" , "^(\d+)$")
                   ]
_CONDITION_TYPE_PATTERN = re.compile(ur"|".join(ur"(?P<%s>%s)" % (_type , _pattern) for _type , _pattern in _CONDITION_TYPES ))
_CONDITION_TYPE_PATTERNS = collections.OrderedDict([(_type , re.compile(_pattern).match) for _type , _pattern in _CONDITION_TYPES ])



class CTCondition(object):
    """crontab条件判断类，每个条件解析成对应判断公式与数值
        test:
            >>> c = CTCondition("12-23/3")
            >>> c.judge(15) == True
            >>> c.judge(9) == False
    """
    

    def __init__(self, condition , time_type ):
        self.time_type = time_type 
        self.condition_string = condition
        self.condition_type , group_tuples = self._get_condition_type(condition)
        self._init_params(self.condition_type , group_tuples)
        self._check_params()

    def _get_condition_type(self , condition):
        for _type , _pattern in _CONDITION_TYPE_PATTERNS.items():
            match = _pattern(condition)
            if match:
                return _type , match.groups()
        raise Exception("{0} is format vaild !".format(condition)) 

    def _init_params(self , condition_type , group_tuples):
        self._start_time = None 
        self._end_time = None 
        self._every = None 
        self._num = None 
        self.judge = None
        group_tuples = [ int(value) if value != "*" else value for value in group_tuples ]
        if self.condition_type == "ALL" or self.condition_type == "NUM":
            self._num = "*"
            if self.condition_type == "NUM":
                self._num = group_tuples[0]
            self.judge = self.equal
        elif self.condition_type == "EVERY":
            self.judge = self.every 
            self._every = group_tuples[0]
        elif self.condition_type == "TIME_RANGE":
            self.judge = self.time_range 
            self._start_time , self._end_time = group_tuples 
        elif self.condition_type == "TIME_RANGE_EVERY":
            self.judge = self.time_range_every
            self._start_time , self._end_time , self._every = group_tuples
        else:
            raise NotImplmetionError 
    
    def _check_num_range(self , value):
        if value is None:
            return True 
        _value_range = None  
        if self.time_type == "hour":
            _value_range = 23 
        elif self.time_range == "minute":
            _value_range = 59
        elif self.time_type == "day":
            _value_range = 31 
        elif self.time_type == "month":
            _value_range = 12 
        elif self.time_type == "week":
            _value_range = 6
        if value != "*" and value > _value_range:
            raise ValueError("crontab time is valid , value range not right , please check %s" % self.condition_string)

    def _check_params(self):
        if self._start_time and self._end_time:
            if self._start_time >=self._end_time:
                raise ValueError("crontab time is valid ! %s" % self.condition_string)
        self._check_num_range(self._start_time) 
        self._check_num_range(self._end_time)
        self._check_num_range(self._num)
        self._check_num_range(self._every)

    def equal(self , value):
        if self._num == "*" or self._num == value:
            return True 
        return False

    def every(self ,value):
        """实现 crontab中 */3 判断语句
            params:
                time_value                      crontab每time_value时间
                value                           传入的时间数字 
            return 
                True                            符合ct条件
                False                           不符合该条件
            raise 
                None 
        """
        if value % self._every == 0:
            return True 
        return False

    def time_range(self , value):
        if value >= self._start_time and self._end_time >= value:
            return True 
        return False
   
    def time_range_every(self , value):
        """实现 crontab中 18-23/3 判断语句,如果满足在18到23之间
            params:
                start_time                      判断时间的开始时间
                end_time                        判断时间的结束时间
                time_diff                       crontab每time_value时间
                value                           时间数字，整形
            return 
                True                            符合条件
                False                           不符合条件判断
            raise
                None 
        """
        if self.time_range(value) is True:
            return self.every(value)
        return False
    
    def __str__(self):
        return "start_time:{start_time} end_time:{end_time} every:{every} num:{num}".format(start_time = self._start_time , end_time = self._end_time , every = self._every , num = self._num )

class CTItem(object):
    """crontab time pattern item
    """

    TIME_TYPE = ["minute" , "hour" , "day" , "month" , "week"]

    def __init__(self , condition ):
        """parse time crontab string 2 function
            param:condition:basestring:crontab string
        """
        self.conditions = self.parse(condition)
        self.condition_string = condition

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
        return [CTCondition(param , self.TIME_TYPE[index]) for index , param in enumerate(params)]
            
class CrontabObject(object):

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


    def __init__(self , command , ct_string = None   , week = None , month = None , day = None , hour = None , minute = None ):
        self.command = command 
        if ct_string is None and (week is None or month is None or day is None or hour is None or minute is None ):
            raise ValueError
        if ct_string is not None:
            self.week , self.month , self.day , self.hour , self.minute = self.parser(ct_string)
        else:
            self.week , self.month , self.day , self.hour , self.minute = CTItem(week) , CTItem(month) , CTItem(day) , CTItem(hour) , CTItem(minute) 

    def parser(self , ct_string):
        params = ct_string.split()
        if len(params) != 5:
            raise ValueError(params)
        week , month , day , hour , minute = [ CTItem(param) for param in params ]
        return week , month , day , hour , minute 

    def __eq__(self , obj):
        if obj and isinstance(obj,(list , tuple)):
            if len(obj) == 5:
                if self.week != obj[4]:
                    return False
                if self.month != obj[3]:
                    return False
                if self.day != obj[2]:
                    return False
                if self.hour != obj[1]:
                    return False
                if self.minute != obj[0]:
                    return False
            return True
        return False
    
    
class PyCt(threading.Thread):


    def __init__(self , pool_size = 100):
        super(PyCt , self).__init__()
        self._run_flag = True
        self.crontabs = []
        self.workers = thread2.ThreadPool(pool_size) 
        self.setDaemon(True)
        self.start()
        self.workers.start()
        
    def add(self , ctstring , command , *argv , **kw ):
        self.crontabs.append(CrontabObject(thread2.Command(command , *argv , **kw) , ctstring))

    def run(self):
        while time.gmtime(time.time()).tm_sec <=1:
            time.sleep(0.1)
        last_minute = time.gmtime(time.time()).tm_min 
        while self._run_flag:
            time.sleep(1)
            _now = time.gmtime(time.time())
            if ( _now.tm_min - last_minute) <1:
                continue 
            last_minute = _now.tm_min 
            for ct in self.crontabs:
                if ct == (_now.tm_min , _now.tm_hour , _now.tm_mday, _now.tm_mon , _now.tm_wday):
                    self.workers.insert(ct.command)
