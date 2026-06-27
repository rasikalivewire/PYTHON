from tkinter import *
from time import strftime

root = Tk()
root.title("Digital Clock")

def update():
    current = strftime("%H:%M:%S")
    lbl.config(text=current)
    lbl.after(1000, update)

lbl = Label(root, font=("Arial", 40))
lbl.pack()

update()
root.mainloop()