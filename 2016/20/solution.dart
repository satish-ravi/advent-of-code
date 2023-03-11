import 'dart:convert';
import 'dart:io';
import 'dart:math';

class Range {
  int low;
  int high;

  Range(this.low, this.high);
}

List<Range> readInput() {
  var ranges = <Range>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    var split = line.split('-');
    ranges.add(Range(int.parse(split[0]), int.parse(split[1])));
  }
  return ranges;
}

int part1(List<Range> ranges) {
  List<Range> local = List.from(ranges);
  local.sort((a, b) => a.low.compareTo(b.low));
  var minIp = 0;
  for (var range in local) {
    if (minIp < range.low) {
      return minIp;
    }
    minIp = max(range.high + 1, minIp);
  }
  throw new Exception('not found');
}

int part2(List<Range> ranges) {
  List<Range> local = List.from(ranges);
  local.sort((a, b) => a.low.compareTo(b.low));
  var allowed = 0;
  var maxSeen = -1;

  for (var range in local) {
    if (range.low > maxSeen + 1) {
      allowed += range.low - (maxSeen + 1);
    }
    maxSeen = max(maxSeen, range.high);
  }
  return allowed + 4294967295 - maxSeen;
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
