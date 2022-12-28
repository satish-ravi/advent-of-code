import 'dart:convert';
import 'dart:io';

bool hasAbba(String str) {
  for (var i = 0; i < str.length - 3; i++) {
    if (str[i] == str[i + 3] &&
        str[i + 1] == str[i + 2] &&
        str[i] != str[i + 1]) {
      return true;
    }
  }
  return false;
}

List<String> getAbas(String str) {
  List<String> abas = [];
  for (var i = 0; i < str.length - 2; i++) {
    if (str[i] == str[i + 2] && str[i] != str[i + 1]) {
      abas.add(str.substring(i, i + 3));
    }
  }
  return abas;
}

String getBab(String aba) {
  return '${aba[1]}${aba[0]}${aba[1]}';
}

class Ipv7 {
  List<String> ins;
  List<String> outs;

  Ipv7(this.ins, this.outs);

  factory Ipv7.fromString(String ipv7) {
    var split = ipv7.split(new RegExp(r'[\[\]]'));
    List<String> ins = List.empty(growable: true);
    List<String> outs = List.empty(growable: true);
    for (var i = 0; i < split.length; i++) {
      if (i % 2 == 0) {
        outs.add(split[i]);
      } else {
        ins.add(split[i]);
      }
    }
    return Ipv7(ins, outs);
  }

  bool supportsTls() {
    return outs.any((element) => hasAbba(element)) &&
        ins.every((element) => !hasAbba(element));
  }

  bool supportsSsl() {
    List<String> potentialBabs = [];
    outs.forEach((element) {
      potentialBabs.addAll(getAbas(element).map((e) => getBab(e)));
    });
    return ins
        .any((element) => potentialBabs.any((bab) => element.contains(bab)));
  }
}

List<Ipv7> readInput() {
  var ips = <Ipv7>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    ips.add(Ipv7.fromString(line));
  }
  return ips;
}

int part1(List<Ipv7> ips) {
  return ips.where((ip) => ip.supportsTls()).length;
}

int part2(List<Ipv7> ips) {
  return ips.where((ip) => ip.supportsSsl()).length;
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
