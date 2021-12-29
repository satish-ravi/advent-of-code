fun readInput(): List<String> {
    val input = generateSequence(::readLine)
    return input.toList()
}

fun countBackslashes(str: String): Int {
    return "\\\\\\\\".toRegex().findAll(str).toList().size
}

fun countQuotes(str: String): Int {
    return "\\\\\"".toRegex().findAll(str.drop(1).dropLast(1)).toList().size
}

fun countHex(str: String): Int {
    return "\\\\x..".toRegex().findAll(str.replace("\\\\\\\\".toRegex(), "")).toList().size
}

fun part1(input: List<String>): Int {
    return input.fold(0, { acc, text -> acc + 2 + countBackslashes(text) + countQuotes(text) + 3 * countHex(text) })
}

fun part2(input: List<String>): Int {
    return input.fold(0, { acc, text -> acc + 4 + 2 * countBackslashes(text) + 2 * countQuotes(text) + countHex(text) })
}

fun main() {
    var input = readInput()
    println("part1: ${part1(input)}")
    println("part2: ${part2(input)}")
}
