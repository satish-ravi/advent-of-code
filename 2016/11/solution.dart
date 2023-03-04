import 'dart:collection';
import 'dart:convert';
import 'dart:io';

const GEN_MASK = 0x5555555555555555;
const CHIP_MASK = 0xAAAAAAAAAAAAAAAA;
const ELEVATOR_FLOOR_LENGTH = 2;
const ELEVATOR_FLOOR_MASK = 3;

int getItems(String state) {
  return noSteps(state) >> ELEVATOR_FLOOR_LENGTH;
}

int getElevatorFloor(String state) {
  return noSteps(state) & ELEVATOR_FLOOR_MASK;
}

int getSteps(String state) {
  return int.parse(state.split('|')[1]);
}

String getState(int items, int elevatorFloor, int steps) {
  return '${(items << ELEVATOR_FLOOR_LENGTH) | elevatorFloor}|${steps}';
}

int noSteps(String state) {
  return int.parse(state.split('|')[0]);
}

class Processor {
  int numItems;
  String initState;

  static Processor prepareInitialState(List<String> arrangement) {
    List<Set<String>> floorGeneratorList = List.empty(growable: true);
    List<Set<String>> floorMicrochipList = List.empty(growable: true);
    for (var floor = 1; floor <= 4; floor++) {
      var currentFloor = arrangement[floor - 1];
      var generators = RegExp(r'([a-z]+) generator')
          .allMatches(currentFloor)
          .map((m) => m.group(1)!);
      var microchips = RegExp(r'([a-z]+)-compatible microchip')
          .allMatches(currentFloor)
          .map((m) => m.group(1)!);
      floorGeneratorList.add(generators.toSet());
      floorMicrochipList.add(microchips.toSet());
    }

    var allGen = floorGeneratorList.reduce((value, element) {
      Set<String> newValue = Set.from(value);
      newValue.addAll(element);
      return newValue;
    }).toList();

    var numItems = allGen.length;
    var items = 0;

    for (var floor = 0; floor < 4; floor++) {
      for (var gen in floorGeneratorList[floor]) {
        items |= 1 << (allGen.indexOf(gen) * 2 + numItems * floor * 2);
      }
      for (var chip in floorMicrochipList[floor]) {
        items |= 1 << (allGen.indexOf(chip) * 2 + 1 + numItems * floor * 2);
      }
    }

    return Processor(numItems, getState(items, 0, 0));
  }

  Processor(this.numItems, this.initState);

  int getFloor(String state, int floor) {
    return getItems(state) >> (numItems * 2 * floor) &
        ((1 << (numItems * 2)) - 1);
  }

  bool isFinal(state) {
    return getItems(state) == ((1 << (numItems * 2)) - 1) << numItems * 2 * 3;
  }

  bool isValid(state) {
    return [0, 1, 2, 3].every((floor) {
      int floorItems = getFloor(state, floor);
      int generators = floorItems & GEN_MASK;
      int microchips = floorItems & CHIP_MASK;
      return generators == 0 || (microchips >> 1) & ~generators == 0;
    });
  }

  String getNewState(
      int items, int elevatorFloor, int step, int move, int dir) {
    var currentFloorMask = ~(move << (elevatorFloor * numItems * 2));
    var newFloorMask = move << ((elevatorFloor + dir) * numItems * 2);
    var newItems = items & currentFloorMask | newFloorMask;
    return getState(newItems, elevatorFloor + dir, step + 1);
  }

  Set<String> getNextStates(String state) {
    Set<String> ups = HashSet();
    Set<String> downs = HashSet();
    var items = getItems(state);
    var elevatorFloor = getElevatorFloor(state);
    var step = getSteps(state);
    List<int> oneMoves = List.empty(growable: true);
    int currentFloor = getFloor(state, elevatorFloor);
    for (int i = 1; i < 1 << numItems * 2; i <<= 1) {
      if (i & currentFloor != 0) {
        oneMoves.add(i);
      }
    }
    Set<int> twoMoves = HashSet();
    for (var i = 0; i < oneMoves.length - 1; i++) {
      for (var j = i + 1; j < oneMoves.length; j++) {
        twoMoves.add(oneMoves[i] | oneMoves[j]);
      }
    }
    if (elevatorFloor < 3) {
      for (var move in twoMoves) {
        var newState = getNewState(items, elevatorFloor, step, move, 1);
        if (isValid(newState)) {
          ups.add(newState);
        }
      }
      if (ups.length == 0) {
        for (var move in oneMoves) {
          var newState = getNewState(items, elevatorFloor, step, move, 1);
          if (isValid(newState)) {
            ups.add(newState);
          }
        }
      }
    }
    if (elevatorFloor > 0) {
      for (var move in oneMoves) {
        var newState = getNewState(items, elevatorFloor, step, move, -1);
        if (isValid(newState)) {
          downs.add(newState);
        }
      }
      if (downs.length == 0) {
        for (var move in twoMoves) {
          var newState = getNewState(items, elevatorFloor, step, move, -1);
          if (isValid(newState)) {
            downs.add(newState);
          }
        }
      }
    }
    ups.addAll(downs);
    return ups;
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
  var processor = Processor.prepareInitialState(arrangement);
  Set<int> visited = new HashSet();
  Queue<String> queue = Queue();
  var start = processor.initState;
  queue.add(start);
  visited.add(noSteps(start));

  while (queue.isNotEmpty) {
    var cur = queue.removeFirst();
    if (processor.isFinal(cur)) {
      return getSteps(cur);
    }
    for (var next in processor.getNextStates(cur)) {
      if (!visited.contains(noSteps(next))) {
        visited.add(noSteps(next));
        queue.add(next);
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
