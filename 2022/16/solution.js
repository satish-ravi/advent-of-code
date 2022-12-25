const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function parseInput(input) {
  const rates = {}
  const edges = {}
  const valves = []
  const nonZeroValves = new Set()
  const valvesToIndices = {}
  for (let i = 0; i < input.length; i++) {
    line = input[i]
    const matches = line.match(/[A-Z]{2}/g)
    const valve = matches[0]
    valves.push(valve)
    edges[valve] = matches.slice(1)
    rates[valve] = parseInt(line.match(/\d+/)[0])
    valvesToIndices[valve] = i
    if (rates[valve] > 0) {
      nonZeroValves.add(valve)
    }
  }
  let distances = Array(valves.length)
    .fill()
    .map(() => Array(valves.length).fill(Number.MAX_SAFE_INTEGER))
  for (let i = 0; i < valves.length; i++) {
    distances[i][i] = 0
    connected = edges[valves[i]]
    for (const v of connected) {
      distances[i][valvesToIndices[v]] = 1
    }
  }
  for (let k = 0; k < valves.length; k++) {
    for (let i = 0; i < valves.length; i++) {
      for (let j = 0; j < valves.length; j++) {
        if (distances[i][j] > distances[i][k] + distances[k][j])
          distances[i][j] = distances[i][k] + distances[k][j]
      }
    }
  }
  return { rates, edges, distances, nonZeroValves, valvesToIndices }
}

function findBest(
  min,
  current,
  pressure,
  openValves,
  valvesToOpen,
  cache,
  valveInfo,
  path,
  max,
) {
  const key = `${current},${min},${Array.from(openValves).join(
    ',',
  )},${pressure}`
  if (cache[key]) {
    return cache[key]
  }
  if (min === max) {
    return { pressure, path }
  }
  let newBest = { pressure, path }
  const newOpenValves = new Set(openValves)
  let nPath = path
  let nMin = min
  let nPressure = pressure

  if (valveInfo.rates[current] > 0) {
    nPath += `open ${current};`
    nMin++
    nPressure += valveInfo.rates[current] * (max - nMin)
    newOpenValves.add(current)
    if (newOpenValves.size === valvesToOpen.size) {
      cache[key] = {
        pressure: nPressure,
        path: nPath,
      }
      return cache[key]
    }
  }
  for (const valve of valvesToOpen) {
    const dist =
      valveInfo.distances[valveInfo.valvesToIndices[current]][
        valveInfo.valvesToIndices[valve]
      ]
    if (valve !== current && !openValves.has(valve) && nMin + dist <= max) {
      const res = findBest(
        nMin + dist,
        valve,
        nPressure,
        newOpenValves,
        valvesToOpen,
        cache,
        valveInfo,
        nPath + `move ${valve};`,
        max,
      )
      if (res.pressure > newBest.pressure) {
        newBest = res
      }
    }
  }
  cache[key] = newBest
  return cache[key]
}

function part1(graph) {
  res = findBest(0, 'AA', 0, new Set(), graph.nonZeroValves, {}, graph, '', 30)
  return res.pressure
}

function part2(graph) {
  const nonZerosArr = Array.from(graph.nonZeroValves)
  let best = -1
  for (let i = 1; i < 2 ** (nonZerosArr.length - 1); i++) {
    const bin = i.toString(2)
    const myValves = new Set()
    for (let b = 0; b < bin.length; b++) {
      if (bin.charAt(b) === '1') {
        myValves.add(nonZerosArr[bin.length - b - 1])
      }
    }
    const eleValves = new Set(nonZerosArr.filter((v) => !myValves.has(v)))
    const human = findBest(0, 'AA', 0, new Set(), myValves, {}, graph, '', 26)
    const ele = findBest(0, 'AA', 0, new Set(), eleValves, {}, graph, '', 26)
    best = Math.max(best, human.pressure + ele.pressure)
  }
  return best
}

const input = readInput()
const graph = parseInput(input)
console.log('part1:', part1(graph))
console.log('part2:', part2(graph))
