const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

NUMERIC = {
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
}

DIRECTIONAL = {
  '^': [0, 1],
  A: [0, 2],
  '<': [1, 0],
  v: [1, 1],
  '>': [1, 2],
}

function generatePaths(x1, x2, y1, y2, [disallowedX, disallowedY]) {
  let cur = [x1, y1]
  let q = [[cur, '']]
  let paths = []

  let dx = x1 < x2 ? 1 : x1 > x2 ? -1 : 0
  let dy = y1 < y2 ? 1 : y1 > y2 ? -1 : 0

  while (q.length > 0) {
    const [[cx, cy], path] = q.shift()

    if (cx === x2 && cy === y2) {
      paths.push(path + 'A')
      continue
    }

    if (cx !== x2) {
      nx = cx + dx
      if (nx !== disallowedX || cy !== disallowedY) {
        q.push([[nx, cy], path + (dx === 1 ? 'v' : '^')])
      }
    }

    if (cy !== y2) {
      ny = cy + dy
      if (cx !== disallowedX || ny !== disallowedY) {
        q.push([[cx, ny], path + (dy === 1 ? '>' : '<')])
      }
    }
  }

  return paths.filter((p) => {
    let s = p[0]
    let flipped = false
    for (let i = 1; i < p.length - 2; i++) {
      if (p[i] !== s) {
        flipped = true
      } else if (flipped) {
        return false
      }
    }
    return true
  })
}

NUMERIC_CACHE = {}

function generateNumeric(key1, key2) {
  if (NUMERIC_CACHE[`${key1}${key2}`]) {
    return NUMERIC_CACHE[`${key1}${key2}`]
  }

  const [x1, y1] = NUMERIC[key1]
  const [x2, y2] = NUMERIC[key2]

  NUMERIC_CACHE[`${key1}${key2}`] = generatePaths(x1, x2, y1, y2, [3, 0])
  return NUMERIC_CACHE[`${key1}${key2}`]
}

DIRECTIONAL_CACHE = {}

function generateDirectional(key1, key2) {
  if (DIRECTIONAL_CACHE[`${key1}${key2}`]) {
    return DIRECTIONAL_CACHE[`${key1}${key2}`]
  }
  const [x1, y1] = DIRECTIONAL[key1]
  const [x2, y2] = DIRECTIONAL[key2]

  DIRECTIONAL_CACHE[`${key1}${key2}`] = generatePaths(x1, x2, y1, y2, [0, 0])
  return DIRECTIONAL_CACHE[`${key1}${key2}`]
}

function generateSequences(str, isNumeric) {
  let cur = 'A'
  let paths = ['']

  for (const c of str) {
    const pathOptions = isNumeric
      ? generateNumeric(cur, c)
      : generateDirectional(cur, c)

    let newPaths = []
    for (const path of paths) {
      for (const option of pathOptions) {
        newPaths.push(path + option)
      }
    }
    paths = newPaths
    cur = c
  }

  return paths
}

function part1(inp) {
  let res = 0

  for (const line of inp) {
    const num = parseInt(line.substring(0, 3))

    const first = generateSequences(line, true)

    const second = []
    for (const seq of first) {
      second.push(...generateSequences(seq, false))
    }

    const third = []
    for (const seq of second) {
      for (const path of generateSequences(seq, false)) {
        third.push(path)
      }
    }

    let minLength = Infinity
    for (const seq of third) {
      minLength = Math.min(minLength, seq.length)
    }

    res += minLength * num
  }

  return res
}

MIN_LENGTH_CACHE = {}

function minLength(str, robot) {
  let cacheKey = str + robot
  if (MIN_LENGTH_CACHE[cacheKey]) {
    return MIN_LENGTH_CACHE[cacheKey]
  }

  let length = 0

  let cur = 'A'

  for (const c of str) {
    const paths = generateDirectional(cur, c)

    if (robot === 1) {
      length += paths[0].length
    } else {
      const options = paths.map((p) => minLength(p, robot - 1))
      length += Math.min(...options)
    }

    cur = c
  }

  MIN_LENGTH_CACHE[cacheKey] = length
  return length
}

function part2(inp) {
  let res = 0

  for (const line of inp) {
    const num = parseInt(line.substring(0, 3))

    const first = generateSequences(line, true)

    const ml = Math.min(...first.map((p) => minLength(p, 25)))

    res += ml * num
  }
  return res
}

const inp = readInput()

console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
