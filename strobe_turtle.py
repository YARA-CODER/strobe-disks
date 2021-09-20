import turtle
from math import pi
tim = turtle.Turtle()
tim.color('black')
def circle(r, precision=360):
    circ = 2 * pi * r
    step_len = circ / precision
    step_rot = 360 / precision
    for step in range(precision):
        tim.fd(step_len)
        tim.left(step_rot)

def drawDisc():
    tim.penup()
    tim.left(90)
    tim.bk(380)
    tim.right(90)
    tim.pd()
    circle(380)
    tim.left(90)
    tim.pu()
    tim.fd(380)

def drawMark(x=6, y=20):
    tim.pd()
    tim.begin_fill()
    tim.fd(y)
    tim.right(90)
    tim.fd(x)
    tim.right(90)
    tim.fd(y)
    tim.right(90)
    tim.fd(x)
    tim.right(90)
    tim.end_fill()


def drawAllMarks(number_of_marks, r):
    deg = 0
    step = 360/number_of_marks
    for m in range(number_of_marks):
        tim.pu()
        tim.right(deg)
        tim.fd(r)
        tim.pd()
        drawMark()
        tim.pu()
        tim.bk(r)
        tim.left(deg)

        deg += step
    pass

drawDisc()
drawAllMarks(180, 340)
turtle.mainloop()
