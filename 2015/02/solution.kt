class Box(val l: Int, val w: Int, val h: Int) {
    companion object {
        fun createFromString(strRep: String): Box {
            var arr = strRep.split("x").map { value -> value.toInt() }
            return Box(arr[0], arr[1], arr[2]);
        }
    }

    fun surfaceArea(): Int {
        return 2 * l * w + 2 * w * h + 2 * l * h;
    }

    fun volume(): Int {
        return l * w * h;
    }

    fun sortedEdges(): Array<Int> {
        val edges = arrayOf(l, w, h);
        edges.sort();
        return edges;
    }

    fun smallestSideArea(): Int {
        val edges = sortedEdges();
        return edges[0] * edges[1];
    }

    fun smallestPerimeter(): Int {
        val edges = sortedEdges();
        return 2 * (edges[0] + edges[1]);
    }
}

fun readInput(): List<Box> {
    val input = generateSequence(::readLine);
    return input.map {
        value -> Box.createFromString(value)
    }.toList();
}

fun part1(input: List<Box>): Int {
    var total = 0;
    for (box in input) {
        total += box.surfaceArea() + box.smallestSideArea();
    }
    return total;
}

fun part2(input: List<Box>): Int {
    var total = 0;
    for (box in input) {
        total += box.volume() + box.smallestPerimeter();
    }
    return total;
}

fun main() {
    var input = readInput();
    println("part1: ${part1(input)}");
    println("part2: ${part2(input)}");
}
