fun readInput(): Triple<Map<String, List<String>>, Map<String, List<String>>, String> {
    val input = generateSequence(::readLine)
    val replacements = hashMapOf<String, MutableList<String>>()
    val reverseReplacements = hashMapOf<String, MutableList<String>>()
    var molecule = ""
    val replacementRegex = "(.*) => (.*)".toRegex()
    for (line in input) {
        if (line == "") {
            continue
        } else if (line.contains(" => ")) {
            val match = replacementRegex.matchEntire(line)!!
            val (lhs, rhs) = match.destructured
            replacements.getOrPut(lhs) { ArrayList<String>() }.add(rhs)
            reverseReplacements.getOrPut(rhs) { ArrayList<String>() }.add(lhs)
        } else {
            molecule = line
        }
    }
    return Triple(replacements, reverseReplacements, molecule)
}

fun get_replacements(replacements: Map<String, List<String>>, molecule: String): HashSet<String> {
    val results = hashSetOf<String>()
    for ((lhs, rhs_list) in replacements) {
        for (i in 0 until molecule.length - lhs.length + 1) {
            if (lhs == molecule.slice(i..i + lhs.length - 1)) {
                for (rhs in rhs_list) {
                    results.add(molecule.slice(0..i - 1) + rhs + molecule.slice(i + lhs.length..molecule.length - 1))
                }
            }
        }
    }
    return results
}

fun part1(replacements: Map<String, List<String>>, molecule: String): Int {
    return get_replacements(replacements, molecule).size
}

fun part2Slow(replacements: Map<String, List<String>>, molecule: String): Int {
    var queue = ArrayDeque<Pair<Int, String>>()
    queue.add(Pair(0, "e"))
    var visited = HashSet<String>()
    while (queue.size > 0) {
        var (steps, current_molecule) = queue.removeFirst()
        visited.add(current_molecule)
        if (current_molecule == molecule) {
            return steps
        }
        if (current_molecule.length >= molecule.length) {
            continue
        }
        for (next_molecule in get_replacements(replacements, current_molecule)) {
            if (!visited.contains(next_molecule)) {
                queue.add(Pair(steps + 1, next_molecule))
            }
        }
    }
    throw Exception("no path found")
}

fun breakBySubstring(main: String, sub: String): List<Pair<String, String>> {
    var result = mutableListOf<Pair<String, String>>()
    for (i in 0 until main.length - sub.length + 1) {
        if (main.slice(i..i + sub.length - 1) == sub) {
            result.add(Pair(main.slice(0..i - 1), main.slice(i + sub.length..main.length - 1)))
        }
    }
    return result
}

fun findShortest(
    revReplacements: Map<String, List<String>>,
    molecule: String,
    currentStep: Int,
    known: HashMap<String, Int>,
    currentKnownBest: Int
): Int {
    if (known.contains(molecule)) {
        var knownBest = known.get(molecule)!!
        return if (knownBest == Int.MAX_VALUE) Int.MAX_VALUE else currentStep + knownBest
    }
    if (currentStep + 1 >= currentKnownBest) {
        return Int.MAX_VALUE
    }
    var knownBest = Int.MAX_VALUE
    for ((rhs, lhsList) in revReplacements) {
        for ((left, right) in breakBySubstring(molecule, rhs)) {
            for (lhs in lhsList) {
                var shortest = findShortest(revReplacements, left + lhs + right, currentStep + 1, known, knownBest)
                if (shortest < knownBest) {
                    knownBest = shortest
                }
            }
        }
    }
    known.put(molecule, knownBest)
    return knownBest
}

fun part2Slow2(reverseReplacements: Map<String, List<String>>, molecule: String): Int {
    var sortedReverseReplacements = reverseReplacements.toSortedMap(compareBy<String> { -it.length }.thenBy { it })
    var knownMap = hashMapOf<String, Int>()
    knownMap.put("e", 0)
    return findShortest(sortedReverseReplacements, molecule, 0, knownMap, Int.MAX_VALUE)
}

fun part2(molecule: String): Int {
    var nTokens = molecule.count { it.isUpperCase() }
    var nY = molecule.count { it == 'Y' }
    var nRnAr = "Rn|Ar".toRegex().findAll(molecule).count()
    return nTokens - nRnAr - nY * 2 - 1
}

fun main() {
    var (replacements, _, molecule) = readInput()
    println("part1: ${part1(replacements, molecule)}")
    println("part2: ${part2(molecule)}")
}
