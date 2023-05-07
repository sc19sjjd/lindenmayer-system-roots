from LSystem import LSystem, ParamLSystem
import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from PIL import ImageGrab, Image

SEG_LENGTH = 20
ANGLE = 35
THICKNESS_SCALE = 1.75
BASE_THICKNESS = 6.0
WIDTH = 800
HEIGHT = 800
TARGET_BOUNDS = (1024, 1024)

def setTurtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    turtle.tracer(0, 0)
    r_turtle.hideturtle()
    r_turtle.screen.title("L-System Derivation")
    r_turtle.pensize(BASE_THICKNESS)
    r_turtle.pu()
    r_turtle.setposition(0, 350)
    r_turtle.speed("fastest")  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    return r_turtle


def drawSystem(system: LSystem, r_turtle: Turtle):
    stack = []
    system_len = len(system.system)
    curr_width = BASE_THICKNESS
    for symbol in system.system[system_len-1]:
        r_turtle.pd()
        if symbol == "F":
            r_turtle.forward(SEG_LENGTH)
        elif symbol == "f":
            r_turtle.pu()
            r_turtle.forward(SEG_LENGTH)
        elif symbol == "+":
            r_turtle.right(ANGLE)
        elif symbol == "-":
            r_turtle.left(ANGLE)
        elif symbol == "!":
            width = width * THICKNESS_SCALE
            r_turtle.pensize(width)
        elif symbol == "?":
            width = width / THICKNESS_SCALE
            r_turtle.pensize(width) 
        elif symbol == "[":
            stack.append((
                r_turtle.position(), 
                r_turtle.heading(),
                curr_width,
            ))
            curr_width = curr_width / THICKNESS_SCALE
        elif symbol == "]":
            r_turtle.pu()
            position, heading, curr_width = stack.pop()
            r_turtle.goto(position)
            r_turtle.setheading(heading)
            r_turtle.pensize(curr_width)

    turtle.update()


Plant = LSystem(
    variables="F".split(),
    constants="[ ] + - ! ?".split(),
    axiom="F",
    rules={
        "F": "F[+F]F[-F]F"
    }
)

# monopodial tree from:
# https://www.houdinikitchen.net/wp-content/uploads/2019/12/L-systems.pdf
CPlant = ParamLSystem(
    variables="F(l,w) A(l,w) B(l,w) C(l,w)".split(),
    constants={
        'b': 0.9,
        'c': 45,
        'd': 45,
        'e': 0.6,
        'h': 0.707,
        'i': 137.5,
    },
    axiom="A(1,10)",
    rules={
        "A(l,w)": "F(l,w)[&B(l*e,w*h)]/A(l*b,w*h)",
        "B(l,w)": "F(l,w)[-$C(l*e,w*h)]C(l*b,w*h)",
        "C(l,w)": "F(l,w)[+$B(l*e,w*h)]B(l*b,w*h)",
    }
)

if __name__ == "__main__":
    print(CPlant.parsed_variables)
    print(CPlant.parsed_rules)

    print(CPlant.parsed_system)
    CPlant.iterate()
    print(CPlant.parsed_system)

    """
    for i in range(3):
        Plant.iterate()
        #print(Plant)

    r_turtle = setTurtle(270)
    turtle_screen = turtle.Screen()
    turtle_screen.screensize(WIDTH, HEIGHT)
    drawSystem(Plant, r_turtle)
    
    turtle_screen.getcanvas().postscript(file="plant.eps")
    
    #turtle_screen.exitonclick()

    pic = Image.open("plant.eps")
    pic.load(scale=10)

    pic = pic.convert("RGBA")

    # Calculate the new size, preserving the aspect ratio
    ratio = min(TARGET_BOUNDS[0] / pic.size[0],
            TARGET_BOUNDS[1] / pic.size[1])
    new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))

    # Resize to fit the target size
    pic = pic.resize(new_size, Image.LANCZOS)

    # Save to PNG
    pic.save("plant.png")

    img = cv2.imread("plant.png")

    white_area = np.sum(img)
    img_inverse = cv2.bitwise_not(img)
    black_area = np.sum(img_inverse)
    print(white_area)
    print(black_area) """