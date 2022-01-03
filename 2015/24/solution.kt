fun readInput(): List<Long> {
    return generateSequence(::readLine).map { it -> it.toLong() }.toList()
}

fun getGroupsOfRequiredSum(sortedNums: List<Long>, sum: Long, startPos: Int, groupLen: Long): List<List<Long>> {
    if (groupLen == 1L) {
        // assume no duplicates in list and return the number matching the list
        for (i in startPos until sortedNums.size) {
            if (sortedNums[i] == sum) {
                return listOf(listOf(sum))
            } else if (sortedNums[i] < sum) {
                return listOf<List<Long>>()
            }
        }
        return listOf<List<Long>>()
    }
    var i = startPos
    while (i < sortedNums.size && sortedNums[i] > sum) {
        i++
    }
    var result = mutableListOf<List<Long>>()
    while (i < sortedNums.size && sortedNums[i] * groupLen > sum) {
        val cur = sortedNums[i]
        var subList = getGroupsOfRequiredSum(sortedNums, sum - cur, i + 1, groupLen - 1)
        for (item in subList) {
            var newList = mutableListOf(cur)
            newList.addAll(item)
            result.add(newList)
        }
        i++
    }
    return result
}

fun solve(nums: List<Long>, numGroups: Int): Long {
    var sortedNums = nums.toMutableList()
    sortedNums.sortDescending()
    val requiredSum = sortedNums.sum() / numGroups
    var minGroupLen = (requiredSum / sortedNums[0]) + 1
    var maxGroupLen = sortedNums.size - 2 * minGroupLen
    var groupLen = minGroupLen
    var groups = mutableListOf<List<Long>>()
    while (groupLen <= maxGroupLen) {
        groups.addAll(getGroupsOfRequiredSum(sortedNums, requiredSum, 0, groupLen))
        if (groups.size > 0) {
            break
        }
        groupLen++
    }
    var minQE = 10000000000000
    for (group in groups) {
        var qe = group.fold(1L) { acc, i -> acc * i }
        if (qe < minQE) {
            minQE = qe
        }
    }
    return minQE
}

fun main() {
    val nums = readInput()
    println("part1: ${solve(nums, 3)}")
    println("part2: ${solve(nums, 4)}")
}
