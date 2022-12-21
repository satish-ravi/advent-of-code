const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function parseInput(input) {
  const monkeys = {}
  for (const line of input) {
    const [name, val] = line.split(': ')
    if (!isNaN(val)) {
      monkeys[name] = { val: parseInt(val) }
    } else {
      const [m1, oper, m2] = val.split(' ')
      monkeys[name] = { m1, oper, m2 }
    }
  }
  return monkeys
}

function computeVal(monkeys, monkey) {
  // if (monkey === 'humn') {
  //   console.log('using humn')
  // }
  if (monkeys[monkey].val) {
    return monkeys[monkey].val
  }
  const m1Val = computeVal(monkeys, monkeys[monkey].m1)
  const m2Val = computeVal(monkeys, monkeys[monkey].m2)
  let res
  switch (monkeys[monkey].oper) {
    case '+':
      res = m1Val + m2Val
      break
    case '-':
      res = m1Val - m2Val
      break
    case '*':
      res = m1Val * m2Val
      break
    case '/':
      res = m1Val / m2Val
      break
    default:
      throw new Error('invalid operator', monkey, monkeys[monkey])
  }
  monkeys[monkey].val = res
  return res
}

function part1(input) {
  const monkeys = parseInput(input)
  return computeVal(monkeys, 'root')
}

function part2(input) {
  let monkeys = parseInput(input)
  m2 = computeVal(monkeys, monkeys.root.m2)
  let lo = 1
  let hi = Number.MAX_SAFE_INTEGER
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2)
    monkeys = parseInput(input)
    monkeys.humn = { val: mid }
    m1 = computeVal(monkeys, monkeys.root.m1)
    if (m1 === m2) {
      return mid
    }
    if (m1 < m2) {
      hi = mid
    } else {
      lo = mid
    }
  }
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
