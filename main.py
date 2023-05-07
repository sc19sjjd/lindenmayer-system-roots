from LSystem import LSystem, ParamLSystem
import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from PIL import ImageGrab, Image
from systemDrawer import setTurtle, drawSystem, drawParamSystem

SEG_LENGTH = 20
ANGLE = 35
THICKNESS_SCALE = 1.75
BASE_THICKNESS = 6.0
WIDTH = 800
HEIGHT = 800
TARGET_BOUNDS = (1024, 1024)

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
MonoTree = ParamLSystem(
    variables="F(l,w) A(l,w) B(l,w) C(l,w) +(c) -(c) T(t)".split(),
    constants={
        'b': 0.9,
        'c': 45,
        'd': 45,
        'e': 0.6,
        'h': 0.707,
        'i': 137.5,
        't': 0.7,
    },
    axiom="A(90,20)",
    rules={
        "A(l,w)": "T(0.8*l*t)F(l,w)([&B(l*e,w*h)]/A(l*b,w*h)",
        "B(l,w)": "T(0.8*l*t)F(l,w)[-(c)$C(l*e,w*h)]C(l*b,w*h)",
        "C(l,w)": "T(0.8*l*t)F(l,w)[+(d)$B(l*e,w*h)]B(l*b,w*h)",
    }
)

# Sympodial tree from same source
SympoTree = ParamLSystem(
    variables="F(l,w) A(l,w) B(l,w) +(c) -(c)".split(),
    constants={
        'b': 0.9,
        'c': 35,
        'd': 35,
        'e': 0.8,
        'h': 0.707,
        'i': 137.5,
        't': 0.7
    },
    axiom="A(90,15)",
    rules={
        "A(l,w)": "F(l,w)[&B(l*b,w*h)]/[B(l*e,w*h)]",
        "B(l,w)": "F(l,w)[+(c)$B(l*b,w*h)][-(d)B(l*e,w*h)]",
    }
)

if __name__ == "__main__":
    #print(CPlant.parsed_variables)
    #print(CPlant.parsed_rules)

    #print(CPlant.parsed_system)
    MonoTree.iterate(12)
    #print(CPlant.parsed_system[4])

    r_turtle = setTurtle(90)
    turtle_screen = turtle.Screen()
    turtle_screen.screensize(WIDTH, HEIGHT)
    drawParamSystem(MonoTree, r_turtle)
    
    turtle_screen.getcanvas().postscript(file="tree.eps")

    pic = Image.open("tree.eps")
    pic.load(scale=10)

    pic = pic.convert("RGBA")

    # Calculate the new size, preserving the aspect ratio
    ratio = min(TARGET_BOUNDS[0] / pic.size[0],
            TARGET_BOUNDS[1] / pic.size[1])
    new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))

    # Resize to fit the target size
    pic = pic.resize(new_size, Image.LANCZOS)

    # Save to PNG
    pic.save("tree.png")

    img = cv2.imread("tree.png")

    white_area = np.sum(img)
    img_inverse = cv2.bitwise_not(img)
    black_area = np.sum(img_inverse)
    print(white_area)
    print(black_area)

    turtle_screen.exitonclick()
    #

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