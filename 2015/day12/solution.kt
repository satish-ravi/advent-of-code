fun readInput(): String {
    return readLine()!!
}

fun part1(input: String): Int {
    val regex = "(-?\\d+)".toRegex()
    return regex.findAll(input).fold(0, { acc, match -> acc + match.value.toInt() })
}

fun main() {
    var input = readInput()
    println("part1: ${part1(input)}")
}
