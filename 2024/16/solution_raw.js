const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

const ser = (r, c) => r * 1000 + c

function part1(inp) {
  let res = 0
  const walls = new Set()
  let start, end

  for (let r = 0; r < inp.length; r++) {
    for (let c = 0; c < inp[r].length; c++) {
      if (inp[r][c] === '#') {
        walls.add(ser(r, c))
      } else if (inp[r][c] === 'S') {
        start = ser(r, c)
      } else if (inp[r][c] === 'E') {
        end = ser(r, c)
      }
    }
  }

  const q = [[start, 1, 0]]
  const visited = new Set()
  visited.add(start)
  while (q.length > 0) {
    const [cur, dir, dist] = q.shift()
    if (cur === end) {
      res = dist
      break
    }
    for (const d of [1, -1, 1000, -1000]) {
      if (d !== dir && Math.abs(d) === Math.abs(dir)) {
        continue
      }
      const nser = cur + d
      if (walls.has(nser) || visited.has(nser)) {
        continue
      }
      visited.add(nser)
      let new_dist = dist + 1
      if (d !== dir) {
        new_dist += 1000
      }
      q.push([nser, d, new_dist])
      q.sort((a, b) => a[2] - b[2])
    }
  }

  return res
}

function part2(inp) {
  let res = 0
  const walls = new Set()
  let start, end

  for (let r = 0; r < inp.length; r++) {
    for (let c = 0; c < inp[r].length; c++) {
      if (inp[r][c] === '#') {
        walls.add(ser(r, c))
      } else if (inp[r][c] === 'S') {
        start = ser(r, c)
      } else if (inp[r][c] === 'E') {
        end = ser(r, c)
      }
    }
  }

  const visited = new Set()
  const allVisited = {}
  visited.add(start)
  const q = [[start, 1, 0, visited]]
  let bestPath = Infinity
  const bestPathNodes = new Set()
  while (q.length > 0) {
    const [cur, dir, dist, visited] = q.shift()
    if (dist > bestPath) {
      break
    }

    if (cur === end) {
      if (dist < bestPath) {
        bestPath = dist
        bestPathNodes.clear()
        for (const v of visited) {
          bestPathNodes.add(v)
        }
      } else if (dist === bestPath) {
        for (const v of visited) {
          bestPathNodes.add(v)
        }
      }
    }
    for (const d of [1, -1, 1000, -1000]) {
      if (d !== dir && Math.abs(d) === Math.abs(dir)) {
        continue
      }
      const nser = cur + d
      if (
        walls.has(nser) ||
        visited.has(nser) ||
        allVisited[nser * 10000 + d] < dist
      ) {
        continue
      }
      const newVisited = new Set(visited)
      newVisited.add(nser)
      let new_dist = dist + 1
      if (d !== dir) {
        new_dist += 1000
      }
      allVisited[nser * 10000 + d] = new_dist
      q.push([nser, d, new_dist, newVisited])
    }
    q.sort((a, b) => a[2] - b[2])
  }

  return bestPathNodes.size
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
