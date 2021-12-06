fun readInput(): Pair<Map<String, List<String>>, String> {
    val input = generateSequence(::readLine)
    val replacements = hashMapOf<String, MutableList<String>>()
    var initial = ""
    val replacementRegex = "(.*) => (.*)".toRegex()
    for (line in input) {
        if (line == "") {
            continue
        } else if (line.contains(" => ")) {
            val match = replacementRegex.matchEntire(line)!!
            val (lhs, rhs) = match.destructured
            if (replacements.contains(lhs)) {
                replacements.get(lhs)!!.add(rhs)
            } else {
                replacements.put(lhs, mutableListOf(rhs))
            }
        } else {
            initial = line
        }
    }
    return Pair(replacements, initial)
}

fun part1(replacements: Map<String, List<String>>, initial: String): Int {
    val results = hashSetOf<String>()
    var token = ""
    var tokenStart = 0
    for (i in 0 until initial.length) {
        token += initial[i]
        if (replacements.contains(token)) {
            for (rhs in replacements.get(token)!!) {
                println("replaceing ${token} with ${rhs} at ${tokenStart}, ${i} to get |${initial.slice(0..tokenStart-1) + rhs + initial.slice(i+1..initial.length-1)}|")
                results.add(initial.slice(0..tokenStart-1) + rhs + initial.slice(i+1..initial.length-1))
            }
            token = ""
            tokenStart = i + 1
        } else if (initial[i].isLowerCase()) {
            token = ""
            tokenStart = i + 1
        }
    }
    print(results)
    return results.size
}

fun main() {
    var (replacements, initial) = readInput()
    println("part1: ${part1(replacements, initial)}")
    // println("part2: ${part2(input)}")
}
