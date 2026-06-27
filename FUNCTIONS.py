# def mobile(brand,price):
#     print(brand)
#     print(price)
# mobile("apple",70000)
# #default arguments
# def mobile(brand="oppo"):
#     print(brand)
# mobile("apple")

#keyword arguments
# def mobile(brand,price,processor):
#     print("your brand is",brand)
#     print("your price is",price)
#     print("your procesor is",processor)
# mobile(price=70000,brand="apple",processor="snapdragon")
# def mobile(**details):
#     print(details)
# mobile(price=70000,brand="apple",processor="snapdragon",camera="44 mega pixel",display="hdr")

#return function
# def add(a,b):
#     return a+b
# def subtract(a,b):
#     return a-b
# def multiply(a,b):
#     return a*b
# a=add(5,6)
# b=subtract(5,6)
# c=multiply(5,6)
# print(a)
# print(b)

#lambda function
#
# cube=lambda c:c*c*c
# print(cube(5))
# def mohan(a):
#     print(a)
# mohan("hi mohan")
a=[1,2,3,4,5]
b=list(map(lambda x:x+2,a))
print(b)
a=[1,2,3,4,5,6,7]
b=list(filter(lambda x:x%2!=0,a))
print(b)












