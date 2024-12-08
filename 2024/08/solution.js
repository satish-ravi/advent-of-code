const fs = require('fs')
const { get } = require('http')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  const antennas = {}

  for (let i = 0; i < inp.length; i++) {
    for (let j = 0; j < inp[0].length; j++) {
      if (inp[i][j] === '.') {
        continue
      }
      if (!antennas[inp[i][j]]) {
        antennas[inp[i][j]] = []
      }
      antennas[inp[i][j]].push([i, j])
    }
  }

  return { antennas, gridSize: inp.length }
}

function serialize(x, y) {
  return x * 1000 + y
}

function getAntinodes({ location1, location2, gridSize, maxDistance }) {
  const antinodes = []
  const [x1, y1] = location1
  const [x2, y2] = location2
  const dx = x1 - x2
  const dy = y1 - y2

  let distance = 0
  let outOfBounds1 = false
  let outOfBounds2 = false
  while (distance++ < maxDistance && !(outOfBounds1 && outOfBounds2)) {
    const [nx1, ny1] = [x1 + dx * distance, y1 + dy * distance]
    if (nx1 >= 0 && nx1 < gridSize && ny1 >= 0 && ny1 < gridSize) {
      antinodes.push(serialize(nx1, ny1))
    } else {
      outOfBounds1 = true
    }

    const [nx2, ny2] = [x2 - dx * distance, y2 - dy * distance]
    if (nx2 >= 0 && nx2 < gridSize && ny2 >= 0 && ny2 < gridSize) {
      antinodes.push(serialize(nx2, ny2))
    } else {
      outOfBounds2 = true
    }
  }

  return antinodes
}

function getAllAntinodes({ antennas, gridSize, maxDistance }) {
  const antinodes = new Set()

  for (const locations of Object.values(antennas)) {
    for (let i = 0; i < locations.length; i++) {
      for (let j = i + 1; j < locations.length; j++) {
        getAntinodes({
          location1: locations[i],
          location2: locations[j],
          gridSize,
          maxDistance,
        }).forEach((element) => {
          antinodes.add(element)
        })
      }
    }
  }

  return antinodes
}

function part1({ antennas, gridSize }) {
  return getAllAntinodes({ antennas, gridSize, maxDistance: 1 }).size
}

function part2({ antennas, gridSize }) {
  const antinodes = getAllAntinodes({
    antennas,
    gridSize,
    maxDistance: gridSize,
  })

  for (const locations of Object.values(antennas)) {
    for (const [x, y] of locations) {
      antinodes.add(serialize(x, y))
    }
  }

  return antinodes.size
}

const { antennas, gridSize } = parseInput(readInput())
console.log('Part 1:', part1({ antennas, gridSize }))
console.log('Part 2:', part2({ antennas, gridSize }))
