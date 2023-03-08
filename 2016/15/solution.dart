import 'dart:collection';
import 'dart:convert';
import 'dart:io';

enum Command { cpy, inc, dec, jnz }

class Disc {
  int num;
  int positions;
  int t0Position;
  Disc(this.num, this.positions, this.t0Position);
}

List<Disc> readInput() {
  var discs = <Disc>[];
  int num = 1;
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    var split = line.split(' ');
    discs.add(
        Disc(num++, int.parse(split[3]), int.parse(split[11].split('.')[0])));
  }
  return discs;
}

int getPosAtTime(Disc disc, int time) {
  return (time + disc.num + disc.t0Position) % disc.positions;
}

int solve(List<Disc> discs) {
  int time = 0;
  while (true) {
    if (discs.every((disc) => getPosAtTime(disc, time) == 0)) {
      return time;
    }
    time++;
  }
}

int part1(List<Disc> discs) {
  return solve(discs);
}

int part2(List<Disc> discs) {
  List<Disc> newDiscs = List.from(discs);
  newDiscs.add(Disc(discs.length + 1, 11, 0));
  return solve(newDiscs);
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
