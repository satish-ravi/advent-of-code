fun readInput(): String {
    return readLine()!!
}

fun getNext(cur: Pair<Int, Int>, dir: Char): Pair<Int, Int> {
    when (dir) {
        '^' -> return Pair(cur.first, cur.second + 1)
        'v' -> return Pair(cur.first, cur.second - 1)
        '>' -> return Pair(cur.first + 1, cur.second)
        '<' -> return Pair(cur.first - 1, cur.second)
        else -> throw Exception("invalid char: $dir")
    }
}

fun part1(input: String): Int {
    val visited = mutableSetOf<Pair<Int, Int>>(Pair(0, 0))
    var cur = Pair(0, 0)
    for (dir in input) {
        cur = getNext(cur, dir)
        visited.add(cur)
    }
    return visited.size
}

fun part2(input: String): Int {
    val visited = mutableSetOf<Pair<Int, Int>>(Pair(0, 0))
    var curSanta = Pair(0, 0)
    var curRobo = Pair(0, 0)
    var isRobo = false
    for (dir in input) {
        if (isRobo) {
            curRobo = getNext(curRobo, dir)
            visited.add(curRobo)
        } else {
            curSanta = getNext(curSanta, dir)
            visited.add(curSanta)
        }
        isRobo = !isRobo
    }
    return visited.size
}

fun main() {
    var input = readInput()
    println("part1: ${part1(input)}")
    println("part2: ${part2(input)}")
}
