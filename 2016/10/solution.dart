import 'dart:collection';
import 'dart:convert';
import 'dart:io';

class Bot {
  int lowVal = -1;
  int highVal = -1;
  String lowIns = '';
  int lowInsVal = -1;
  String highIns = '';
  int highInsVal = -1;

  bool hasTwoValues() {
    return lowVal != -1 && highVal != -1;
  }

  void setInstruction(String ins) {
    var split = ins.split('and');
    var lowInsSplit = split[0].split('to ')[1].split(' ');
    var highInsSplit = split[1].split('to ')[1].split(' ');
    lowIns = lowInsSplit[0];
    lowInsVal = int.parse(lowInsSplit[1]);
    highIns = highInsSplit[0];
    highInsVal = int.parse(highInsSplit[1]);
  }

  void setValue(int val) {
    if (lowVal == -1) {
      lowVal = val;
    } else if (highVal == -1) {
      if (val < lowVal) {
        highVal = lowVal;
        lowVal = val;
      } else {
        highVal = val;
      }
    } else {
      throw new Exception('bot already has two values');
    }
  }

  void clear() {
    lowVal = -1;
    highVal = -1;
  }
}

class State {
  Map<int, Bot> bots = HashMap();
  Map<int, int> outputs = HashMap();

  void prepareState(List<String> instructions) {
    for (var ins in instructions) {
      var split = ins.split(' ');
      if (ins.startsWith('value')) {
        var botNum = int.parse(split[5]);
        bots.putIfAbsent(botNum, () => Bot());
        bots[botNum]!.setValue(int.parse(split[1]));
      } else if (ins.startsWith('bot')) {
        var botNum = int.parse(split[1]);
        bots.putIfAbsent(botNum, () => Bot());
        bots[botNum]!.setInstruction(ins);
      } else {
        throw new Exception("invalid instruction ${ins}");
      }
    }
  }

  void runOneBot() {
    for (var entry in bots.entries) {
      var num = entry.key;
      var bot = entry.value;
      if (bot.hasTwoValues()) {
        if (bot.lowIns == 'bot') {
          bots[bot.lowInsVal]!.setValue(bot.lowVal);
        } else {
          outputs[bot.lowInsVal] = bot.lowVal;
        }

        if (bot.highIns == 'bot') {
          bots[bot.highInsVal]!.setValue(bot.highVal);
        } else {
          outputs[bot.highInsVal] = bot.highVal;
        }
        bot.clear();
        return;
      }
    }
    throw new Exception('no bot with 2 values');
  }

  int getBotWithVal(int low, int high) {
    for (var entry in bots.entries) {
      var num = entry.key;
      var bot = entry.value;
      if (bot.lowVal == low && bot.highVal == high) {
        return num;
      }
    }
    return -1;
  }

  int getOutputVals() {
    if (outputs[0] != null && outputs[1] != null && outputs[2] != null) {
      return outputs[0]! * outputs[1]! * outputs[2]!;
    }
    return -1;
  }
}

List<String> readInput() {
  var instructions = <String>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    instructions.add(line);
  }
  return instructions;
}

int part1(List<String> instructions) {
  var state = State();
  state.prepareState(instructions);
  while (true) {
    var bot = state.getBotWithVal(17, 61);
    if (bot != -1) {
      return bot;
    }
    state.runOneBot();
  }
}

int part2(List<String> instructions) {
  var state = State();
  state.prepareState(instructions);
  while (true) {
    var product = state.getOutputVals();
    if (product != -1) {
      return product;
    }
    state.runOneBot();
  }
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
