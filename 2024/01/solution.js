const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(lines) {
  const left = []
  const right = []

  for (const line of lines) {
    const [a, b] = line.split('   ')
    left.push(+a)
    right.push(+b)
  }

  return { left, right }
}

function part1({ left, right }) {
  const sortedLeft = [...left].sort()
  const sortedRight = [...right].sort()

  let result = 0

  for (let i = 0; i < left.length; i++) {
    result += Math.abs(sortedLeft[i] - sortedRight[i])
  }

  return result
}

function part2({ left, right }) {
  let result = 0

  left.forEach((element) => {
    result +=
      element * right.filter((rightElement) => rightElement === element).length
  })

  return result
}

const parsedInput = parseInput(readInput())
console.log('Part 1:', part1(parsedInput))
console.log('Part 2:', part2(parsedInput))
