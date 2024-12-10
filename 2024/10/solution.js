const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  return inp.map((x) => x.split('').map((x) => +x))
}

function getTrailDestinations(grid, i, j, cache = {}) {
  if (cache[`${i},${j}`]) return cache[`${i},${j}`]
  if (grid[i][j] === 9) return [[i, j]]
  let destinations = []
  const v = grid[i][j]
  if (i > 0 && grid[i - 1][j] === v + 1)
    destinations.push(...getTrailDestinations(grid, i - 1, j, cache))
  if (i < grid.length - 1 && grid[i + 1][j] === v + 1)
    destinations.push(...getTrailDestinations(grid, i + 1, j, cache))
  if (j > 0 && grid[i][j - 1] === v + 1)
    destinations.push(...getTrailDestinations(grid, i, j - 1, cache))
  if (j < grid[i].length - 1 && grid[i][j + 1] === v + 1)
    destinations.push(...getTrailDestinations(grid, i, j + 1, cache))
  cache[`${i},${j}`] = destinations
  return destinations
}

function getAllTrailDestinations(grid) {
  const allDestinations = []
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      if (grid[i][j] === 0) {
        allDestinations.push(getTrailDestinations(grid, i, j))
      }
    }
  }

  return allDestinations
}

function part1(grid) {
  const allDestinations = getAllTrailDestinations(grid)

  return allDestinations.reduce(
    (acc, x) => acc + new Set(x.map(([i, j]) => i * 1000 + j)).size,
    0,
  )
}

function part2(inp) {
  const allDestinations = getAllTrailDestinations(grid)

  return allDestinations.reduce((acc, x) => acc + x.length, 0)
}

const grid = parseInput(readInput())
console.log('Part 1:', part1(grid))
console.log('Part 2:', part2(grid))
