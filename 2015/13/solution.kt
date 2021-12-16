import kotlin.math.*;

data class Statement(val person: String, val next: String, val happiness_units: Int) {
    companion object {
        fun createFromString(strRep: String): Statement {
            val regex = "(.+) would (gain|lose) (\\d+) happiness units by sitting next to (.+).".toRegex()
            val match = regex.matchEntire(strRep)!!
            var (person, gain_or_loss, hap, next) = match.destructured
            var happiness_units = hap.toInt()
            if (gain_or_loss == "lose") {
                happiness_units = -happiness_units
            }
            return Statement(person, next, happiness_units)
        }
    }
}

fun genPermutations(list: List<Int>): List<List<Int>> {
    if (list.size == 1) {
        return arrayListOf(list)
    }
    val arr = list.toTypedArray()
    val result = ArrayList<List<Int>>()
    for (i in 0..list.size-1) {
        val start: Int = arr[i]
        arr[i] = arr[0]
        arr[0] = start
        
        val subPermutations: List<List<Int>> = genPermutations(arr.slice(1..list.size-1))
        result.addAll(subPermutations.map { perm: List<Int> -> arrayListOf(start) + perm})

        arr[0] = arr[i]
        arr[i] = start
    }
    return result
}

class TableArranger {
    val people: List<String>
    val happiness: Array<Array<Int>>

    constructor(statements: List<Statement>) {
        val peopleSet = HashSet<String>()
        for (statement in statements) {
            peopleSet.add(statement.person)
        }
        people = peopleSet.toList()
        happiness = Array(people.size) { Array(people.size) { 0 }}
        for (statement in statements) {
            val i1 = people.indexOf(statement.person)
            val i2 = people.indexOf(statement.next)
            happiness[i1][i2] = statement.happiness_units
        }   
    }

    fun getAllArragementsHappiness(): ArrayList<Int> {
        val allArrangements = genPermutations((0..people.size-1).toList())
        val result = ArrayList<Int>()
        for (arrangement in allArrangements) {
            var sum = 0;
            for (i in 0..people.size-1) {
                var cur = arrangement[i]
                val next = arrangement[(i + 1) % people.size]
                sum += happiness[cur][next] + happiness[next][cur]
            }
            result.add(sum)
        }
        return result
    }
}

fun readInput(): List<Statement> {
    val input = generateSequence(::readLine);
    return input.map {
        value -> Statement.createFromString(value)
    }.toList();
}

fun compute(input: List<Statement>): Int {
    val tableArranger = TableArranger(input)
    val all = tableArranger.getAllArragementsHappiness()
    return all.maxOrNull()!!
}

fun part1(input: List<Statement>): Int {
    return compute(input)
}

fun part2(input: List<Statement>): Int {
    return compute(listOf(*input.toTypedArray(), Statement("Me", "Me", 0)))
}

fun main() {
    var input = readInput()
    println("part1: ${part1(input)}")
    println("part2: ${part2(input)}")
}
