import 'dart:collection';
import 'dart:convert';
import 'dart:io';
import 'dart:math';

class Node {
  int x;
  int y;
  int size;
  int used;
  int avail;
  int usePercent;

  Node(this.x, this.y, this.size, this.used, this.avail, this.usePercent);

  static Node createNode(String str) {
    var nums = RegExp(r'\d+')
        .allMatches(str)
        .map((m) => m.group(0))
        .map((e) => int.parse(e!))
        .toList();
    return Node(nums[0], nums[1], nums[2], nums[3], nums[4], nums[5]);
  }
}

List<Node> readInput() {
  var nodes = <Node>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    if (line.startsWith('/dev')) nodes.add(Node.createNode(line));
  }
  return nodes;
}

int part1(List<Node> nodes) {
  var count = 0;
  for (int i = 0; i < nodes.length; i++) {
    for (int j = 0; j < nodes.length; j++) {
      if (i != j && nodes[i].used > 0 && nodes[j].avail >= nodes[i].used) {
        // print('${nodes[i].x}, ${nodes[i].y}, ${nodes[j].x}, ${nodes[j].y}');
        count++;
      }
    }
  }
  return count;
}

int part2(List<Node> nodes) {
  Map<String, Node> indexed = HashMap();
  var xMax = 0;
  var yMax = 0;
  for (var node in nodes) {
    xMax = max(node.x, xMax);
    yMax = max(node.y, yMax);
    indexed['${node.x},${node.y}'] = node;
  }
  assert((xMax + 1) * (yMax + 1) == nodes.length);

  var emptyKey;

  for (var x = 0; x <= xMax; x++) {
    var row = [];
    for (var y = 0; y <= yMax; y++) {
      var key = '${x},${y}';
      if (x == 0 && y == 0) {
        row.add('D');
      } else if (y == 0 && x == xMax) {
        row.add('S');
      } else if (indexed[key]!.used == 0) {
        emptyKey = key;
        row.add('-');
      } else if (indexed[key]!.used >= 100) {
        row.add('#');
      } else {
        row.add('.');
      }
    }
    print(row.join(' ') + '  ${x}');
  }
  print(emptyKey);
  // bring the empty space to '0,xMax-1' (needs to go 4 up to then empty.y left,
  // then xMax-1-empty.x-4 down)
  // move target 1 up, empty space moves down
  // then repeat moving empty space from below the destination to above (4
  // steps and then move the target file up)
  return 4 + 12 + 10 + 1 + 5 * 33;
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
