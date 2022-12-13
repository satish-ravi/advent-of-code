const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file
    .split('\n\n')
    .map((pair) => pair.split('\n').slice(0, 2).map(eval))
}

function compare(left, right) {
  if (typeof left === 'number' && typeof right === 'number') {
    return left - right
  }
  if (typeof left === 'object' && typeof right === 'object') {
    for (let i = 0; i < left.length; i++) {
      if (i === right.length) {
        return 1
      }
      const res = compare(left[i], right[i])
      if (res !== 0) {
        return res
      }
    }
    return left.length < right.length ? -1 : 0
  }
  if (typeof left === 'number') {
    return compare([left], right)
  } else {
    return compare(left, [right])
  }
}

function part1(input) {
  return input
    .map(([left, right], idx) => (compare(left, right) < 0 ? idx + 1 : 0))
    .reduce((acc, cur) => acc + cur)
}

function part2(input) {
  const dividers = [[[2]], [[6]]]
  const allPackets = input.reduce(
    (acc, [left, right]) => [...acc, left, right],
    [...dividers],
  )
  allPackets.sort(compare)
  return (
    (allPackets.indexOf(dividers[0]) + 1) *
    (allPackets.indexOf(dividers[1]) + 1)
  )
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
