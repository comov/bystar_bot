import turtle
tim = turtle.Turtle()
tim.color("red", "blue")  # Blue is the fill color
tim.speed(1)
tim.width(5)

tim.begin_fill()
for x in range(4):  # This will draw a square filled in
    tim.forward(100)
    tim.right(90)

tim.end_fill()