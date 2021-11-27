import kotlin.math.*;

data class Reindeer(val name: String, val speed: Int, val flying: Int, val resting: Int) {
    companion object {
        fun createFromString(strRep: String): Reindeer {
            val regex = "(.+) can fly (\\d+) km/s for (\\d+) seconds, but then must rest for (\\d+) seconds.".toRegex()
            val match = regex.matchEntire(strRep)!!
            var (name, speed, flying, resting) = match.destructured
            return Reindeer(name, speed.toInt(), flying.toInt(), resting.toInt())
        }
    }
}

fun readInput(): List<Reindeer> {
    val input = generateSequence(::readLine);
    return input.map {
        value -> Reindeer.createFromString(value)
    }.toList();
}

fun getDistanceTravelled(reindeer: Reindeer, time: Int): Int {
    val units = time / (reindeer.flying + reindeer.resting)
    val remaining = time % (reindeer.flying + reindeer.resting)
    return units * reindeer.speed * reindeer.flying + min(reindeer.flying, remaining) * reindeer.speed
}

fun part1(input: List<Reindeer>): Int {
    return input.map { reindeer -> getDistanceTravelled(reindeer, 2053) }.toList().maxOrNull()!!
}

fun part2(input: List<Reindeer>): Int {
    val points = IntArray(input.size) {0}
    for (t in 1..2503) {
        val distances = input.map { reindeer -> getDistanceTravelled(reindeer, t) }.toList()
        val max = distances.maxOrNull()!!
        for (i in 0..input.size - 1) {
            if (distances[i] == max) {
                points[i]++
            }
        }
    }
    return points.toList().maxOrNull()!!
}

fun main() {
    var input = readInput()
    println("part1: ${part1(input)}")
    println("part2: ${part2(input)}")
}
