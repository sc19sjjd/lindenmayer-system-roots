from LindenmayerSystem import LSystem
import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from PIL import ImageGrab

WIDTH = 800
HEIGHT = 800
IMG_FILENAME = "plant.png"


def setTurtle(alpha_zero, screen):
    t = turtle.RawTurtle(screen.getcanvas())  # recursive turtle
    t.pu()
    t.setposition(0, 350)
    t.speed("fastest")  # adjust as needed (0 = fastest)
    t.setheading(alpha_zero)  # initial heading
    return t


def drawSystem(system: LSystem, canvas):
    turtle_screen = turtle.TurtleScreen(canvas)
    t = setTurtle(270, turtle_screen)
    t.hideturtle()
    turtle.tracer(0, 0)

    stack = []
    system_len = len(system.system)
    for symbol in system.system[system_len-1]:
        t.pd()
        if symbol == "F":
            t.forward(20)
        elif symbol == "f":
            t.pu()
            t.forward(20)
        elif symbol == "+":
            t.right(20)
        elif symbol == "-":
            t.left(20)
        elif symbol == "[":
            stack.append((t.position(), t.heading()))
        elif symbol == "]":
            t.pu()
            position, heading = stack.pop()
            t.goto(position)
            t.setheading(heading)

    turtle.update()


def getter(root, widget):
    x = root.winfo_rootx() + widget.winfo_x()
    y = root.winfo_rooty() + widget.winfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    return ImageGrab.grab(xdisplay=":0").crop((x, y, x1, y1))

def save_file(root, canvas, filename):
    """ Convert the Canvas widget into a bitmapped image. """
    # Get image of Canvas and convert it to bitmapped image.
    img = getter(root, canvas).convert('L').convert('1')
    img.save(filename)  # Save image file.


Plant = LSystem(
    variables="F".split(),
    constants="[ ] + -".split(),
    axiom="F",
    rules={
        "F": "F[+F]F[-F]F"
    }
)

if __name__ == "__main__":
    print(Plant)

    for i in range(3):
        Plant.iterate()
        print(Plant)

    root = tk.Tk()
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                   borderwidth=0, highlightthickness=0)
    canvas.pack()
    
    drawSystem(Plant, canvas)
    
    save_file(root, canvas, IMG_FILENAME)

    image = cv2.imread("plant.png")
    white_area = np.sum(image)
    print(white_area)