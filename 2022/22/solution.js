const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function parseInput(input) {
  const rawMap = input.slice(0, input.length - 1)
  const map = rawMap.map((line) => line.split(''))
  const colStarts = rawMap.map((line) => line.length - line.trim().length)
  const colEnds = rawMap.map((line) => line.length - 1)
  const rowStarts = []
  const rowEnds = []
  for (let c = 0; c < Math.max(...colEnds) + 1; c++) {
    let rs, re
    for (let r = 0; r < rawMap.length; r++) {
      if (rs === undefined && c < map[r].length && map[r][c] !== ' ') {
        rs = r
        continue
      }
      if (rs !== undefined && (c >= map[r].length || map[r][c] === ' ')) {
        re = r - 1
        break
      }
    }
    rowStarts.push(rs)
    rowEnds.push(re ?? rawMap.length - 1)
  }

  const moves = input[input.length - 1].split(/R|L/)
  const dirs = input[input.length - 1].split(/\d+/).slice(1, -1)

  return { map, colStarts, colEnds, rowStarts, rowEnds, moves, dirs }
}

function part1(input) {
  const { map, colStarts, colEnds, rowStarts, rowEnds, moves, dirs } =
    parseInput(input)

  const dirDelta = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0],
  ]

  let r = 0
  let c = colStarts[0]
  let curDir = 0

  for (let i = 0; i < moves.length; i++) {
    const [dr, dc] = dirDelta[curDir]

    for (let j = 0; j < moves[i]; j++) {
      let nr = r + dr
      let nc = c + dc
      if (dr !== 0) {
        if (nr < rowStarts[nc]) {
          nr = rowEnds[nc]
        } else if (nr > rowEnds[nc]) {
          nr = rowStarts[nc]
        }
      } else {
        if (nc < colStarts[nr]) {
          nc = colEnds[nr]
        } else if (nc > colEnds[nr]) {
          nc = colStarts[nr]
        }
      }

      if (map[nr][nc] === '.') {
        r = nr
        c = nc
      } else {
        break
      }
    }

    if (i < dirs.length) {
      if (dirs[i] === 'R') curDir = (curDir + 1) % 4
      else curDir = (curDir + 3) % 4
    }
  }
  return (r + 1) * 1000 + (c + 1) * 4 + curDir
}

function part2(input) {
  let { map, colStarts, colEnds, rowStarts, rowEnds, moves, dirs } =
    parseInput(input)

  const dirDelta = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0],
  ]

  //   12
  //   3
  //  45
  //  6

  //  1 = white
  //  2 = green
  //  3 = orange
  //  4 = blue
  //  5 = yellow
  //  6 = red

  //  1 L -> 4 R flip
  //  2 R -> 5 L flip
  //  4 L -> 1 R flip
  //  5 R -> 2 L flip
  //  3 L -> 4 D flip
  //  4 U -> 3 R flip
  //  1 U -> 6 R flip
  //  2 U -> 6 U
  //  6 L -> 1 D flip
  //  6 D -> 2 D
  //  2 D -> 3 L flip
  //  3 R -> 2 U flip
  //  5 D -> 6 L flip
  //  6 R -> 5 U flip

  let r = 0
  let c = colStarts[0]
  let curDir = 0

  for (let i = 0; i < moves.length; i++) {
    for (let j = 0; j < moves[i]; j++) {
      const [dr, dc] = dirDelta[curDir]
      let nr = r + dr
      let nc = c + dc
      let nDir = curDir
      if (dr !== 0) {
        if (nr < rowStarts[nc]) {
          if (nc < 50) {
            // 4 U -> 3 R
            nr = c + 50
            nc = 50
            nDir = 0
          } else if (nc < 100) {
            // 1 U -> 6 R
            nr = c + 100
            nc = 0
            nDir = 0
          } else {
            // 2 U -> 6 U
            nc = c - 100
            nr = 199
            nDir = 3
          }
        } else if (nr > rowEnds[nc]) {
          if (nc < 50) {
            // 6 D -> 2 D
            nr = 0
            nc = c + 100
            nDir = 1
          } else if (nc < 100) {
            // 5 D -> 6 L
            nr = c + 100
            nc = 49
            nDir = 2
          } else {
            // 2 D -> 3 L
            nr = c - 50
            nc = 99
            nDir = 2
          }
        }
      } else {
        if (nc < colStarts[nr]) {
          if (nr < 50) {
            // 1 L -> 4 R
            nr = 149 - r
            nc = 0
            nDir = 0
          } else if (nr < 100) {
            // 3 L -> 4 D
            nc = r - 50
            nr = 100
            nDir = 1
          } else if (nr < 150) {
            // 4 L -> 1 R
            nc = 50
            nr = 149 - r
            nDir = 0
          } else {
            // 6 L -> 1 D
            nr = 0
            nc = r - 100
            nDir = 1
          }
        } else if (nc > colEnds[nr]) {
          if (nr < 50) {
            // 2 R -> 5 L
            nr = 149 - r
            nc = 99
            nDir = 2
          } else if (nr < 100) {
            // 3 R -> 2 U
            nc = r + 50
            nr = 49
            nDir = 3
          } else if (nr < 150) {
            // 5 R -> 2 L
            nc = 149
            nr = 149 - r
            nDir = 2
          } else {
            // 6 R -> 5 U
            nc = r - 100
            nr = 149
            nDir = 3
          }
        }
      }

      if (map[nr][nc] === '.') {
        r = nr
        c = nc
        curDir = nDir
      } else {
        break
      }
    }

    if (i < dirs.length) {
      if (dirs[i] === 'R') curDir = (curDir + 1) % 4
      else curDir = (curDir + 3) % 4
    }
  }
  return (r + 1) * 1000 + (c + 1) * 4 + curDir
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
