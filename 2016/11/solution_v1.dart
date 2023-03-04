import 'dart:collection';
import 'dart:convert';
import 'dart:io';

bool isGenerator(String item) {
  return item.endsWith('-G');
}

bool isMicrochip(String item) {
  return item.endsWith('-M');
}

List<Set<String>> cloneItems(List<Set<String>> items) {
  List<Set<String>> newItems = List.empty(growable: true);
  for (var item in items) {
    newItems.add(Set.from(item));
  }
  return newItems;
}

class State {
  List<Set<String>> items;
  int elevatorFloor;
  int step;

  static State prepareInitialState(List<String> arrangement) {
    List<Set<String>> items = List.empty(growable: true);
    for (var floor = 1; floor <= 4; floor++) {
      var currentFloor = arrangement[floor - 1];
      Set<String> floorItems = HashSet();
      floorItems.addAll(RegExp(r'([a-z]+) generator')
          .allMatches(currentFloor)
          .map((m) => "${m.group(1)!}-G"));
      floorItems.addAll(RegExp(r'([a-z]+)-compatible microchip')
          .allMatches(currentFloor)
          .map((m) => "${m.group(1)!}-M"));
      items.add(floorItems);
    }

    return State(0, items, 0);
  }

  State(this.elevatorFloor, this.items, this.step);

  Set<String> getGenerators(int floor) {
    return items[floor].where(isGenerator).map((g) => g.split('-')[0]).toSet();
  }

  Set<String> getMicrochips(int floor) {
    return items[floor].where(isMicrochip).map((m) => m.split('-')[0]).toSet();
  }

  bool isFinal() {
    return [0, 1, 2].every((floor) => items[floor].isEmpty);
  }

  bool isValid() {
    return [0, 1, 2, 3].every((floor) =>
        getGenerators(floor).isEmpty ||
        getGenerators(floor).containsAll(getMicrochips(floor)));
  }

  Set<State> getNextStates() {
    Set<State> nextStates = HashSet();
    Set<State> downStates = HashSet();
    Set<Set<String>> oneMoves = HashSet();
    Set<Set<String>> twoMoves = HashSet();

    var itemsAsList = items[elevatorFloor].toList();

    for (var i = 0; i < itemsAsList.length; i++) {
      oneMoves.add(Set.from([itemsAsList[i]]));
      for (var j = i + 1; j < itemsAsList.length; j++) {
        twoMoves.add(Set.from([itemsAsList[i], itemsAsList[j]]));
      }
    }

    if (elevatorFloor < 3) {
      for (var itemsToMove in twoMoves) {
        List<Set<String>> newFloors = cloneItems(items);
        newFloors[elevatorFloor].removeAll(itemsToMove);
        newFloors[elevatorFloor + 1].addAll(itemsToMove);
        var nextState = State(elevatorFloor + 1, newFloors, step + 1);
        if (nextState.isValid()) {
          nextStates.add(nextState);
        }
      }
      if (nextStates.length == 0) {
        for (var itemsToMove in oneMoves) {
          List<Set<String>> newFloors = cloneItems(items);
          newFloors[elevatorFloor].removeAll(itemsToMove);
          newFloors[elevatorFloor + 1].addAll(itemsToMove);
          var nextState = State(elevatorFloor + 1, newFloors, step + 1);
          if (nextState.isValid()) {
            nextStates.add(nextState);
          }
        }
      }
    }

    if (elevatorFloor > 0) {
      for (var itemsToMove in oneMoves) {
        List<Set<String>> newFloors = cloneItems(items);
        newFloors[elevatorFloor].removeAll(itemsToMove);
        newFloors[elevatorFloor - 1].addAll(itemsToMove);
        var nextState = State(elevatorFloor - 1, newFloors, step + 1);
        if (nextState.isValid()) {
          downStates.add(nextState);
        }
      }
      if (downStates.length == 0) {
        for (var itemsToMove in twoMoves) {
          List<Set<String>> newFloors = cloneItems(items);
          newFloors[elevatorFloor].removeAll(itemsToMove);
          newFloors[elevatorFloor - 1].addAll(itemsToMove);
          var nextState = State(elevatorFloor - 1, newFloors, step + 1);
          if (nextState.isValid()) {
            downStates.add(nextState);
          }
        }
      }
    }

    nextStates.addAll(downStates);
    return nextStates;
  }

  String serialize() {
    return elevatorFloor.toString() +
        '|' +
        items.map((item) {
          var sortedItems = item.toList();
          sortedItems.sort();
          return sortedItems.join(',');
        }).join('|');
  }

  @override
  int get hashCode => serialize().hashCode;

  @override
  bool operator ==(other) {
    return other is State && this.serialize() == other.serialize();
  }
}

List<String> readInput() {
  var arrangement = <String>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    arrangement.add(line);
  }
  return arrangement;
}

int solve(List<String> arrangement) {
  var start = State.prepareInitialState(arrangement);
  Set<State> visited = new HashSet();
  Queue<State> queue = Queue();
  queue.add(start);
  visited.add(start);
  var prevStep = 0;

  while (queue.isNotEmpty) {
    var cur = queue.removeFirst();
    var curStep = cur.step;
    if (prevStep != curStep) {
      print('${curStep}, ${queue.length}, ${visited.length}');
      prevStep = curStep;
    }
    if (cur.isFinal()) {
      return cur.step;
    }
    for (var next in cur.getNextStates()) {
      if (!visited.contains(next)) {
        queue.add(next);
        visited.add(next);
      }
    }
  }

  throw new Exception('not found');
}

int part1(List<String> arrangement) {
  return solve(arrangement);
}

int part2(List<String> arrangement) {
  arrangement[0] +=
      'elerium generator, elerium-compatible microchip, dilithium generator, dilithium-compatible microchip';
  return solve(arrangement);
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
