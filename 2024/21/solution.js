const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

const NUMERIC = {
  7: [0, 0],
  8: [0, 1],
  9: [0, 2],
  4: [1, 0],
  5: [1, 1],
  6: [1, 2],
  1: [2, 0],
  2: [2, 1],
  3: [2, 2],
  0: [3, 1],
  A: [3, 2],
  X: [3, 0],
}

const DIRECTIONAL = {
  '^': [0, 1],
  A: [0, 2],
  '<': [1, 0],
  v: [1, 1],
  '>': [1, 2],
  X: [0, 0],
}

function getPaths(src, dest, map) {
  const [r1, c1] = map[src]
  const [r2, c2] = map[dest]

  const dr = r2 - r1
  const dc = c2 - c1

  const paths = new Set()

  const horizontal = (dc > 0 ? '>' : '<').repeat(Math.abs(dc))
  const vertical = (dr > 0 ? 'v' : '^').repeat(Math.abs(dr))

  // shortest paths always go fully in one direction before the other
  // so we can skip paths that go back and forth
  // we also need to avoid the disallowed cell which is always in the corner
  if (!(r2 === map.X[0] && c1 === map.X[1])) {
    paths.add(vertical + horizontal + 'A')
  }
  if (!(r1 === map.X[0] && c2 === map.X[1])) {
    paths.add(horizontal + vertical + 'A')
  }

  return paths
}

function solve(inp, numKeypads) {
  let res = 0

  for (const line of inp) {
    const num = parseInt(line)
    const minLength = getMinLength(line, numKeypads, NUMERIC, {})
    res += minLength * num
  }

  return res
}

// Assumes all subsequent keypads are directional
function getMinLength(str, keypadLevel, keypadMap, cache) {
  let cacheKey = str + keypadLevel
  if (cache[cacheKey]) {
    return cache[cacheKey]
  }

  let length = 0
  let cur = 'A'
  for (const c of str) {
    const paths = Array.from(getPaths(cur, c, keypadMap))

    if (keypadLevel === 1) {
      length += paths[0].length
    } else {
      const options = paths.map((p) =>
        getMinLength(p, keypadLevel - 1, DIRECTIONAL, cache),
      )
      length += Math.min(...options)
    }

    cur = c
  }

  cache[cacheKey] = length
  return length
}

function part1(inp) {
  return solve(inp, 3)
}

function part2(inp) {
  return solve(inp, 26)
}

const inp = readInput()

console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
