const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(input) {
  const store = {}

  function addToStore(curDir, item, val) {
    let curLoc = store
    const path = curDir.split('/').slice(1)
    for (const folder of path) {
      curLoc = curLoc[folder]
    }
    curLoc[item] = val
  }

  let curDir = ''
  for (const line of input.slice(1)) {
    if (line.startsWith('$ cd ')) {
      const [, , dir] = line.split(' ')
      if (dir === '..') {
        const paths = curDir.split('/')
        curDir = paths.slice(0, paths.length - 1).join('/')
      } else {
        curDir = curDir + '/' + dir
      }
    } else if (line.startsWith('$ ls')) {
      continue
    } else if (line.startsWith('dir')) {
      dir = line.split(' ')[1]
      addToStore(curDir, dir, {})
    } else if (line.length) {
      const [size, file] = line.split(' ')
      addToStore(curDir, file, parseInt(size))
    }
  }

  const sizes = {}
  computeSize(store, sizes, '/')

  return { store, sizes }

  const totalOccupied = sizes['/']
  const freeSpace = 70000000 - totalOccupied
  const required = 30000000 - freeSpace

  console.log(required)

  console.log(
    Math.min(...Object.values(sizes).filter((size) => size >= required)),
  )
}

function computeSize(dir, mem, prefix) {
  let size = 0
  Object.entries(dir).forEach(([key, val]) => {
    if (typeof val === 'object') {
      size += computeSize(val, mem, prefix + key + '/')
    } else {
      size += val
    }
  })
  mem[prefix] = size
  return size
}

function part1(sizes) {
  return Object.values(sizes)
    .filter((size) => size <= 100000)
    .reduce((acc, cur) => acc + cur)
}

function part2(sizes) {
  const totalOccupied = sizes['/']
  const freeSpace = 70000000 - totalOccupied
  const required = 30000000 - freeSpace

  return Math.min(...Object.values(sizes).filter((size) => size >= required))
}

const { sizes } = parseInput(readInput())
console.log('part1:', part1(sizes))
console.log('part2:', part2(sizes))
