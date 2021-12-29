import kotlin.math.max

data class Item(val name: String, val cost: Int, val damage: Int, val armor: Int)

data class Player(var hitPoints: Int, val damage: Int, val armor: Int, val cost: Int = 0, val name: String = "player")

fun readInput(): Player {
    val parsed = generateSequence(::readLine).map { it -> it.split(": ").get(1).toInt() }.toList()
    return Player(parsed.get(0), parsed.get(1), parsed.get(2), 0, "boss")
}

fun getWeapons(): List<Item> {
    return listOf(
        Item("Dagger", 8, 4, 0),
        Item("Shortsword", 10, 5, 0),
        Item("Warhammer", 25, 6, 0),
        Item("Warhammer", 40, 7, 0),
        Item("Greataxe", 74, 8, 0)
    )
}

fun getArmors(): List<Item> {
    return listOf(
        Item("None", 0, 0, 0),
        Item("Leather", 13, 0, 1),
        Item("Chainmail", 31, 0, 2),
        Item("Splintmail", 53, 0, 3),
        Item("Bandedmail", 75, 0, 4),
        Item("Platemail", 102, 0, 5)
    )
}

fun getRings(): Pair<List<Item>, List<Item>> {
    return Pair(
        listOf(
            Item("None", 0, 0, 0),
            Item("Damage + 1", 25, 1, 0),
            Item("Damage + 2", 50, 2, 0),
            Item("Damage + 3", 100, 3, 0)
        ),
        listOf(
            Item("None", 0, 0, 0),
            Item("Defense + 1", 20, 0, 1),
            Item("Defense + 2", 40, 0, 2),
            Item("Defense + 3", 80, 0, 3)
        )
    )
}

fun getAllStartingCombos(hitPoints: Int): List<Player> {
    var players = mutableListOf<Player>()
    for (weapon in getWeapons()) {
        for (armor in getArmors()) {
            var (rings1, rings2) = getRings()
            for (ring1 in rings1) {
                for (ring2 in rings2) {
                    players.add(
                        Player(
                            hitPoints,
                            weapon.damage + ring1.damage,
                            armor.armor + ring2.armor,
                            weapon.cost + armor.cost + ring1.cost + ring2.cost
                        )
                    )
                }
            }
        }
    }
    return players.sortedWith(compareBy { it.cost })
}

fun simulateGame(player1: Player, player2: Player): String {
    var attacker = player1.copy()
    var defender = player2.copy()
    while (attacker.hitPoints > 0) {
        defender.hitPoints -= max(1, attacker.damage - defender.armor)
        val temp = attacker
        attacker = defender
        defender = temp
    }
    return defender.name
}

fun part1(boss: Player): Int {
    for (player in getAllStartingCombos(100)) {
        if (simulateGame(player, boss) == "player") {
            return player.cost
        }
    }
    throw Exception("player cannot win")
}

fun part2(boss: Player): Int {
    for (player in getAllStartingCombos(100).reversed()) {
        if (simulateGame(player, boss) == "boss") {
            return player.cost
        }
    }
    throw Exception("player cannot win")
}

fun main() {
    val boss = readInput()
    println("part1: ${part1(boss)}")
    println("part2: ${part2(boss)}")
}
