const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  let ids = []
  let spaces = []

  let position = 0

  for (let i = 0; i < inp[0].length; i++) {
    if (i % 2 === 0) {
      ids.push({ length: +inp[0][i], position })
    } else {
      spaces.push({ length: +inp[0][i], position })
    }
    position += +inp[0][i]
  }

  return { ids, spaces }
}

function part1({ ids, spaces }) {
  let res = 0
  let pos = 0

  const lastPosition = ids.reduce((a, b) => a + b.length, 0)

  console.log(lastPosition)

  let curId = 0
  let curSpace = 0
  let posAtId = true
  let posAtCurId = 0
  let posAtCurSpace = 0
  let curReverseId = ids.length - 1
  let posAtCurRevId = 0

  while (pos < lastPosition) {
    if (posAtId) {
      if (posAtCurId === ids[curId].length) {
        posAtCurId = 0
        posAtId = false
        curId++
        continue
      }
      res += pos * curId
      posAtCurId++
    } else {
      if (posAtCurSpace === spaces[curSpace].length) {
        posAtCurSpace = 0
        posAtId = true
        curSpace++
        continue
      }
      if (posAtCurRevId === ids[curReverseId].length) {
        posAtCurRevId = 0
        curReverseId--
      }
      res += pos * curReverseId
      posAtCurRevId++
      posAtCurSpace++
    }
    pos++
  }

  return res
}

function part2({ ids, spaces }) {
  let res = 0

  for (let i = ids.length - 1; i >= 0; i--) {
    for (
      let j = 0;
      j < spaces.length && spaces[j].position < ids[i].position; // if spaces starts after position of id, we can stop
      j++
    ) {
      if (spaces[j].length >= ids[i].length) {
        ids[i].position = spaces[j].position
        spaces[j].length -= ids[i].length
        spaces[j].position += ids[i].length
        break
      }
    }
  }

  for (let i = 0; i < ids.length; i++) {
    for (let r = 0; r < ids[i].length; r++) {
      res += i * (ids[i].position + r)
    }
  }

  return res
}

const { ids, spaces } = parseInput(readInput())
console.log('Part 1:', part1({ ids, spaces }))
console.log('Part 2:', part2({ ids, spaces }))
