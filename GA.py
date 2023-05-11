import pygad
import cv2
from LSystem import ParamLSystem
from systemDrawer import ParamLSystemDrawer
import numpy as np
import copy

GA_INSTANCE_NAME =  "ga_instance3"

def getColourArea(lower_bound, upper_bound, img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(img_hsv, lower_bound, upper_bound)
    detected = cv2.bitwise_and(img, img, mask=mask)

    # Remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # Find contours and find total area
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    area = 0
    for c in cnts:
        area += cv2.contourArea(c)

    return area


def calcSurfaceArea(filename):
    img = cv2.imread(filename+".png")

    lower_black = np.array([0, 200, 200])
    upper_black = np.array([0, 255, 255])
    
    black_area = getColourArea(lower_black, upper_black, img)

    # match the surface area from multiplying turtle line length and width
    # just approximate from comparing test values
    return black_area

def calcSurfaceArea4(filename):
    img = cv2.imread(filename+".png")

    lower_black = np.array([0, 230, 230])
    upper_black = np.array([0, 255, 255])
    lower_red = np.array([0, 230, 230])
    upper_red = np.array([15, 255, 255])
    lower_blue = np.array([78, 200, 200])
    upper_blue = np.array([138, 255, 255])
    lower_green = np.array([40, 200, 200])
    upper_green = np.array([78, 255, 255])

    black_area = getColourArea(lower_black, upper_black, img)
    red_area = getColourArea(lower_red, upper_red, img)
    blue_area = getColourArea(lower_blue, upper_blue, img)
    green_area = getColourArea(lower_green, upper_green, img)

    return black_area, red_area, green_area, blue_area


def createRootSystem(inputs):
    a1, a2, a3, a4, a5 = inputs[:5]
    l ,w = inputs[5:7]
    b, c, e, f, h = inputs[7:]

    lsystem = ParamLSystem(
        variables="F(l,w) A(l,w) C(l,w) +(c) -(c) T(t) P(l,w)".split(),
        constants={
            'b': b,
            'c': c,
            'e': e,
            'f': f,
            'h': h,
        },
        axiom=(f"[-({a1})A({l},{w})][-({a2})A({l},{w})][-({a3})"
               f"A({l},{w})][+({a4})A({l},{w})][+({a5})A({l},{w})]"),
        rules={
            "P(l,w)": "T(l*0.15)F(l/2,w)+(30)-(30)[-(c)C(l*e,w*h)]T(l*0.15)F(l/2,w)+(30)-(30)[+(c)C(l*e,w*h)]",
            "A(l,w)": "P(l,w)P(l,w)A(l*b,w*f)",
            "C(l,w)": "T(l*0.1)F(l,w)A(l*b,w*f)",
        },
        iterations=10,
    )

    return lsystem


def fitness_func_4(ga_instance, solution, solution_idx):
    drawer = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(0, 590),
        screensize=(1200,1200),
    )
    
    root_systems = []
    root_area_systems = []
    energy_spent = []
    for index, s in enumerate(solution):
        root_systems.append(createRootSystem(s))    
        
        area_covered_inputs = copy.deepcopy(s)
        area_covered_inputs[6] += 40
        root_area_systems.append(createRootSystem(area_covered_inputs))

        energy_spent.append(drawer.drawSystem(root_systems[index], None, True, False))
       
    fpath = f"training/root_area_{solution_idx[0]}"
    drawer.setTurtle(270, (-325, 590))
    drawer.drawSystem(root_area_systems[0], None, False, False, (0,0,0), ((-600,600), (-50,50)))
    drawer.setTurtle(270, (-325, -60))
    drawer.drawSystem(root_area_systems[1], None, False, False, (255,0,0), ((-600,-50), (-50,-600)))
    drawer.setTurtle(270, (325, 590))
    drawer.drawSystem(root_area_systems[2], None, False, False, (0,255,0), ((50,600), (600,50)))
    drawer.setTurtle(270, (325, -60))
    drawer.drawSystem(root_area_systems[3], fpath, False, False, (0,0,255), ((50,-50), (600,-600)))

    areas_covered = calcSurfaceArea4("fpath")

    fitness = []
    for i in range(len(areas_covered)):
        fitness.append(areas_covered[i] - energy_spent[i])

    return fitness


def fitness_func(ga_instance, solution, solution_idx):
    root_system = createRootSystem(solution)

    area_covered_inputs = copy.deepcopy(solution)
    area_covered_inputs[6] += 40
    root_area_system = createRootSystem(area_covered_inputs)

    root_system.iterate(10)
    root_area_system.iterate(10)

    drawer = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(0, 290),
        screensize=(600,600)
    )
    energy_spent = drawer.drawSystem(root_system, False)
    
    drawer_area = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(0, 290),
        screensize=(600,600)
    )   
    drawer_area.drawSystem(root_area_system, f"training/root_area{solution_idx}", False)

    area_covered = int(calcSurfaceArea(f"training/root_area{solution_idx}"))

    return area_covered - energy_spent

def on_gen(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    print("Fitness of the best solution :", ga_instance.best_solution()[1])

    if ga_instance.generations_completed % 5 == 0:
        ga_instance.save(filename=GA_INSTANCE_NAME)