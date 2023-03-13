import 'dart:collection';
import 'dart:convert';
import 'dart:io';
import 'dart:math';

List<String> readInput() {
  var input = <String>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    input.add(line);
  }
  return input;
}

Map<int, String> parse(List<String> input) {
  Map<int, String> parsed = HashMap();
  for (int i = 0; i < input.length; i++) {
    for (int j = 0; j < input[i].length; j++) {
      parsed[i * 1000 + j] = input[i][j];
    }
  }
  return parsed;
}

int getTotalNumbers(Map<int, String> parsed) {
  return parsed.values
      .where((element) => element != '#' && element != '.')
      .length;
}

int getStart(Map<int, String> parsed) {
  for (var key in parsed.keys) {
    if (parsed[key] == '0') {
      return key;
    }
  }
  throw new Exception('no 0 found');
}

String noSteps(String state) {
  var split = state.split('|');
  return '${split[0]}|${split[1]}';
}

int getVisitedNumbers(String state) {
  var split = state.split('|');
  return int.parse(split[1]);
}

int getSteps(String state) {
  var split = state.split('|');
  return int.parse(split[2]);
}

int getLocation(String state) {
  var split = state.split('|');
  return int.parse(split[0]);
}

List<String> getNextStates(Map<int, String> parsed, String cur, int totalNum) {
  List<String> nextStates = [];
  var loc = getLocation(cur);
  var steps = getSteps(cur);
  var visitedNum = getVisitedNumbers(cur);
  var i = loc ~/ 1000;
  var j = loc % 1000;
  for (var delta in [
    [-1, 0],
    [1, 0],
    [0, -1],
    [0, 1]
  ]) {
    var newloc = (i + delta[0]) * 1000 + (j + delta[1]);
    if (parsed[newloc] == '.') {
      nextStates.add('${newloc}|${visitedNum}|${steps + 1}');
    } else if (parsed[newloc] != '#') {
      var num = int.parse(parsed[newloc]!);
      if (visitedNum != pow(2, totalNum) - 1) {
        nextStates.add('${newloc}|${visitedNum | 1 << num}|${steps + 1}');
      } else if (num == 0) {
        nextStates.add('${newloc}|${visitedNum | 1 << totalNum}|${steps + 1}');
      }
    }
  }
  return nextStates;
}

int solve(List<String> input, bool comeback) {
  var parsed = parse(input);
  Set<String> visited = new HashSet();
  Queue<String> queue = Queue();

  var totalNum = getTotalNumbers(parsed);
  var startKey = getStart(parsed);
  var dest = pow(2, comeback ? totalNum + 1 : totalNum) - 1;

  var start = '${startKey}|1|0';
  queue.add(start);
  visited.add(start);

  while (queue.isNotEmpty) {
    var cur = queue.removeFirst();
    if (getVisitedNumbers(cur) == dest) {
      return getSteps(cur);
    }
    for (var next in getNextStates(parsed, cur, totalNum)) {
      if (!visited.contains(noSteps(next))) {
        visited.add(noSteps(next));
        queue.add(next);
      }
    }
  }

  throw new Exception('not found');
}

int part1(List<String> input) {
  return solve(input, false);
}

int part2(List<String> input) {
  return solve(input, true);
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
