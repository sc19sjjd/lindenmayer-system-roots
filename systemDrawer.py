import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from LSystem import *

SEG_LENGTH = 20
ANGLE = 40
THICKNESS_SCALE = 1.75
BASE_THICKNESS = 6.0
WIDTH = 800
HEIGHT = 800
TARGET_BOUNDS = (1024, 1024)

def setTurtle(alpha_zero):
    t = turtle.Turtle()  # recursive turtle
    turtle.tracer(0, 0)
    t.hideturtle()
    t.screen.title("L-System Derivation")
    t.pensize(BASE_THICKNESS)
    t.pu()
    t.setposition(0, -350)
    t.speed("fastest")  # adjust as needed (0 = fastest)
    t.setheading(alpha_zero)  # initial heading
    return t

def drawSystem(system: LSystem, t: Turtle):
    turtle.tracer(0, 0)
    stack = []
    system_len = len(system.system)
    width = BASE_THICKNESS
    for symbol in system.system[system_len-1]:
        t.pd()
        if symbol == "F":
            t.pd()
            t.forward(SEG_LENGTH)
        elif symbol == "f":
            t.pu()
            t.forward(SEG_LENGTH)
        elif symbol == "+":
            t.right(ANGLE)
        elif symbol == "-":
            t.left(ANGLE)
        elif symbol == "!":
            width = width * THICKNESS_SCALE
            t.pensize(width)
        elif symbol == "?":
            width = width / THICKNESS_SCALE
            t.pensize(width) 
        elif symbol == "[":
            stack.append((
                t.position(), 
                t.heading(),
            ))
        elif symbol == "]":
            t.pu()
            position, heading = stack.pop()
            t.goto(position)
            t.setheading(heading)

    turtle.update()

def drawParamSystem(system: ParamLSystem, t: Turtle):
    stack = []
    system_len = len(system.system)
    for symbol in system.parsed_system[system_len-1]:
        if symbol[0] == "F":
            #print(f"symbol: {symbol}")
            t.pd()
            t.pensize(float(symbol[2]))
            t.forward(float(symbol[1]))
        elif symbol[0] == "+":
            t.right(ANGLE)
        elif symbol[0] == "-":
            t.left(ANGLE)
        elif symbol[0] == "[":
            stack.append((
                t.position(),
                t.heading(),
            ))
        elif symbol[0] == "]":
            t.pu()
            position, heading = stack.pop()
            t.goto(position)
            t.setheading(heading)

    turtle.update()