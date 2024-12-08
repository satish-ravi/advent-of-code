const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  const nodes = {}

  for (let i = 0; i < inp.length; i++) {
    for (let j = 0; j < inp[0].length; j++) {
      if (inp[i][j] === '.') {
        continue
      }
      if (!nodes[inp[i][j]]) {
        nodes[inp[i][j]] = []
      }
      nodes[inp[i][j]].push([i, j])
    }
  }

  const antis = new Set()

  for (const [key, locs] of Object.entries(nodes)) {
    for (let i = 0; i < locs.length; i++) {
      for (let j = i + 1; j < locs.length; j++) {
        const [x1, y1] = locs[i]
        const [x2, y2] = locs[j]
        const dx = x1 - x2
        const dy = y1 - y2
        if (
          x1 + dx >= 0 &&
          x1 + dx < inp.length &&
          y1 + dy >= 0 &&
          y1 + dy < inp[0].length
        ) {
          antis.add((x1 + dx) * 1000 + y1 + dy)
        }
        if (
          x2 - dx >= 0 &&
          x2 - dx < inp.length &&
          y2 - dy >= 0 &&
          y2 - dy < inp[0].length
        ) {
          antis.add((x2 - dx) * 1000 + y2 - dy)
        }
      }
    }
  }

  return antis.size
}

function part2(inp) {
  const nodes = {}

  for (let i = 0; i < inp.length; i++) {
    for (let j = 0; j < inp[0].length; j++) {
      if (inp[i][j] === '.') {
        continue
      }
      if (!nodes[inp[i][j]]) {
        nodes[inp[i][j]] = []
      }
      nodes[inp[i][j]].push([i, j])
    }
  }

  const antis = new Set()

  for (const [key, locs] of Object.entries(nodes)) {
    for (let i = 0; i < locs.length; i++) {
      for (let j = i + 1; j < locs.length; j++) {
        const [x1, y1] = locs[i]
        const [x2, y2] = locs[j]
        const dx = x1 - x2
        const dy = y1 - y2

        let [nx, ny] = [x1 + dx, y1 + dy]

        while (nx >= 0 && nx < inp.length && ny >= 0 && ny < inp[0].length) {
          antis.add(nx * 1000 + ny)
          nx += dx
          ny += dy
        }

        ;[nx, ny] = [x2 - dx, y2 - dy]
        while (nx >= 0 && nx < inp.length && ny >= 0 && ny < inp[0].length) {
          antis.add(nx * 1000 + ny)
          nx -= dx
          ny -= dy
        }
      }
    }
    for (const loc of locs) {
      antis.add(loc[0] * 1000 + loc[1])
    }
  }

  return antis.size
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
