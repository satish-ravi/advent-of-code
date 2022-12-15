const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file
    .split('\n')
    .filter((line) => line.length)
    .map((line) => line.match(/-?(\d)+/g).map((x) => parseInt(x)))
}

function part1(input) {
  const reqY = 2000000
  const noBeaconsAtY = new Set()
  for (const [sx, sy, bx, by] of input) {
    const distance = Math.abs(bx - sx) + Math.abs(by - sy)
    const reqdy = Math.abs(reqY - sy)
    for (let d = reqdy; d <= distance; d++) {
      const reqdx = d - Math.abs(reqdy)
      if (reqdx >= 0) {
        if (by != reqY || sx + reqdx !== bx) noBeaconsAtY.add(sx + reqdx)
        if (by != reqY || sx - reqdx !== bx) noBeaconsAtY.add(sx - reqdx)
      }
    }
  }
  return noBeaconsAtY.size
}

function part2(input) {
  const max = 4000000
  const sensors = input.map(([sx, sy, bx, by]) => ({
    x: sx,
    y: sy,
    d: Math.abs(bx - sx) + Math.abs(by - sy),
  }))
  const isOutOfRange = (x, y) => {
    if (x < 0 || x > max || y < 0 || y > max) return false
    for (const s of sensors) {
      if (Math.abs(s.x - x) + Math.abs(s.y - y) <= s.d) {
        return false
      }
    }
    return true
  }
  for (const { x, y, d } of sensors) {
    for (let dx = 0; dx <= d + 1; dx++) {
      const dy = d + 1 - dx
      for (const [cx, cy] of [
        [x + dx, y + dy],
        [x - dx, y + dy],
        [x + dx, y - dy],
        [x - dx, y - dy],
      ]) {
        if (isOutOfRange(cx, cy)) {
          return cx * 4000000 + cy
        }
      }
    }
  }
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
