const fs = require('fs')

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file.split('\n')
}

function part1(inp) {
  const gates = {}
  const expressions = []
  const results = []
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

      expressions.push([op1, op, op2, rhs])
      results.push(rhs)
    }
  }

  const zGates = new Set(results.filter((r) => r.startsWith('z')))

  while (zGates.size) {
    for (const [op1, op, op2, res] of expressions) {
      if (
        gates[op1] !== undefined &&
        gates[op2] !== undefined &&
        gates[res] === undefined
      ) {
        if (op === 'AND') {
          gates[res] = gates[op1] & gates[op2]
        } else if (op === 'OR') {
          gates[res] = gates[op1] | gates[op2]
        } else if (op === 'XOR') {
          gates[res] = gates[op1] ^ gates[op2]
        }
        zGates.delete(res)
      }
    }
  }

  let resVal = ''

  for (const key of results.filter((r) => r.startsWith('z')).sort()) {
    resVal += gates[key].toString()
  }

  return parseInt(resVal.split('').reverse().join(''), 2)
}

function resolve(gates, expressions, cache, key) {
  if (cache[key] !== undefined) {
    return cache[key]
  }
  let resolvedOp1
  let resolvedOp2
  const [op1, op, op2] = expressions[key]
  if (op1.startsWith('x') || op1.startsWith('y')) {
    resolvedOp1 = op1
  } else {
    resolvedOp1 = `(${resolve(gates, expressions, cache, op1)})`
  }
  if (op2.startsWith('x') || op2.startsWith('y')) {
    resolvedOp2 = op2
  } else {
    resolvedOp2 = `(${resolve(gates, expressions, cache, op2)})`
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

  cache[key] = `${resolvedOp1} ${op} ${resolvedOp2}`
  return cache[key]
}

function swap(expressions, a, b) {
  const temp = expressions[a]
  expressions[a] = expressions[b]
  expressions[b] = temp
}

function part2(inp) {
  const gates = {}
  const expressions = {}
  const results = []
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
      results.push(rhs)
    }
  }
  const zGates = results.filter((r) => r.startsWith('z')).sort()

  let cache = {}
  for (const key of zGates) {
    console.log(
      key + ':' + resolve(gates, expressions, cache, key).substring(0, 100),
    )
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

  swap(expressions, 'gws', 'nnt')
  swap(expressions, 'z13', 'npf')
  swap(expressions, 'z19', 'cph')
  swap(expressions, 'z33', 'hgj')

  cache = {}
  for (const key of zGates) {
    console.log(
      key + ':' + resolve(gates, expressions, cache, key).substring(0, 100),
    )
  }

  return ['gws', 'nnt', 'z13', 'npf', 'z19', 'cph', 'z33', 'hgj']
    .sort()
    .join(',')
}

const inp = readInput()
console.log('Part 1:', part1(inp))
console.log('Part 2:', part2(inp))
