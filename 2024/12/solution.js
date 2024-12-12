const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  const nodes = {}

  for (let i = 0; i < inp.length; i++) {
    for (let j = 0; j < inp[i].length; j++) {
      let horizontalEdges = []
      let verticalEdges = []
      if (i === 0) horizontalEdges.push(j + 1)
      if (j === 0) verticalEdges.push(i + 1)
      if (i === inp.length - 1)
        horizontalEdges.push(-(1000 * (i + 1) + (j + 1)))
      if (j === inp[i].length - 1)
        verticalEdges.push(-(1000 * (j + 1) + (i + 1)))
      nodes[i * 1000 + j] = {
        id: i * 1000 + j,
        val: inp[i][j],
        parent: null,
        horizontalEdges,
        verticalEdges,
      }
    }
  }

  function find(id) {
    if (nodes[id].parent === null) return id
    return find(nodes[id].parent)
  }

  function union(a, b) {
    const rootA = find(a)
    const rootB = find(b)
    if (rootA !== rootB) {
      nodes[rootA].parent = nodes[rootB].id
    }
  }

  for (const node of Object.values(nodes)) {
    for (const [di, dj] of [
      [-1, 0],
      [1, 0],
      [0, -1],
      [0, 1],
    ]) {
      const i = Math.floor(node.id / 1000)
      const j = node.id % 1000
      const ni = i + di
      const nj = j + dj

      if (ni < 0 || nj < 0 || ni >= inp.length || nj >= inp[ni].length) continue

      if (inp[ni][nj] === node.val) {
        union(node.id, ni * 1000 + nj)
      } else {
        if (di === 0)
          node.verticalEdges.push(
            dj === -1 ? (j + 1) * 1000 + i + 1 : -((j + 1) * 1000 + i + 1),
          )
        if (dj === 0)
          node.horizontalEdges.push(
            di === -1 ? (i + 1) * 1000 + j + 1 : -((i + 1) * 1000 + j + 1),
          )
      }
    }
  }

  const groups = {}

  for (const node of Object.values(nodes)) {
    const root = find(node.id)
    if (groups[root] === undefined)
      groups[root] = {
        horizontalEdges: [],
        verticalEdges: [],
        val: nodes[root].val,
        ids: [],
      }
    groups[root].ids.push(node.id)
    groups[root].horizontalEdges.push(...node.horizontalEdges)
    groups[root].verticalEdges.push(...node.verticalEdges)
  }

  return groups
}

function part1(groups) {
  let res = 0

  for (const group of Object.values(groups)) {
    res +=
      group.ids.length *
      (group.horizontalEdges.length + group.verticalEdges.length)
  }

  return res
}

function part2(groups) {
  let res = 0
  for (const group of Object.values(groups)) {
    const sortedHorizontalEdges = group.horizontalEdges.sort((a, b) => a - b)
    const sortedVerticalEdges = group.verticalEdges.sort((a, b) => a - b)

    let h = 1
    for (let i = 1; i < sortedHorizontalEdges.length; i++) {
      if (sortedHorizontalEdges[i] - sortedHorizontalEdges[i - 1] > 1) h++
    }

    let v = 1
    for (let i = 1; i < sortedVerticalEdges.length; i++) {
      if (sortedVerticalEdges[i] - sortedVerticalEdges[i - 1] > 1) v++
    }

    res += group.ids.length * (h + v)
  }

  return res
}

const groups = parseInput(readInput())
console.log('Part 1:', part1(groups))
console.log('Part 2:', part2(groups))
