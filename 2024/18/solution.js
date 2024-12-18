const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  return inp.map((line) => line.split(',').map(Number))
}

const serialize = (x, y) => x * 1000 + y
const deserialize = (n) => [Math.floor(n / 1000), n % 1000]

const EDGE = 70

function solve(blocks) {
  let cur = 0
  const end = serialize(EDGE, EDGE)
  let q = [[cur, 0]]
  const visited = new Set()
  while (q.length) {
    let [cur, steps] = q.shift()
    if (cur === end) {
      return steps
    }

    if (visited.has(cur)) {
      continue
    }

    visited.add(cur)

    const [x, y] = deserialize(cur)

    for (const [dx, dy] of [
      [-1, 0],
      [1, 0],
      [0, 1],
      [0, -1],
    ]) {
      const nx = x + dx
      const ny = y + dy
      const n = serialize(nx, ny)
      if (nx < 0 || ny < 0 || nx > EDGE || ny > EDGE || blocks.has(n)) {
        continue
      }

      q.push([n, steps + 1])
    }
  }

  return
}

function part1(parsed) {
  return solve(new Set(parsed.slice(0, 1024).map(([x, y]) => serialize(x, y))))
}

function part2(parsed) {
  const blocks = parsed.map(([x, y]) => serialize(x, y))

  let left = 1025
  let right = blocks.length - 1
  let result = null

  while (left <= right) {
    const mid = Math.floor((left + right) / 2)
    if (solve(new Set(blocks.slice(0, mid)))) {
      left = mid + 1
    } else {
      result = mid
      right = mid - 1
    }
  }

  if (result !== null) {
    return `${Math.floor(blocks[result - 1] / 1000)},${
      blocks[result - 1] % 1000
    }`
  }
}

const inp = readInput()
const parsed = parseInput(inp)
console.log('Part 1:', part1(parsed))
console.log('Part 2:', part2(parsed))
