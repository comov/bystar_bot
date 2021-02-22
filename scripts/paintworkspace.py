import turtle
from turtle import *

tim = turtle.Turtle()

color('red', 'yellow')
begin_fill()
while True:
    forward(500)
    left(170)
    if abs(pos()) < 1:
        break
end_fill()
done()