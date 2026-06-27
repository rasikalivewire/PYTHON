'''try:
    a=4
    b=0

    print(a/b)
except ZeroDivisionError:
    print("can't divide by zero")
print("bye program end")'''
'''try:
    a=5
    b=0
    print(a/b)
except Exception as e:
    print("error",e)'''
'''age=-5
if age<0:
    raise ValueError("age can't be negative")'''
'''def dob(year):
    if 2020<=year<=2026:
        raise ValueError("you are too young")
    else:
        raise ValueError("you are allowed")
a=int(input("enter your age"))
dob(a)'''
'''class err(Exception):
    pass
try:
    raise err("my error message")
except err as e:
    print(e)'''
'''try:
    a=int(input("enter value"))
    c=10/a
    #print(10/a)
except ZeroDivisionError:
    print("can't divide by zero")
#if a<0:
#   raise ValueError("value can't be negative")
except ValueError as e:
    print("enter a valid number",e)
else:
    print("ok",c)
finally:
    print("finally",c)'''




