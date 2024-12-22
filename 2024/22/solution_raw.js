const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
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

function part1(inp) {
  let res = 0n

  for (const line of inp) {
    let n = BigInt(line)
    for (let i = 0; i < 2000; i++) {
      n = nextSecret(n)
    }
    res += n
  }

  return res
}

function part2(inp) {
  const allPrices = {}

  for (const line of inp) {
    const prices = []
    let n = BigInt(line)
    for (let i = 0; i < 2000; i++) {
      n = nextSecret(n)
      prices.push(n % 10n)
    }

    const priceMap = new Set()

    for (let i = 4; i < prices.length; i++) {
      const d0 = prices[i - 3] - prices[i - 4]
      const d1 = prices[i - 2] - prices[i - 3]
      const d2 = prices[i - 1] - prices[i - 2]
      const d3 = prices[i] - prices[i - 1]

      const key = `${d0},${d1},${d2},${d3}`

      if (!priceMap.has(key)) {
        priceMap.add(key)
        if (allPrices[key] === undefined) {
          allPrices[key] = 0n
        }
        allPrices[key] += prices[i]
      }
    }
  }

  return Math.max(...Object.values(allPrices).map(Number))
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
