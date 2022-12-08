const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file
    .split('\n')
    .filter((line) => line.length)
    .map((line) => line.split('').map((x) => parseInt(x)))
}

function part1(input) {
  R = input.length
  C = input[0].length

  let maxLeft = [...Array(R)].map((x) => Array(C))
  let maxRight = [...Array(R)].map((x) => Array(C))
  let maxTop = [...Array(R)].map((x) => Array(C))
  let maxBottom = [...Array(R)].map((x) => Array(C))
  for (let i = 0; i < R; i++) {
    maxLeft[i][0] = -1
    for (let j = 1; j < C; j++) {
      maxLeft[i][j] = Math.max(maxLeft[i][j - 1], input[i][j - 1])
    }
  }
  for (let i = 0; i < R; i++) {
    maxRight[i][C - 1] = -1
    for (let j = C - 2; j >= 0; j--) {
      maxRight[i][j] = Math.max(maxRight[i][j + 1], input[i][j + 1])
    }
  }
  for (let j = 0; j < C; j++) {
    maxTop[0][j] = -1
    for (let i = 1; i < R; i++) {
      maxTop[i][j] = Math.max(maxTop[i - 1][j], input[i - 1][j])
    }
  }
  for (let j = 0; j < C; j++) {
    maxBottom[R - 1][j] = -1
    for (let i = R - 2; i >= 0; i--) {
      maxBottom[i][j] = Math.max(maxBottom[i + 1][j], input[i + 1][j])
    }
  }
  let ans = 0
  for (let i = 0; i < R; i++) {
    for (let j = 0; j < C; j++) {
      if (
        input[i][j] >
        Math.min(maxLeft[i][j], maxRight[i][j], maxTop[i][j], maxBottom[i][j])
      ) {
        ans++
      }
    }
  }
  return ans
}

function part2(input) {
  R = input.length
  C = input[0].length

  let maxScore = 1
  for (i = 1; i < R - 1; i++) {
    for (j = 1; j < C - 1; j++) {
      let di = i - 1
      while (di > 0 && input[di][j] < input[i][j]) {
        di--
      }
      const up = i - di
      di = i + 1
      while (di < R - 1 && input[di][j] < input[i][j]) {
        di++
      }
      const down = di - i
      let dj = j - 1
      while (dj > 0 && input[i][dj] < input[i][j]) {
        dj--
      }
      const left = j - dj
      dj = j + 1
      while (dj < C - 1 && input[i][dj] < input[i][j]) {
        dj++
      }
      const right = dj - j
      const score = up * down * left * right
      maxScore = Math.max(score, maxScore)
    }
  }
  return maxScore
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
