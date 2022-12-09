const fs = require('fs')

const deltas = {
  L: [-1, 0],
  R: [1, 0],
  U: [0, 1],
  D: [0, -1],
}

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function solve(input, length) {
  let xpos = Array(length).fill(0)
  let ypos = Array(length).fill(0)

  const tailsVisited = new Set(['0,0'])

  for (const ins of input) {
    const [dir, len] = ins.split(' ')
    const [dx, dy] = deltas[dir]

    for (let i = 0; i < parseInt(len); i++) {
      xpos[0] += dx
      ypos[0] += dy

      for (let r = 1; r < length; r++) {
        const xDelta = xpos[r - 1] - xpos[r]
        const yDelta = ypos[r - 1] - ypos[r]
        if (Math.abs(xDelta) >= 2 || Math.abs(yDelta) >= 2) {
          xpos[r] += xDelta === 0 ? 0 : xDelta / Math.abs(xDelta)
          ypos[r] += yDelta === 0 ? 0 : yDelta / Math.abs(yDelta)
        }
      }

      tailsVisited.add(`${xpos[length - 1]},${ypos[length - 1]}`)
    }
  }

  return tailsVisited.size
}

const input = readInput()
console.log('part1:', solve(input, 2))
console.log('part2:', solve(input, 10))
