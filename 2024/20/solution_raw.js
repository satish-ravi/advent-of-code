const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  let res = 0

  const track = new Set()
  let S = null
  let E = null

  for (let r = 0; r < inp.length; r++) {
    for (let c = 0; c < inp[r].length; c++) {
      if (inp[r][c] === '.') {
        track.add(r * 1000 + c)
      } else if (inp[r][c] === 'S') {
        S = r * 1000 + c
      } else if (inp[r][c] === 'E') {
        E = r * 1000 + c
      }
    }
  }

  track.add(S)
  track.add(E)

  let path = [S]
  let cur = S

  while (cur !== E) {
    const candidates = [cur + 1, cur - 1, cur + 1000, cur - 1000]

    const n = candidates.filter((c) => track.has(c) && path.at(-2) !== c)

    if (n.length !== 1) {
      throw new Error('Invalid path')
    }

    path.push(n[0])
    cur = n[0]
  }

  D = 100

  for (let i = 0; i < path.length - D - 3; i++) {
    for (let j = i + D + 2; j < path.length; j++) {
      const [r1, c1] = [Math.floor(path[i] / 1000), path[i] % 1000]
      const [r2, c2] = [Math.floor(path[j] / 1000), path[j] % 1000]

      if (Math.abs(r1 - r2) + Math.abs(c1 - c2) <= 2) {
        res++
      }
    }
  }

  return res
}

function part2(inp) {
  let res = 0

  const track = new Set()
  let S = null
  let E = null

  for (let r = 0; r < inp.length; r++) {
    for (let c = 0; c < inp[r].length; c++) {
      if (inp[r][c] === '.') {
        track.add(r * 1000 + c)
      } else if (inp[r][c] === 'S') {
        S = r * 1000 + c
      } else if (inp[r][c] === 'E') {
        E = r * 1000 + c
      }
    }
  }

  track.add(S)
  track.add(E)

  let path = [S]
  let cur = S

  while (cur !== E) {
    const candidates = [cur + 1, cur - 1, cur + 1000, cur - 1000]

    const n = candidates.filter((c) => track.has(c) && path.at(-2) !== c)

    if (n.length !== 1) {
      throw new Error('Invalid path')
    }

    path.push(n[0])
    cur = n[0]
  }

  D = 100

  for (let i = 0; i < path.length - D - 3; i++) {
    for (let j = i + D + 2; j < path.length; j++) {
      const [r1, c1] = [Math.floor(path[i] / 1000), path[i] % 1000]
      const [r2, c2] = [Math.floor(path[j] / 1000), path[j] % 1000]

      if (Math.abs(r1 - r2) + Math.abs(c1 - c2) <= Math.min(20, j - i - D)) {
        res++
      }
    }
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
