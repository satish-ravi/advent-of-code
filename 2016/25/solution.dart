import 'dart:collection';
import 'dart:convert';
import 'dart:io';

enum Command { cpy, inc, dec, jnz, tgl, out }

class Instruction {
  Command cmd;
  String op1;
  String? op2;

  Instruction(this.cmd, this.op1, this.op2);

  @override
  String toString() {
    return '${cmd},${op1},${op2}';
  }
}

class Assembuny {
  List<Instruction> instructions;
  Map<String, int> registers;

  Assembuny(this.instructions, this.registers);

  bool producesClockSignal() {
    var cur = 0;
    var out = '';
    var nextOut = 0;
    while (cur >= 0 && cur < instructions.length) {
      var ins = instructions[cur];
      switch (ins.cmd) {
        case Command.cpy:
          var op1 = int.tryParse(ins.op1);
          if (registers.containsKey(ins.op2)) {
            if (op1 != null) {
              registers[ins.op2!] = op1;
            } else {
              registers[ins.op2!] = registers[ins.op1]!;
            }
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
          var op2 = int.tryParse(ins.op2!);
          if (op2 == null) {
            op2 = registers[ins.op2!];
          }
          if ((op1 != null && op1 != 0) ||
              (op1 != 0 && registers[ins.op1]! != 0)) {
            cur += op2!;
          } else {
            cur++;
          }
          break;
        case Command.tgl:
          var jump = int.tryParse(ins.op1);
          if (jump == null) {
            jump = registers[ins.op1]!;
          }
          var dest = cur + jump;
          if (dest >= 0 && dest < instructions.length) {
            var destIns = instructions[dest];
            if (destIns.op2 == null) {
              if (destIns.cmd == Command.inc) {
                instructions[dest] =
                    Instruction(Command.dec, destIns.op1, destIns.op2);
              } else {
                instructions[dest] =
                    Instruction(Command.inc, destIns.op1, destIns.op2);
              }
            } else {
              if (destIns.cmd == Command.jnz) {
                instructions[dest] =
                    Instruction(Command.cpy, destIns.op1, destIns.op2);
              } else {
                instructions[dest] =
                    Instruction(Command.jnz, destIns.op1, destIns.op2);
              }
            }
          }
          cur++;
          break;
        case Command.out:
          var op1 = int.tryParse(ins.op1);
          if (op1 == null) {
            op1 = registers[ins.op1];
          }
          out += op1!.toString();
          if (op1 != nextOut) {
            return false;
          }
          if (out.length == 20) {
            return true;
          }
          nextOut = (nextOut + 1) % 2;
          cur++;
          break;
      }
      // print(instructions);
    }
    return false;
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
      case 'tgl':
        instructions.add(Instruction(Command.tgl, split[1], null));
        break;
      case 'out':
        instructions.add(Instruction(Command.out, split[1], null));
        break;
      default:
        throw new Exception('invalid instruction ${line}');
    }
  }
  return instructions;
}

int part1(List<Instruction> instructions) {
  var aValue = 1;
  while (true) {
    var code = Assembuny(List.from(instructions),
        HashMap.from({'a': aValue, 'b': 0, 'c': 0, 'd': 0}));
    if (code.producesClockSignal()) {
      return aValue;
    }
    aValue++;
  }
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
}
