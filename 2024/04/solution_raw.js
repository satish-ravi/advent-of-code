const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

const dirs = [
  [-1, -1],
  [-1, 0],
  [-1, 1],
  [0, -1],
  [0, 1],
  [1, -1],
  [1, 0],
  [1, 1],
]

function part1(inp) {
  let res = 0
  let mat = inp.map((x) => x.split(''))
  for (let i = 0; i < mat.length; i++) {
    for (let j = 0; j < mat[i].length; j++) {
      if (mat[i][j] !== 'X') {
        continue
      }
      for (let [dx, dy] of dirs) {
        if (
          i + dx * 3 < 0 ||
          i + dx * 3 >= mat.length ||
          j + dy * 3 < 0 ||
          j + dy * 3 >= mat[i].length
        ) {
          continue
        }
        if (
          mat[i + dx][j + dy] === 'M' &&
          mat[i + dx * 2][j + dy * 2] === 'A' &&
          mat[i + dx * 3][j + dy * 3] === 'S'
        ) {
          res++
        }
      }
    }
  }
  return res
}

function part2(inp) {
  let res = 0
  let mat = inp.map((x) => x.split(''))
  for (let i = 1; i < mat.length - 1; i++) {
    for (let j = 1; j < mat[i].length - 1; j++) {
      if (mat[i][j] !== 'A') {
        continue
      }
      if (
        mat[i - 1][j - 1] === 'M' &&
        mat[i - 1][j + 1] === 'S' &&
        mat[i + 1][j - 1] === 'M' &&
        mat[i + 1][j + 1] === 'S'
      ) {
        res++
      }
      if (
        mat[i - 1][j - 1] === 'M' &&
        mat[i - 1][j + 1] === 'M' &&
        mat[i + 1][j - 1] === 'S' &&
        mat[i + 1][j + 1] === 'S'
      ) {
        res++
      }
      if (
        mat[i - 1][j - 1] === 'S' &&
        mat[i - 1][j + 1] === 'S' &&
        mat[i + 1][j - 1] === 'M' &&
        mat[i + 1][j + 1] === 'M'
      ) {
        res++
      }
      if (
        mat[i - 1][j - 1] === 'S' &&
        mat[i - 1][j + 1] === 'M' &&
        mat[i + 1][j - 1] === 'S' &&
        mat[i + 1][j + 1] === 'M'
      ) {
        res++
      }
    }
  }
  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
