import 'dart:collection';
import 'dart:convert';
import 'dart:io';
import 'package:crypto/crypto.dart';

String readInput() {
  var line = stdin.readLineSync(encoding: utf8);
  return line!;
}

Map<String, String> memory = HashMap();

String getHash(String salt, int n, int rehash) {
  var memkey = '${n},${rehash}';
  if (!memory.containsKey(memkey)) {
    var hash = md5.convert(utf8.encode('${salt}${n}')).toString();
    for (var i = 0; i < rehash; i++) {
      hash = md5.convert(utf8.encode(hash)).toString();
    }
    memory[memkey] = hash;
  }
  return memory[memkey]!;
}

bool isKey(String salt, int n, int rehash) {
  var hash = getHash(salt, n, rehash);
  String? repeat = null;
  for (var i = 0; i < hash.length - 2; i++) {
    if (hash[i] == hash[i + 1] && hash[i + 1] == hash[i + 2]) {
      repeat = hash[i];
      break;
    }
  }
  if (repeat != null) {
    var repeat5 = '${repeat}${repeat}${repeat}${repeat}${repeat}';
    for (var i = 1; i <= 1000; i++) {
      if (getHash(salt, n + i, rehash).contains(repeat5)) {
        return true;
      }
    }
  }
  return false;
}

int solve(String salt, int rehash) {
  List<int> keys = [];
  var index = 0;
  while (keys.length < 64) {
    if (isKey(salt, index, rehash)) {
      keys.add(index);
    }
    index++;
  }
  return keys[63];
}

int part1(String input) {
  return solve(input, 0);
}

int part2(String input) {
  return solve(input, 2016);
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
