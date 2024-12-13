const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  const machines = []

  for (let i = 0; i < inp.length; i += 4) {
    const [ax, ay] = inp[i].match(/-?\d+/g).map(Number)
    const [bx, by] = inp[i + 1].match(/-?\d+/g).map(Number)
    const [px, py] = inp[i + 2].match(/-?\d+/g).map(Number)

    machines.push({ buttonA: [ax, ay], buttonB: [bx, by], prize: [px, py] })
  }

  return machines
}

function solveLinearEquations(a1, b1, c1, a2, b2, c2) {
  // Solve one equation for one variable
  let x = (c2 - b2 * (c1 / b1)) / (a2 - b2 * (a1 / b1))
  let y = (c1 - a1 * x) / b1
  return [parseFloat(x.toFixed(3)), parseFloat(y.toFixed(3))]
}

function solve(machines, prizeAddOn = 0) {
  let res = 0

  for (let i = 0; i < machines.length; i++) {
    const { buttonA, buttonB, prize } = machines[i]

    const [a, b] = solveLinearEquations(
      buttonA[0],
      buttonB[0],
      prize[0] + prizeAddOn,
      buttonA[1],
      buttonB[1],
      prize[1] + prizeAddOn,
    )

    if (
      a >= 0 &&
      b >= 0 &&
      !a.toString().includes('.') &&
      !b.toString().includes('.')
    ) {
      res += a * 3 + b
    }
  }

  return res
}

const machines = parseInput(readInput())
console.log('Part 1:', solve(machines))
console.log('Part 2:', solve(machines, 10000000000000))
