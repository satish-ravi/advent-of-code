const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function traverse(inp) {
  let pos = null
  for (let i = 0; i < inp.length; i++) {
    for (let j = 0; j < inp[0].length; j++) {
      if (inp[i][j] === '^') {
        pos = [i, j]
        break
      }
    }
    if (pos) break
  }

  const ds = [
    [-1, 0],
    [0, 1],
    [1, 0],
    [0, -1],
  ]

  const visited = new Set()

  let dir = 0
  let cur = pos

  let loop = false

  while (true) {
    const [i, j] = cur
    if (visited.has(dir * 1000000 + i * 1000 + j)) {
      loop = true
      break
    }

    visited.add(dir * 1000000 + i * 1000 + j)

    let [ni, nj] = [i + ds[dir][0], j + ds[dir][1]]

    if (ni < 0 || ni >= inp.length || nj < 0 || nj >= inp[0].length) {
      break
    }

    if (inp[ni][nj] === '#') {
      dir = (dir + 1) % 4
      continue
    }

    cur = [ni, nj]
  }

  const posArr = new Set(Array.from(visited).map((v) => v % 1000000))

  return { posArr, loop, start: pos }
}

function part1(inp) {
  const { posArr } = traverse(inp)
  return posArr.size
}

function part2(inp) {
  const { posArr, start } = traverse(inp)
  let res = 0
  for (const pos of posArr) {
    const i = Math.floor(pos / 1000)
    const j = pos % 1000
    if (i === start[0] && j === start[1]) continue
    let newInp = Array.from(inp)
    newInp[i] = newInp[i].substr(0, j) + '#' + newInp[i].substr(j + 1)

    const { loop } = traverse(newInp)
    if (loop) res++
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
