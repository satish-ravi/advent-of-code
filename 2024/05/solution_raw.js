const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function topologicalSort(pairs) {
  const graph = {}
  const inDegree = {}

  // Build the graph and calculate in-degrees
  for (const [u, v] of pairs) {
    if (!graph[u]) graph[u] = []
    if (!graph[v]) graph[v] = []
    graph[u].push(v)

    inDegree[v] = (inDegree[v] || 0) + 1
    if (!inDegree[u]) inDegree[u] = 0
  }

  return graph
}

function part1(inp) {
  let res = 0

  let r = 0
  let pairs = []
  while (inp[r] !== '') {
    pairs.push(inp[r].split('|'))
    r++
  }

  const graph = topologicalSort(pairs)

  while (r++ < inp.length - 1) {
    const cur = inp[r].split(',')

    let valid = true

    for (let i = 0; i < cur.length - 1; i++) {
      for (let j = i + 1; j < cur.length; j++) {
        if (!graph[cur[i]].includes(cur[j])) {
          valid = false
          break
        }
      }
      if (!valid) break
    }

    if (valid) {
      res += +cur[Math.floor(cur.length / 2)]
    }
  }

  return res
}

function part2(inp) {
  let res = 0

  let r = 0
  let pairs = []
  while (inp[r] !== '') {
    pairs.push(inp[r].split('|'))
    r++
  }

  const graph = topologicalSort(pairs)

  while (r++ < inp.length - 1) {
    const cur = inp[r].split(',')

    let valid = true

    for (let i = 0; i < cur.length - 1; i++) {
      for (let j = i + 1; j < cur.length; j++) {
        if (!graph[cur[i]].includes(cur[j])) {
          valid = false
          break
        }
      }
      if (!valid) break
    }

    if (!valid) {
      const nums = []

      for (let i = 0; i < cur.length; i++) {
        let after = 0
        for (let j = 0; j < cur.length; j++) {
          if (i === j) continue
          if (graph[cur[i]].includes(cur[j])) {
            after++
          }
        }
        nums.push([cur[i], after])
      }

      nums.sort((a, b) => b[1] - a[1])

      res += +nums[Math.floor(cur.length / 2)][0]
    }
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
