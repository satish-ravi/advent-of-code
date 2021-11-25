class Circuit(val instructions: HashMap<String, String>) {
    val resolvedValues = HashMap<String,Int>()

    fun get(wire: String): Int {
        if (!resolvedValues.containsKey(wire)) {
            resolvedValues.put(wire, resolve(wire))
        }
        return resolvedValues.getValue(wire)
    }

    fun checkInt(text: String): Int {
        try {
            return text.toInt()
        } catch (ex: NumberFormatException) {
            return get(text)
        }
    }

    fun resolve(wire: String): Int {
        val ins = instructions.getValue(wire)
        val splitIns = ins.split(" ")
        if (splitIns.size == 1) {
            return checkInt(ins)
        } else if ("NOT" in ins) {
            return checkInt(splitIns[1]).inv().and(65535)
        } else if ("AND" in ins) {
            return checkInt(splitIns[0]).and(checkInt(splitIns[2]))
        } else if ("OR" in ins) {
            return checkInt(splitIns[0]).or(checkInt(splitIns[2]))
        } else if ("LSHIFT" in ins) {
            return checkInt(splitIns[0]) shl splitIns[2].toInt()
        } else if ("RSHIFT" in ins) {
            return checkInt(splitIns[0]) shr splitIns[2].toInt()
        }
        throw Exception("invalid instruction: $ins")
    }
}

fun readInput(): HashMap<String,String> {
    val input = generateSequence(::readLine)
    val regex = "(.+) -> (.+)".toRegex()
    val instructions = HashMap<String,String>()
    for (line in input) {
        val (lhs, rhs) = regex.find(line)!!.destructured
        instructions.put(rhs, lhs)
    }
    return instructions
}

fun part1(input: HashMap<String,String>): Int {
    var circuit = Circuit(input)
    return circuit.get("a")
}

fun part2(input: HashMap<String,String>, part1Res: Int): Int {
    input.put("b", part1Res.toString())
    var circuit = Circuit(input)
    return circuit.get("a")
}

fun main() {
    var input = readInput()
    val part1Res = part1(input)
    println("part1: $part1Res")
    println("part2: ${part2(input, part1Res)}")
}
