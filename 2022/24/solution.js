const fs = require('fs')
const { exit } = require('process')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function ser(r, c) {
  return `${r},${c}`
}

function deser(st) {
  const [r, c] = st.split(',').map((x) => parseInt(x))
  return { r, c }
}

function parseInput(input) {
  const walls = new Set()
  const blizzards = []
  let start, end
  for (let r = 0; r < input.length; r++) {
    for (let c = 0; c < input[0].length; c++) {
      const val = input[r][c]
      switch (val) {
        case '#':
          walls.add(ser(r, c))
          continue
        case '.':
          if (r === 0) {
            start = ser(r, c)
          } else if (r === input.length - 1) {
            end = ser(r, c)
          }
          continue
        default:
          blizzards.push({ r, c, dir: val })
          continue
      }
    }
  }
  return {
    walls,
    blizzards,
    start,
    end,
    bd: input.length - 1,
    br: input[0].length - 1,
  }
}

// Recursive function to return gcd of a and b
function gcd(a, b) {
  if (b == 0) return a
  return gcd(b, a % b)
}

// Function to return LCM of two numbers
function lcm(a, b) {
  return (a / gcd(a, b)) * b
}

function getBlizzardAtTimes(blizzards, bd, br) {
  max = lcm(bd - 1, br - 1)
  const blizAtT = Array(max)
    .fill(0)
    .map((_) => new Set())
  for (const blizzard of blizzards) {
    let r = blizzard.r
    let c = blizzard.c
    for (let t = 0; t < max; t++) {
      blizAtT[t].add(ser(r, c))
      switch (blizzard.dir) {
        case '>':
          c = c === br - 1 ? 1 : c + 1
          break
        case '<':
          c = c === 1 ? br - 1 : c - 1
          break
        case 'v':
          r = r === bd - 1 ? 1 : r + 1
          break
        case '^':
          r = r === 1 ? bd - 1 : r - 1
          break
      }
    }
  }
  return blizAtT
}

function findBest(walls, blizAtT, start, end, min = 0) {
  let options = new Set([start])
  while (true) {
    let nextOptions = new Set()
    for (const cur of options) {
      if (cur === end) {
        return min
      }
      const { r, c } = deser(cur)
      for (const [dr, dc] of [
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1],
        [0, 0],
      ]) {
        const next = ser(r + dr, c + dc)
        if (
          !blizAtT[(min + 1) % blizAtT.length].has(next) &&
          !walls.has(next) &&
          r + dr >= 0
        ) {
          nextOptions.add(next)
        }
      }
    }
    options = nextOptions
    min += 1
  }
}

function part1(input) {
  const { walls, blizzards, start, end, bd, br } = parseInput(input)
  const blizAtT = getBlizzardAtTimes(blizzards, bd, br)
  return findBest(walls, blizAtT, start, end, 0)
}

function part2(input) {
  const { walls, blizzards, start, end, bd, br } = parseInput(input)
  const blizAtT = getBlizzardAtTimes(blizzards, bd, br)
  const first = findBest(walls, blizAtT, start, end, 0)
  const second = findBest(walls, blizAtT, end, start, first)
  return findBest(walls, blizAtT, start, end, second)
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
