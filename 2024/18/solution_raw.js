const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function solve(blocks) {
  let cur = 0
  let end = 70070
  let q = [[cur, []]]
  const visited = new Set()
  while (q.length) {
    let [cur, steps] = q.shift()
    if (cur === end) {
      return steps.length
    }

    if (visited.has(cur)) {
      continue
    }

    visited.add(cur)

    const x = Math.floor(cur / 1000)
    const y = cur % 1000

    for (const [dx, dy] of [
      [-1, 0],
      [1, 0],
      [0, 1],
      [0, -1],
    ]) {
      const nx = x + dx
      const ny = y + dy
      const n = nx * 1000 + ny
      if (nx < 0 || ny < 0 || nx > 70 || ny > 70 || blocks.has(n)) {
        continue
      }

      q.push([n, [...steps, [nx, ny]]])
    }
  }

  return
}

function part1(inp) {
  const blocks = new Set()
  for (let i = 0; i < 1024; i++) {
    const [x, y] = inp[i].split(',').map(Number)
    blocks.add(x * 1000 + y)
  }

  return solve(blocks)
}

function part2(inp) {
  const blocks = inp.map((line) => {
    const [x, y] = line.split(',').map(Number)
    return x * 1000 + y
  })

  for (let i = 1025; i < blocks.length; i++) {
    if (!solve(new Set(blocks.slice(0, i)))) {
      return `${Math.floor(blocks[i - 1] / 1000)},${blocks[i - 1] % 1000}`
    }
  }
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
