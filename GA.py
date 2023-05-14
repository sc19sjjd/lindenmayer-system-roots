import pygad
import cv2
from LSystem import ParamLSystem
from systemDrawer import ParamLSystemDrawer
import numpy as np
import copy
import time

GA_INSTANCE_NAME =  "ga_instance_adv"

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


# same root l-system as roots in main.py
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
            't': 0.12,
        },
        axiom=(f"[-({a1})A({l},{w})][-({a2})A({l},{w})][-({a3})"
               f"A({l},{w})][+({a4})A({l},{w})][+({a5})A({l},{w})]"),
        rules={
            "P(l,w)": [(1, "T(l*t)F(l/2,w)[-(c)C(l*e,w*h)]T(l*t)F(l/2,w)[+(c)C(l*e,w*h)]")],
            "A(l,w)": [(1, "P(l,w)P(l,w)A(l*b,w*f)")],
            "C(l,w)": [(1, "T(l*t)F(l,w)A(l*b,w*f)")],
        },
        iterations=10,
    )

    return lsystem

def createAdvancedRootSystem(inputs):
    a1, a2, a3, a4 = inputs[:4]
    l, w = inputs[4:6]
    a, z, b, c, d, e, f, g = inputs[6:]

    advanced_root = ParamLSystem(
        variables="F(l,w) A(l,w) B(l,w) C(l,w) D(l,w) E(l,w) G(l,w) H(l,w) Z(l,w,a) Y(l,w,a) X(l,w,a) T(t) +(a) -(a) $(a)".split(),
        constants={
            'a': a, # branching angle
            'z': z, # branching angle 2
            'b': b, # branching width factor
            'c': c, # branching length factor
            'd': d, # root width factor
            'e': e, # root length factor
            'f': f, # angle randomness 1
            'g': g, # angle randomness 2
            't': 0.27, # gravitropism factor
        },
        axiom=f"[-({a1})A({l},{w})][-({a2})A({l},{w})][+({a3})A({l},{w})][+({a4})A({l},{w})]",
        # axiom="A(70, 20)",
        rules={
            # first stage with no branching (basal zone)
            "A(l,w)": [(1, "Y(l,w,f)C(l*e,w*d)")],
            "B(l,w)": [(1, "C(l,w)")],

            # second stage with branching (branching zone)
            "C(l,w)": [(2, "Z(l,w,f)[+(a)A(l*c,w*b)]D(l*e,w*d)"),
                        (2, "Z(l,w,f)[-(a)A(l*c,w*b)]D(l*e,w*d)"),
                        (1, "Z(l,w,f)[+(z)A(l*c,w*b)]D(l*e,w*d)"), # alternative branching angles for variation
                        (1, "Z(l,w,f)[-(z)A(l*c,w*b)]D(l*e,w*d)")],
            "D(l,w)": [(1, "Z(l,w,f)X(l,w,f)E(l*e,w*d)")],
            "E(l,w)": [(3, "Z(l,w,f)[+(a)A(l*c,w*b)]G(l*e,w*d)"),
                        (3, "Z(l,w,f)[-(a)A(l*c,w*b)]G(l*e,w*d)"),
                        (2, "Z(l,w,f)[+(z)A(l*c,w*b)]G(l*e,w*d)"),  # alternative branching angles
                        (2, "Z(l,w,f)[-(z)A(l*c,w*b)]G(l*e,w*d)"),
                        (3, "Z(l,w,f)G(l*e,w*d)")],
            "G(l,w)": [(1, "Z(l,w,f)X(l,w,f)E(l*e,w*d)")],

            # final non branching stage (apical zone)
            "H(l,w)": [(1, "Z(l,w,g)H(l*e,w*d)")],

            # rule to introduce slight random variation in forward direction
            "$(a)": [(1, "+(a)-(a)")],
            # simplifying rules and added random length variation
            "X(l,w,a)": [(1, ""), (2, "Z(l*e,w*d,f)")],
            "Y(l,w,a)": [(3, "Z(l,w,f)"),
                            (4, "Z(l,w,f)Z(l*e,w*d,f)"),
                            (1, "Z(l,w,f)Z(l,w,f)Z(l*e,w*d,f)")],
            "Z(l,w,a)": [(1, "$(a)T(l*t)F(l,w)T(l*t)F(l,w)")],
        },
        iterations=12,
    )

    return advanced_root

# allow for batch size of up to 4
def fitness_func_4(ga_instance, solution, solution_idx):
    # none type is given at the end
    if solution_idx is None:
        return 0

    drawer = ParamLSystemDrawer(
        alpha_zero=270,
        start_position=(0, 580),
        screensize=(1400,1400),
    )
    
    root_systems = []
    root_area_systems = []
    energy_spent = []
    for index, s in enumerate(solution):
        root_systems.append(createAdvancedRootSystem(s))    
        
        area_covered_inputs = copy.deepcopy(s)
        area_covered_inputs[5] += 30 # increase starting width
        # branch width falloff, resize the range from 0.0-1.0 to 0.6-1.0
        # NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        area_covered_inputs[8] = (area_covered_inputs[8] * 0.3) + 0.6
        root_area_systems.append(createAdvancedRootSystem(area_covered_inputs))

        energy_spent.append(drawer.drawSystem(root_systems[index], None, True, False) * 2)
       
    fpath = "training/root_area"
    drawer.setTurtle(270, (-400, 680))
    drawer.drawSystem(root_area_systems[0], False, False, False, (0,0,0), ((-700,700), (-100,100)))
    # fix for batch size issues
    if len(root_systems) > 1:
        drawer.setTurtle(270, (-400, -120))
        drawer.drawSystem(root_area_systems[1], False, False, False, (255,0,0), ((-700,-100), (-100,-700)))
    if len(root_systems) > 2:
        drawer.setTurtle(270, (400, 680))
        drawer.drawSystem(root_area_systems[2], False, False, False, (0,255,0), ((100,700), (700,100)))
    if len(root_systems) > 3:
        drawer.setTurtle(270, (400, -120))
        drawer.drawSystem(root_area_systems[3], False, False, False, (0,0,255), ((100,-100), (700,-700)))

    drawer.saveScreen(fpath)

    areas_covered = calcSurfaceArea4(fpath)

    fitness = []
    for i in range(len(energy_spent)):
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
    
    energy_spent = drawer.drawSystem(root_system, None, True, False)

    drawer.drawSystem(root_area_system, f"training/root_area{solution_idx}", False, False)
    area_covered = int(calcSurfaceArea(f"training/root_area{solution_idx}"))

    return area_covered - energy_spent

# called at the end of each generation
def on_gen(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    print("Fitness of the best solution :", ga_instance.best_solution()[1])
    print(f"Time taken:  {time.time() - ga_instance.current_time : .2f} seconds")

    ga_instance.current_time = time.time()

    if ga_instance.generations_completed % 5 == 0:
        ga_instance.save(filename=GA_INSTANCE_NAME)