const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file
    .split('\n\n')
    .map((group) => group.split('\n').map((calories) => parseInt(calories)))
}

function solve(elves, num) {
  const elvesCalories = elves.map((calories) =>
    calories.reduce((acc, cur) => acc + cur),
  )
  elvesCalories.sort((a, b) => b - a)
  return elvesCalories.slice(0, num).reduce((acc, cur) => acc + cur)
}

const elves = readInput()
console.log('part1:', solve(elves, 1))
console.log('part2:', solve(elves, 3))
