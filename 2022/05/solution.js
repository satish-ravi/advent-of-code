const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(input) {
  const stackEndIdx = input.findIndex((line) => line.startsWith(' 1'))
  const numStacks = input[stackEndIdx].split('').filter((x) => x != ' ').length
  const stacks = []
  for (let stackNum = 0; stackNum < numStacks; stackNum++) {
    const idx = stackNum * 4 + 1
    let stack = ''
    for (let lineIdx = stackEndIdx - 1; lineIdx >= 0; lineIdx--) {
      if (!input[lineIdx][idx] || input[lineIdx][idx] === ' ') {
        break
      }
      stack += input[lineIdx][idx]
    }
    stacks.push(stack)
  }

  const moves = input
    .slice(stackEndIdx + 2)
    .filter((line) => line.startsWith('move'))
    .map((line) => {
      const [num, src, dest] = [...line.matchAll(/(\d+)/g)].map(
        (match) => match[0],
      )
      return { num, src: src - 1, dest: dest - 1 }
    })

  return { stacks, moves }
}

function solve({ stacks: origStack, moves }, rev) {
  const stacks = [...origStack]
  for (const { num, src, dest } of moves) {
    const mv = stacks[src].substring(stacks[src].length - num)
    stacks[src] = stacks[src].substring(0, stacks[src].length - num)
    stacks[dest] = stacks[dest] + (rev ? mv.split('').reverse().join('') : mv)
  }
  let ans = ''
  for (const stack of stacks) {
    ans += stack[stack.length - 1]
  }
  return ans
}

const input = readInput()
const { stacks, moves } = parseInput(input)
console.log('part1:', solve({ stacks, moves }, true))
console.log('part2:', solve({ stacks, moves }, false))
