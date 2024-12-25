const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  let res = 0
  const lk = inp
    .join('\n')
    .split('\n\n')
    .map((x) => x.split('\n'))

  const locks = []
  const keys = []

  for (const item of lk) {
    const isKey = item[0].startsWith('.')
    const itemNum = []
    for (let c = 0; c < item[0].length; c++) {
      let n = 0
      for (let r = 1; r < item.length; r++) {
        if (item[r][c] === '#') n++
      }
      itemNum.push(isKey ? n - 1 : n)
    }
    if (isKey) keys.push(itemNum)
    else locks.push(itemNum)
  }

  for (const key of keys) {
    for (const lock of locks) {
      let match = true
      for (let i = 0; i < key.length; i++) {
        if (key[i] + lock[i] > 5) {
          match = false
          break
        }
      }
      if (match) res++
    }
  }

  return res
}

function part2(inp) {
  let res = 0
  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
