from __future__ import annotations

from math import sqrt
from scipy.optimize import least_squares

class Circle:
    def __init__(self, center: tuple[float, float], rad: float):
        self.x = center[0]
        self.y = center[1]
        self.radius = rad

def get_intersects(circ1: Circle, circ2: Circle):
    if ((circ1.x == circ2.x) and (circ1.y == circ2.y)):
        print('ERROR: circles cannot have the same center')
        return
    
    # Case 1: circles share the same x-coordinate, but not the same y-coordinate
    if circ1.x == circ2.x:
        new_y = ((circ1.radius**2) - (circ2.radius**2) + (circ2.y**2) - (circ1.y**2)) / (2 * (circ2.y - circ1.y))
        new_x1 = circ1.x + sqrt((circ1.radius**2) - ((new_y - circ1.y)**2))
        new_x2 = circ1.x - sqrt((circ1.radius**2) - ((new_y - circ1.y)**2))

        return [(new_x1, new_y), (new_x2, new_y)]
    
    # Case 2: circles share the same y-coordinate, but not the same x-coordinate
    if circ1.y == circ2.y:
        new_x = ((circ1.radius**2) - (circ2.radius**2) + (circ2.x**2) - (circ1.x**2)) / (2 * (circ2.x - circ1.x))
        new_y1 = circ1.y + sqrt((circ1.radius**2) - ((new_x - circ1.x)**2))
        new_y2 = circ1.y - sqrt((circ1.radius**2) - ((new_x - circ1.x)**2))

        return [(new_x, new_y1), (new_x, new_y2)]
    
    # Case 3: Circles do not share the same x or y coordinates
    a = -((circ2.x - circ1.x)/(circ2.y - circ1.y))
    b = ((circ1.radius**2) - (circ2.radius**2) + (circ2.x**2) - (circ1.x**2) + (circ2.y**2) - (circ1.y**2))/(2 * (circ2.y - circ1.y))
    c = (circ1.radius**2) - (circ1.x**2) - ((circ1.y - b)**2)
    d = 1 + (a**2)
    e = 2 * ((a * (b - circ1.y)) - circ1.x)

    new_x1 = (-e + sqrt((e**2) + (4 * d * c)))/(2 * d)
    new_x2 = (-e - sqrt((e**2) + (4 * d * c)))/(2 * d)
    new_y1 = (a * new_x1) + b
    new_y2 = (a * new_x2) + b

    return [(new_x1, new_y1), (new_x2, new_y2)]

def get_dist(p1: tuple[float, float], p2: tuple[float, float]):
    return sqrt(((p2[0] - p1[0])**2) + ((p2[1] - p1[1])**2))

def get_min_points(c1: Circle, c2: Circle, c3: Circle):
    points = []

    c1_c2 = get_intersects(c1, c2)
    c2_c3 = get_intersects(c2, c3)
    c1_c3 = get_intersects(c1, c3)

    min_perimeter = None

    for i in c1_c2:
        for j in c2_c3:
            for k in c1_c3:
                curr_perimeter = get_dist(i, j) + get_dist(j, k) + get_dist(k , i)

                if min_perimeter == None or curr_perimeter < min_perimeter:
                    points = [i, j, k]
                    min_perimeter = curr_perimeter
    
    #print(min_perimeter)
    return points

def get_midpoint(*points):
    mid_x, mid_y = 0, 0

    for point in points:
        mid_x += point[0]
        mid_y += point[1]
    
    mid_x /= len(points)
    mid_y /= len(points)

    return (mid_x, mid_y)

def estimate_intersection(c1:Circle, c2:Circle, c3:Circle):

    min_circ = c1

    if c2.radius < min_circ.radius:
        min_circ = c2
    
    if c3.radius < min_circ.radius:
        min_circ = c3
    
    guess = (min_circ.x, min_circ.y)

    def eq(g):
        x, y = g

        return (
            (x - c1.x)**2 + (y - c1.y)**2 - c1.radius**2,
            (x - c2.x)**2 + (y - c2.y)**2 - c1.radius**2,
            (x - c3.x)**2 + (y - c3.y)**2 - c1.radius**2
        )

    val = least_squares(eq, guess, method='lm')

    return val.x

'''
c1 = Circle((2, 2), 5)
c2 = Circle((-2, 2), 5)
c3 = Circle((1, 3), 5)

test_val = estimate_intersection(c1, c2, c3)

print(test_val)
'''