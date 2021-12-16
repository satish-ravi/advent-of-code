import kotlin.math.*;

data class Ingredient(val name: String, val capacity: Int, val durability: Int, val flavor: Int, val texture: Int, val calories: Int) {
    companion object {
        fun createFromString(strRep: String): Ingredient {
            val regex = "(.+): capacity (-?\\d+), durability (-?\\d+), flavor (-?\\d+), texture (-?\\d+), calories (-?\\d+)".toRegex()
            val match = regex.matchEntire(strRep)!!
            var (name, capacity, durability, flavor, texture, calories) = match.destructured
            return Ingredient(name, capacity.toInt(), durability.toInt(), flavor.toInt(), texture.toInt(), calories.toInt())
        }
    }
}

fun readInput(): List<Ingredient> {
    val input = generateSequence(::readLine);
    return input.map {
        value -> Ingredient.createFromString(value)
    }.toList();
}

fun generatePairs(): List<Array<Int>> {
    var result = ArrayList<Array<Int>>()
    for (i in 1..99) {
        result.add(arrayOf(i, 100-i))
    }
    return result
}

fun generateQuads(): List<Array<Int>> {
    var result = ArrayList<Array<Int>>()
    for (i in 1..97) {
        for (j in 1..98-i) {
            for (k in 1..99-i-j) {
                result.add(arrayOf(i, j, k, 100-i-j-k))
            }
        }
    }
    return result
}

fun getBestCombo(input: List<Ingredient>, req_calories: Int = 0): Int {
    val combos = when (input.size) {
        2 -> generatePairs()
        4 -> generateQuads()
        else -> throw Exception("invalid")
    }
    var max = 0
    for (combo in combos) {
        var capacity = 0
        var durability = 0
        var flavor = 0
        var texture = 0
        var calories = 0
        for (i in 0 until input.size) {
            capacity += combo[i] * input[i].capacity
            durability += combo[i] * input[i].durability
            flavor += combo[i] * input[i].flavor
            texture += combo[i] * input[i].texture
            calories += combo[i] * input[i].calories
        }
        val score = max(capacity,0) * max(durability,0) * max(flavor,0) * max(texture,0)
        if (score > max && (req_calories == 0 || req_calories == calories)) {
            max = score
        }
    }
    return max
}

fun main() {
    var input = readInput()
    println("part1: ${getBestCombo(input)}")
    println("part2: ${getBestCombo(input, 500)}")
}
