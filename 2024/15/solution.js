const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function serialize(r, c) {
  return r * 100 + c
}

function deserialize(p) {
  return [Math.floor(p / 100), p % 100]
}

const DIRS = {
  '^': serialize(-1, 0),
  v: serialize(1, 0),
  '<': serialize(0, -1),
  '>': serialize(0, 1),
}

function parseInput(inp) {
  let endOfMap
  const walls = new Set()
  const boxes = new Set()
  let robot
  for (let r = 0; r < inp.length; r++) {
    if (inp[r].length == 0) {
      endOfMap = r
      break
    }

    for (let c = 0; c < inp[r].length; c++) {
      if (inp[r][c] == '#') {
        walls.add(serialize(r, c))
      } else if (inp[r][c] == 'O') {
        boxes.add(serialize(r, c))
      } else if (inp[r][c] == '@') {
        robot = serialize(r, c)
      }
    }
  }

  const moves = []
  for (let r = endOfMap + 1; r < inp.length; r++) {
    for (let c = 0; c < inp[r].length; c++) {
      moves.push(inp[r][c])
    }
  }

  return { walls, boxes, robot, moves }
}

function part1({ walls, boxes, robot, moves }) {
  boxes = new Set(boxes)
  for (const move of moves) {
    const nextRobot = robot + DIRS[move]
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
      boxEnd += DIRS[move]
    }

    if (walls.has(boxEnd)) {
      continue
    }

    boxes.delete(boxStart)
    boxes.add(boxEnd)
    robot = nextRobot
  }

  return Array.from(boxes).reduce((acc, box) => acc + box, 0)
}

function part2({ walls, boxes, robot, moves }) {
  robot = serialize(deserialize(robot)[0], deserialize(robot)[1] * 2)
  boxes = new Set(
    Array.from(boxes).map((box) =>
      serialize(deserialize(box)[0], deserialize(box)[1] * 2),
    ),
  )
  walls = new Set(
    Array.from(walls).map((wall) =>
      serialize(deserialize(wall)[0], deserialize(wall)[1] * 2),
    ),
  )
  for (const wall of Array.from(walls)) {
    walls.add(wall + 1)
  }

  for (const move of moves) {
    const nextRobot = robot + DIRS[move]
    if (walls.has(nextRobot)) {
      continue
    }
    if (!boxes.has(nextRobot) && !boxes.has(nextRobot - 1)) {
      robot = nextRobot
      continue
    }

    let collidingBox = boxes.has(nextRobot) ? nextRobot : nextRobot - 1

    let candidateBoxes = []

    if (move === '<' || move === '>') {
      let curBox = collidingBox
      while (boxes.has(curBox)) {
        candidateBoxes.push(curBox)
        curBox += 2 * DIRS[move]
      }

      if (
        (move === '>' && walls.has(curBox)) ||
        (move === '<' && walls.has(curBox + 1))
      ) {
        continue
      }
    } else {
      let queue = [collidingBox]
      let possible = true
      while (queue.length && possible) {
        let curBox = queue.shift()

        if (
          walls.has(curBox + DIRS[move]) ||
          walls.has(curBox + DIRS[move] + 1)
        ) {
          possible = false
          break
        }

        candidateBoxes.push(curBox)
        for (const dc of [-1, 0, 1]) {
          const nextBox = curBox + DIRS[move] + dc
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
      boxes.add(box + DIRS[move])
    }

    robot = nextRobot
  }

  return Array.from(boxes).reduce((acc, box) => acc + box, 0)
}

const parsed = parseInput(readInput())
console.log('Part 1:', part1(parsed))
console.log('Part 2:', part2(parsed))
