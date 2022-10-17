import 'dart:collection';
import 'dart:convert';
import 'dart:io';

List<String> readInput() {
  var input = stdin.readLineSync(encoding: utf8)!;
  return input.split(", ");
}

int solve(List<String> input, [bool part2 = false]) {
  var x = 0;
  var y = 0;
  var facing = 0;
  final visited = HashSet<String>();
  for (var item in input) {
    var dir = item[0];
    var len = int.parse(item.substring(1));
    facing = (facing + (dir == 'R' ? 1 : -1) + 4) % 4;
    final newPoints = <String>[];
    switch (facing) {
      case 0:
        {
          for (var dy = 1; dy <= len; dy++) {
            var cy = y + dy;
            newPoints.add('$x,$cy');
          }
          y += len;
        }
        break;
      case 1:
        {
          for (var dx = 1; dx <= len; dx++) {
            var cx = x + dx;
            newPoints.add('$cx,$y');
          }
          x += len;
        }
        break;
      case 2:
        {
          for (var dy = 1; dy <= len; dy++) {
            var cy = y - dy;
            newPoints.add('$x,$cy');
          }
          y -= len;
        }
        break;
      case 3:
        {
          for (var dx = 1; dx <= len; dx++) {
            var cx = x - dx;
            newPoints.add('$cx,$y');
          }
          x -= len;
        }
        break;
      default:
        {
          throw Exception('invalid facing direction');
        }
    }
    for (var point in newPoints) {
      if (part2 && visited.contains(point)) {
        var splitPoint = point.split(",");
        var cx = int.parse(splitPoint[0]);
        var cy = int.parse(splitPoint[1]);
        return cx.abs() + cy.abs();
      }
      visited.add(point);
    }
  }
  if (part2) {
    print(visited);
    throw new Exception('no intersection point found');
  }
  return x.abs() + y.abs();
}

void main() {
  var input = readInput();
  print('part1: ${solve(input)}');
  print('part2: ${solve(input, true)}');
}
