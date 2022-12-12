const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file
    .split('\n')
    .filter((line) => line.length)
    .map((line) => line.split(''))
}

function solve(input) {
  const queue = new Set([])
  const edges = {}
  const vals = {}
  const dist = {}
  for (let i = 0; i < input.length; i++) {
    for (let j = 0; j < input[0].length; j++) {
      const curVal = input[i][j]
      const cur = `${i},${j}`
      queue.add(cur)
      edges[cur] = []
      vals[cur] = curVal
      dist[cur] = curVal === 'E' ? 0 : Number.MAX_SAFE_INTEGER
      for (const [di, dj] of [
        [-1, 0],
        [1, 0],
        [0, 1],
        [0, -1],
      ]) {
        const ni = i + di
        const nj = j + dj
        if (ni >= 0 && ni < input.length && nj >= 0 && nj < input[0].length) {
          const adjVal = input[ni][nj]
          const adj = `${ni},${nj}`
          if (adjVal === 'S') {
            if (curVal === 'a') {
              edges[cur].push(adj)
            }
          } else if (curVal === 'E') {
            if (adjVal === 'z') {
              edges[cur].push(adj)
            }
          } else if (
            adjVal.charCodeAt(0) - curVal.charCodeAt(0) === -1 ||
            adjVal.charCodeAt(0) - curVal.charCodeAt(0) >= 0
          ) {
            edges[cur].push(adj)
          }
        }
      }
    }
  }
  while (queue.size) {
    let cur = Array.from(queue)[0]
    for (const item of Array.from(queue)) {
      if (dist[item] < dist[cur]) {
        cur = item
      }
    }
    queue.delete(cur)
    for (const n of edges[cur]) {
      if (queue.has(n) && dist[cur] + 1 < dist[n]) {
        dist[n] = dist[cur] + 1
      }
    }
  }
  return dist
}

function part1(input, dist) {
  for (let i = 0; i < input.length; i++) {
    for (let j = 0; j < input[0].length; j++) {
      if (input[i][j] === 'S') {
        return dist[`${i},${j}`]
      }
    }
  }
}

function part2(input, dist) {
  let minDist = Number.MAX_SAFE_INTEGER
  for (let i = 0; i < input.length; i++) {
    for (let j = 0; j < input[0].length; j++) {
      if (input[i][j] === 'S' || input[i][j] === 'a') {
        const curDist = dist[`${i},${j}`]
        minDist = Math.min(minDist, curDist)
      }
    }
  }
  return minDist
}

const input = readInput()
const dist = solve(input)
console.log('part1:', part1(input, dist))
console.log('part2:', part2(input, dist))
