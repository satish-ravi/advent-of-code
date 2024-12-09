const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  let res = 0

  let ids = []
  let sps = []

  for (let i = 0; i < inp[0].length; i++) {
    if (i % 2 === 0) {
      ids.push(+inp[0][i])
    } else {
      sps.push(+inp[0][i])
    }
  }

  let fw = 0

  let total = ids.reduce((a, b) => a + b)

  let curId = 0
  let curSp = 0
  let atId = true
  let curIdIdx = 0
  let curSpIdx = 0
  let revId = ids.length - 1
  let revIdIdx = 0

  while (fw < total) {
    if (atId) {
      if (curIdIdx === ids[curId]) {
        curIdIdx = 0
        atId = false
        curId++
        continue
      }
      res += fw * curId
      curIdIdx++
    } else {
      if (curSpIdx === sps[curSp]) {
        curSpIdx = 0
        atId = true
        curSp++
        continue
      }
      if (revIdIdx === ids[revId]) {
        revIdIdx = 0
        revId--
      }
      res += fw * revId
      revIdIdx++
      curSpIdx++
    }
    fw++
  }

  return res
}

function part2(inp) {
  let res = 0

  let ids = []
  let sps = []

  let pos = 0

  for (let i = 0; i < inp[0].length; i++) {
    if (i % 2 === 0) {
      ids.push([+inp[0][i], pos])
    } else {
      sps.push([+inp[0][i], pos])
    }
    pos += +inp[0][i]
  }

  for (let i = ids.length - 1; i >= 0; i--) {
    for (let j = 0; j < sps.length; j++) {
      if (sps[j][0] >= ids[i][0] && ids[i][1] > sps[j][1]) {
        ids[i][1] = sps[j][1]
        sps[j][0] -= ids[i][0]
        sps[j][1] += ids[i][0]
        break
      }
    }
  }

  for (let i = 0; i < ids.length; i++) {
    for (let r = 0; r < ids[i][0]; r++) {
      res += i * (ids[i][1] + r)
    }
  }

  return res
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
