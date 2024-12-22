const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  return inp.map(BigInt)
}

function mix(a, b) {
  return a ^ b
}

function prune(a) {
  return a % 16777216n
}

function nextSecret(a) {
  const x = prune(mix(a * 64n, a))
  const y = prune(mix(x / 32n, x))
  return prune(mix(y * 2048n, y))
}

function part1(secrets) {
  return Number(
    secrets
      .map((secret) => {
        let n = secret
        for (let i = 0; i < 2000; i++) {
          n = nextSecret(n)
        }
        return n
      })
      .reduce((a, b) => a + b, 0n),
  )
}

function part2(secrets) {
  const allPrices = {}

  for (const secret of secrets) {
    let n = secret
    let p4, p3, p2, p1, cur
    const keys = new Set()
    for (let i = 0; i < 2000; i++) {
      n = nextSecret(n)
      cur = n % 10n

      if (p4 !== undefined) {
        const key = `${p3 - p4},${p2 - p3},${p1 - p2},${cur - p1}`
        if (!keys.has(key)) {
          keys.add(key)
          if (allPrices[key] === undefined) {
            allPrices[key] = 0n
          }
          allPrices[key] += cur
        }
      }

      p4 = p3
      p3 = p2
      p2 = p1
      p1 = cur
    }
  }

  return Math.max(...Object.values(allPrices).map(Number))
}

const inp = readInput()
const parsed = parseInput(inp)
console.log('Part 1:', part1(parsed))
console.log('Part 2:', part2(parsed))
