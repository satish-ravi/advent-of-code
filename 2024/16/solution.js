const fs = require('fs')

class PriorityQueue {
  constructor() {
    this.heap = []
  }

  enqueue(node, priority) {
    this.heap.push({ node, priority })
    this.bubbleUp()
  }

  dequeue() {
    if (this.size() === 1) return this.heap.pop()
    const min = this.heap[0]
    this.heap[0] = this.heap.pop()
    this.bubbleDown()
    return min
  }

  bubbleUp() {
    let index = this.heap.length - 1
    while (index > 0) {
      const parentIndex = Math.floor((index - 1) / 2)
      if (this.heap[index].priority >= this.heap[parentIndex].priority) break
      ;[this.heap[index], this.heap[parentIndex]] = [
        this.heap[parentIndex],
        this.heap[index],
      ]
      index = parentIndex
    }
  }

  bubbleDown() {
    let index = 0
    const length = this.heap.length
    while (true) {
      const leftChildIndex = 2 * index + 1
      const rightChildIndex = 2 * index + 2
      let smallest = index

      if (
        leftChildIndex < length &&
        this.heap[leftChildIndex].priority < this.heap[smallest].priority
      ) {
        smallest = leftChildIndex
      }
      if (
        rightChildIndex < length &&
        this.heap[rightChildIndex].priority < this.heap[smallest].priority
      ) {
        smallest = rightChildIndex
      }
      if (smallest === index) break
      ;[this.heap[index], this.heap[smallest]] = [
        this.heap[smallest],
        this.heap[index],
      ]
      index = smallest
    }
  }

  size() {
    return this.heap.length
  }
}

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

const ser = (r, c) => r * 1000 + c
const DIRS = [ser(0, 1), ser(0, -1), ser(1, 0), ser(-1, 0)]

const serNode = (pos, dir) => `${pos},${dir}`
const deserNode = (node) => node.split(',').map(Number)

function parseInput(inp) {
  const walls = new Set()
  let start, end

  for (let r = 0; r < inp.length; r++) {
    for (let c = 0; c < inp[r].length; c++) {
      if (inp[r][c] === '#') {
        walls.add(ser(r, c))
      } else if (inp[r][c] === 'S') {
        start = ser(r, c)
      } else if (inp[r][c] === 'E') {
        end = ser(r, c)
      }
    }
  }

  return { walls, start, end }
}

function part1({ walls, start, end }) {
  const q = new PriorityQueue()
  q.enqueue(serNode(start, 1), 0)

  const visited = new Set()
  const distances = {}
  while (q.size() > 0) {
    const { node, priority: dist } = q.dequeue()
    if (visited.has(node)) continue
    visited.add(node)

    const [cur, dir] = deserNode(node)
    if (cur === end) {
      return dist
    }
    for (const d of DIRS) {
      if (d !== dir && Math.abs(d) === Math.abs(dir)) {
        continue
      }
      const next = cur + d
      let new_dist = dist + 1
      if (d !== dir) {
        new_dist += 1000
      }
      const nextNode = serNode(next, d)
      if (
        walls.has(next) ||
        (distances[nextNode] && distances[nextNode] < new_dist)
      ) {
        continue
      }
      distances[nextNode] = new_dist
      q.enqueue(nextNode, new_dist)
    }
  }

  throw new Error('No path found')
}

function part2({ walls, start, end }) {
  const q = new PriorityQueue()
  q.enqueue([serNode(start, 1)], 0)

  const distances = {}
  let bestPath = Infinity
  const bestPathNodes = new Set()
  while (q.size() > 0) {
    const { node: path, priority: dist } = q.dequeue()
    const node = path[path.length - 1]
    if (dist > bestPath) {
      break
    }

    const [cur, dir] = deserNode(node)
    if (cur === end) {
      if (dist < bestPath) {
        bestPath = dist
        bestPathNodes.clear()
      }
      for (const n of path) {
        bestPathNodes.add(deserNode(n)[0])
      }
    }
    for (const d of DIRS) {
      if (d !== dir && Math.abs(d) === Math.abs(dir)) {
        continue
      }
      const next = cur + d
      let new_dist = dist + 1
      if (d !== dir) {
        new_dist += 1000
      }
      const nextNode = serNode(next, d)
      if (
        walls.has(next) ||
        (distances[nextNode] && distances[nextNode] < new_dist)
      ) {
        continue
      }
      distances[nextNode] = new_dist
      q.enqueue([...path, nextNode], new_dist)
    }
  }

  return bestPathNodes.size
}

const inp = readInput()
const parsed = parseInput(inp)
console.log('Part 1:', part1(parsed))
console.log('Part 2:', part2(parsed))
