import 'dart:convert';
import 'dart:io';

class Room {
  String name;
  int sectorId;
  String checkSum;

  Room(this.name, this.sectorId, this.checkSum);

  String computeCheckSum() {
    Map<String, int> charCounts = {};
    for (int i = 0; i < this.name.length; i++) {
      if (this.name[i] == '-') {
        continue;
      }
      int count = charCounts[this.name[i]] ?? 0;
      charCounts[this.name[i]] = count + 1;
    }
    var sortedChars = charCounts.keys.toList(growable: false)
      ..sort((k1, k2) {
        int valCompare = charCounts[k2]!.compareTo(charCounts[k1]!);
        return valCompare == 0 ? k1.compareTo(k2) : valCompare;
      });
    return sortedChars.sublist(0, 5).join();
  }

  bool isValid() {
    return checkSum == computeCheckSum();
  }

  String decrypt() {
    List charCodes = this.name.codeUnits;
    return String.fromCharCodes(charCodes
        .map((ch) => ch == 45 ? 32 : ((ch - 97 + sectorId) % 26) + 97));
  }
}

List<Room> readInput() {
  var rooms = <Room>[];
  var re = RegExp(r'(.*)-(\d+)\[([a-z]{5})\]');
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    var match = re.firstMatch(line);
    assert(match != null);
    var name = match!.group(1)!;
    var sectorId = int.parse(match.group(2)!);
    var checkSum = match.group(3)!;
    rooms.add(Room(name, sectorId, checkSum));
  }
  return rooms;
}

int part1(List<Room> rooms) {
  return rooms
      .where((room) => room.isValid())
      .map((room) => room.sectorId)
      .reduce((value, element) => value + element);
}

int part2(List<Room> rooms) {
  return rooms
      .where((room) => room.isValid())
      .firstWhere((room) => room.decrypt() == 'northpole object storage')
      .sectorId;
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
