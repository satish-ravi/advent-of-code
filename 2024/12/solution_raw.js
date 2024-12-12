const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  let res = 0

  const nodes = {}

  for (let i = 0; i < inp.length; i++) {
    for (let j = 0; j < inp[i].length; j++) {
      let edges = 0
      if (i === 0) edges++
      if (j === 0) edges++
      if (i === inp.length - 1) edges++
      if (j === inp[i].length - 1) edges++
      nodes[i * 1000 + j] = {
        id: i * 1000 + j,
        val: inp[i][j],
        parent: null,
        edges,
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
      const ni = Math.floor(node.id / 1000) + di
      const nj = (node.id % 1000) + dj

      if (ni < 0 || nj < 0 || ni >= inp.length || nj >= inp[ni].length) continue

      if (inp[ni][nj] === node.val) {
        union(node.id, ni * 1000 + nj)
      } else {
        node.edges++
      }
    }
  }

  const groups = {}

  for (const node of Object.values(nodes)) {
    const root = find(node.id)
    if (groups[root] === undefined) groups[root] = []
    groups[root].push(node.id)
  }

  for (const group of Object.values(groups)) {
    res +=
      group.length *
      group.map((id) => nodes[id].edges).reduce((a, b) => a + b, 0)
  }

  return res
}

function part2(inp) {
  let res = 0

  const nodes = {}

  for (let i = 0; i < inp.length; i++) {
    for (let j = 0; j < inp[i].length; j++) {
      let hedges = []
      let vedges = []
      if (i === 0) hedges.push(j + 1)
      if (j === 0) vedges.push(i + 1)
      if (i === inp.length - 1) hedges.push(-(1000 * (i + 1) + (j + 1)))
      if (j === inp[i].length - 1) vedges.push(-(1000 * (j + 1) + (i + 1)))
      nodes[i * 1000 + j] = {
        id: i * 1000 + j,
        val: inp[i][j],
        parent: null,
        hedges,
        vedges,
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
          node.vedges.push(
            dj === -1 ? (j + 1) * 1000 + i + 1 : -((j + 1) * 1000 + i + 1),
          )
        if (dj === 0)
          node.hedges.push(
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
        hedges: [],
        vedges: [],
        val: nodes[root].val,
        ids: [],
      }
    groups[root].ids.push(node.id)
    groups[root].hedges.push(...node.hedges)
    groups[root].vedges.push(...node.vedges)
  }

  for (const group of Object.values(groups)) {
    const sortedHedges = group.hedges.sort((a, b) => a - b)
    const sortedVedges = group.vedges.sort((a, b) => a - b)

    let h = 1
    for (let i = 1; i < sortedHedges.length; i++) {
      if (sortedHedges[i] - sortedHedges[i - 1] > 1) h++
    }

    let v = 1
    for (let i = 1; i < sortedVedges.length; i++) {
      if (sortedVedges[i] - sortedVedges[i - 1] > 1) v++
    }

    res += group.ids.length * (h + v)
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
