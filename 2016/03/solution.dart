import 'dart:convert';
import 'dart:io';

class Triangle {
  List<int> sides;
  Triangle(this.sides);

  bool isValid() {
    sides.sort();
    return sides[2] < sides[1] + sides[0];
  }
}

List<List<int>> readInput() {
  var lines = <List<int>>[];
  RegExp re = RegExp(r'(\d+)');
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    List<int> sides = [];
    re.allMatches(line).forEach((match) {
      sides.add(int.parse(line.substring(match.start, match.end)));
    });
    assert(sides.length == 3);
    lines.add(sides);
  }
  return lines;
}

int part1(List<List<int>> lines) {
  return lines
      .map((sides) => Triangle([...sides]))
      .where((triangle) => triangle.isValid())
      .length;
}

int part2(List<List<int>> lines) {
  assert(lines.length % 3 == 0);
  var triangles = <Triangle>[];
  for (var i = 0; i < lines.length; i += 3) {
    for (var j = 0; j < 3; j++) {
      triangles.add(Triangle([lines[i][j], lines[i + 1][j], lines[i + 2][j]]));
    }
  }
  return triangles.where((triangle) => triangle.isValid()).length;
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
