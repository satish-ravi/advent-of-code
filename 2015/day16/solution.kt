data class AuntSue(val number: Int, val properties: HashMap<String, Int>) {
    companion object {
        fun createFromString(strRep: String): AuntSue {
            val regex = "Sue (\\d+): (.*): (\\d+), (.*): (\\d+), (.*): (\\d+)".toRegex()
            val match = regex.matchEntire(strRep)!!
            var (number, p1, val1, p2, val2, p3, val3) = match.destructured
            return AuntSue(number.toInt(), hashMapOf(p1 to val1.toInt(), p2 to val2.toInt(), p3 to val3.toInt()))
        }
    }
}

fun readInput(): List<AuntSue> {
    val input = generateSequence(::readLine);
    return input.map {
        value -> AuntSue.createFromString(value)
    }.toList();
}

fun part1(aunts: List<AuntSue>): Int {
    val tape = hashMapOf("children" to 3, "cats" to 7, "samoyeds" to 2, "pomeranians" to 3, "akitas" to 0, "vizslas" to 0, "goldfish" to 5, "trees" to 3, "cars" to 2, "perfumes" to 1)
    for (aunt in aunts) {
        var isMatch = true
        for ((name, value) in aunt.properties) {
            if (tape[name] != value) {
                isMatch = false
            }
        }
        if (isMatch) {
            return aunt.number
        }
    }
    throw Exception("no match found")
}

fun part2(aunts: List<AuntSue>): Int {
    val tape = hashMapOf("children" to 3, "samoyeds" to 2, "akitas" to 0, "vizslas" to 0, "cars" to 2, "perfumes" to 1)
    val greater = hashMapOf("cats" to 7, "trees" to 3)
    var lesser = hashMapOf("pomeranians" to 3, "goldfish" to 5)
    for (aunt in aunts) {
        var isMatch = true
        for ((name, value) in aunt.properties) {
            if (tape.contains(name) && tape[name] != value) {
                isMatch = false
            }
            if (greater.contains(name) && value <= greater[name]!!) {
                isMatch = false
            }
            if (lesser.contains(name) && value >= lesser[name]!!) {
                isMatch = false
            }
        }
        if (isMatch) {
            return aunt.number
        }
    }
    throw Exception("no match found")
}


fun main() {
    var input = readInput()
    println("part1: ${part1(input)}")
    println("part2: ${part2(input)}")
}
