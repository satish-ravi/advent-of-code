const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function parseCubes(cubeStrings) {
  return cubeStrings.map((cs) => cs.split(',').map((v) => parseInt(v)))
}

const dirs = [
  [1, 0, 0],
  [-1, 0, 0],
  [0, 1, 0],
  [0, -1, 0],
  [0, 0, 1],
  [0, 0, -1],
]

function getExposedSides(input) {
  const cubes = new Set(input)
  const parsedCubes = parseCubes(input)
  const exposedSides = []
  for (const [x, y, z] of parsedCubes) {
    exposedSides.push(
      ...dirs
        .map(([dx, dy, dz]) => [x + dx, y + dy, z + dz].join(','))
        .filter((side) => !cubes.has(side)),
    )
  }
  return exposedSides
}

function part1(input) {
  return getExposedSides(input).length
}

function part2(input) {
  const cubes = new Set(input)
  const parsedCubes = parseCubes(input)
  const mins = Array(3).fill(Number.MAX_VALUE)
  const maxs = Array(3).fill(-1)
  for (const cube of parsedCubes) {
    for (let i = 0; i < 3; i++) {
      if (cube[i] < mins[i]) {
        mins[i] = cube[i]
      }
      if (cube[i] > maxs[i]) {
        maxs[i] = cube[i]
      }
    }
  }
  for (let i = 0; i < 3; i++) {
    mins[i]--
    maxs[i]++
  }

  let queue = []
  queue.push([...mins])
  const filled = new Set([mins.join(',')])

  while (queue.length > 0) {
    const [x, y, z] = queue[queue.length - 1]
    queue.pop()

    for (const [dx, dy, dz] of dirs) {
      const n = [x + dx, y + dy, z + dz]
      const ns = n.join(',')
      if (
        !filled.has(ns) &&
        !cubes.has(ns) &&
        n.every((v, i) => v >= mins[i] && v <= maxs[i])
      ) {
        filled.add(ns)
        queue.push(n)
      }
    }
  }

  const exposedSides = getExposedSides(input)
  return exposedSides.filter((side) => filled.has(side)).length
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
