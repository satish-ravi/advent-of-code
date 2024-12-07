const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  return inp.map((line) => {
    const [result, operands] = line.split(': ')
    return {
      result: +result,
      operands: operands.split(' ').map((x) => +x),
    }
  })
}

function isValid(result, operands, allowConcat) {
  if (operands.length === 1) {
    return result === operands[0]
  }

  const last = operands.at(-1)
  const resStr = `${result}`
  const lastStr = `${last}`
  const operandsWithoutLast = operands.slice(0, operands.length - 1)

  return (
    isValid(result - last, operandsWithoutLast, allowConcat) ||
    (result % last === 0 &&
      isValid(result / last, operandsWithoutLast, allowConcat)) ||
    (allowConcat &&
      resStr.endsWith(lastStr) &&
      isValid(
        +resStr.substring(0, resStr.length - lastStr.length),
        operandsWithoutLast,
        allowConcat,
      ))
  )
}

function solve(equations, allowConcat = false) {
  return equations
    .filter(({ result, operands }) => {
      return isValid(result, operands, allowConcat)
    })
    .reduce((sum, { result }) => sum + result, 0)
}

function part1(equations) {
  return solve(equations)
}

function part2(equations) {
  return solve(equations, true)
}

const inp = readInput()
const equations = parseInput(inp)
console.log('Part 1:', part1(equations))
console.log('Part 2:', part2(equations))
