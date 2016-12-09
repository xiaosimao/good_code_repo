# usr/bin/env python
# coding:utf-8
import time
import functools

def log(text):
    # 判断此时的text是函数，还是文本
    if callable(text):
        @functools.wraps(text)
        def outer(*args,**kw):
            print 'i am callable'
            return text(*args,**kw)
        return outer
    
    else:
        # 此时为文本
        def outer(func):
            @functools.wraps(func)
            def inner(*args,**kw):
                print text
                return func(*args,**kw)
            return inner
        return outer
        
# 函数        
@log
def time_now():
    return time.ctime()        

@log('hello')
def time_now2():
    return time.ctime()

print time_now()
print time_now2()





