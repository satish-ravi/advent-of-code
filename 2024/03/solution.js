const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  let res = 0

  inp.forEach((line) => {
    line.match(/mul\(\d+,\d+\)/g)?.forEach((match) => {
      const [a, b] = match.split(',')
      res += Number(a.substring(4)) * Number(b.substring(0, b.length - 1))
    })
  })

  return res
}

function part2(inp) {
  let res = 0
  let shouldDo = true
  inp.forEach((line) => {
    line.match(/mul\(\d+,\d+\)|do\(\)|don't\(\)/g)?.forEach((match) => {
      if (match === 'do()') {
        shouldDo = true
      } else if (match === "don't()") {
        shouldDo = false
      } else if (shouldDo) {
        const [a, b] = match.split(',')
        res += Number(a.substring(4)) * Number(b.substring(0, b.length - 1))
      }
    })
  })

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
