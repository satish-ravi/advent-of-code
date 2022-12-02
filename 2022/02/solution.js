const fs = require('fs')

const scores = {
  X: 1,
  Y: 2,
  Z: 3,
}

const mappings = {
  A: ['Z', 'X', 'Y'],
  B: ['X', 'Y', 'Z'],
  C: ['Y', 'Z', 'X'],
}

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').map((row) => row.split(' '))
}

function part1(guide) {
  const results = guide.map(
    ([opponent, player]) =>
      mappings[opponent].indexOf(player) * 3 + scores[player],
  )
  return results.reduce((acc, cur) => acc + cur)
}

function part2(guide) {
  const results = guide.map(
    ([opponent, result]) =>
      (scores[result] - 1) * 3 + scores[mappings[opponent][scores[result] - 1]],
  )
  return results.reduce((acc, cur) => acc + cur)
}

const guide = readInput()
console.log('part1:', part1(guide))
console.log('part1:', part2(guide))
