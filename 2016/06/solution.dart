import 'dart:convert';
import 'dart:io';

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

Map getCharCounts(str) {
  var charCounts = Map();
  str.split('').forEach((ch) {
    if (!charCounts.containsKey(ch)) {
      charCounts[ch] = 0;
    }
    charCounts[ch] += 1;
  });
  return charCounts;
}

String getMostOccurringCharacter(String str) {
  var charCounts = getCharCounts(str);
  var maxChar = '';
  var maxCount = -1;
  charCounts.forEach((ch, count) {
    if (count > maxCount) {
      maxCount = count;
      maxChar = ch;
    }
  });
  return maxChar;
}

String getLeastOccurringCharacter(String str) {
  var charCounts = getCharCounts(str);
  var minChar = '';
  var minCount = double.maxFinite.toInt();
  charCounts.forEach((ch, count) {
    if (count < minCount) {
      minCount = count;
      minChar = ch;
    }
  });
  return minChar;
}

String solve(List<String> lines, Function(String) fn) {
  var cols = List.filled(lines[0].length, '');
  lines.forEach((line) {
    for (var i = 0; i < line.length; i++) {
      cols[i] += line[i];
    }
  });
  var ans = '';
  cols.forEach((col) {
    ans += fn(col);
  });
  return ans;
}

void main() {
  var input = readInput();
  print('part1: ${solve(input, getMostOccurringCharacter)}');
  print('part2: ${solve(input, getLeastOccurringCharacter)}');
}
