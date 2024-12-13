const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function solveLinearEquations(a1, b1, c1, a2, b2, c2) {
  // Solve one equation for one variable
  let x = (c2 - b2 * (c1 / b1)) / (a2 - b2 * (a1 / b1))
  let y = (c1 - a1 * x) / b1
  return [parseFloat(x.toFixed(3)), parseFloat(y.toFixed(3))]
}

function part1(inp) {
  let res = 0

  for (let i = 0; i < inp.length; i += 4) {
    const [ax, ay] = inp[i].match(/-?\d+/g).map(Number)
    const [bx, by] = inp[i + 1].match(/-?\d+/g).map(Number)
    const [px, py] = inp[i + 2].match(/-?\d+/g).map(Number)

    const [a, b] = solveLinearEquations(ax, bx, px, ay, by, py)

    if (a >= 0 && b >= 0 && (a | 0) === a && (b | 0) === b) {
      res += a * 3 + b
    }
  }

  return res
}

function part2(inp) {
  let res = 0

  for (let i = 0; i < inp.length; i += 4) {
    const [ax, ay] = inp[i].match(/-?\d+/g).map(Number)
    const [bx, by] = inp[i + 1].match(/-?\d+/g).map(Number)
    const [px, py] = inp[i + 2].match(/-?\d+/g).map(Number)

    const [a, b] = solveLinearEquations(
      ax,
      bx,
      px + 10000000000000,
      ay,
      by,
      py + 10000000000000,
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

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
