import sys
# from sympy.solvers import solve
# from sympy import Symbol
import z3

inp = list(l.strip() for l in sys.stdin.readlines())

ans = 0
points = []

for row in inp:
    p, v = row.split(' @ ')
    x, y, z = p.split(', ')
    vx, vy, vz = v.split(', ')

    points.append(((int(x), int(y), int(z)), (int(vx), int(vy), int(vz))))

def get_mb(point):
    (x, y, z), (vx, vy, vz) = point
    m = vy / vx
    b = y - m*x
    return m, b

# ir = (7, 27)
ir = (200000000000000, 400000000000000)

for i in range(len(points) - 1):
    for j in range(i+1, len(points)):
        m1, b1 = get_mb(points[i])
        m2, b2 = get_mb(points[j])
        if m1 == m2:
            if b1 == b2:
                ans += 1
            continue
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
        t1 = (x - points[i][0][0]) / points[i][1][0]
        t2 = (x - points[j][0][0]) / points[j][1][0]
        if ir[0] <= x <= ir[1] and ir[0] <= y <= ir[1] and t1 >= 0 and t2 >= 0:
            ans += 1

print(ans)

# x = Symbol('x')
# y = Symbol('y')
# z = Symbol('z')
# vx = Symbol('vx')
# vy = Symbol('vy')
# vz = Symbol('vz')
# ts = [Symbol(f't{i}') for i in range(len(points))]

# eqs = []

# for i in range(len(points)):
#     (xi, yi, zi), (vxi, vyi, vzi) = points[i]
#     eqs.append(x + ts[i] * vx - xi - ts[i] * vxi)
#     eqs.append(y + ts[i] * vy - yi - ts[i] * vyi)
#     eqs.append(z + ts[i] * vz - zi - ts[i] * vzi)

# print(solve(eqs, x, y, z))

x = z3.Real('x')
y = z3.Real('y')
z = z3.Real('z')
vx = z3.Real('vx')
vy = z3.Real('vy')
vz = z3.Real('vz')

solver = z3.Solver()

for i, point in enumerate(points):
    (xi, yi, zi), (vxi, vyi, vzi) = point
    ti = z3.Real(f't{i}')
    solver.add(x + ti * vx == xi + ti * vxi)
    solver.add(y + ti * vy == yi + ti * vyi)
    solver.add(z + ti * vz == zi + ti * vzi)

solver.check()
model = solver.model()
print(model[x], model[y], model[z], model[vx], model[vy], model[vz])
print(model.eval(x+y+z))
