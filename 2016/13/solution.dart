import 'dart:collection';
import 'dart:convert';
import 'dart:io';

const DESTINATION = '31,39';

int readInput() {
  var line = stdin.readLineSync(encoding: utf8);
  return int.parse(line!);
}

Map<String, bool> memory = HashMap();

bool isWall(int x, int y, int fav) {
  var str = '${x},${y}';
  if (!memory.containsKey(str)) {
    var val = x * x + 3 * x + 2 * x * y + y + y * y + fav;
    memory[str] = '1'.allMatches(val.toRadixString(2)).length % 2 != 0;
  }
  return memory[str]!;
}

String noSteps(String state) {
  return state.split('|')[0];
}

int getSteps(String state) {
  return int.parse(state.split('|')[1]);
}

List<String> getNextStates(String state, int fav) {
  var split = noSteps(state).split(',');
  int x = int.parse(split[0]);
  int y = int.parse(split[1]);
  List<String> next = [];
  for (var delta in [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1]
  ]) {
    var nx = x + delta[0];
    var ny = y + delta[1];
    if (nx >= 0 && ny >= 0 && !isWall(nx, ny, fav)) {
      next.add('${nx},${ny}');
    }
  }
  return next;
}

int part1(int input) {
  Set<String> visited = new HashSet();
  Queue<String> queue = Queue();

  var start = '1,1|0';
  queue.add(start);
  visited.add(noSteps(start));

  while (queue.isNotEmpty) {
    var cur = queue.removeFirst();
    if (cur.startsWith(DESTINATION)) {
      return getSteps(cur);
    }
    var nextStep = int.parse(cur.split('|')[1]) + 1;
    for (var next in getNextStates(cur, input)) {
      if (!visited.contains(next)) {
        visited.add(next);
        queue.add('${next}|${nextStep}');
      }
    }
  }

  throw new Exception('not found');
}

int part2(int input) {
  Set<String> visited = new HashSet();
  Set<String> visitedPrev = new HashSet();
  Queue<String> queue = Queue();

  var start = '1,1|0';
  queue.add(start);
  visited.add(noSteps(start));

  while (queue.isNotEmpty) {
    var cur = queue.removeFirst();
    if (cur.endsWith('51')) {
      return visitedPrev.length;
    }
    visitedPrev.add(noSteps(cur));
    var nextStep = int.parse(cur.split('|')[1]) + 1;
    for (var next in getNextStates(cur, input)) {
      if (!visited.contains(next)) {
        visited.add(next);
        queue.add('${next}|${nextStep}');
      }
    }
  }

  throw new Exception('not found');
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
