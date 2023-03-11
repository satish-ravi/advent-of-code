import 'dart:convert';
import 'dart:io';

class Elf {
  int num;
  Elf? left = null;

  Elf(this.num);
}

Elf prepareInitialState(int n) {
  var last = Elf(n);
  var prev = last;
  for (var i = n - 1; i >= 1; i--) {
    var cur = Elf(i);
    cur.left = prev;
    prev = cur;
  }
  last.left = prev;

  return prev;
}

int readInput() {
  var line = stdin.readLineSync(encoding: utf8);
  return int.parse(line!);
}

int part1(int input) {
  var elf = prepareInitialState(input);

  while (elf.left!.num != elf.num) {
    elf.left = elf.left!.left;
    elf = elf.left!;
  }
  return elf.num;
}

int part2(int input) {
  var elf = prepareInitialState(input);
  var oppPrev = elf;
  var dist = 0;
  var len = input;
  while (dist < len ~/ 2 - 1) {
    oppPrev = oppPrev.left!;
    dist++;
  }

  while (len > 1) {
    var target = len ~/ 2;
    while (dist < target - 1) {
      oppPrev = oppPrev.left!;
      dist++;
    }

    oppPrev.left = oppPrev.left!.left;

    len--;
    elf = elf.left!;
    dist--;
  }
  return elf.num;
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
