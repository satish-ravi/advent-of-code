import 'dart:convert';
import 'dart:io';
import 'dart:math';

abstract class Keypad {
  void apply(String dir);
  String current();
}

class Point {
  int x, y;
  Point(this.x, this.y);

  @override
  operator ==(o) => o is Point && o.x == x && o.y == y;

  @override
  int get hashCode => '$x,$y'.hashCode;
}

class Keypad1 implements Keypad {
  Point p = Point(1, 1);

  void apply(String dir) {
    switch (dir) {
      case 'U':
        {
          this.p.y = max(this.p.y - 1, 0);
        }
        break;
      case 'D':
        {
          this.p.y = min(this.p.y + 1, 2);
        }
        break;
      case 'L':
        {
          this.p.x = max(this.p.x - 1, 0);
        }
        break;
      case 'R':
        {
          this.p.x = min(this.p.x + 1, 2);
        }
        break;
      default:
        {
          throw new Exception('invalid instruction $dir');
        }
    }
  }

  String current() {
    return '${this.p.y * 3 + this.p.x + 1}';
  }
}

class Keypad2 implements Keypad {
  var pointToCode = {
    Point(2, 0): '1',
    Point(1, 1): '2',
    Point(2, 1): '3',
    Point(3, 1): '4',
    Point(0, 2): '5',
    Point(1, 2): '6',
    Point(2, 2): '7',
    Point(3, 2): '8',
    Point(4, 2): '9',
    Point(1, 3): 'A',
    Point(2, 3): 'B',
    Point(3, 3): 'C',
    Point(2, 4): 'D',
  };

  Point p = Point(2, 0);

  void apply(String dir) {
    var newPoint = Point(this.p.x, this.p.y);
    switch (dir) {
      case 'U':
        {
          newPoint.y = max(this.p.y - 1, 0);
        }
        break;
      case 'D':
        {
          newPoint.y = min(this.p.y + 1, 4);
        }
        break;
      case 'L':
        {
          newPoint.x = max(this.p.x - 1, 0);
        }
        break;
      case 'R':
        {
          newPoint.x = min(this.p.x + 1, 4);
        }
        break;
      default:
        {
          throw new Exception('invalid instruction $dir');
        }
    }
    if (pointToCode.containsKey(newPoint)) {
      this.p = newPoint;
    }
  }

  String current() {
    return '${pointToCode[this.p]}';
  }
}

List<String> readInput() {
  var lines = <String>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    lines.add(line);
  }
  return lines;
}

String solve(List<String> instructions, Keypad keypad) {
  var code = '';
  for (var instruction in instructions) {
    for (var dir in instruction.split('')) {
      keypad.apply(dir);
    }
    var currentCode = keypad.current();
    code = '$code$currentCode';
  }
  return code;
}

void main() {
  var input = readInput();
  print('part1: ${solve(input, Keypad1())}');
  print('part2: ${solve(input, Keypad2())}');
}
