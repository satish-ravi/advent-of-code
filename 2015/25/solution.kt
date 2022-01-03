fun part1(row: Int, col: Int): Long {
    var r = 1
    var c = 1
    var value = 20151125L
    while (true) {
        value = (value * 252533) % 33554393
        if (r == 1) {
            r = c + 1
            c = 1
        } else {
            r -= 1
            c += 1
        }
        if (r == row && c == col) {
            return value
        }
    }
}

fun main() {
    println("part1: ${part1(3010, 3019)}")
}
