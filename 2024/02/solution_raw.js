const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function isSafe(parsed) {
  let inc = parsed[0] < parsed[1]
  for (let i = 1; i < parsed.length; i++) {
    const d = parsed[i] - parsed[i - 1]
    if (Math.abs(d) < 1 || Math.abs(d) > 3) {
      return false
    }
    if (inc && d < 0) {
      return false
    }
    if (!inc && d > 0) {
      return false
    }
  }
  return true
}

function part1(inp) {
  let safe = 0
  inp.forEach((line) => {
    const parsed = line.split(' ').map((x) => parseInt(x))
    if (isSafe(parsed)) {
      safe++
    }
  })
  return safe
}

function part2(inp) {
  let safe = 0
  inp.forEach((line) => {
    const parsed = line.split(' ').map((x) => parseInt(x))
    if (isSafe(parsed)) {
      safe++
      return
    }
    for (let i = 0; i < parsed.length; i++) {
      let newParsed = [...parsed]
      newParsed.splice(i, 1)
      if (isSafe(newParsed)) {
        safe++
        return
      }
    }
  })
  return safe
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
