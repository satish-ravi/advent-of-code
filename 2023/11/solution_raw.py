import sys

inp = list(l.strip() for l in sys.stdin.readlines())

rows, cols = len(inp), len(inp[0])

empty_rows = []
empty_cols = []

for r in range(rows):
    if not '#' in inp[r]:
        empty_rows.append(r)

for c in range(cols):
    if not '#' in [inp[r][c] for r in range(rows)]:
        empty_cols.append(c)

image = []
for r in range(rows):
    if r in empty_rows:
        image.append(['.'] * (cols + len(empty_cols)))
    row = []
    for c in range(cols):
        if c in empty_cols:
            row.append('.')
        row.append(inp[r][c])
    image.append(row)

galaxies = []

nr = len(image)
nc = len(image[0])
for r in range(nr):
    for c in range(nc):
        if image[r][c] == '#':
            galaxies.append((r, c))

ans = 0
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        ans += abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])

print(ans)

galaxies = []

nr = len(inp)
nc = len(inp[0])
for r in range(nr):
    for c in range(nc):
        if inp[r][c] == '#':
            galaxies.append((r, c))

ans = 0
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        r1, c1 = galaxies[i]
        r2, c2 = galaxies[j]
        dr = abs(r1 - r2)
        dc = abs(c1 - c2)
        dr += 999999 * len([er for er in empty_rows if min(r1, r2) < er < max(r1, r2)])
        dc += 999999 * len([ec for ec in empty_cols if min(c1, c2) < ec < max(c1, c2)])
        ans += dr + dc

print(ans)