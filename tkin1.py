#1pack
'''from tkinter import *
root = Tk()
label = Label(root, text="Hello students").pack(side=TOP)
label = Label(root, text="Hello rasi").pack(side=LEFT)
label = Label(root, text="Hello alwin").pack(side=RIGHT)
label=Label(root,text="alwin mca").pack(side=BOTTOM)
root.mainloop()'''
#2grid
'''from tkinter import *

root = Tk()

Label(root, text="Name").grid(row=0, column=0)
Label(root, text="Age").grid(row=1, column=2)
Label(root,text="Gender").grid(row=2, column=3)

root.mainloop()'''

'''from tkinter import *
root=Tk()
def hello():
    label=Label(root,text="hello alwin anna")
    label.pack()
button = Button(root,text="hello click me",command=hello,fg="red",bg="blue")
button.pack()
root.mainloop()'''
#5
'''from tkinter import *
root=Tk()
entry = Entry(root,bd=200,relief=GROOVE,fg="red",bg="black")
entry.pack()
def hello():
    label=Label(root,text=entry.get()+"students")
    label.pack()
button=Button(root,text="click me",command=hello,fg="red",bg="blue").pack()
root.mainloop()'''
'''from tkinter import *
import tkinter

root = Tk()

B1 = Button(root, text ="FLAT", relief=FLAT ,bd=20)
B2 = Button(root, text ="RAISED", relief=RAISED,bd=100 )
B3 = Button(root, text ="SUNKEN", relief=SUNKEN,bd=100)
B4 = Button(root, text ="GROOVE", relief=GROOVE,bd=50 )
B5 = Button(root, text ="RIDGE", relief=RIDGE,bd=200 )

B1.pack()
B2.pack()
B3.pack()
B4.pack()
B5.pack(side=RIGHT)
root.mainloop()'''
