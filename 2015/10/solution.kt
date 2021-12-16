fun transform(sequence: String): String {
    var prev = sequence[0]
    var count = 1
    var newSequence = ""
    for (i in 1..sequence.length-1) {
        if (sequence[i] == prev) {
            count++
        } else {
            newSequence += count.toString() + prev.toString()
            prev = sequence[i]
            count = 1
        }
    }
    return newSequence + count.toString() + prev.toString()
}

fun transformRegex(sequence: String): String {
    val regex = "(\\d)\\1*".toRegex()
    return regex.findAll(sequence).fold("", { acc, matchResult -> acc + matchResult.value.length + matchResult.value[0]})
}

fun readInput(): String {
    return readLine()!!
}

fun main() {
    var input = readInput()
    var newSequence = input
    for (i in 1..50) {
        newSequence = transform(newSequence)
        if (i == 40) {
            println("part1: ${newSequence.length}")
        }
    }
    println("part2: ${newSequence.length}")
}
