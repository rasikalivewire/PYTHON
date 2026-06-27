import turtle
# screen = turtle.Screen()
# t = turtle.Turtle()
# t.shape("turtle")
# t.color("yellow")
# t.circle(100)
# turtle.done()
# screen = turtle.Screen()
# t = turtle.Turtle()
# t.shape("turtle")
# for _ in range(4):
#     t.forward(100)
#     t.right(90)
# turtle.done()
import turtle

turtle.bgcolor("black")
t = turtle.Turtle()
t.speed(0)  # Fastest speed

colors = ["red", "purple", "blue", "green", "orange", "yellow"]

for x in range(200):
    t.pencolor(colors[x % 6])  # Cycle through colors
    t.width(x / 100 + 1)  # Gradually increase line thickness
    t.forward(x)  # Move forward more each time
    t.left(59)  # Turn slightly off 60 degrees to spiral

turtle.done()