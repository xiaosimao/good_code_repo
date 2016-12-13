#!/usr/bin/env python
# coding: utf-8

# singleton

"""
http://ghostfromheaven.iteye.com/blog/1562618
"""
print "------------------method1-----------------------"
# method 1  __new__
"""
实现__new__方法，并将一个类的实例绑定到类变量_instance上，

如果 cls._instance 为None，则说明该类还没有实例化过，实例化该类，然后返回

如果cls._instance 不为None,则直接返回cls._instance

注意从Singleton派生子类的时候，不要重载__new__。

"""


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class MyClass(Singleton):
    a = 1


one = MyClass()
two = MyClass()

print id(one), id(two)  # 可以建立多个实例，但是每个实例都是一样的，ID相同

print "------------------method2-----------------------"

# method 2 共享变量，创建实例时，把所有实例的__dict__指向同一个字典，这样他们就具有相同的属性和方法。
"""
所谓单例就是所有的引用（实例、对象）拥有相同的状态（属性）和行为（方法）
只要保证同一个类的所有实例具有相同的状态（属性）即可
所有实例共享属性的最简单最直接的方法就是 把所有实例的__dict__指向同一个字典

有时候我们并不关心生成的实例是否具有同一id，而只关心其状态和行为方式。
我们可以允许许多个实例被创建，但所有的实例都共享状态和行为方式
"""


class Borg(object):
    """
    将所有实例的__dict__指向同一个字典，这样实例就共享相同的方法和属性。
    对任何实例的名字属性的设置，无论是在__init__中修改还是直接修改，所有的实例都会受到影响。
    不过实例的id是不同的。要保证类实例能共享属性，但不和子类共享，
    注意使用cls._state,而不是Borg._state。
    """
    _state = {}

    def __new__(cls, *args, **kwargs):
        ob = super(Borg, cls).__new__(cls, *args, **kwargs)
        ob.__dict__ = cls._state
        return ob


class MyClass2(Borg):
    a = 1


three = MyClass2()
four = MyClass2()

four.a = 3
print three.a
print id(three), id(four)  # 实例不同，id不同，但是实例之间共享变量

print id(three.__dict__)
print id(four.__dict__)  # 相同

print "------------------method3-----------------------"

# method 3 :本质上是方法1的升级（或者高级版）
"""
使用 __metaclass__ (元类) 的高级python 用法

当你编写一个类的时候，某种机制会使用类名字，基类元组，类字典来创建一个类对象。
新型类中这种机制默认为type，而且这种机制是可编程的，称为元类__metaclass__ 。
"""


class Singleton2(type):
    """
    例子中我们构造了一个Singleton元类，并使用__call__方法使其能够模拟函数的行为。构造类A时，将其元类设为Singleton，那么创建类对象A时，行为发生如下：

    A=Singleton(name,bases,class_dict),A其实为Singleton类的一个实例。

    创建A的实例时，A()=Singleton(name,bases,class_dict)()=Singleton(name,bases,class_dict).__call__()，这样就将A的所有实例都指向了A的属性_instance上，这种方法与方法1其实是相同的。
    """

    def __init__(cls, name, bases, dict):
        super(Singleton2, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton2, cls).__call__(*args, **kw)
        return cls._instance


class MyClass3(object):
    __metaclass__ = Singleton2


one = MyClass3()
two = MyClass3()

two.a = 3
print one.a
# 3
print id(one)
# 31495472
print id(two)
# 31495472
print one == two
# True
print one is two

print "------------------method4-----------------------"

# method 4： 使用装饰器
"""
单例本身并不知道自己是单例的，因为他本身（自己的代码）不是单例的
"""


def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class MyClass4(object):
    a = 1

    def __init__(self, x=0):
        self.x = x


o = MyClass4()
t = MyClass4()

print id(o), id(t)

print "---------------method 5 -------------------"
"""
import 方法
"""


# mysingleton.py
class My_Singleton(object):
    def foo(self):
        pass


my_singleton = My_Singleton

# to use
# from mysingleton import my_singleton
# my_singleton.foo()
