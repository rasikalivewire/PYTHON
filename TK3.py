from tkinter import *

root = Tk()

canvas = Canvas(root, width=400, height=300, bg="white")
canvas.pack()

def draw(event):
    x, y = event.x, event.y
    canvas.create_oval(x, y, x+3, y+3, fill="black")

canvas.bind("<B1-Motion>", draw)

root.mainloop()