const exp = require('constants')
const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function parseInput(inp) {
  const gates = {}
  const expressions = {}

  let parsingGate = true
  for (const line of inp) {
    if (line === '') {
      parsingGate = false
      continue
    }
    if (parsingGate) {
      const [gate, val] = line.split(': ')
      gates[gate] = Number(val)
    } else {
      const [lhs, rhs] = line.split(' -> ')
      const [op1, op, op2] = lhs.split(' ')

      expressions[rhs] = [op1, op, op2]
    }
  }

  return { gates, expressions }
}

function resolveGates({ gates, expressions, gate }) {
  if (gates[gate] !== undefined) {
    return gates[gate]
  }

  const [op1, op, op2] = expressions[gate]
  const resolvedOp1 = resolveGates({ gates, expressions, gate: op1 })
  const resolvedOp2 = resolveGates({ gates, expressions, gate: op2 })

  let res
  if (op === 'AND') {
    res = resolvedOp1 & resolvedOp2
  } else if (op === 'OR') {
    res = resolvedOp1 | resolvedOp2
  } else if (op === 'XOR') {
    res = resolvedOp1 ^ resolvedOp2
  }

  gates[gate] = res
  return res
}

function getBinaryValue({ resolvedGates, prefix }) {
  return parseInt(
    Object.keys(resolvedGates)
      .filter((gate) => gate.startsWith(prefix))
      .sort()
      .reverse()
      .map((key) => resolvedGates[key].toString())
      .join(''),
    2,
  )
}

function part1({ gates, expressions }) {
  const zGates = Object.keys(expressions).filter((r) => r.startsWith('z'))

  const resolvedGates = { ...gates }

  for (const gate of zGates) {
    resolveGates({ gates: resolvedGates, expressions, gate })
  }

  return getBinaryValue({ resolvedGates, prefix: 'z' })

  return parseInt(
    zGates
      .sort()
      .reverse()
      .map((key) => resolvedGates[key].toString())
      .join(''),
    2,
  )
}

function resolveExpressions({ expressions, cache, gate }) {
  if (cache[gate] !== undefined) {
    return cache[gate]
  }
  let resolvedOp1
  let resolvedOp2
  const [op1, op, op2] = expressions[gate]
  if (op1.startsWith('x') || op1.startsWith('y')) {
    resolvedOp1 = op1
  } else {
    resolvedOp1 = `(${resolveExpressions({ expressions, cache, gate: op1 })})`
  }
  if (op2.startsWith('x') || op2.startsWith('y')) {
    resolvedOp2 = op2
  } else {
    resolvedOp2 = `(${resolveExpressions({ expressions, cache, gate: op2 })})`
  }

  if (
    (resolvedOp1.startsWith('y') && resolvedOp2.startsWith('x')) ||
    resolvedOp1.length > resolvedOp2.length ||
    (resolvedOp1.length === resolvedOp2.length &&
      resolvedOp1.includes('AND') &&
      resolvedOp2.includes('XOR'))
  ) {
    const temp = resolvedOp1
    resolvedOp1 = resolvedOp2
    resolvedOp2 = temp
  }

  cache[gate] = `${resolvedOp1} ${op} ${resolvedOp2}`
  return cache[gate]
}

function resolveAndPrintExpressions({ expressions, gates }) {
  const cache = {}
  for (const gate of gates.sort()) {
    console.log(
      gate +
        ':' +
        resolveExpressions({ expressions, cache, gate }).substring(0, 100),
    )
  }
}

function part2({ gates, expressions }) {
  const zGates = Object.keys(expressions)
    .filter((r) => r.startsWith('z'))
    .sort()

  resolveAndPrintExpressions({ expressions, gates: zGates })

  const resolvedGates = { ...gates }
  for (const gate of zGates) {
    resolveGates({ gates: resolvedGates, expressions, gate })
  }

  const xValue = getBinaryValue({ resolvedGates, prefix: 'x' })
  const yValue = getBinaryValue({ resolvedGates, prefix: 'y' })

  if (
    getBinaryValue({ resolvedGates: gates, prefix: 'z' }) ===
    xValue + yValue
  ) {
    throw new Error('z should not be x + y')
  }

  // wrong zs: z09, z13, z19, z33
  // z09 fix: gws <-> nnt

  // z13 fix:
  // fmh OR tqs -> z13
  // x13 AND y13 -> fmh
  // hgw AND kvr -> tqs
  // x13 XOR y13 -> kvr
  // hgw XOR kvr -> npf
  // npf <-> z13

  // z19 fix:
  // y19 AND x19 -> z19
  // x19 XOR y19 -> fnq
  // rsm XOR fnq -> cph
  // z19 <-> cph

  // z33 fix:
  // wgq AND wtm -> z33
  // x33 XOR y33 -> wtm
  // wtm XOR wgq -> hgj
  // z33 <-> hgj

  const newExpressions = expressions

  const swap = (gate1, gate2) => {
    const temp = newExpressions[gate1]
    newExpressions[gate1] = newExpressions[gate2]
    newExpressions[gate2] = temp
  }

  swap('gws', 'nnt')
  swap('z13', 'npf')
  swap('z19', 'cph')
  swap('z33', 'hgj')

  resolveAndPrintExpressions({ expressions: newExpressions, gates: zGates })

  const newResolvedGates = { ...gates }
  for (const gate of zGates) {
    resolveGates({ gates: newResolvedGates, expressions: newExpressions, gate })
  }

  if (
    getBinaryValue({ resolvedGates: newResolvedGates, prefix: 'z' }) !==
    xValue + yValue
  ) {
    throw new Error('z should be x + y')
  }

  return ['gws', 'nnt', 'z13', 'npf', 'z19', 'cph', 'z33', 'hgj']
    .sort()
    .join(',')
}

const inp = readInput()
const parsed = parseInput(inp)
console.log('Part 1:', part1(parsed))
console.log('Part 2:', part2(parsed))
