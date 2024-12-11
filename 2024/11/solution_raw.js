const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function blink(stones) {
  const res = []
  for (const stone of stones) {
    const stonestr = stone.toString()
    if (stone === 0) {
      res.push(1)
    } else if (stonestr.length % 2 === 0) {
      res.push(+stonestr.substr(0, stonestr.length / 2))
      res.push(+stonestr.substr(stonestr.length / 2))
    } else {
      res.push(stone * 2024)
    }
  }
  return res
}

function blink_count(stone, iterations, cache = {}) {
  let cacheKey = `${stone}-${iterations}`
  if (cache[cacheKey]) {
    return cache[cacheKey]
  }

  if (iterations === 0) {
    return 1
  }

  const stonestr = stone.toString()

  if (stone === 0) res = blink_count(1, iterations - 1, cache)
  else if (stonestr.length % 2 === 0) {
    res =
      blink_count(
        +stonestr.substr(0, stonestr.length / 2),
        iterations - 1,
        cache,
      ) +
      blink_count(+stonestr.substr(stonestr.length / 2), iterations - 1, cache)
  } else {
    res = blink_count(stone * 2024, iterations - 1, cache)
  }

  cache[cacheKey] = res
  return res
}

function part1(inp) {
  let res = 0
  let stones = inp[0].split(' ').map(Number)
  for (let i = 0; i < 25; i++) {
    stones = blink(stones)
  }
  return stones.length
}

function part2(inp) {
  let res = 0

  let stones = inp[0].split(' ').map(Number)
  let cache = {}
  for (const stone of stones) {
    res += blink_count(stone, 75, cache)
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
