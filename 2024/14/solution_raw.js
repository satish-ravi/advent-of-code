const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

X = 101
Y = 103

// X = 11
// Y = 7

function part1(inp) {
  let quads = [0, 0, 0, 0]

  for (const line of inp) {
    const [px, py, vx, vy] = line.match(/-?\d+/g).map(Number)

    fx = (px + 100 * vx) % X
    fy = (py + 100 * vy) % Y

    if (fx < 0) fx += X
    if (fy < 0) fy += Y

    if (fx == Math.floor(X / 2) || fy == Math.floor(Y / 2)) continue

    if (fx < Math.floor(X / 2) && fy < Math.floor(Y / 2)) quads[0]++
    if (fx > Math.floor(X / 2) && fy < Math.floor(Y / 2)) quads[1]++
    if (fx < Math.floor(X / 2) && fy > Math.floor(Y / 2)) quads[2]++
    if (fx > Math.floor(X / 2) && fy > Math.floor(Y / 2)) quads[3]++

    // console.log(fx, fy, quads)
  }

  return quads[0] * quads[1] * quads[2] * quads[3]
}

function part2(inp) {
  let i = 1

  let robots = []

  for (const line of inp) {
    const [px, py, vx, vy] = line.match(/-?\d+/g).map(Number)
    robots.push([px, py, vx, vy])
  }

  while (true) {
    let pos = new Set()

    for (const [px, py, vx, vy] of robots) {
      fx = (px + i * vx) % X
      fy = (py + i * vy) % Y

      if (fx < 0) fx += X
      if (fy < 0) fy += Y

      pos.add(fx * 1000 + fy)
    }

    if (pos.size != robots.length) {
      i++
      continue
    }

    for (let x = 0; x < X; x++) {
      for (let y = 0; y < Y; y++) {
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

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
