const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  const rawMonkeys = file.split('\n\n').map((line) => line.split('\n'))
  return rawMonkeys.map((rawMonkey) => {
    const items = rawMonkey[1]
      .split(': ')[1]
      .split(', ')
      .map((x) => BigInt(x))
    const operation = eval(
      rawMonkey[2]
        .split(': ')[1]
        .replace('new = ', 'old => ')
        .replace(/(\d+)/, '$1n'),
    )
    const divTest = BigInt(rawMonkey[3].split('by ')[1])
    const trueIndex = parseInt(rawMonkey[4].split('y ')[1])
    const falseIndex = parseInt(rawMonkey[5].split('y ')[1])
    return { items, operation, divTest, trueIndex, falseIndex }
  })
}

function solve(input, iterations, divide) {
  const monkeys = input.map((monkey) => ({
    ...monkey,
    items: [...monkey.items],
  }))
  let itemsInspected = Array(monkeys.length).fill(0)
  const factor = monkeys.reduce((acc, val) => acc * val.divTest, 1n)
  for (let i = 0; i < iterations; i++) {
    for (let m = 0; m < monkeys.length; m++) {
      itemsInspected[m] += monkeys[m].items.length
      for (const item of monkeys[m].items) {
        let newItem = monkeys[m].operation(item)
        if (divide) {
          newItem = BigInt(Math.floor(Number(newItem / divide)))
        } else {
          newItem %= factor
        }
        if (newItem % monkeys[m].divTest === 0n) {
          monkeys[monkeys[m].trueIndex].items.push(newItem)
        } else {
          monkeys[monkeys[m].falseIndex].items.push(newItem)
        }
      }
      monkeys[m].items = []
    }
  }
  itemsInspected.sort((a, b) => b - a)
  return itemsInspected[0] * itemsInspected[1]
}

const input = readInput()
console.log('part1:', solve(input, 20, 3n))
console.log('part2:', solve(input, 10000))
