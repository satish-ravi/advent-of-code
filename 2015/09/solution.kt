data class Route(val loc1: String, val loc2: String, val distance: Int) {
    companion object {
        fun createFromString(strRep: String): Route {
            val regex = "(.+) to (.+) = (\\d+)".toRegex()
            return regex.matchEntire(strRep)?.destructured?.let {
                (loc1, loc2, distance) ->
                Route(loc1, loc2, distance.toInt())
            } ?: throw IllegalArgumentException("Bad input $strRep")
        }
    }
}

fun genPermutations(list: List<Int>): List<List<Int>> {
    if (list.size == 1) {
        return arrayListOf(list)
    }
    val arr = list.toTypedArray()
    val result = ArrayList<List<Int>>()
    for (i in 0..list.size - 1) {
        val start: Int = arr[i]
        arr[i] = arr[0]
        arr[0] = start

        val subPermutations: List<List<Int>> = genPermutations(arr.slice(1..list.size - 1))
        result.addAll(subPermutations.map { perm: List<Int> -> arrayListOf(start) + perm })

        arr[0] = arr[i]
        arr[i] = start
    }
    return result
}

class RoutesProcessor {
    val locations: List<String>
    val routes: Array<Array<Int>>

    constructor(inputRoutes: List<Route>) {
        val locationsSet = HashSet<String>()
        for (route in inputRoutes) {
            locationsSet.add(route.loc1)
            locationsSet.add(route.loc2)
        }
        locations = locationsSet.toList()
        routes = Array(locations.size) { Array(locations.size) { 0 } }
        for (route in inputRoutes) {
            val i1 = locations.indexOf(route.loc1)
            val i2 = locations.indexOf(route.loc2)
            routes[i1][i2] = route.distance
            routes[i2][i1] = route.distance
        }
    }

    fun getAllDistances(): ArrayList<Int> {
        val allPaths = genPermutations((0..locations.size - 1).toList())
        val result = ArrayList<Int>()
        for (path in allPaths) {
            var sum = 0
            for (i in 1..locations.size - 1) {
                sum += routes[path[i - 1]][path[i]]
            }
            result.add(sum)
        }
        return result
    }
}

fun readInput(): List<Route> {
    val input = generateSequence(::readLine)
    return input.map {
        value ->
        Route.createFromString(value)
    }.toList()
}

fun main() {
    var input = readInput()
    var routesProcessor = RoutesProcessor(input)
    val allDistances = routesProcessor.getAllDistances()
    println("part1: ${allDistances.minOrNull()}")
    println("part2: ${allDistances.maxOrNull()}")
}
