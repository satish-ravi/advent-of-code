const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  return inp[0].split(' ').map(Number)
}

function get_stone_count(stone, iterations, cache = {}) {
  let cacheKey = `${stone}-${iterations}`
  if (cache[cacheKey]) {
    return cache[cacheKey]
  }

  if (iterations === 0) {
    return 1
  }

  const stonestr = stone.toString()

  if (stone === 0) res = get_stone_count(1, iterations - 1, cache)
  else if (stonestr.length % 2 === 0) {
    res =
      get_stone_count(
        +stonestr.substr(0, stonestr.length / 2),
        iterations - 1,
        cache,
      ) +
      get_stone_count(
        +stonestr.substr(stonestr.length / 2),
        iterations - 1,
        cache,
      )
  } else {
    res = get_stone_count(stone * 2024, iterations - 1, cache)
  }

  cache[cacheKey] = res
  return res
}

function solve(stones, iterations) {
  let res = 0

  let cache = {}
  for (const stone of stones) {
    res += get_stone_count(stone, iterations, cache)
  }

  return res
}

const stones = parseInput(readInput())
console.log('Part 1:', solve(stones, 25))
console.log('Part 2:', solve(stones, 75))
