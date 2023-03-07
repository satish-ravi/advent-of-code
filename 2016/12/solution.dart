import 'dart:collection';
import 'dart:convert';
import 'dart:io';

enum Command { cpy, inc, dec, jnz }

class Instruction {
  Command cmd;
  String op1;
  String? op2;

  Instruction(this.cmd, this.op1, this.op2);
}

class Assembuny {
  List<Instruction> instructions;
  Map<String, int> registers;

  Assembuny(this.instructions, this.registers);

  void run() {
    var cur = 0;
    while (cur >= 0 && cur < instructions.length) {
      var ins = instructions[cur];
      switch (ins.cmd) {
        case Command.cpy:
          var op1 = int.tryParse(ins.op1);
          if (op1 != null) {
            registers[ins.op2!] = op1;
          } else {
            registers[ins.op2!] = registers[ins.op1]!;
          }
          cur++;
          break;
        case Command.inc:
          registers[ins.op1] = registers[ins.op1]! + 1;
          cur++;
          break;
        case Command.dec:
          registers[ins.op1] = registers[ins.op1]! - 1;
          cur++;
          break;
        case Command.jnz:
          var op1 = int.tryParse(ins.op1);
          var op2 = int.parse(ins.op2!);
          if ((op1 != null && op1 != 0) || registers[ins.op1]! != 0) {
            cur += op2;
          } else {
            cur++;
          }
      }
    }
  }
}

List<Instruction> readInput() {
  var instructions = <Instruction>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    var split = line.split(' ');
    switch (split[0]) {
      case 'cpy':
        instructions.add(Instruction(Command.cpy, split[1], split[2]));
        break;
      case 'inc':
        instructions.add(Instruction(Command.inc, split[1], null));
        break;
      case 'dec':
        instructions.add(Instruction(Command.dec, split[1], null));
        break;
      case 'jnz':
        instructions.add(Instruction(Command.jnz, split[1], split[2]));
        break;
      default:
        throw new Exception('invalid instruction ${line}');
    }
  }
  return instructions;
}

int part1(List<Instruction> instructions) {
  var code =
      Assembuny(instructions, HashMap.from({'a': 0, 'b': 0, 'c': 0, 'd': 0}));
  code.run();
  return code.registers['a']!;
}

int part2(List<Instruction> instructions) {
  var code =
      Assembuny(instructions, HashMap.from({'a': 0, 'b': 0, 'c': 1, 'd': 0}));
  code.run();
  return code.registers['a']!;
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
