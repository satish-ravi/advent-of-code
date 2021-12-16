import kotlin.math.*;

enum class Operation {
    ON, OFF, TOGGLE
}

fun stringToOperation(text: String): Operation {
    when (text) {
        "turn on" -> return Operation.ON
        "turn off" -> return Operation.OFF
        "toggle" -> return Operation.TOGGLE
        else -> throw Exception("invalid operation: $text")
    }
}

data class Instruction(val op: Operation, val start: Pair<Int, Int>, val end: Pair<Int, Int>) {
    companion object {
        fun createFromString(strRep: String): Instruction {
            val regex = "(turn off|turn on|toggle) (\\d+),(\\d+) through (\\d+),(\\d+)".toRegex()
            return regex.matchEntire(strRep)?.destructured?.let { (ins, sx, sy, ex, ey) -> Instruction(stringToOperation(ins), Pair(sx.toInt(), sy.toInt()), Pair(ex.toInt(), ey.toInt()))} ?: throw IllegalArgumentException("Bad input $strRep")
        }
    }
}

class LightSystem(val isPart2: Boolean = false) {
    val lights = Array(1000000) {0}

    fun applyInstruction(ins: Instruction) {
        for (x in ins.start.first..ins.end.first) {
            for (y in ins.start.second..ins.end.second) {
                var pos = x * 1000 + y
                if (isPart2) {
                    part2Language(ins.op, pos)
                } else {
                    part1Language(ins.op, pos)
                }
            }
        }
    }

    fun part1Language(op: Operation, pos: Int) {
        when (op) {
            Operation.ON -> lights[pos] = 1
            Operation.OFF -> lights[pos] = 0
            Operation.TOGGLE -> lights[pos] = (lights[pos] + 1) % 2
        }
    }

    fun part2Language(op: Operation, pos: Int) {
        when (op) {
            Operation.ON -> lights[pos] += 1
            Operation.OFF -> lights[pos] = max(0, lights[pos] - 1)
            Operation.TOGGLE -> lights[pos] += 2
        }
    }

    fun totalOn(): Int {
        return lights.sum()
    }
}

fun readInput(): List<Instruction> {
    val input = generateSequence(::readLine);
    return input.map {
        value -> Instruction.createFromString(value)
    }.toList();
}

fun part1(input: List<Instruction>): Int {
    var system = LightSystem()
    for (ins in input) {
        system.applyInstruction(ins)
    }
    return system.totalOn()
}

fun part2(input: List<Instruction>): Int {
    var system = LightSystem(true)
    for (ins in input) {
        system.applyInstruction(ins)
    }
    return system.totalOn()
}

fun main() {
    var input = readInput();
    println("part1: ${part1(input)}");
    println("part2: ${part2(input)}");
}
