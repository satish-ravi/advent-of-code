import 'dart:collection';
import 'dart:convert';
import 'dart:io';
import 'dart:math';
import 'package:crypto/crypto.dart';

String readInput() {
  var line = stdin.readLineSync(encoding: utf8);
  return line!;
}

int noSteps(String state) {
  return int.parse(state.split('|')[0]);
}

String getSteps(String state) {
  return state.split('|')[1];
}

Map<String, List<int>> directions = {
  'U': [-1, 0],
  'D': [1, 0],
  'L': [0, -1],
  'R': [0, 1]
};

Set<String> openChars = Set.from(['b', 'c', 'd', 'e', 'f']);

List<String> getNextStates(String state, String input) {
  String steps = getSteps(state);
  int pos = noSteps(state);
  int i = pos ~/ 10;
  int j = pos % 10;
  String hash = md5.convert(utf8.encode('${input}${steps}')).toString();
  List<String> nextStates = [];

  for (var dir in ['U', 'D', 'L', 'R'].asMap().entries) {
    var delta = directions[dir.value]!;
    var ni = i + delta[0];
    var nj = j + delta[1];
    if (ni >= 0 &&
        ni < 4 &&
        nj >= 0 &&
        nj <= 3 &&
        openChars.contains(hash[dir.key])) {
      nextStates.add('${ni * 10 + nj}|${steps}${dir.value}');
    }
  }
  return nextStates;
}

String part1(String input) {
  Set<String> visited = new HashSet();
  Queue<String> queue = Queue();

  var start = '0|';
  queue.add(start);
  visited.add(start);

  while (queue.isNotEmpty) {
    var cur = queue.removeFirst();
    if (cur.startsWith('33')) {
      return getSteps(cur);
    }
    for (var next in getNextStates(cur, input)) {
      if (!visited.contains(next)) {
        visited.add(next);
        queue.add(next);
      }
    }
  }

  throw new Exception('not found');
}

int part2(String input) {
  Set<String> visited = new HashSet();
  Queue<String> queue = Queue();

  var start = '0|';
  queue.add(start);
  visited.add(start);
  int maxSteps = 0;

  while (queue.isNotEmpty) {
    var cur = queue.removeFirst();
    if (cur.startsWith('33')) {
      maxSteps = max(maxSteps, getSteps(cur).length);
      continue;
    }
    for (var next in getNextStates(cur, input)) {
      if (!visited.contains(next)) {
        visited.add(next);
        queue.add(next);
      }
    }
  }

  return maxSteps;
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
