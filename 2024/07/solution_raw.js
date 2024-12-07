const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function isValid(res, ops) {
  if (Math.floor(res) !== res) {
    return false
  }
  if (ops.length === 1) {
    return res === ops[0]
  }
  return (
    isValid(res - ops[ops.length - 1], ops.slice(0, ops.length - 1)) ||
    isValid(res / ops[ops.length - 1], ops.slice(0, ops.length - 1))
  )
}

function isValid2(res, ops) {
  if (Math.floor(res) !== res) {
    return false
  }
  if (ops.length === 1) {
    return res === ops[0]
  }

  const last = ops[ops.length - 1]
  const resStr = `${res}`

  return (
    isValid2(res - ops[ops.length - 1], ops.slice(0, ops.length - 1)) ||
    isValid2(res / ops[ops.length - 1], ops.slice(0, ops.length - 1)) ||
    (resStr.endsWith(last.toString()) &&
      isValid2(
        +resStr.substring(0, resStr.length - `${last}`.length),
        ops.slice(0, ops.length - 1),
      ))
  )
}

function part1(inp) {
  let res = 0
  for (const line of inp) {
    const [ans, ops] = line.split(': ')

    const opVals = ops.split(' ').map((x) => parseInt(x))
    if (isValid(parseInt(ans), opVals)) {
      res += parseInt(ans)
    }
  }

  return res
}

function part2(inp) {
  let res = 0
  for (const line of inp) {
    const [ans, ops] = line.split(': ')

    const opVals = ops.split(' ').map((x) => parseInt(x))
    if (isValid2(parseInt(ans), opVals)) {
      res += parseInt(ans)
    }
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
