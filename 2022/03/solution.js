const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function getIntersection(list1, list2, ...rest) {
  return list1.filter(
    (element) =>
      list2.includes(element) && rest.every((list) => list.includes(element)),
  )
}

function getPriority(item) {
  let priority = item.charCodeAt(0)
  if (priority >= 97) {
    priority = priority - 97 + 1
  } else {
    priority = priority - 65 + 27
  }
  return priority
}

function part1(input) {
  let sum = 0
  input.forEach((item) => {
    const left = item.slice(0, item.length / 2).split('')
    const right = item.slice(item.length / 2, item.length).split('')
    sum += getPriority(getIntersection(left, right)[0])
  })
  return sum
}

function part2(input) {
  let sum = 0
  for (let i = 0; i < input.length; i += 3) {
    const sack1 = input[i].split('')
    const sack2 = input[i + 1].split('')
    const sack3 = input[i + 2].split('')
    sum += getPriority(getIntersection(sack1, sack2, sack3)[0])
  }
  return sum
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
