const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  let A = inp[0].match(/(\d+)/g).map(BigInt)[0]
  let B = inp[1].match(/(\d+)/g).map(BigInt)[0]
  let C = inp[2].match(/(\d+)/g).map(BigInt)[0]

  let program = inp[4].match(/(\d+)/g).map(BigInt)

  return { A, B, C, program }
}

// B = A % 8
// B = B ^ 3
// C = A >> B
// A = A >> 3
// B = B ^ 5
// B = B ^ C
// out(B % 8)
function runOnce(A) {
  let B = A % 8n
  B = B ^ 3n
  let C = A >> B
  A = A >> 3n
  B = B ^ 5n
  B = B ^ C
  return B % 8n
}

function runProgram({ program, A, B, C }) {
  let cur = 0

  const getComboOperand = (val) => {
    if (val <= 3n) return val
    if (val === 4n) return A
    if (val === 5n) return B
    if (val === 6n) return C
    throw new Error('Invalid comboOp val ' + val)
  }

  const out = []

  while (cur < program.length - 1) {
    const operand = program[cur + 1]
    const comboOperand = getComboOperand(operand)
    switch (Number(program[cur])) {
      case 0:
        A = A >> comboOperand
        cur += 2
        break
      case 1:
        B = B ^ operand
        cur += 2
        break
      case 2:
        B = comboOperand % 8n
        cur += 2
        break
      case 3:
        if (A !== 0n) {
          cur = Number(operand)
          break
        }
        cur += 2
        break
      case 4:
        B = B ^ C
        cur += 2
        break
      case 5:
        out.push(comboOperand % 8n)
        cur += 2
        break
      case 6:
        B = A >> comboOperand
        cur += 2
        break
      case 7:
        C = A >> comboOperand
        cur += 2
        break
      default:
        throw new Error('Invalid op ' + program[cur])
    }
  }

  return out.join(',')
}

function part1({ A, B, C, program }) {
  return runProgram({ program, A, B, C })
}

function part2({ program }) {
  let candidateAs = new Set()
  candidateAs.add(0n)

  for (let i = program.length - 1; i >= 0; i--) {
    let newCandidateAs = new Set()
    for (const a of candidateAs) {
      for (let v = 0; v < 8; v++) {
        const potentialA = (a << 3n) + BigInt(v)
        if (runOnce(potentialA) === program[i]) {
          newCandidateAs.add(potentialA)
        }
      }
    }
    candidateAs = newCandidateAs
  }

  return Array.from(candidateAs).map(String).sort()[0]
}

const inp = readInput()
const parsed = parseInput(inp)
console.log('Part 1:', part1(parsed))
console.log('Part 2:', part2(parsed))
