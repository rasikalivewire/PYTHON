#1 simple hello world
'''from tkinter import *
root=Tk()
label=Label(root,text="Hello World")
label.pack()
#label.grid(row=0,column=0)
root.mainloop()
#2 hello world with rows and coloumns
from tkinter import *
root=Tk()
label=Label(root,text="Hello World")
#label.pack()
label.grid(row=0,column=0)
label1=Label(root,text="Hello  rasika")
label1.grid(row=0,column=1)

root.mainloop()'''


#3 buttons
'''from tkinter import *
root=Tk()
def greeting():
    label=Label(root,text=" hi rasika click this button")
    label.pack()

button=Button(root,text="hey Click me",command=greeting,fg="white",bg="black")#fg-foreground colour,bg-background colour
button.pack()
#n=input("enter your name")

root.mainloop()

'''#4 buttons disable
from tkinter import *
root=Tk()
def greeting():
    label=Label(root,text=" hi rasika click this button")
    label.pack()

button=Button(root,text="hey Click me",command=greeting,state=DISABLED,)
button.pack()


root.mainloop()



'''#5 getting input from user
from tkinter import *
root=Tk()
input=Entry(root,width=50,bd=200,bg="red")
input.pack()
def greeting():
    label=Label(root,text=input.get() + "hi rasika click this button")
    label.pack()
    label.pack()

button=Button(root,text="hey Click me",command=greeting)
button.pack()


root.mainloop()'''