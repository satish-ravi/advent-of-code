const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  const l1 = []
  const l2 = []
  inp.forEach((line) => {
    const [a, b] = line.split('   ')
    l1.push(a)
    l2.push(b)
  })

  l1.sort()
  l2.sort()

  let res = 0

  for (let i = 0; i < l1.length; i++) {
    res += Math.abs(l1[i] - l2[i])
  }

  return res
}

function part2(inp) {
  const l1 = []
  const l2 = []
  inp.forEach((line) => {
    const [a, b] = line.split('   ')
    l1.push(a)
    l2.push(b)
  })

  let res = 0

  l1.forEach((el) => {
    res += el * l2.filter((el2) => el2 === el).length
  })

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
