from LSystem import LSystem, ParamLSystem
import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from PIL import ImageGrab, Image
from systemDrawer import *
import pygad
from GA import *

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
        "P(l,w)": "T(l*0.15)F(l/2,w)+(30)-(30)[-(c)C(l*e,w*h)]T(l*0.15)F(l/2,w)+(30)-(30)[+(c)C(l*e,w*h)]",
        "A(l,w)": "P(l,w)P(l,w)A(l*b,w*f)",
        "C(l,w)": "T(l*0.1)F(l,w)A(l*b,w*f)",
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

test_system = ParamLSystem(variables='F(l,w)', constants={}, axiom="F(100,30)", rules={'F(l,w)': "F(l,w)F(l,w)"}, iterations=1)


if __name__ == "__main__":
    # create gene space
    angle_space = {'low': 0, 'high': 180}
    factor_space = {'low': 0, 'high': 1}
    gene_space = [
        angle_space, # a1
        angle_space, # a2
        angle_space, # a3
        angle_space, # a4
        angle_space, # a5
        {'low': 5, 'high': 200}, #l
        {'low': 1, 'high': 50}, #w
        factor_space, #b
        angle_space, #c
        factor_space, #e
        factor_space, #f
        factor_space #h
    ]

    ga_instance = pygad.GA(
        num_generations=40,
        num_parents_mating=4,
        fitness_func=fitness_func_4,
        sol_per_pop=12,
        num_genes=12,
        gene_space=gene_space,
        parent_selection_type="rws",
        keep_parents=1,
        keep_elitism=2,
        crossover_type="single_point",
        mutation_type="adaptive",
        mutation_probability=(0.3, 0.1),
        on_generation=on_gen,
        save_best_solutions=True,
        suppress_warnings=True,
        fitness_batch_size=4,
    )

    ga_instance.run()


    #print(CPlant.parsed_variables)
    #print(CPlant.parsed_rules)
    #print(CPlant.parsed_system)
    #MonoTree.iterate(10)
    #print(CPlant.parsed_system[4])

    drawer = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(-325, 580),
        screensize=(1200,1200)
    )

    #Roots.iterate(12)
    # print(drawer.drawSystem(test_system, None, colour=(0,0,0), clear=False, onClick=False))
    # drawer.setTurtle(270, (-325, -70))
    # print(drawer.drawSystem(test_system, None, colour=(255,0,0), clear=False, onClick=False))
    # drawer.setTurtle(270, (325, 580))
    # print(drawer.drawSystem(test_system, None, colour=(0,255,0), clear=False, onClick=False))
    # drawer.setTurtle(270, (325, -70))
    # print(drawer.drawSystem(test_system, filename='test', colour=(0,0,255), clear=False, onClick=True))

    #print(calcSurfaceArea('test'))
    #drawer.drawSystem(Roots)

    #calcSurfaceArea("tree")