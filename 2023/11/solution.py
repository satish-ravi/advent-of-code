import sys

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    rows, cols = len(inp), len(inp[0])

    empty_rows = []
    empty_cols = []
    galaxies = []

    for r in range(rows):
        if not '#' in inp[r]:
            empty_rows.append(r)

    for c in range(cols):
        if not '#' in [inp[r][c] for r in range(rows)]:
            empty_cols.append(c)

    for r in range(rows):
        for c in range(cols):
            if inp[r][c] == '#':
                galaxies.append((r, c))

    return galaxies, empty_rows, empty_cols

def solve(galaxies, empty_rows, empty_cols, empty_size):
    result = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            r1, c1 = galaxies[i]
            r2, c2 = galaxies[j]
            dr = abs(r1 - r2) + (empty_size - 1) * len([er for er in empty_rows if min(r1, r2) < er < max(r1, r2)])
            dc = abs(c1 - c2) + (empty_size - 1) * len([ec for ec in empty_cols if min(c1, c2) < ec < max(c1, c2)])
            result += dr + dc
    return result

galaxies, empty_rows, empty_cols = parse_input(inp)
print('part1:', solve(galaxies, empty_rows, empty_cols, 2))
print('part2:', solve(galaxies, empty_rows, empty_cols, 1000000))
