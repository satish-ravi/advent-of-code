const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function getRocks(input) {
  const rocks = new Set()
  let maxY = -1
  for (const line of input) {
    const edges = line
      .split(' -> ')
      .map((edge) => edge.split(',').map((x) => parseInt(x)))
    for (let i = 0; i < edges.length - 1; i++) {
      const [x1, y1] = edges[i]
      const [x2, y2] = edges[i + 1]
      const dx = x1 === x2 ? 0 : x2 > x1 ? 1 : -1
      const dy = y1 === y2 ? 0 : y2 > y1 ? 1 : -1
      let cx = x1
      let cy = y1
      while (cx !== x2 || cy !== y2) {
        rocks.add(`${cx},${cy}`)
        maxY = Math.max(cy, maxY)
        cx += dx
        cy += dy
      }
      rocks.add(`${cx},${cy}`)
      maxY = Math.max(cy, maxY)
    }
  }
  return { rocks, maxY }
}

function part1(rocks, maxY) {
  const sands = new Set()
  while (true) {
    let sx = 500
    let sy = 0
    while (true) {
      if (sy === maxY) {
        return sands.size
      }
      const down = `${sx},${sy + 1}`
      if (!rocks.has(down) && !sands.has(down)) {
        sy += 1
        continue
      }
      const downLeft = `${sx - 1},${sy + 1}`
      if (!rocks.has(downLeft) && !sands.has(downLeft)) {
        sx -= 1
        sy += 1
        continue
      }
      const downRight = `${sx + 1},${sy + 1}`
      if (!rocks.has(downRight) && !sands.has(downRight)) {
        sx += 1
        sy += 1
        continue
      }
      sands.add(`${sx},${sy}`)
      break
    }
  }
}

function part2(rocks, maxY) {
  const sands = new Set()
  while (true) {
    let sx = 500
    let sy = 0
    while (true) {
      if (sy === maxY + 1) {
        sands.add(`${sx},${sy}`)
        break
      }
      const down = `${sx},${sy + 1}`
      if (!rocks.has(down) && !sands.has(down)) {
        sy += 1
        continue
      }
      const downLeft = `${sx - 1},${sy + 1}`
      if (!rocks.has(downLeft) && !sands.has(downLeft)) {
        sx -= 1
        sy += 1
        continue
      }
      const downRight = `${sx + 1},${sy + 1}`
      if (!rocks.has(downRight) && !sands.has(downRight)) {
        sx += 1
        sy += 1
        continue
      }
      sands.add(`${sx},${sy}`)
      if (sx === 500 && sy === 0) {
        return sands.size
      }
      break
    }
  }
}

const input = readInput()
const { rocks, maxY } = getRocks(input)
console.log('part1:', part1(rocks, maxY))
console.log('part2:', part2(rocks, maxY))
