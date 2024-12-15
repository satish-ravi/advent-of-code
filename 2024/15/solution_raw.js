const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function ser(r, c) {
  return r * 100 + c
}

function deser(p) {
  return [Math.floor(p / 100), p % 100]
}

function part1(inp) {
  let br = 0
  const walls = new Set()
  const boxes = new Set()
  let robot
  for (let r = 0; r < inp.length; r++) {
    if (inp[r].length == 0) {
      br = r
      break
    }

    for (let c = 0; c < inp[r].length; c++) {
      if (inp[r][c] == '#') {
        walls.add(ser(r, c))
      } else if (inp[r][c] == 'O') {
        boxes.add(ser(r, c))
      } else if (inp[r][c] == '@') {
        robot = ser(r, c)
      }
    }
  }

  const DIRS = {
    '^': ser(-1, 0),
    v: ser(1, 0),
    '<': ser(0, -1),
    '>': ser(0, 1),
  }

  for (let r = br + 1; r < inp.length; r++) {
    for (let c = 0; c < inp[r].length; c++) {
      const dir = inp[r][c]
      const nextRobot = robot + DIRS[dir]
      if (walls.has(nextRobot)) {
        continue
      }
      if (!boxes.has(nextRobot)) {
        robot = nextRobot
        continue
      }

      let boxStart = nextRobot
      let boxEnd = nextRobot

      while (boxes.has(boxEnd)) {
        boxEnd += DIRS[dir]
      }

      if (walls.has(boxEnd)) {
        continue
      }

      boxes.delete(boxStart)
      boxes.add(boxEnd)
      robot = nextRobot
    }
  }

  return Array.from(boxes).reduce((acc, box) => acc + box, 0)
}

function print(rows, cols, walls, boxes, robot) {
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (walls.has(ser(r, c))) {
        process.stdout.write('#')
      } else if (boxes.has(ser(r, c))) {
        process.stdout.write('[')
      } else if (boxes.has(ser(r, c - 1))) {
        process.stdout.write(']')
      } else if (robot == ser(r, c)) {
        process.stdout.write('@')
      } else {
        process.stdout.write('.')
      }
    }
    process.stdout.write('\n')
  }
  process.stdout.write('\n')
}

function part2(inp) {
  let br = 0
  const walls = new Set()
  const boxes = new Set()
  let robot
  for (let r = 0; r < inp.length; r++) {
    if (inp[r].length == 0) {
      br = r
      break
    }

    for (let c = 0; c < inp[r].length; c++) {
      if (inp[r][c] == '#') {
        walls.add(ser(r, 2 * c))
        walls.add(ser(r, 2 * c + 1))
      } else if (inp[r][c] == 'O') {
        boxes.add(ser(r, 2 * c))
      } else if (inp[r][c] == '@') {
        robot = ser(r, 2 * c)
      }
    }
  }

  const DIRS = {
    '^': ser(-1, 0),
    v: ser(1, 0),
    '<': ser(0, -1),
    '>': ser(0, 1),
  }

  for (let r = br + 1; r < inp.length; r++) {
    for (let c = 0; c < inp[r].length; c++) {
      // print(br, inp[0].length * 2, walls, boxes, robot)

      const dir = inp[r][c]
      // console.log('Move', dir)
      const nextRobot = robot + DIRS[dir]
      if (walls.has(nextRobot)) {
        continue
      }
      if (!boxes.has(nextRobot) && !boxes.has(nextRobot - 1)) {
        robot = nextRobot
        continue
      }

      let boxStart = boxes.has(nextRobot) ? nextRobot : nextRobot - 1

      let candidateBoxes = []

      if (dir == '<' || dir == '>') {
        let curBox = boxStart
        while (boxes.has(curBox)) {
          candidateBoxes.push(curBox)
          curBox += 2 * DIRS[dir]
        }

        if (
          (dir === '>' && walls.has(curBox)) ||
          (dir === '<' && walls.has(curBox + 1))
        ) {
          continue
        }
      } else {
        let queue = [boxStart]
        let possible = true
        while (queue.length && possible) {
          let curBox = queue.shift()

          if (
            walls.has(curBox + DIRS[dir]) ||
            walls.has(curBox + DIRS[dir] + 1)
          ) {
            possible = false
            break
          }

          candidateBoxes.push(curBox)
          for (const dc of [-1, 0, 1]) {
            const nextBox = curBox + DIRS[dir] + dc
            if (boxes.has(nextBox)) {
              queue.push(nextBox)
            }
          }
        }

        if (!possible) continue
      }

      for (const box of candidateBoxes) {
        boxes.delete(box)
      }
      for (const box of candidateBoxes) {
        boxes.add(box + DIRS[dir])
      }

      robot = nextRobot
    }
  }

  // print(br, inp[0].length * 2, walls, boxes, robot)

  return Array.from(boxes).reduce((acc, box) => acc + box, 0)
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
