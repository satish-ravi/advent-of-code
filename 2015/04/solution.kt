import java.security.MessageDigest
import kotlin.text.Charsets.UTF_8

fun md5(str: String): ByteArray = MessageDigest.getInstance("MD5").digest(str.toByteArray(UTF_8))
fun ByteArray.toHex() = joinToString(separator = "") { byte -> "%02x".format(byte) }

fun readInput(): String {
    return readLine()!!
}

fun findMd5HexWithPrefix(input: String, prefix: String): Int {
    var num = 1
    while (true) {
        var md5str = md5(input + num).toHex()
        if (md5str.startsWith(prefix)) {
            return num
        }
        num++
    }
}

fun part1(input: String): Int {
    return findMd5HexWithPrefix(input, "00000")
}

fun part2(input: String): Int {
    return findMd5HexWithPrefix(input, "000000")
}

fun main() {
    var input = readInput()
    println("part1: ${part1(input)}")
    println("part2: ${part2(input)}")
}
