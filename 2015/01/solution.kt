fun readInput(): String {
    return readLine()!!;
}

fun part1(input: String): Int {
    var floor = 0;
    for (c in input) {
        if (c == '(') {
            floor += 1;
        } else {
            floor -= 1;
        }
    }
    return floor;
}

fun part2(input: String): Int {
    var floor = 0;
    for (i in input.indices) {
        var c = input[i];
        if (c == '(') {
            floor += 1;
        } else {
            floor -= 1;
            if (floor == -1) {
                return i + 1;
            }
        }
    }
    throw Exception("unexpected");
}

fun main() {
    var input = readInput();
    println("part1: ${part1(input)}");
    println("part2: ${part2(input)}");
}
