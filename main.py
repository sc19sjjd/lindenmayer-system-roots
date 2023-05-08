from LSystem import LSystem, ParamLSystem
import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from PIL import ImageGrab, Image
from systemDrawer import *

SEG_LENGTH = 20
ANGLE = 35
THICKNESS_SCALE = 1.75
BASE_THICKNESS = 6.0
WIDTH = 800
HEIGHT = 800
TARGET_BOUNDS = (1024, 1024)


def calcSurfaceArea(filename):
    img = cv2.imread(filename+".png")

    white_area = np.sum(img)
    img_inverse = cv2.bitwise_not(img)
    black_area = np.sum(img_inverse)
    print(white_area)
    print(black_area)


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
        'c': 55,
        'd': 55,
        'e': 0.6,
        'h': 0.707,
        'i': 137.5,
        't': 0.08,
    },
    axiom="A(90,20)",
    rules={
        "A(l,w)": "T(l*w*t)F(l,w)([&B(l*e,w*h)]/A(l*b,w*h)",
        "B(l,w)": "T(l*w*t)F(l,w)[-(c)$C(l*e,w*h)]C(l*b,w*h)",
        "C(l,w)": "T(l*w*t)F(l,w)[+(d)$B(l*e,w*h)]B(l*b,w*h)",
    }
)


Roots = ParamLSystem(
    variables="F(l,w) A(l,w) B(l,w) C(l,w) D(l,w) E(l,w) +(c) -(c) T(t) P(l,w)".split(),
    constants={
        'b': 0.9,
        'c': 40,
        'd': 60,
        'e': 0.2,
        'g': 0.75,
        'f': 0.85,
        'h': 0.55,
        'i': 137.5,
    },
    axiom="[-(80)A(50,15)][-(51)A(50,15)][-(12)A(50,15)][+(14)A(50,15)][+(45)A(50,15)][+(83)A(50,15)]",
    rules={
        "P(l,w)": "T(w*0.5)F(l/2,w)+(30)-(30)[-(c)C(l*e,w*h)]F(l/2,w)+(30)-(30)[+(c)C(l*e,w*h)]",
        "A(l,w)": "T(w*0.1)P(l,w)P(l,w)A(l*b,w*f)",
        "C(l,w)": "T(w*0.1)F(l,w)A(l*b,w*f)",
    }
)

#ignore this, was the original attempt at roots, kept for reference purposes
"""    "A(l,w)": "T(l*w*t*0.2)F(l,w)[-(c)C(l*e,w*h)]+(15)-(15)B(l*b,w*f)",
        "B(l,w)": "T(l*w*t*0.2)F(l,w)[+(c)C(l*e,w*h)]+(15)-(15)A(l*b,w*f)",
        "C(l,w)": "T(l*w*t)F(l,w)[D(l*g,w*h)]+(25)-(25)C(l*b,w*f)",
        "D(l,w)": "T(l*w*t)F(l,w)[-(d)E(l*e,w*h)]E(l*b,w*f)",
        "E(l,w)": "T(l*w*t)F(l,w)[+(d)D(l*e,w*h)]D(l*b,w*f)",
        "F(l,w)": "F(l*0.6,w)T(l*w*t*0.01)F(l*0.6,w)"
    }"""



if __name__ == "__main__":
    #print(CPlant.parsed_variables)
    #print(CPlant.parsed_rules)
    #print(CPlant.parsed_system)
    #MonoTree.iterate(10)
    #print(CPlant.parsed_system[4])

    Roots.iterate(12)

    drawer = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(0, 350),
    )

    drawer.drawSystem(Roots, "test")
    #drawer.drawSystem(Roots)

    #calcSurfaceArea("tree")