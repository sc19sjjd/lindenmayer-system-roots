import turtle
import numpy as np
from LSystem import *
from PIL import Image

TARGET_BOUNDS = (1500, 1500)


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
            self.screen = turtle.Screen()
            self.screen.setup(screensize[0] + 4, screensize[1] + 8)
            self.screen.title("L-System Derivation")
            self.setTurtle(alpha_zero, start_position)

    def setTurtle(self, alpha_zero, start_position):
        self.turtle.hideturtle()
        self.turtle.pu()
        self.turtle.setposition(start_position)
        self.turtle.speed("fastest")  # adjust as needed (0 = fastest)
        self.turtle.setheading(alpha_zero)  # initial heading

    # returns the total surface area drawn by the turtle
    def drawSystem(self, system: LSystem, filename=None, colour=(0,0,0)) -> int: 
        turtle.tracer(0, 0)
        stack = []
        system_len = len(system.system)
        width = self.base_thickness
        self.turtle.pensize(width)

        turtle.colormode(255)
        self.turtle.pencolor(colour)

        total_drawn_area = 0.0
        for symbol in system.system[system_len-1]:
            self.turtle.pd()
            if symbol == "F":
                self.turtle.pd()
                self.turtle.forward(self.segment_length)
                total_drawn_area += self.segment_length * (width * 1.5)
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
            self.saveScreen(filename)
        
        self.screen.exitonclick()

        return int(total_drawn_area)
    

    def saveScreen(self, filename):
        self.screen.getcanvas().postscript(file=filename+".eps")

        img = Image.open(filename+".eps")
        img.load(scale=5)

        img = img.convert("RGB")

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
            self.screen = turtle.Screen()
            self.screen.setup(screensize[0] + 10, screensize[1] + 10)
            self.setTurtle(alpha_zero, start_position)

    # convert angle in degrees to unit vector heading direction
    def getVectorHeading(self, degrees):
        radians = np.deg2rad(degrees)
        heading = np.array([
            np.cos(radians),
            np.sin(radians)
        ])
        return heading
    
    def isTurtleInsideArea(self, area):
        x, y = self.turtle.position()

        if x <= area[0][0]:
            return False
        elif y >= area[0][1]:
            return False
        elif x >= area[1][0]:
            return False
        elif y <= area[1][1]:
            return False
        else:
            return True

    def drawSystem(
        self, 
        system: ParamLSystem, 
        filename=None, 
        clear=True, 
        onClick=True, 
        colour=(0,0,0),
        area=((-np.inf, np.inf), (np.inf, -np.inf)) # area in screen that the turtle can draw in ((top left), (bottom right))
    ) -> int:
        turtle.tracer(0, 0)
        stack = []
        system_len = len(system.system)
        total_drawn_area = 0.0
        
        turtle.colormode(255)
        self.turtle.pencolor(colour)

        for symbol in system.parsed_system[system_len-1]:
            if symbol[0] == "F":
                if self.isTurtleInsideArea(area):
                    self.turtle.pd()
                else:
                    self.turtle.pu()

                #generate a random length based on normal distribution
                length = float(symbol[1])
                #length = np.random.normal(length, length * self.lsdf)
                
                self.turtle.pensize(float(symbol[2]))
                self.turtle.forward(length)
                
                total_drawn_area += length * (self.turtle.pensize() * 1.1)
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
            # gravitropism,
            # calculate beta (change in heading angle towards stimulus direction)
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
            self.saveScreen(filename)
        
        if onClick:
            self.screen.exitonclick()

        if clear:
            try:
                turtle.clearscreen()
            except:
                pass

        return int(total_drawn_area)