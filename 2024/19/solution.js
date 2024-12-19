const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  const patterns = new Set(inp[0].split(', '))
  const designs = inp.slice(2)
  return { patterns, designs }
}

function numWays(design, patterns, cache) {
  if (design in cache) {
    return cache[design]
  }

  if (design === '') {
    return 1
  }

  let num = 0

  for (const pattern of patterns) {
    if (design.startsWith(pattern)) {
      const newDesign = design.slice(pattern.length)
      num += numWays(newDesign, patterns, cache)
    }
  }

  cache[design] = num
  return num
}

function solve({ patterns, designs }) {
  const cache = {}

  return designs.map((design) => numWays(design, patterns, cache))
}

function part1(ways) {
  return ways.filter((way) => way > 0).length
}

function part2(ways) {
  return ways.reduce((acc, way) => acc + way, 0)
}

const inp = readInput()
const parsed = parseInput(inp)
const ways = solve(parsed)
console.log('Part 1:', part1(ways))
console.log('Part 2:', part2(ways))
