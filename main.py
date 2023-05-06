from LindenmayerSystem import LSystem
import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from PIL import ImageGrab


def setTurtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.screen.title("L-System Derivation")
    r_turtle.pu()
    r_turtle.setposition(0, 350)
    r_turtle.speed("fastest")  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    return r_turtle


def drawSystem(system: LSystem, r_turtle: Turtle):
    turtle.tracer(0, 0)
    stack = []
    system_len = len(system.system)
    for symbol in system.system[system_len-1]:
        r_turtle.pd()
        if symbol == "F":
            r_turtle.forward(20)
        elif symbol == "f":
            r_turtle.pu()
            r_turtle.forward(20)
        elif symbol == "+":
            r_turtle.right(20)
        elif symbol == "-":
            r_turtle.left(20)
        elif symbol == "[":
            stack.append((r_turtle.position(), r_turtle.heading()))
        elif symbol == "]":
            r_turtle.pu()
            position, heading = stack.pop()
            r_turtle.goto(position)
            r_turtle.setheading(heading)

    turtle.update()


def getter(root, widget):
    x = root.winfo_rootx() + widget.winfo_x()
    y = root.winfo_rooty() + widget.winfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    return ImageGrab.grab().crop((x, y, x1, y1))

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


    #root = tk.Tk()
    r_turtle = setTurtle(270)
    turtle_screen = turtle.Screen()
    turtle_screen.screensize(500, 500)
    drawSystem(Plant, r_turtle)
    
    save_file(turtle_screen, turtle_screen.getcanvas(), "plant.png")
    
    turtle_screen.exitonclick()

    image = cv2.imread("plant.eps")
    white_area = np.sum(image)
    print(white_area)