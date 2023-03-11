import 'dart:collection';
import 'dart:convert';
import 'dart:io';

String readInput() {
  var line = stdin.readLineSync(encoding: utf8);
  return line!;
}

String getNext(String current) {
  List<String> next = [];
  for (var i = 0; i < current.length; i++) {
    bool left = i == 0 || current[i - 1] == '.';
    bool right = i == current.length - 1 || current[i + 1] == '.';
    if (left && !right || right && !left) {
      next.add('^');
    } else {
      next.add('.');
    }
  }
  return next.join();
}

int solve(String input, int rows) {
  var cur = input;
  var res = 0;
  for (int i = 0; i < rows; i++) {
    res += cur.split('').where((element) => element == '.').length;
    cur = getNext(cur);
  }
  return res;
}

int part1(String input) {
  return solve(input, 40);
}

int part2(String input) {
  return solve(input, 400000);
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
