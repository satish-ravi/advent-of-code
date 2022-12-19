const fs = require('fs')

class Blueprint {
  constructor(line) {
    const parsedLine = line.match(/\d+/g).map((x) => parseInt(x))
    this.id = parsedLine[0]
    this.oreOre = parsedLine[1]
    this.clayOre = parsedLine[2]
    this.obsidianOre = parsedLine[3]
    this.obsidianClay = parsedLine[4]
    this.geodeOre = parsedLine[5]
    this.geodeObsidian = parsedLine[6]
  }

  _findBest(robots, resources, minRemaining, cache) {
    const key = `${resources.ore},${resources.clay},${resources.obsidian},${resources.geode},${robots.ore},${robots.clay},${robots.obsidian},${robots.geode},${minRemaining}`
    if (cache[key]) return cache[key]
    const nextResources = {
      ore: resources.ore + robots.ore,
      clay: resources.clay + robots.clay,
      obsidian: resources.obsidian + robots.obsidian,
      geode: resources.geode + robots.geode,
    }
    if (minRemaining === 1) {
      return nextResources.geode
    }
    if (
      resources.ore >= this.geodeOre &&
      resources.obsidian >= this.geodeObsidian
    ) {
      cache[key] = this._findBest(
        { ...robots, geode: robots.geode + 1 },
        {
          ...nextResources,
          ore: nextResources.ore - this.geodeOre,
          obsidian: nextResources.obsidian - this.geodeObsidian,
        },
        minRemaining - 1,
        cache,
      )
      return cache[key]
    }
    const options = []
    if (resources.ore <= 8) {
      options.push(
        this._findBest(
          { ...robots },
          { ...nextResources },
          minRemaining - 1,
          cache,
        ),
      )
    }

    if (
      resources.ore >= this.obsidianOre &&
      resources.clay >= this.obsidianClay &&
      robots.obsidian < this.geodeObsidian
    ) {
      options.push(
        this._findBest(
          { ...robots, obsidian: robots.obsidian + 1 },
          {
            ...nextResources,
            ore: nextResources.ore - this.obsidianOre,
            clay: nextResources.clay - this.obsidianClay,
          },
          minRemaining - 1,
          cache,
        ),
      )
    }
    if (
      resources.ore >= this.oreOre &&
      robots.ore <
        Math.max(this.oreOre, this.clayOre, this.obsidianOre, this.geodeOre)
    ) {
      options.push(
        this._findBest(
          { ...robots, ore: robots.ore + 1 },
          {
            ...nextResources,
            ore: nextResources.ore - this.oreOre,
          },
          minRemaining - 1,
          cache,
        ),
      )
    }
    if (resources.ore >= this.clayOre && robots.clay < this.obsidianClay) {
      options.push(
        this._findBest(
          { ...robots, clay: robots.clay + 1 },
          {
            ...nextResources,
            ore: nextResources.ore - this.clayOre,
          },
          minRemaining - 1,
          cache,
        ),
      )
    }
    cache[key] = Math.max(...options)
    return cache[key]
  }

  findBest(minRemaining) {
    return this._findBest(
      { ore: 1, clay: 0, obsidian: 0, geode: 0 },
      { ore: 0, clay: 0, obsidian: 0, geode: 0 },
      minRemaining,
      {},
    )
  }

  getQualityLevel() {
    return this.id * this.findBest(24)
  }
}

function readInput() {
  const file = fs.readFileSync(process.argv[2]).toString()
  return file
    .split('\n')
    .filter((line) => line.length)
    .map((line) => new Blueprint(line))
}

function part1(blueprints) {
  return blueprints
    .map((blueprint) => blueprint.getQualityLevel())
    .reduce((acc, cur) => acc + cur, 0)
}

function part2(blueprints) {
  return blueprints
    .slice(0, 3)
    .map((blueprint) => blueprint.findBest(32))
    .reduce((acc, cur) => acc * cur, 1)
}

const input = readInput()
console.log('part1:', part1(input))
console.log('part2:', part2(input))
