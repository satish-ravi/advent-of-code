import java.util.PriorityQueue
import kotlin.math.max

data class Effect(val name: String, val armor: Int, val damage: Int, val mana: Int, var turns: Int = 0)

data class Spell(val name: String, val mana: Int, val damage: Int, val hitPoints: Int, val effect: Effect? = null)

data class State(val playerHitPoints: Int, val bossHitPoints: Int, val mana: Int, val spentMana: Int, val effects: List<Effect>, val playerTurn: Boolean = true, val prevState: State? = null, val spells: String = "")

fun readInput(): Pair<Int, Int> {
    val parsed = generateSequence(::readLine).map { it -> it.split(": ").get(1).toInt() }.toList()
    return Pair(parsed.get(0), parsed.get(1))
}

fun getSpells(): List<Spell> {
    return listOf(
        Spell("Magic Missile", 53, 4, 0),
        Spell("Drain", 73, 2, 2),
        Spell("Shield", 113, 0, 0, Effect("Shield", 7, 0, 0, 6)),
        Spell("Poison", 173, 0, 0, Effect("Poison", 0, 3, 0, 6)),
        Spell("Recharge", 229, 0, 0, Effect("Recharge", 0, 0, 101, 5))
    )
}

fun toShortString(effects: List<Effect>): String {
    var result = ""
    for (effect in effects) {
        result += "${effect.name},${effect.turns};"
    }
    return result
}

fun solve(startBossHitPoints: Int, bossDamage: Int, perRoundLoss: Int = 0): Int {
    val compareByMana: Comparator<State> = compareBy { it.spentMana }
    val queue = PriorityQueue<State>(compareByMana)
    queue.add(State(50, startBossHitPoints, 500, 0, listOf<Effect>()))
    while (!queue.isEmpty()) {
        var current = queue.remove()
        if (current.bossHitPoints <= 0) {
            return current.spentMana
        }
        var playerHitPoints: Int = current.playerHitPoints
        if (current.playerTurn) {
            playerHitPoints -= perRoundLoss
        }
        if (playerHitPoints <= 0) {
            continue
        }
        var bossHitPoints: Int = current.bossHitPoints
        var mana: Int = current.mana
        var spentMana: Int = current.spentMana
        // apply effects
        var armor = 0
        val activeEffects = mutableListOf<Effect>()
        val activeEffectNames = HashSet<String>()
        for (effect in current.effects) {
            bossHitPoints -= effect.damage
            mana += effect.mana
            armor = max(armor, effect.armor)
            if (effect.turns > 1) {
                activeEffects.add(Effect(effect.name, effect.armor, effect.damage, effect.mana, effect.turns - 1))
                activeEffectNames.add(effect.name)
            }
        }
        if (current.playerTurn) {
            for (spell in getSpells()) {
                if (activeEffectNames.contains(spell.name) || spell.mana > mana) {
                    continue
                }
                var newEffects = activeEffects
                if (spell.effect != null) {
                    newEffects = mutableListOf(spell.effect)
                    for (effect in activeEffects) {
                        newEffects.add(effect.copy())
                    }
                }
                queue.add(State(playerHitPoints + spell.hitPoints, bossHitPoints - spell.damage, mana - spell.mana, spentMana + spell.mana, newEffects, false, current, current.spells + spell.name + ";"))
            }
        } else {
            queue.add(State(playerHitPoints - max(1, bossDamage - armor), bossHitPoints, mana, spentMana, activeEffects, true, current, current.spells))
        }
    }
    throw Exception("player cannot win")
}


fun main() {
    val (bossHitPoints, bossDamage) = readInput()
    println("part1: ${solve(bossHitPoints, bossDamage)}")
    println("part2: ${solve(bossHitPoints, bossDamage, 1)}")
}
