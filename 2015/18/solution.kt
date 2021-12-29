fun readInput(): Array<Array<Boolean>> {
    val input = generateSequence(::readLine)
    return input.map {
        value ->
        value.map { it == '#' }.toList().toTypedArray()
    }.toList().toTypedArray()
}

fun getNeighbors(i: Int, j: Int, r: Int, c: Int): List<Pair<Int, Int>> {
    var result = mutableListOf<Pair<Int, Int>>()
    for (di in listOf(-1, 0, 1)) {
        for (dj in listOf(-1, 0, 1)) {
            if (di == 0 && dj == 0) {
                continue
            }
            val ni = i + di
            val nj = j + dj
            if (ni >= 0 && ni < r && nj >= 0 && nj < c) {
                result.add(Pair(ni, nj))
            }
        }
    }
    return result
}

fun animate(current: Array<Array<Boolean>>): Array<Array<Boolean>> {
    var result = Array(current.size) { Array(current[0].size) { false } }
    for (i in 0 until current.size) {
        for (j in 0 until current[0].size) {
            var onNeighbors = 0
            for ((ni, nj) in getNeighbors(i, j, current.size, current[0].size)) {
                if (current[ni][nj]) {
                    onNeighbors++
                }
            }
            result[i][j] = (current[i][j] && (onNeighbors == 2 || onNeighbors == 3)) || (!current[i][j] && onNeighbors == 3) // ktlint-disable max-length
        }
    }
    return result
}

fun part1(input: Array<Array<Boolean>>): Int {
    var next = input
    for (i in 1..100) {
        next = animate(next)
    }
    return next.map { row -> row.count { it } }.sum()
}

fun part2(input: Array<Array<Boolean>>): Int {
    var next = input
    next[0][0] = true
    next[0][input[0].size - 1] = true
    next[input.size - 1][0] = true
    next[input.size - 1][input[0].size - 1] = true
    for (i in 1..100) {
        next = animate(next)
        next[0][0] = true
        next[0][input[0].size - 1] = true
        next[input.size - 1][0] = true
        next[input.size - 1][input[0].size - 1] = true
    }
    return next.map { row -> row.count { it } }.sum()
}

fun main() {
    var input = readInput()
    println("part1: ${part1(input)}")
    println("part2: ${part2(input)}")
}
