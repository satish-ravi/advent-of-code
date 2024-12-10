const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function getScore(grid, i, j) {
  if (grid[i][j] === 9) return [i * 1000 + j]
  let score = []
  const v = grid[i][j]
  if (i > 0 && grid[i - 1][j] === v + 1) score.push(...getScore(grid, i - 1, j))
  if (i < grid.length - 1 && grid[i + 1][j] === v + 1)
    score.push(...getScore(grid, i + 1, j))
  if (j > 0 && grid[i][j - 1] === v + 1) score.push(...getScore(grid, i, j - 1))
  if (j < grid[i].length - 1 && grid[i][j + 1] === v + 1)
    score.push(...getScore(grid, i, j + 1))
  return score
}

function part1(inp) {
  let res = 0
  const grid = inp.map((x) => x.split('').map((x) => +x))

  for (let i = 0; i < inp.length; i++) {
    for (let j = 0; j < inp[i].length; j++) {
      if (grid[i][j] === 0) {
        const allDest = getScore(grid, i, j)
        res += new Set(allDest).size
      }
    }
  }

  return res
}

function part2(inp) {
  let res = 0
  const grid = inp.map((x) => x.split('').map((x) => +x))

  for (let i = 0; i < inp.length; i++) {
    for (let j = 0; j < inp[i].length; j++) {
      if (grid[i][j] === 0) {
        const allDest = getScore(grid, i, j)
        res += allDest.length
      }
    }
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
