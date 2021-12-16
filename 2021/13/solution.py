import sys

FoldInstruction = tuple[str, int]
Point = tuple[int, int]


def read_input() -> tuple[set[Point], list[FoldInstruction]]:
    points = set()
    folds = []
    reading_points = True
    for l in sys.stdin.readlines():
        line = l.strip()
        if line.strip() == "":
            reading_points = False
            continue
        if reading_points:
            (a, b) = line.split(",")
            points.add((int(a), int(b)))
        else:
            (dir, amt) = line.split(" ")[-1].split("=")
            folds.append((dir, int(amt)))
    return points, folds


def fold(points: set[Point], fold_ins: FoldInstruction) -> set[Point]:
    new_points = set()
    fold_dir, fold_amt = fold_ins
    for (x, y) in points:
        if fold_dir == "x" and x > fold_amt:
            new_points.add((fold_amt * 2 - x, y))
        elif fold_dir == "y" and y > fold_amt:
            new_points.add((x, fold_amt * 2 - y))
        else:
            new_points.add((x, y))
    return new_points


def part1(points: set[Point], folds: list[FoldInstruction]) -> int:
    return len(fold(points, folds[0]))


def part2(points: set[Point], folds: list[FoldInstruction]) -> str:
    new_points = points
    for fold_ins in folds:
        new_points = fold(new_points, fold_ins)
    max_x = max(x for (x, _) in new_points)
    max_y = max(y for (_, y) in new_points)

    result = ""
    for y in range(max_y + 1):
        result += "\n"
        for x in range(max_x + 1):
            result += "#" if (x, y) in new_points else "."
    return result


points, folds = read_input()
print("part1:", part1(points, folds))
print("part2:", part2(points, folds))
