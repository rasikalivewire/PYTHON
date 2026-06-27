# a=[1,2,3]
# b=a
# b.append(5)
# print(a)
# #iterator
# c=["red","green","blue"]
# # for i in c:
# #     print(i)
# i=iter(c)
# print(next(i))
# print(next(i))
# print(i.__next__())
#generator
'''def my_generator():
    yield 1
    yield 2
    yield 3
g=my_generator()
print(next(g))
print(next(g))
print(g.__next__())'''
'''def my_generator():
    for i in range(1,10):
        yield i
for g in my_generator():
         print(g)'''
'''def my_gen():
    a=10
    b=20
    return a
    return b
    return 5
c=my_gen()
print(c)

def my_generator():
    name="rasi"
    age=25
    yield name
    yield age
    yield place
d=my_generator()
print(d)
print(next(d))
print(next(d))
print(next(d))'''
'''def my_mul(n):
    def mul(x):
        #return x*n
    return mul
d=my_mul(5)
t=my_mul(3)
print(d(2))
print(t(2))
def greet():
    print("Hello World")
    def message():
        print("Hello World2")
    return message
m=greet()
m()'''
# def my_decorator(func):
#     def wrapper():
#         print("before arguments")
#         func()
#         print("after arguments")
#     return wrapper
# @my_decorator
# def greet():
#     print("Hello World")
# greet()

# def my_decorator1(func):
#     def wrapper(n):
#         print("Hello " + n)
#         func(n)
#         print("hi buddy")
#     return wrapper
# @my_decorator1
# def greet(n):
#     print("good morning",n)
# greet("rasi")
def outer():
    message="live wire"
    def inner():
        print(message)
    return inner
o=outer()
o()


