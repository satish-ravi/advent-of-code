const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseAssignment(assignmentStr) {
  const [e1, e2] = assignmentStr.split(',')
  const [e1s, e1e] = e1.split('-').map((x) => parseInt(x))
  const [e2s, e2e] = e2.split('-').map((x) => parseInt(x))
  return { e1s, e1e, e2s, e2e }
}

function part1(input) {
  return input.filter(
    ({ e1s, e1e, e2s, e2e }) =>
      (e1s <= e2s && e1e >= e2e) || (e2s <= e1s && e2e >= e1e),
  ).length
}

function part2(input) {
  return input.filter(({ e1s, e1e, e2s, e2e }) => !(e1e < e2s || e1s > e2e))
    .length
}

const input = readInput().map((line) => parseAssignment(line))
console.log('part1:', part1(input))
console.log('part2:', part2(input))
