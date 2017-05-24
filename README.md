

pyct
==============



+ 简单的python crontab服务
+ 调用接口简单
+ 需要安装依赖包：[b2](https://github.com/intohole/b2) 

```python
c = PyCt()
def p(*argv , **kw):
	print "hi"
c.add("* * * * *", p , *[] , **{}) #添加执行命令 ， 现在只支持python函数 , 函数形式类似于这种 def xxx(*argv , **kw):  
time.sleep(100) # 或者用c.join()
```


后续计划
------
+ 分布式crontab系统
+ 支持复杂简单定时任务；支持队列
