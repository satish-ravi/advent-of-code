const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  let res = 0

  const connections = {}

  for (const line of inp) {
    const [a, b] = line.split('-')
    if (!connections[a]) connections[a] = new Set()
    if (!connections[b]) connections[b] = new Set()
    connections[a].add(b)
    connections[b].add(a)
  }

  const visited = new Set()

  for (const node1 of Object.keys(connections)) {
    c1 = connections[node1]
    for (const node2 of c1) {
      c2 = connections[node2]
      for (const node3 of c2) {
        if (node3 === node1) continue
        if (!c1.has(node3)) continue
        const nodes = [node1, node2, node3].sort()
        const key = nodes.join(',')
        if (!visited.has(key)) {
          visited.add(key)
          if (
            nodes[0].startsWith('t') ||
            nodes[1].startsWith('t') ||
            nodes[2].startsWith('t')
          ) {
            res++
          }
        }
      }
    }
  }

  return res
}

function findLargestClique(graph) {
  // Bron–Kerbosch algorithm
  function bronKerbosch(R, P, X) {
    if (P.length === 0 && X.length === 0) {
      cliques.push(R)
      return
    }

    const pivot = P[0] || X[0]
    const neighbors = graph[pivot] || []
    const candidates = P.filter((node) => !neighbors.has(node))

    for (const node of candidates) {
      const newR = [...R, node]
      const newP = P.filter((n) => graph[node].has(n))
      const newX = X.filter((n) => graph[node].has(n))

      bronKerbosch(newR, newP, newX)

      P.splice(P.indexOf(node), 1)
      X.push(node)
    }
  }

  const cliques = []
  bronKerbosch([], Object.keys(graph), [])
  return cliques
}

function part2(inp) {
  const connections = {}

  for (const line of inp) {
    const [a, b] = line.split('-')
    if (!connections[a]) connections[a] = new Set()
    if (!connections[b]) connections[b] = new Set()
    connections[a].add(b)
    connections[b].add(a)
  }

  const cliques = findLargestClique(connections)

  return cliques
    .reduce((max, clique) => (clique.length > max.length ? clique : max), [])
    .sort()
    .join(',')
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
