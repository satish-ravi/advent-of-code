import kotlin.math.*

fun solve(n: Int): Pair<Int, Int> {
    var house = 1
    var p1 = Int.MAX_VALUE
    var p2 = Int.MAX_VALUE
    while (p1 == Int.MAX_VALUE || p2 == Int.MAX_VALUE) {
        var p1Presents = 0
        var p2Presents = 0
        for (i in 1..sqrt(house.toDouble()).toInt()) {
            if (house % i == 0) {
                p1Presents += i * 10 + (house / i) * 10
                if (p1 == Int.MAX_VALUE && p1Presents >= n) {
                    p1 = house
                }
                if (house / i <= 50) {
                    p2Presents += i * 11
                }
                if (i <= 50 && i != house / i) {
                    p2Presents += (house / i) * 11
                }
                if (p2 == Int.MAX_VALUE && p2Presents >= n) {
                    p2 = house
                }
            }
        }
        house += 1
    }
    return Pair(p1, p2)
}

fun main() {
    var inp = 36000000
    var (p1, p2) = solve(inp)
    println("part1: $p1")
    println("part2: $p2")
}
