const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
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

function runProgram(program, A, B, C, expectProg = false) {
  let cur = 0

  A = BigInt(A)
  B = BigInt(B)
  C = BigInt(C)

  const startA = A

  const comboOp = (val) => {
    if (val <= 3) return BigInt(val)
    if (val === 4) return A
    if (val === 5) return B
    if (val === 6) return C
    throw new Error('Invalid comboOp val ' + val)
  }

  const out = []

  // out(B)

  while (cur < program.length - 1) {
    const op = BigInt(program[cur + 1])
    const cOp = comboOp(program[cur + 1])
    switch (program[cur]) {
      case 0:
        A = A >> cOp
        cur += 2
        break
      case 1:
        B = B ^ op
        cur += 2
        break
      case 2:
        B = cOp % 8n
        cur += 2
        break
      case 3:
        if (A !== 0n) {
          cur = Number(op)
          break
        }
        cur += 2
        break
      case 4:
        B = B ^ C
        cur += 2
        break
      case 5:
        out.push(cOp % 8n)
        if (expectProg && out.at(-1) !== BigInt(program[out.length - 1])) {
          if (out.length > 5) {
            console.log('A:', startA, 'out:', out.length)
          }
          return 'NO'
        }
        cur += 2
        break
      case 6:
        B = A >> cOp
        cur += 2
        break
      case 7:
        C = A >> cOp
        cur += 2
        break
      default:
        throw new Error('Invalid op ' + program[cur])
    }
  }

  return out.join(',')
}

function part1(inp) {
  let A = inp[0].match(/(\d+)/g).map(Number)[0]
  let B = inp[1].match(/(\d+)/g).map(Number)[0]
  let C = inp[2].match(/(\d+)/g).map(Number)[0]

  let program = inp[4].match(/(\d+)/g).map(Number)

  return runProgram(program, A, B, C)
}

function part2(inp) {
  const program = inp[4].match(/(\d+)/g).map(Number)

  let candidateAs = new Set()
  candidateAs.add(0n)

  for (let i = program.length - 1; i >= 0; i--) {
    let newCandidateAs = new Set()
    for (const a of candidateAs) {
      for (let v = 0; v < 8; v++) {
        const potentialA = (a << 3n) + BigInt(v)
        if (runOnce(potentialA) === BigInt(program[i])) {
          newCandidateAs.add(potentialA)
        }
      }
    }
    candidateAs = newCandidateAs
  }

  return Array.from(candidateAs).map(String).sort()[0]
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
