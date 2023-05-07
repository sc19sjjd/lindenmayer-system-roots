import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from LSystem import *

SEG_LENGTH = 20
ANGLE = 45
THICKNESS_SCALE = 1.75
BASE_THICKNESS = 6.0
WIDTH = 800
HEIGHT = 800
TARGET_BOUNDS = (1024, 1024)
T_HEADING = np.array([0, -1])

# convert angle in degrees to unit vector heading direction
def getVectorHeading(degrees):
    radians = np.deg2rad(degrees)
    heading = np.array([
        np.cos(radians),
        np.sin(radians)
    ])
    return heading

def getCross(v1, v2):
    return np.cross(v1, v2)

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
            if len(symbol) > 1:
                t.right(float(symbol[1]))
            else:
                t.right(ANGLE)
        elif symbol[0] == "-":
            if len(symbol) > 1:
                t.left(float(symbol[1]))
            else:
                t.left(ANGLE)
        #gravitropism,
        #calculate beta (change in heading angle towards stimulus direction)
        # beta = e|H * T| where H and T are vectors and e is susceptibility
        elif symbol[0] == "T":
            heading = t.heading()
            v_heading = getVectorHeading(heading)
            
            cross_prod = np.cross(v_heading, T_HEADING)
            beta = float(symbol[1]) * cross_prod

            t.setheading(heading + beta)
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
