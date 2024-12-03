const fs = require('fs')

const MUL_REGEX = /mul\(\d+,\d+\)/g
const MUL_DO_DONT_REGEX = /mul\(\d+,\d+\)|do\(\)|don't\(\)/g
const DO_STRING = 'do()'
const DONT_STRING = "don't()"

function evaluateMul(match) {
  const [a, b] = match
    .substring(4, match.length - 1)
    .split(',')
    .map(Number)
  return a * b
}

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  let res = 0

  inp.forEach((line) => {
    line.match(MUL_REGEX)?.forEach((match) => {
      res += evaluateMul(match)
    })
  })

  return res
}

function part2(inp) {
  let res = 0
  let shouldDo = true
  inp.forEach((line) => {
    line.match(MUL_DO_DONT_REGEX)?.forEach((match) => {
      switch (match) {
        case DO_STRING:
          shouldDo = true
          break
        case DONT_STRING:
          shouldDo = false
          break
        default:
          if (shouldDo) {
            res += evaluateMul(match)
          }
      }
    })
  })

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
