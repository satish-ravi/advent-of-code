const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function getValAtCycles(input) {
  let x = 1
  let cycle = 0
  let valAtCycles = { 0: 1 }
  for (const line of input) {
    const [ins, val] = line.split(' ')
    if (ins === 'noop') {
      cycle++
      valAtCycles[cycle] = x
    } else {
      valAtCycles[cycle + 1] = x
      valAtCycles[cycle + 2] = x
      cycle += 2
      x += parseInt(val)
    }
  }

  return valAtCycles
}

function part1(valAtCycles) {
  return [20, 60, 100, 140, 180, 220]
    .map((cycle) => cycle * valAtCycles[cycle])
    .reduce((acc, cur) => acc + cur)
}

function part2(valAtCycles) {
  R = 6
  C = 40
  let img = ''

  for (i = 0; i < R; i++) {
    img += '\n'
    for (j = 0; j < C; j++) {
      const cycle = i * C + j + 1
      if (Math.abs(j - valAtCycles[cycle]) <= 1) {
        img += '#'
      } else {
        img += '.'
      }
    }
  }
  return img
}

const input = readInput()
const valAtCycles = getValAtCycles(input)
console.log('part1:', part1(valAtCycles))
console.log('part2:', part2(valAtCycles))
