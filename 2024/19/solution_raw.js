const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function isPossible(design, patterns, cache) {
  if (design in cache) {
    return cache[design]
  }

  if (design === '') {
    return true
  }

  for (const pattern of patterns) {
    if (design.startsWith(pattern)) {
      const newDesign = design.slice(pattern.length)
      if (isPossible(newDesign, patterns, cache)) {
        cache[design] = true
        return true
      }
    }
  }

  cache[design] = false
  return false
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

function part1(inp) {
  let res = 0

  const patterns = new Set(inp[0].split(', '))
  const cache = {}

  for (let i = 2; i < inp.length; i++) {
    if (isPossible(inp[i], patterns, cache)) {
      res++
    }
  }

  return res
}

function part2(inp) {
  let res = 0

  const patterns = new Set(inp[0].split(', '))
  const cache = {}

  for (let i = 2; i < inp.length; i++) {
    res += numWays(inp[i], patterns, cache)
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
