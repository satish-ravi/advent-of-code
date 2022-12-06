const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')[0]
}

function solve(input, distinctChars) {
  for (let i = distinctChars - 1; i < input.length; i++) {
    const s = new Set()
    for (let j = 0; j < distinctChars; j++) {
      s.add(input[i - j])
    }
    if (s.size === distinctChars) {
      return i + 1
    }
  }
  throw new Error('not found')
}

const input = readInput()
console.log('part1:', solve(input, 4))
console.log('part2:', solve(input, 14))
