fun readInput(): List<String> {
    val input = generateSequence(::readLine);
    return input.toList();
}

fun countVowels(str: String): Int {
    val vowels = arrayOf('a', 'e', 'i', 'o', 'u');
    return str.toList().filter{c -> vowels.contains(c)}.size
}

fun hasRepeat(str: String, offset: Int): Boolean {
    for (i in offset until str.length) {
        if (str[i - offset] == str[i]) {
            return true
        }
    }
    return false;
}

fun hasInvalid(str: String): Boolean {
    val invalidStrings = arrayOf("ab", "cd", "pq", "xy").toList();
    return str.findAnyOf(invalidStrings) != null;
}

fun hasRepeatingPair(str: String): Boolean {
    var pairs = HashMap<String, Int>()
    for (i in 0 until str.length - 1) {
        var pair = str.substring(i, i + 2)
        if (pairs.containsKey(pair)) {
            if (pairs.get(pair) != i - 1) {
                return true;
            }
        } else {
            pairs.put(pair, i);
        }
    }
    return false;
}

fun part1(input: List<String>): Int {
    return input.filter{str -> !hasInvalid(str) && countVowels(str) >= 3 && hasRepeat(str, 1)}.size
}

fun part2(input: List<String>): Int {
    return input.filter{str -> hasRepeatingPair(str) && hasRepeat(str, 2)}.size
}

fun main() {
    var input = readInput();
    println("part1: ${part1(input)}");
    println("part2: ${part2(input)}");
}
