const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)
}

function toSnafu(num) {
  let base5 = [
    0,
    ...num
      .toString(5)
      .split('')
      .map((digit) => parseInt(digit)),
  ]

  for (let i = base5.length - 1; i > 0; i--) {
    if (base5[i] === 5) {
      base5[i] = 0
      base5[i - 1]++
    } else if (base5[i] === 4) {
      base5[i] = '-'
      base5[i - 1]++
    } else if (base5[i] === 3) {
      base5[i] = '='
      base5[i - 1]++
    }
  }
  if (base5[0] === 0) base5 = base5.slice(1)
  return base5.join('')
}

function fromSnafu(snafu) {
  let num = 0
  for (let i = 0; i < snafu.length; i++) {
    let val = snafu[snafu.length - i - 1]
    if (val === '=') val = -2
    else if (val === '-') val = -1
    else val = parseInt(val)
    num += 5 ** i * val
  }
  return num
}

function part1(input) {
  return toSnafu(
    input.map((snafu) => fromSnafu(snafu)).reduce((acc, cur) => acc + cur, 0),
  )
}

const input = readInput()
console.log('part1:', part1(input))
