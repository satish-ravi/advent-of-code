const fs = require('fs')

function ser(r, c) {
  return `${r},${c}`
}

function deser(st) {
  const [r, c] = st.split(',').map((x) => parseInt(x))
  return { r, c }
}

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function parseInput(input) {
  const elves = new Set()
  for (let r = 0; r < input.length; r++) {
    for (let c = 0; c < input[0].length; c++) {
      if (input[r][c] === '#') {
        elves.add(ser(r, c))
      }
    }
  }
  return elves
}

function doRound(elves, round) {
  const proposals = {}
  const dests = {}
  for (const elf of Array.from(elves)) {
    const { r, c } = deser(elf)
    let needsToMove = false
    for (const dr of [-1, 0, 1]) {
      for (const dc of [-1, 0, 1]) {
        if (dc === 0 && dr === 0) {
          continue
        }
        if (elves.has(ser(r + dr, c + dc))) {
          needsToMove = true
          break
        }
      }
      if (needsToMove) break
    }
    if (!needsToMove) {
      continue
    }

    const north = {
      fn: () =>
        [-1, 0, 1].map((dc) => ser(r - 1, c + dc)).every((p) => !elves.has(p)),
      dest: ser(r - 1, c),
    }
    const south = {
      fn: () =>
        [-1, 0, 1].map((dc) => ser(r + 1, c + dc)).every((p) => !elves.has(p)),
      dest: ser(r + 1, c),
    }
    const west = {
      fn: () =>
        [-1, 0, 1].map((dr) => ser(r + dr, c - 1)).every((p) => !elves.has(p)),
      dest: ser(r, c - 1),
    }
    const east = {
      fn: () =>
        [-1, 0, 1].map((dr) => ser(r + dr, c + 1)).every((p) => !elves.has(p)),
      dest: ser(r, c + 1),
    }

    const checks = [north, south, west, east]
    let dest
    for (let i = 0; i < 4; i++) {
      if (checks[(i + round) % 4].fn()) {
        dest = checks[(i + round) % 4].dest
        break
      }
    }
    if (dest) {
      proposals[elf] = dest
      if (!dests[dest]) dests[dest] = 0
      dests[dest]++
    }
  }

  let newElves = new Set()
  for (const elf of Array.from(elves)) {
    if (!proposals[elf] || dests[proposals[elf]] > 1) {
      newElves.add(elf)
    } else {
      newElves.add(proposals[elf])
    }
  }

  return { elves: newElves, moves: Object.keys(proposals).length }
}

function part1(input) {
  let elves = parseInput(input)
  for (let i = 0; i < 10; i++) {
    elves = doRound(elves, i).elves
  }

  let minr = Number.MAX_SAFE_INTEGER
  let minc = Number.MAX_SAFE_INTEGER
  let maxr = Number.MIN_SAFE_INTEGER
  let maxc = Number.MIN_SAFE_INTEGER
  for (const elf of Array.from(elves)) {
    const { r, c } = deser(elf)
    minr = Math.min(minr, r)
    minc = Math.min(minc, c)
    maxr = Math.max(maxr, r)
    maxc = Math.max(maxc, c)
  }

  let grid = ''
  let ans = 0

  for (let r = minr; r <= maxr; r++) {
    for (let c = minc; c <= maxc; c++) {
      if (!elves.has(ser(r, c))) {
        ans++
        grid += '.'
      } else {
        grid += '#'
      }
    }
    grid += '\n'
  }
  return ans
}

function part2(input) {
  let elves = parseInput(input)
  let round = 0
  while (true) {
    res = doRound(elves, round++)
    if (res.moves === 0) {
      return round
    }
    elves = res.elves
  }
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
