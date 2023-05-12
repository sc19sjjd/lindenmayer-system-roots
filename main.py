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
import time

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
        't': 0.08,
    },
    axiom="A(90,20)",
    rules={
        "A(l,w)": [(1, "F(l,w)([&B(l*e,w*h)]/A(l*b,w*h)")],
        "B(l,w)": [(1, "F(l,w)[-(c)$C(l*e,w*h)]C(l*b,w*h)")],
        "C(l,w)": [(1, "F(l,w)[+(d)$B(l*e,w*h)]B(l*b,w*h)")],
    }
)


# simple root system
roots = ParamLSystem(
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
        "P(l,w)": [(1, "T(l*0.15)F(l/2,w)+(30)-(30)[-(c)C(l*e,w*h)]T(l*0.15)F(l/2,w)+(30)-(30)[+(c)C(l*e,w*h)]")],
        "A(l,w)": [(1, "P(l,w)P(l,w)A(l*b,w*f)")],
        "C(l,w)": [(1, "T(l*0.1)F(l,w)A(l*b,w*f)")],
    },
    iterations=0,
)

# test_system = ParamLSystem(variables='F(l,w)', constants={}, axiom="F(100,30)", rules={'F(l,w)': [(1, "F(l,w)F(l,w)")]}, iterations=1)

advanced_root = ParamLSystem(
    variables="A(l,w) B(l,w) C(l,w) D(l,w) E(l,w) F(l,w) G(l,w) Z(l,w,a) Y(l,w,a) X(l,w,a) T(t) +(a) -(a) $(a)".split(),
    constants={
        'a': 40, # branching angle
        'b': 0.7, # branching width factor
        'c': 0.85, # branching length factor
        'd': 0.88, # root width factor
        'e': 0.85, # root length factor
        'f': 20, # angle randomness 1
        'g': 25, # angle randomness 2
        't': 0.15, # gravitropism factor
    },
    axiom="[-(75)A(8, 15)][-(25)A(8,15)][+(25)A(8,15)][+(70)A(8,15)]",
    # axiom="A(30, 20)",
    rules={
        # first stage with no branching (basal zone)
        "A(l,w)": [(1, "Y(l,w,f)C(l*e,w*d)")],
        "B(l,w)": [(1, "C(l,w)")],

        # second stage with branching (branching zone)
        "C(l,w)": [(1, "Z(l,w,f)[+(a)A(l*c,w*b)]D(l*e,w*d)"),
                   (1, "Z(l,w,f)[-(a)A(l*c,w*b)]D(l*e,w*d)")],
        "D(l,w)": [(1, "Z(l,w,f)X(l,w,f)E(l*e,w*d)")],
        "E(l,w)": [(4, "Z(l,w,f)[+(a)A(l*c,w*b)]F(l*e,w*d)"),
                   (4, "Z(l,w,f)[-(a)A(l*c,w*b)]F(l*e,w*d)"),
                   (1, "Z(l,w,f)G(l*e,w*d)")],
        "F(l,w)": [(1, "Z(l,w,f)X(l,w,f)E(l*e,w*d)")],

        # final non branching stage (apical zone)
        "G(l,w)": [(1, "Z(l,w,g)G(l*e,w*d)")],

        # rule to introduce slight random variation in forward direction
        "$(a)": [(1, "+(a)-(a)")],
        # simplifying rules and added random length variation
        "X(l,w,a)": [(1, ""), (2, "Z(l*e,w*d,f)")],
        "Y(l,w,a)": [(3, "Z(l,w,f)"),
                     (4, "Z(l,w,f)Z(l*e,w*d,f)"),
                     (1, "Z(l,w,f)Z(l,w,f)Z(l*e,w*d,f)")],
        "Z(l,w,a)": [(1, "T(l*t)$(a)F(l,w)")],
    },
    iterations=0,
)


if __name__ == "__main__":
    # create gene space for simple root system
    angle_space = {'low': 0, 'high': 180}
    factor_space = {'low': 0, 'high': 1}
    gene_space = [
        angle_space, # a1
        angle_space, # a2
        angle_space, # a3
        angle_space, # a4
        angle_space, # a5
        {'low': 5, 'high': 150}, #l
        {'low': 1, 'high': 50}, #w
        factor_space, #b
        angle_space, #c
        factor_space, #e
        factor_space, #f
        factor_space #h
    ]

    ga_instance = pygad.GA(
        num_generations=40,
        num_parents_mating=5,
        fitness_func=fitness_func_4,
        sol_per_pop=12,
        num_genes=12,
        gene_space=gene_space,
        parent_selection_type="rws",
        keep_parents=2,
        keep_elitism=0,
        crossover_type="single_point",
        mutation_type="adaptive",
        mutation_probability=(0.4, 0.2),
        on_generation=on_gen,
        save_best_solutions=True,
        suppress_warnings=True,
        fitness_batch_size=4,
    )

    ga_instance = pygad.load('ga_instance3')

    ga_instance.current_time = time.time()

    # ga_instance.run()

    drawer = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(0, 430),
        screensize=(900,900)
    )

    #ga_instance.plot_fitness()
    # lsystem = createRootSystem(ga_instance.best_solutions[100])
    # drawer.drawSystem(lsystem, "best_4", False, True)

    # MonoTree.iterate(12)
    # drawer.drawSystem(MonoTree, 'tree_gravitropism', False, True)
    advanced_root.iterate(12)
    # print(advanced_root.system)
    drawer.drawSystem(advanced_root, 'advanced_root', False, True)
    # roots.iterate(12)
    # drawer.drawSystem(roots, 'roots', False, True)

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