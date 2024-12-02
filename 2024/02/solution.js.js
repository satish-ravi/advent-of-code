const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  return inp.map((line) => line.split(' ').map((x) => parseInt(x)))
}

function isSafe(parsed) {
  let inc = parsed[0] < parsed[1]
  for (let i = 1; i < parsed.length; i++) {
    const d = parsed[i] - parsed[i - 1]
    if (inc && d < 0) {
      return false
    }
    if (!inc && d > 0) {
      return false
    }
    if (Math.abs(d) < 1 || Math.abs(d) > 3) {
      return false
    }
  }
  return true
}

function part1(inp) {
  return inp.filter((line) => isSafe(line)).length
}

function part2(inp) {
  return inp.filter((line) => {
    if (isSafe(line)) {
      return true
    }
    for (let i = 0; i < line.length; i++) {
      let newParsed = [...line]
      newParsed.splice(i, 1)
      if (isSafe(newParsed)) {
        return true
      }
    }
    return false
  }).length
}

const parsedInput = parseInput(readInput())
console.log('Part 1:', part1(parsedInput))
console.log('Part 2:', part2(parsedInput))
