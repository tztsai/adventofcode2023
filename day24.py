from utils import *
import sympy as sp

def intersect(p1, p2, v1, v2):
    """Returns the intersection point of two lines."""
    x1, y1, _ = p1
    x2, y2, _ = p2
    vx1, vy1, _ = v1
    vx2, vy2, _ = v2
    det = vx1 * vy2 - vy1 * vx2
    if det != 0:
        b1 = vy1 * x1 - vx1 * y1
        b2 = vy2 * x2 - vx2 * y2
        x = (b2 * vx1 - b1 * vx2) / det
        y = (b2 * vy1 - b1 * vy2) / det
        if (x - x1) * vx1 >= 0 and (x - x2) * vx2 >= 0 and \
           (y - y1) * vy1 >= 0 and (y - y2) * vy2 >= 0:
            return x, y  # only consider intersections in the future

def parse(line):
    """Parses a line of the input."""
    return [tuple(map(int, s.split(', '))) for s in line.split(' @ ')]

lines = read_input()
hailstones = list(map(parse, lines))
area = ((200000000000000, 400000000000000),
        (200000000000000, 400000000000000),
        (200000000000000, 400000000000000))

intersects = []
for i, (p1, v1) in enumerate(hailstones):
    for j, (p2, v2) in enumerate(hailstones[:i]):
        interpos = intersect(p1, p2, v1, v2)
        if interpos and all(a <= x <= b for (a, b), x in zip(area, interpos)):
            intersects.append((i, j))

print(len(intersects))

symbols = x0, y0, z0, u0, v0, w0 = sp.symbols('x0 y0 z0 u0 v0 w0')
system = []
for p, v in hailstones:
    x, y, z = p
    u, v, w = v
    system.extend([
        (y0 - y) * (u0 - u) - (x0 - x) * (v0 - v),
        (z0 - z) * (v0 - v) - (y0 - y) * (w0 - w),
        (x0 - x) * (w0 - w) - (z0 - z) * (u0 - u),
    ])
    """ System of equations:
    (x0 - xi) + (u0 - ui) * ti = 0
    (y0 - yi) + (v0 - vi) * ti = 0
    (z0 - zi) + (w0 - wi) * ti = 0
    ==>
    (y0 - yi) * (u0 - ui) - (x0 - xi) * (v0 - vi) = 0
    (z0 - zi) * (v0 - vi) - (y0 - yi) * (w0 - wi) = 0
    (x0 - xi) * (w0 - wi) - (z0 - zi) * (u0 - ui) = 0
    """

sol = sp.solve(system, symbols)
print(*sol)
print(sol[0][x0] + sol[0][y0] + sol[0][z0])
