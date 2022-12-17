const fs = require('fs')

const rocks = [
  [parseInt('0011110', 2)],
  [parseInt('0001000', 2), parseInt('0011100', 2), parseInt('0001000', 2)],
  [parseInt('0000100', 2), parseInt('0000100', 2), parseInt('0011100', 2)],
  [
    parseInt('0010000', 2),
    parseInt('0010000', 2),
    parseInt('0010000', 2),
    parseInt('0010000', 2),
  ],
  [parseInt('0011000', 2), parseInt('0011000', 2)],
]

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n').filter((line) => line.length)[0]
}
function solve(input, numRocks) {
  let chamber = Array(10000000).fill(0)
  let maxHeight = -1
  let marker = false
  let jet = 0
  for (let rn = 0; rn < numRocks; rn++) {
    let rock = rocks[rn % rocks.length]
    let ry = maxHeight + 3 + rock.length
    while (true) {
      if (jet % input.length === 0) {
        marker = true
        console.log(rn % 5, chamber.slice(maxHeight - 5, maxHeight), ry)
      }
      const dir = input.charAt(jet++ % input.length)
      if (
        dir === '>' &&
        rock.every((row) => (row & 1) === 0) &&
        rock.every((row, index) => ((row >> 1) & chamber[ry - index]) === 0)
      ) {
        rock = rock.map((row) => row >> 1)
        // console.log('shifting right', ry, rock)
      }
      if (
        dir === '<' &&
        rock.every((row) => (row & 64) === 0) &&
        rock.every((row, index) => ((row << 1) & chamber[ry - index]) === 0)
      ) {
        rock = rock.map((row) => row << 1)
        // console.log('shifting left', ry, rock)
      }

      if (
        rock.some(
          (row, index) =>
            ry - index - 1 < 0 || (row & chamber[ry - index - 1]) !== 0,
        )
      ) {
        // console.log('landing', ry, rock)
        rock.forEach((row, index) => {
          chamber[ry - index] |= row
        })
        maxHeight = Math.max(ry, maxHeight)
        if (marker && rn % 5 === 4) {
          console.log(rn, maxHeight, chamber.slice(maxHeight - 5, maxHeight))
          marker = false
        }
        if ((rn - 4 - 745) % 1750 === 0) {
          console.log(rn, maxHeight, chamber.slice(maxHeight - 5, maxHeight))
        }
        break
      }
      ry--
    }
  }
  return maxHeight + 1
}

function part1(input) {
  return solve(input, 2022)
}

function part2(input) {
  solve(input, 8000)
  return ((1000000000000 - 1 - 7749) / 1750) * 2781 + 12355 + 1
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
