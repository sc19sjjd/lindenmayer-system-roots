import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from LSystem import *
from PIL import Image

SEG_LENGTH = 20
ANGLE = 45
THICKNESS_SCALE = 1.75
BASE_THICKNESS = 6.0
WIDTH = 800
HEIGHT = 800
TARGET_BOUNDS = (1024, 1024)
T_HEADING = np.array([0, -1])
ANGLE_DEVIATION_FACTOR = 0.1
LENGTH_DEVIATION_FACTOR = 0.2

class LSystemDrawer():
    def __init__(
            self, 
            alpha_zero=0, 
            start_position=(0,0),
            screensize=(800,800),
            base_thickness=8,
            thickness_scale=0.75,
            angle=45,
            segment_length=25
        ):
            self.base_thickness = base_thickness
            self.thickness_scale = thickness_scale
            self.angle = angle
            self.segment_length = segment_length

            self.turtle = turtle.Turtle()
            self.setTurtle(alpha_zero, start_position)
            self.screen = turtle.Screen()
            self.screen.screensize(screensize[0], screensize[1])

    def setTurtle(self, alpha_zero, start_position):
        turtle.tracer(0, 0)
        self.turtle.hideturtle()
        self.turtle.screen.title("L-System Derivation")
        self.turtle.pu()
        self.turtle.setposition(start_position)
        self.turtle.speed("fastest")  # adjust as needed (0 = fastest)
        self.turtle.setheading(alpha_zero)  # initial heading

    def drawSystem(self, system: LSystem, filename=None):
        turtle.tracer(0, 0)
        stack = []
        system_len = len(system.system)
        width = self.base_thickness
        self.turtle.pensize(width)
        for symbol in system.system[system_len-1]:
            self.turtle.pd()
            if symbol == "F":
                self.turtle.pd()
                self.turtle.forward(self.segment_length)
            elif symbol == "f":
                self.turtle.pu()
                self.turtle.forward(self.segment_length)
            elif symbol == "+":
                self.turtle.right(self.angle)
            elif symbol == "-":
                self.turtle.left(self.angle)
            elif symbol == "!":
                width = width * self.thickness_scale
                self.turtle.pensize(width)
            elif symbol == "?":
                width = width / self.thickness_scale
                self.turtle.pensize(width) 
            elif symbol == "[":
                stack.append((
                    self.turtle.position(), 
                    self.turtle.heading(),
                ))
            elif symbol == "]":
                self.turtle.pu()
                position, heading = stack.pop()
                self.turtle.goto(position)
                self.turtle.setheading(heading)

        turtle.update()

        if filename:
            self.__saveScreen__(filename)
        
        self.screen.exitonclick()

    def __saveScreen__(self, filename):
        self.screen.getcanvas().postscript(file=filename+".eps")

        img = Image.open(filename+".eps")
        img.load(scale=10)

        img = img.convert("RGBA")

        # Calculate the new size, preserving the aspect ratio
        ratio = min(TARGET_BOUNDS[0] / img.size[0],
                TARGET_BOUNDS[1] / img.size[1])
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))

        # Resize to fit the target size
        img = img.resize(new_size, Image.LANCZOS)

        # Save to PNG
        img.save(filename+".png")


class ParamLSystemDrawer(LSystemDrawer):
    def __init__(
            self, 
            alpha_zero=0, 
            start_position=(0,0),
            screensize=(800,800),
            t_heading=np.array([0,-1]),
            angle=45,
            asdf=0.1, # angle standard deviation factor
            lsdf=0.2, # legnth standard deviation factor
        ):
            self.t_heading=t_heading
            self.angle = angle
            self.asdf = asdf
            self.lsdf = lsdf

            self.turtle = turtle.Turtle()
            self.setTurtle(alpha_zero, start_position)
            self.screen = turtle.Screen()
            self.screen.screensize(screensize[0], screensize[1])

    # convert angle in degrees to unit vector heading direction
    def getVectorHeading(self, degrees):
        radians = np.deg2rad(degrees)
        heading = np.array([
            np.cos(radians),
            np.sin(radians)
        ])
        return heading

    def drawSystem(self, system: ParamLSystem, filename=None):
        turtle.tracer()
        stack = []
        system_len = len(system.system)
        for symbol in system.parsed_system[system_len-1]:
            if symbol[0] == "F":
                #print(f"symbol: {symbol}")
                #generate a random length based on normal distribution
                length = float(symbol[1])
                length = np.random.normal(length, length * self.lsdf)
                self.turtle.pd()
                self.turtle.pensize(float(symbol[2]))
                self.turtle.forward(length)
            elif symbol[0] == "+":
                if len(symbol) > 1:
                    #generate a random angle based on normal distribution
                    angle = float(symbol[1])
                    angle = np.random.normal(angle, angle * self.asdf)
                    self.turtle.right(angle)
                else:
                    self.turtle.right(self.angle)
            elif symbol[0] == "-":
                if len(symbol) > 1:
                    angle = float(symbol[1])
                    angle = np.random.normal(angle, angle * self.asdf)
                    self.turtle.left(angle)
                else:
                    self.turtle.left(self.angle)
            #gravitropism,
            #calculate beta (change in heading angle towards stimulus direction)
            # beta = e|H * T| where H and T are vectors and e is susceptibility
            elif symbol[0] == "T":
                heading = self.turtle.heading()
                v_heading = self.getVectorHeading(heading)
                
                cross_prod = np.cross(v_heading, self.t_heading)
                beta = float(symbol[1]) * cross_prod

                self.turtle.setheading(heading + beta)
            elif symbol[0] == "[":
                stack.append((
                    self.turtle.position(),
                    self.turtle.heading(),
                ))
            elif symbol[0] == "]":
                self.turtle.pu()
                position, heading = stack.pop()
                self.turtle.goto(position)
                self.turtle.setheading(heading)

        turtle.update()

        if filename:
            self.__saveScreen__(filename)
        
        self.screen.exitonclick()