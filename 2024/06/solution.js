const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function traverse(grid) {
  let start = null
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[0].length; j++) {
      if (grid[i][j] === '^') {
        start = [i, j]
        break
      }
    }
    if (start) break
  }

  const deltas = [
    [-1, 0],
    [0, 1],
    [1, 0],
    [0, -1],
  ]

  const visited = new Set()

  let dir = 0
  let cur = start

  let loop = false

  while (true) {
    const [i, j] = cur
    if (visited.has(dir * 1000000 + i * 1000 + j)) {
      loop = true
      break
    }

    visited.add(dir * 1000000 + i * 1000 + j)

    let [ni, nj] = [i + deltas[dir][0], j + deltas[dir][1]]

    if (ni < 0 || ni >= grid.length || nj < 0 || nj >= grid[0].length) {
      break
    }

    if (grid[ni][nj] === '#') {
      dir = (dir + 1) % 4
      continue
    }

    cur = [ni, nj]
  }

  const visitedPositions = Array.from(
    new Set(Array.from(visited).map((v) => v % 1000000)),
  ).map((v) => [Math.floor(v / 1000), v % 1000])

  return { visitedPositions, loop, start }
}

function part1(inp) {
  return traverse(inp).visitedPositions.length
}

function part2(inp) {
  const { visitedPositions, start } = traverse(inp)
  let res = 0
  for (const [i, j] of visitedPositions) {
    if (i === start[0] && j === start[1]) continue
    let newGrid = Array.from(inp)
    newGrid[i] = newGrid[i].substr(0, j) + '#' + newGrid[i].substr(j + 1)

    const { loop } = traverse(newGrid)
    if (loop) res++
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
