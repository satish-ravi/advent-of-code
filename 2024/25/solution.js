const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  const locksAndKeys = inp
    .join('\n')
    .split('\n\n')
    .map((x) => x.split('\n'))

  const locks = []
  const keys = []

  for (const item of locksAndKeys) {
    const pins = []
    for (let c = 0; c < item[0].length; c++) {
      let n = 0
      for (let r = 1; r < item.length - 1; r++) {
        if (item[r][c] === '#') n++
      }
      pins.push(n)
    }
    if (item[0].startsWith('.')) keys.push(pins)
    else locks.push(pins)
  }

  return { locks, keys, size: locksAndKeys[0].length - 2 }
}

function part1({ locks, keys, size }) {
  let res = 0
  for (const key of keys) {
    for (const lock of locks) {
      let match = true
      for (let i = 0; i < key.length; i++) {
        if (key[i] + lock[i] > size) {
          match = false
          break
        }
      }
      if (match) res++
    }
  }

  return res
}

const inp = readInput()
const parsed = parseInput(inp)
console.log('Part 1:', part1(parsed))
