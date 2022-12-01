import 'dart:convert';
import 'dart:io';
import 'package:crypto/crypto.dart';

String readInput() {
  var input = stdin.readLineSync(encoding: utf8);
  return input;
}

String generateMd5(String input) {
  return md5.convert(utf8.encode(input)).toString();
}

String part1(String input) {
  String password = '';
  int i = 0;
  while (password.length < 8) {
    var bytes = utf8.encode('$input$i');
    var md5Hash = generateMd5('$input$i');
    if (md5Hash.startsWith('00000')) {
      password += md5Hash[5];
    }
    i++;
  }
  return password;
}

String part2(String input) {
  List<String> password = ['', '', '', '', '', '', '', ''];
  int i = 0;
  while (password.join().length < 8) {
    var bytes = utf8.encode('$input$i');
    var md5Hash = generateMd5('$input$i');
    if (md5Hash.startsWith('00000')) {
      int pos = int.tryParse(md5Hash[5]);
      if (pos != null && pos >= 0 && pos < 8 && password[pos] == '') {
        password[pos] = md5Hash[6];
      }
    }
    i++;
  }
  return password.join();
}

void main() {
  var input = readInput();
  print('part1: ${part1(input)}');
  print('part2: ${part2(input)}');
}
