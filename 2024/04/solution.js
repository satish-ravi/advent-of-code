const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

const ALL_DIRS = [
  [-1, -1],
  [-1, 0],
  [-1, 1],
  [0, -1],
  [0, 1],
  [1, -1],
  [1, 0],
  [1, 1],
]

function part1(matrix) {
  let res = 0
  const [m, n] = [matrix.length, matrix[0].length]
  for (let i = 0; i < m; i++) {
    for (let j = 0; j < n; j++) {
      if (matrix[i][j] !== 'X') {
        continue
      }
      for (let [di, dj] of ALL_DIRS) {
        if (
          i + di * 3 < 0 ||
          i + di * 3 >= m ||
          j + dj * 3 < 0 ||
          j + dj * 3 >= n
        ) {
          continue
        }
        if (
          matrix[i + di][j + dj] === 'M' &&
          matrix[i + di * 2][j + dj * 2] === 'A' &&
          matrix[i + di * 3][j + dj * 3] === 'S'
        ) {
          res++
        }
      }
    }
  }
  return res
}

function part2(matrix) {
  let res = 0
  for (let i = 1; i < matrix.length - 1; i++) {
    for (let j = 1; j < matrix[i].length - 1; j++) {
      if (matrix[i][j] !== 'A') {
        continue
      }
      const [tl, tr, bl, br] = [
        matrix[i - 1][j - 1],
        matrix[i - 1][j + 1],
        matrix[i + 1][j - 1],
        matrix[i + 1][j + 1],
      ]
      if (tl === 'M' && tr === 'S' && bl === 'M' && br === 'S') {
        res++
      }
      if (tl === 'M' && tr === 'M' && bl === 'S' && br === 'S') {
        res++
      }
      if (tl === 'S' && tr === 'S' && bl === 'M' && br === 'M') {
        res++
      }
      if (tl === 'S' && tr === 'M' && bl === 'S' && br === 'M') {
        res++
      }
    }
  }
  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
