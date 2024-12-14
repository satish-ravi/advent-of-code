const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  return {
    robots: inp.map((line) => {
      const [px, py, vx, vy] = line.match(/-?\d+/g).map(Number)
      return { px, py, vx, vy }
    }),
    width: 101,
    height: 103,
  }
}

function part1({ robots, width, height }) {
  let quads = [0, 0, 0, 0]

  const seconds = 100

  for (const { px, py, vx, vy } of robots) {
    fx = (px + seconds * vx) % width
    fy = (py + seconds * vy) % height

    if (fx < 0) fx += width
    if (fy < 0) fy += height

    const midX = Math.floor(width / 2)
    const midY = Math.floor(height / 2)

    if (fx < midX && fy < midY) quads[0]++
    if (fx > midX && fy < midY) quads[1]++
    if (fx < midX && fy > midY) quads[2]++
    if (fx > midX && fy > midY) quads[3]++
  }

  return quads.reduce((acc, quad) => acc * quad, 1)
}

function part2({ robots, width, height }) {
  let i = 1

  while (true) {
    let pos = new Set()

    for (const { px, py, vx, vy } of robots) {
      fx = (px + i * vx) % width
      fy = (py + i * vy) % height

      if (fx < 0) fx += width
      if (fy < 0) fy += height

      pos.add(fx * 1000 + fy)
    }

    if (pos.size != robots.length) {
      i++
      continue
    }

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        if (pos.has(x * 1000 + y)) {
          process.stdout.write('#')
        } else {
          process.stdout.write('.')
        }
      }
      process.stdout.write('\n')
    }
    return i
  }
}

const parsed = parseInput(readInput())
console.log('Part 1:', part1(parsed))
console.log('Part 2:', part2(parsed))
