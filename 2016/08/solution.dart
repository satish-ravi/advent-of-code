import 'dart:convert';
import 'dart:io';

class Display {
  int width;
  int height;
  Set<int> pixels = new Set();

  Display(this.width, this.height);

  void rect(int A, int B) {
    for (var i = 0; i < B; i++) {
      for (var j = 0; j < A; j++) {
        pixels.add(i * width + j);
      }
    }
  }

  void rotateRow(int A, int B) {
    Set<int> newPixels = new Set();
    for (var pixel in pixels) {
      var i = pixel ~/ width;
      var j = pixel % width;
      if (i == A) {
        newPixels.add(i * width + (j + B) % width);
      } else {
        newPixels.add(pixel);
      }
    }
    this.pixels = newPixels;
  }

  void rotateColumn(int A, int B) {
    Set<int> newPixels = new Set();
    for (var pixel in pixels) {
      var i = pixel ~/ width;
      var j = pixel % width;
      if (j == A) {
        newPixels.add(((i + B) % height) * width + j);
      } else {
        newPixels.add(pixel);
      }
    }
    this.pixels = newPixels;
  }

  void applyInstruction(String ins) {
    var nums = RegExp(r'\d+').allMatches(ins).map((m) => m.group(0));
    if (nums.length != 2) {
      throw new Exception("invalid instruction ${ins}");
    }
    int A = int.parse(nums.first!);
    int B = int.parse(nums.last!);
    if (ins.startsWith("rect")) {
      rect(A, B);
    } else if (ins.startsWith("rotate") && ins.contains("row")) {
      rotateRow(A, B);
    } else if (ins.startsWith("rotate") && ins.contains("column")) {
      rotateColumn(A, B);
    } else {
      throw new Exception("invalid instruction ${ins}");
    }
  }

  String getPixelDisplay() {
    var disp = '';
    for (var i = 0; i < height; i++) {
      disp += '\n';
      for (var j = 0; j < width; j++) {
        if (pixels.contains(i * width + j)) {
          disp += '#';
        } else {
          disp += '.';
        }
      }
    }
    return disp;
  }

  int count() {
    return pixels.length;
  }
}

List<String> readInput() {
  var instructions = <String>[];
  while (true) {
    var line = stdin.readLineSync(encoding: utf8);
    if (line == null) {
      break;
    }
    instructions.add(line);
  }
  return instructions;
}

Display solve(List<String> ins) {
  Display display = new Display(50, 6);
  for (var instruction in ins) {
    display.applyInstruction(instruction);
  }
  return display;
}

int part1(Display display) {
  return display.count();
}

String part2(Display display) {
  return display.getPixelDisplay();
}

void main() {
  var input = readInput();
  var display = solve(input);
  print('part1: ${part1(display)}');
  print('part2: ${part2(display)}');
}
