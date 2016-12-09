# coding:utf-8
"""
learn more ,never stop
"""
# map
'''每一项都加1,注意其中add函数的参数只有一个，因为每次只取一个
它接收一个函数 f 和一个 list，并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回,map()函数不改变原有的 list，而是返回一个新的 list'''
def add(a):
    return a+1
print map(add,[1,2,3,4,5]) # output:[2, 3, 4, 5, 6]

# reduce
"""reduce()传入的函数 f 必须接收两个参数
用传给reduce中的函数func()（必须是一个二元操作函数）先对集合中的第1，2个数据进行操作，得到的结果再与第三个数据用func()函数运算，最后得到一个结果。
reduce()还可以接收第3个可选参数，作为计算的初始值。"""
def add(a,b):
    return a+b
print reduce(add,[1,2,3,4,5]) # output:15
print reduce(add,[1,2,3,4,5],15) # output:30

# filter (function, iterable)
"""
这个函数的功能就是过滤出iterable 中所有以元素自身作为参数调用f时返回true的元素以列表返回
"""
def which_is_larger_than_4(a):
    return a>4

print filter(which_is_larger_than_4,range(10)) # output:[5, 6, 7, 8, 9]

# zip
"""
zip函数接受任意多个 序列 作为参数，返回一个tuple列表
"""
print zip(range(5), range(1,6)) # [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]

# zip函数的长度的处理方式
print zip(range(5), range(1,7)) # [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
print zip(range(5), range(1,5)) # [(0, 1), (1, 2), (2, 3), (3, 4)]

# 只要一个参数时，zip函数的处理方式
print zip(range(5)) # [(0,), (1,), (2,), (3,), (4,)]

# 没有参数时的处理方式
print zip() # []

"""
一般认为这是一个unzip的过程，它的运行机制是这样的：

在运行zip(*xyz)之前，xyz的值是：[(1, 4, 7), (2, 5, 8), (3, 6, 9)]

在函数的调用中，当使用*xyz时，则意味着要把原来的这个列表转化为tuple，则实际
向函数中的传的参数为 ((1,4,7),(2,5,8),(3,6,9))

那么，zip(*xyz) 等价于 zip((1, 4, 7), (2, 5, 8), (3, 6, 9))

所以，运行结果是：[(1, 2, 3), (4, 5, 6), (7, 8, 9)]
"""
x = [1,2,3]
y = [4,5,6]
z = [7,8,9]

xyz = zip(x,y,z) #[(1, 4, 7), (2, 5, 8), (3, 6, 9)]
print xyz
u = zip(*xyz)
print u # [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

"""
运行机制解释：
[x]*3 = [[1,2,3],[1,2,3],[1,2,3]]
*[x]=*[[1,2,3],[1,2,3],[1,2,3]]
当以这种形式往函数中进行传参的时候，在函数中得到的则为元祖形式：([1,2,3],[1,2,3],[1,2,3])
def test(*args,**kwargs):
    print args,kwargs
test(*[[1,1],[2,2]])   # ([1, 1], [2, 2]) {}
最后 zip函数去出每个序列的相应的每一个元素，得到[(1,1,1),(2,2,2),(3,3,3)]
"""

x = [1, 2, 3]
r = zip(* [x] * 3)
print r  # [(1, 1, 1), (2, 2, 2), (3, 3, 3)]

# zip反转字典
dic = {"a":1,"b":2,"c":3,"d":4}
print dict(zip(dic.values(),dic.keys())) # {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

# 与序列有关的内建函数有：sorted()、reversed()、enumerate()、zip()
# enumerate
for index,value in enumerate([1,2,3]):
    print index,value  # 0 1
                       # 1 2
                       # 2 3

#sorted(iterable,cmp,key,reverse)
# cmp  用户比较的函数，比较什么由key决定
# key  用列表元素的某个属性或函数作为排序的关键字
# reverse  排序规则，默认false，则升序

# 根据可迭代对象的长度来进行升序排序
L = [{1:5,3:4},{1:3,6:3},{1:1,2:4,5:6},{1:9}]
def f(x):
    return len(x)
print sorted(L,key=f) # [{1: 9}, {1: 5, 3: 4}, {1: 3, 6: 3}, {1: 1, 2: 4, 5: 6}]
print sorted(L,key=f,reverse=True) # [{1: 1, 2: 4, 5: 6}, {1: 5, 3: 4}, {1: 3, 6: 3}, {1: 9}]

# 更广泛的使用情况是用复杂对象的某些值来对复杂对象的序列排序
student_tuples = [
        ('john', 'A', 15),
        ('jane', 'B', 12),
        ('dave', 'B', 10),
]
# 根据学生的年龄来排序
print sorted(student_tuples,key=lambda x:x[2]) # [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]


#apply 
"""
apply(func[,args[,kwargs]]) 函数用于当函数的参数以及存在于一个元祖或字典中，间接的
调用函数，其中  args 是一个元祖，其中包含要提供给函数的按位置传递的参数

"""
tup=('a','b')  
dic={'A':'AB','B':'Ab'}  
  
def ab(a,b,A,B):  
    print a,b,A,B  
  
def main(*d,**k):  
    print d,k  
  

#使用apply函数  
apply(main,(2,3))  # only tuple,no dict     output:(2, 3) {}
apply(main,tup,dic)  # tuple, dict     output:('a', 'b') {'A': 'AB', 'B': 'Ab'}
apply(main,(),{'a':'5','b':'6'})  # tuple has no value  output:() {'a': '5', 'b': '6'}

#普通的函数传参  
main(2,3,a=4,b=5)  
ab(*tup,**dic)  

#实质上，以下两种写法效果相同
apply(main,tup,dic)  
main(*tup,**dic) # note：当使用**时，参数可以直接传入字典，而不用写成a=1,b=2的形式
                 #      ：当使用*时，tup传入的列表或原组都将变为元祖
                 # eg：
                 
def test(*args,**kwargs):
    print args,kwargs
test_list = [1,2]
test_tuple = (1,2)
test_dict = {"a":1,"b":2}

# notice the difference
test(*test_list) # output:(1,2) {}
test(test_list)  # output:([1,2]) {}

test(*test_tuple) # output:(1, 2) {}
test(test_tuple) #  output:((1, 2),) {}
test(1,2)   # output:(1, 2) {}
test(**test_dict) # output:() {'a': 1, 'b': 2}
test(a=1,b=2) # output:() {'a': 1, 'b': 2}
test(test_dict) # output:({'a': 1, 'b': 2},) {}

test(*test_list,**test_dict) # (1, 2) {'a': 1, 'b': 2}

