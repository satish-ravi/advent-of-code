fun readInput(): List<Int> {
    val input = generateSequence(::readLine);
    return input.map {
        value -> value.toInt()
    }.toList();
}

fun getSubsetSum(expected_sum: Int, current_array: List<Int>, remaining: List<Int>): ArrayList<List<Int>> {
    val sum = current_array.sum()
    if (sum == expected_sum) {
        return arrayListOf(current_array)
    }
    if (sum > expected_sum) {
        return arrayListOf()
    }
    val result = ArrayList<List<Int>>()
    for (i in 0 until remaining.size) {
        val next_array = current_array + remaining.slice(i..i)
        val next_remaining = remaining.slice(i+1..remaining.size-1)
        result.addAll(getSubsetSum(expected_sum, next_array, next_remaining))
    }
    return result
}

fun part1(input: List<Int>): Int {
    return getSubsetSum(150, listOf(), input).size
}

fun part2(input: List<Int>): Int {
    val allSubsets = getSubsetSum(150, listOf(), input)
    var minSize = (allSubsets.minByOrNull { it.size })!!.size
    return allSubsets.count { it.size == minSize }
}

fun main() {
    var input = readInput()
    println("part1: ${part1(input)}")
    println("part2: ${part2(input)}")
}
