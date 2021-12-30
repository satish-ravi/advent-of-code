data class Instruction(val operator: String, val operand: String)

class Program(val instructions: List<Instruction>, val a: Int = 0) {
    var pointer = 0
    var registers = hashMapOf("a" to a, "b" to 0)

    fun run(): Boolean {
        if (pointer >= 0 && pointer < instructions.size) {
            var ins = instructions[pointer]
            when (ins.operator) {
                "hlf" -> {
                    registers.put(ins.operand, registers.get(ins.operand)!! / 2)
                    pointer += 1
                }
                "tpl" -> {
                    registers.put(ins.operand, registers.get(ins.operand)!! * 3)
                    pointer += 1
                }
                "inc" -> {
                    registers.put(ins.operand, registers.get(ins.operand)!! + 1)
                    pointer += 1
                }
                "jmp" -> {
                    pointer += ins.operand.toInt()
                }
                "jie" -> {
                    var register = ins.operand.split(", ")[0]
                    var offset = ins.operand.split(", ")[1].toInt()
                    if (registers.get(register)!! % 2 == 0) {
                        pointer += offset
                    } else {
                        pointer += 1
                    }
                }
                "jio" -> {
                    var register = ins.operand.split(", ")[0]
                    var offset = ins.operand.split(", ")[1].toInt()
                    if (registers.get(register)!! == 1) {
                        pointer += offset
                    } else {
                        pointer += 1
                    }
                }
                else -> throw Exception("invalid ins")
            }
            return true
        }
        return false
    }

    fun runToCompletion(): Pair<Int, Int> {
        while (run()) {
        }
        return Pair(registers.get("a")!!, registers.get("b")!!)
    }
}

fun readInput(): List<Instruction> {
    return generateSequence(::readLine).map {
        it ->
        Instruction(it.split(" ", limit = 2)[0], it.split(" ", limit = 2)[1])
    }.toList()
}

fun part1(instructions: List<Instruction>): Int {
    val program = Program(instructions)
    return program.runToCompletion().second
}

fun part2(instructions: List<Instruction>): Int {
    val program = Program(instructions, 1)
    return program.runToCompletion().second
}

fun main() {
    val instructions = readInput()
    println("part1: ${part1(instructions)}")
    println("part2: ${part2(instructions)}")
}
