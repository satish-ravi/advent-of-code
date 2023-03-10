import 'dart:math';
import 'dart:convert';
import 'dart:io';

String readInput() {
  var line = stdin.readLineSync(encoding: utf8);
  return line!;
}

String getInverted(String bits) {
  if (bits.length < 62) {
    var asNum = int.parse(bits, radix: 2);
    var reversed = (~asNum & (pow(2, 61).toInt() - 1)).toRadixString(2);
    return reversed.substring(reversed.length - bits.length);
  }
  var split = bits.length ~/ 2;
  return getInverted(bits.substring(0, split)) +
      getInverted(bits.substring(split));
}

String getNext(String bits) {
  return bits + '0' + getInverted(bits).split('').reversed.join();
}

String getChecksum(String bits) {
  List<String> checksum = [];
  for (var i = 0; i < bits.length; i += 2) {
    if (bits[i] == bits[i + 1]) {
      checksum.add('1');
    } else {
      checksum.add('0');
    }
  }
  if (checksum.length % 2 == 0) {
    return getChecksum(checksum.join());
  }
  return checksum.join();
}

String solve(String input, int diskLength) {
  var disk = input;
  while (disk.length < diskLength) {
    disk = getNext(disk);
  }
  disk = disk.substring(0, diskLength);
  return getChecksum(disk);
}

String part1(String input) {
  return solve(input, 272);
}

String part2(String input) {
  return solve(input, 35651584);
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
