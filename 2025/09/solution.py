import sys

from typing import List, Tuple

Point = Tuple[int, int]
Polygon = List[Point]

# ---------- Basic geometry helpers ----------

def orient(a: Point, b: Point, c: Point) -> int:
    """Cross product (b - a) x (c - a). >0 left turn, <0 right, 0 collinear."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a: Point, b: Point, c: Point) -> bool:
    """True if c lies on segment ab (assuming collinear)."""
    return (min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))


def segments_properly_intersect(p1: Point, p2: Point, q1: Point, q2: Point) -> bool:
    """
    True if segments p1p2 and q1q2 have a *proper* intersection:
    they cross at a point strictly inside both segments
    (no touching at endpoints, no collinear overlap).
    """
    o1 = orient(p1, p2, q1)
    o2 = orient(p1, p2, q2)
    o3 = orient(q1, q2, p1)
    o4 = orient(q1, q2, p2)

    return (o1 * o2 < 0) and (o3 * o4 < 0)


# ---------- Point in polygon (including boundary) ----------

def point_in_polygon(pt: Point, poly: Polygon) -> bool:
    """
    True if pt is inside or on boundary of polygon poly.
    poly: vertices [(x0,y0), ..., (xn-1,yn-1)] in order.
    """
    x, y = pt
    inside = False
    n = len(poly)

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        # 1) On edge? (treat as inside)
        if orient((x1, y1), (x2, y2), (x, y)) == 0 and on_segment((x1, y1), (x2, y2), (x, y)):
            return True

        # 2) Ray casting:
        # Does the edge cross the horizontal ray to the right of (x, y)?
        #
        # ((y1 > y) != (y2 > y)) means the edge straddles the horizontal line y.
        if (y1 > y) != (y2 > y):
            # x-coordinate of intersection between edge and horizontal line y
            x_int = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
            # Strict '>' is standard here; avoids double-counting vertices.
            if x_int > x:
                inside = not inside

    return inside


# ---------- Rectangle containment: full rectangle inside polygon ----------

def rectangle_inside_polygon(poly: Polygon,
                             x_min: int, y_min: int,
                             x_max: int, y_max: int) -> bool:
    """
    Check if axis-aligned rectangle [x_min,x_max] × [y_min,y_max]
    is fully contained in poly.

    - All four corners must be inside or on the boundary.
    - Rectangle edges must not properly cross polygon edges.
      (Touching at vertices / lying on edges is allowed.)
    """
    # 1. Corners
    rect_corners = [
        (x_min, y_min),
        (x_min, y_max),
        (x_max, y_min),
        (x_max, y_max),
    ]

    for c in rect_corners:
        if not point_in_polygon(c, poly):
            return False

    # 2. Edges vs polygon edges
    rect_edges = [
        (rect_corners[0], rect_corners[1]),
        (rect_corners[1], rect_corners[3]),
        (rect_corners[3], rect_corners[2]),
        (rect_corners[2], rect_corners[0]),
    ]

    n = len(poly)
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]

        for r1, r2 in rect_edges:
            if segments_properly_intersect(r1, r2, p1, p2):
                # Proper crossing ⇒ the interior of the rectangle leaves the polygon.
                return False

    return True

inp = list(l for l in sys.stdin.readlines())

def parse_input(inp):
    return [tuple(map(int, line.split(','))) for line in inp]

def part1(points):
    max_area = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            max_area = max(max_area, area)
    return max_area

def part2(points):
    max_area = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area <= max_area:
                continue

            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)
            if rectangle_inside_polygon(points, x_min, y_min, x_max, y_max):
                max_area = area

    return max_area

points = parse_input(inp)
print('part1:', part1(points))
print('part2:', part2(points))
