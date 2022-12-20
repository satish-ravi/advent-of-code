const fs = require('fs')

class Node {
  constructor(val) {
    this.val = val
    this.next = null
    this.prev = null
  }
}

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file
    .split('\n')
    .filter((line) => line.length)
    .map((line) => parseInt(line))
}

function createNodes(input) {
  const nodes = {}
  for (let i = 0; i < input.length; i++) {
    nodes[i] = new Node(input[i])
  }
  for (let i = 0; i < input.length; i++) {
    prev = i == 0 ? input.length - 1 : i - 1
    next = i == input.length - 1 ? 0 : i + 1
    nodes[i].prev = nodes[prev]
    nodes[i].next = nodes[next]
  }
  return nodes
}

function solve(input, factor, times) {
  const original = input.map((val) => val * factor)
  const nodes = createNodes(original)
  let zeroth = input.indexOf(0)
  for (let t = 0; t < times; t++) {
    for (let i = 0; i < original.length; i++) {
      const cur = original[i]
      const curNode = nodes[i]
      if (cur === 0) {
        continue
      }
      let node = curNode
      let [dir, moves] = cur > 0 ? ['next', cur] : ['prev', -cur + 1]
      moves = moves % (original.length - 1)
      for (let c = 0; c < moves; c++) {
        node = node[dir]
        if (node === curNode) {
          node = node[dir]
        }
      }
      if (node.next === curNode) {
        continue
      }
      curNode.next.prev = curNode.prev
      curNode.prev.next = curNode.next
      curNode.next = node.next
      curNode.prev = node
      node.next.prev = curNode
      node.next = curNode
    }
  }
  let cur = nodes[zeroth]
  let ans = 0
  for (let i = 1; i <= 3000; i++) {
    cur = cur.next
    if (i % 1000 === 0) {
      ans += cur.val
    }
  }
  return ans
}

function part1(input) {
  return solve(input, 1, 1)
}

function part2(input) {
  return solve(input, 811589153, 10)
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
