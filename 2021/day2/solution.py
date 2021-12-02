import sys

inp = sys.stdin.readlines()

horizontal = 0
p1_depth = 0
p2_depth = 0
aim = 0

for l in inp:
    dir, unit_str = l.split(" ")
    unit = int(unit_str)
    if dir == "forward":
        horizontal += unit
        p2_depth += unit * aim
    if dir == "down":
        p1_depth += unit
        aim += unit
    if dir == "up":
        p1_depth -= unit
        aim -= unit

print("part1:", horizontal*p1_depth)
print("part2:", horizontal*p2_depth)
