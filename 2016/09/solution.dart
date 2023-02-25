import 'dart:convert';
import 'dart:io';

String readInput() {
  return stdin.readLineSync(encoding: utf8)!;
}

int getLength(String compressed, int level, int maxDepth) {
  if (!compressed.contains('(') || (maxDepth > 0 && level > maxDepth)) {
    return compressed.length;
  }
  var cur = 0;
  var isMarker = false;
  var markerString = '';
  var length = 0;
  while (cur < compressed.length) {
    if (isMarker) {
      if (compressed[cur] == ')') {
        var split = markerString.split('x').map((e) => int.parse(e));
        var chars = split.first;
        var repeat = split.last;
        var toRepeat = compressed.substring(cur + 1, cur + chars + 1);
        length += repeat * getLength(toRepeat, level + 1, maxDepth);
        cur = cur + chars;
        isMarker = false;
        markerString = '';
      } else {
        markerString += compressed[cur];
      }
    } else {
      if (compressed[cur] == '(') {
        isMarker = true;
      } else {
        length++;
      }
    }
    cur += 1;
  }
  return length;
}

int part1(String compressed) {
  return getLength(compressed, 1, 1);
}

int part2(String compressed) {
  return getLength(compressed, 1, -1);
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
