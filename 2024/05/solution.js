const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  const graph = {}
  const pageNumbers = []

  let row = 0

  while (inp[row] !== '') {
    const [p1, p2] = inp[row].split('|').map(Number)
    if (!graph[p1]) graph[p1] = new Set()
    if (!graph[p2]) graph[p2] = new Set()
    graph[p1].add(p2)
    row++
  }

  while (row++ < inp.length - 1) {
    pageNumbers.push(inp[row].split(',').map(Number))
  }

  return { graph, pageNumbers }
}

function getValidAndInvalidPageNumbers({ graph, pageNumbers }) {
  const validPages = []
  const invalidPages = []

  for (const pages of pageNumbers) {
    let valid = true

    for (let i = 0; i < pages.length - 1; i++) {
      for (let j = i + 1; j < pages.length; j++) {
        if (!graph[pages[i]].has(pages[j])) {
          valid = false
          break
        }
      }
      if (!valid) break
    }

    if (valid) {
      validPages.push(pages)
    } else {
      invalidPages.push(pages)
    }
  }

  return { validPages, invalidPages }
}

function getMiddlePageNumberSum(pageNumbers) {
  return pageNumbers.reduce(
    (acc, pages) => acc + pages[Math.floor(pages.length / 2)],
    0,
  )
}

function part1({ validPages }) {
  return getMiddlePageNumberSum(validPages)
}

function getValidatedPage({ invalidPage, graph }) {
  const pageNumbersWithScore = []
  for (let i = 0; i < invalidPage.length; i++) {
    let score = 0
    for (let j = 0; j < invalidPage.length; j++) {
      if (graph[invalidPage[i]].has(invalidPage[j])) {
        score++
      }
    }
    pageNumbersWithScore.push({ page: invalidPage[i], score })
  }

  pageNumbersWithScore.sort((a, b) => b.score - a.score)

  return pageNumbersWithScore.map(({ page }) => page)
}

function part2({ invalidPages, graph }) {
  return getMiddlePageNumberSum(
    invalidPages.map((invalidPage) => getValidatedPage({ invalidPage, graph })),
  )
}

const inp = readInput()
const { graph, pageNumbers } = parseInput(inp)
const { validPages, invalidPages } = getValidAndInvalidPageNumbers({
  graph,
  pageNumbers,
})
console.log('Part 1:', part1({ validPages }))
console.log('Part 2:', part2({ invalidPages, graph }))
