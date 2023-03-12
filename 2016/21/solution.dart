import 'dart:convert';
import 'dart:io';

enum Operator {
  SWAP_POS,
  SWAP_LETTER,
  ROTATE_L,
  ROTATE_R,
  ROTATE_LETTER,
  REVERSE,
  MOVE
}

class Operation {
  Operator op;
  String op1;
  String? op2;

  Operation(this.op, this.op1, this.op2);

  List<String> apply(List<String> text) {
    List<String> newText = List.from(text);

    switch (op) {
      case Operator.SWAP_POS:
        var p1 = int.parse(op1);
        var p2 = int.parse(op2!);
        var temp = newText[p1];
        newText[p1] = newText[p2];
        newText[p2] = temp;
        break;
      case Operator.SWAP_LETTER:
        var p1 = newText.indexOf(op1);
        var p2 = newText.indexOf(op2!);
        var temp = newText[p1];
        newText[p1] = newText[p2];
        newText[p2] = temp;
        break;
      case Operator.ROTATE_L:
        var d = int.parse(op1);
        for (int i = 0; i < text.length; i++) {
          newText[(i - d) % text.length] = text[i];
        }
        break;
      case Operator.ROTATE_R:
        var d = int.parse(op1);
        for (int i = 0; i < text.length; i++) {
          newText[(i + d) % text.length] = text[i];
        }
        break;
      case Operator.ROTATE_LETTER:
        var d = text.indexOf(op1) + 1;
        if (d > 4) {
          d++;
        }
        for (int i = 0; i < text.length; i++) {
          newText[(i + d) % text.length] = text[i];
        }
        break;
      case Operator.REVERSE:
        var p1 = int.parse(op1);
        var p2 = int.parse(op2!);
        var sub = text.sublist(p1, p2 + 1).reversed.toList();
        for (int i = p1; i <= p2; i++) {
          newText[i] = sub[i - p1];
        }
        break;
      case Operator.MOVE:
        var p1 = int.parse(op1);
        var p2 = int.parse(op2!);
        newText[p2] = text[p1];
        if (p1 < p2) {
          for (int i = p1 + 1; i <= p2; i++) {
            newText[i - 1] = text[i];
          }
        } else {
          for (int i = p2; i <= p1 - 1; i++) {
            newText[i + 1] = text[i];
          }
        }
        break;
    }

    return newText;
  }

  List<String> applyInverse(List<String> text) {
    switch (op) {
      case Operator.SWAP_POS:
      case Operator.SWAP_LETTER:
      case Operator.REVERSE:
        return apply(text);
      case Operator.ROTATE_L:
        return Operation(Operator.ROTATE_R, op1, op2).apply(text);
      case Operator.ROTATE_R:
        return Operation(Operator.ROTATE_L, op1, op2).apply(text);
      case Operator.ROTATE_LETTER:
        // assumes 8 letter strings
        var leftRotations = [9, 1, 6, 2, 7, 3, 8, 4];
        return Operation(Operator.ROTATE_L,
                leftRotations[text.indexOf(op1)].toString(), null)
            .apply(text);
      case Operator.MOVE:
        return Operation(Operator.MOVE, op2!, op1).apply(text);
    }
  }
}

List<Operation> readInput() {
  var operations = <Operation>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    var split = line.split(' ');
    if (line.startsWith('swap position')) {
      operations.add(Operation(Operator.SWAP_POS, split[2], split[5]));
    } else if (line.startsWith('swap letter')) {
      operations.add(Operation(Operator.SWAP_LETTER, split[2], split[5]));
    } else if (line.startsWith('rotate left')) {
      operations.add(Operation(Operator.ROTATE_L, split[2], null));
    } else if (line.startsWith('rotate right')) {
      operations.add(Operation(Operator.ROTATE_R, split[2], null));
    } else if (line.startsWith('rotate based')) {
      operations.add(Operation(Operator.ROTATE_LETTER, split[6], null));
    } else if (line.startsWith('reverse')) {
      operations.add(Operation(Operator.REVERSE, split[2], split[4]));
    } else if (line.startsWith('move')) {
      operations.add(Operation(Operator.MOVE, split[2], split[5]));
    } else {
      throw new Exception('invalid line ${line}');
    }
  }
  return operations;
}

String part1(List<Operation> operations) {
  List<String> text = 'abcdefgh'.split('');
  for (var operation in operations) {
    text = operation.apply(text);
  }
  return text.join();
}

String part2(List<Operation> operations) {
  List<String> text = 'fbgdceah'.split('');
  for (var operation in operations.reversed) {
    text = operation.applyInverse(text);
  }
  return text.join();
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
