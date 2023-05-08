from LSystem import LSystem, ParamLSystem
import turtle
import numpy as np
import cv2
import tkinter as tk
from turtle import Turtle
from PIL import ImageGrab, Image
from systemDrawer import *
import pygad

def calcSurfaceArea(filename):
    img = cv2.imread(filename+".png")

    white_area = np.sum(img)
    img_inverse = cv2.bitwise_not(img)
    black_area = np.sum(img_inverse)
    
    return black_area


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


def fitness_func(ga_instance, solution, solution_idx):
    #setup the LSystem Parameters
    a1, a2, a3, a4, a5 = solution[0:5]
    l, w = solution[5:7]
    b, c, e, f, h = solution[7:]

    lsystem = ParamLSystem(
        variables="F(l,w) A(l,w) C(l,w) +(c) -(c) T(t) P(l,w)".split(),
        constants={
            'b': b,
            'c': c,
            'e': e,
            'f': f,
            'h': h,
        },
        axiom=f"[-({a1})A({l},{w})][-({a2})A({l},{w})][-({a3})A({l},{w})][+({a4})A({l},{w})][+({a5})A({l},{w})]",
        rules={
            "P(l,w)": "T(l*0.15)F(l/2,w)+(30)-(30)[-(c)C(l*e,w*h)]T(l*0.15)F(l/2,w)+(30)-(30)[+(c)C(l*e,w*h)]",
            "A(l,w)": "P(l,w)P(l,w)A(l*b,w*f)",
            "C(l,w)": "T(l*0.1)F(l,w)A(l*b,w*f)",
        }
    )


    w2 = w + 20
    lsystem_area = ParamLSystem(
        variables="F(l,w) A(l,w) C(l,w) +(c) -(c) T(t) P(l,w)".split(),
        constants={
            'b': b,
            'c': c,
            'e': e,
            'f': f,
            'h': h,
        },
        axiom=f"[-({a1})A({l},{w2})][-({a2})A({l},{w2})][-({a3})A({l},{w2})][+({a4})A({l},{w2})][+({a5})A({l},{w2})]",
        rules={
            "P(l,w)": "T(l*0.15)F(l/2,w)+(30)-(30)[-(c)C(l*e,w*h)]T(l*0.15)F(l/2,w)+(30)-(30)[+(c)C(l*e,w*h)]",
            "A(l,w)": "P(l,w)P(l,w)A(l*b,w*f)",
            "C(l,w)": "T(l*0.1)F(l,w)A(l*b,w*f)",
        }
    )

    lsystem.iterate(10)
    lsystem_area.iterate(10)

    drawer = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(0, 340),
        screensize=(700,700)
    )

    drawer_area = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(0, 340),
        screensize=(700,700)
    )

    drawer.drawSystem(lsystem, f"training/root{solution_idx}", False)
    drawer_area.drawSystem(lsystem_area, f"training/root_area{solution_idx}", False)

    energy_spent = int(calcSurfaceArea(f"training/root{solution_idx}") / 1000000)
    area_covered = int(calcSurfaceArea(f"training/root_area{solution_idx}") / 1000000)

    return area_covered - energy_spent

def on_gen(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    print("Fitness of the best solution :", ga_instance.best_solution()[1])

    if ga_instance.generations_completed % 5 == 0:
        ga_instance.save(filename="ga_instance1")

if __name__ == "__main__":
    angle_space = {'low': 0, 'high': 180}
    factor_space = {'low': 0, 'high': 1}
    gene_space = [
        angle_space,
        angle_space,
        angle_space,
        angle_space,
        angle_space,
        {'low': 5, 'high': 200},
        {'low': 1, 'high': 50},
        factor_space,
        angle_space,
        factor_space,
        factor_space,
        factor_space
    ]

    num_generations = 20
    num_parents_mating = 4

    fitness_function = fitness_func
    on_generation = on_gen

    sol_per_pop = 8
    num_genes = 12

    parent_selection_type = "sss"
    keep_parents = 1

    crossover_type = "single_point"

    mutation_type = "adaptive"
    mutation_probability = (0.3, 0.1)

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_function,
        sol_per_pop=sol_per_pop,
        num_genes=num_genes,
        gene_space=gene_space,
        parent_selection_type=parent_selection_type,
        keep_parents=keep_parents,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_probability=mutation_probability,
        on_generation=on_generation
    )

    ga_instance.run()

    #print(CPlant.parsed_variables)
    #print(CPlant.parsed_rules)
    #print(CPlant.parsed_system)
    #MonoTree.iterate(10)
    #print(CPlant.parsed_system[4])

    #Roots.iterate(12)

    drawer = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(0, 340),
        screensize=(700,700)
    )

    #drawer.drawSystem(Roots)
    #drawer.drawSystem(Roots)

    #calcSurfaceArea("tree")"""