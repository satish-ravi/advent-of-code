use std::io::{self, BufRead};
use std::convert::TryFrom;

struct Program {
    memory: Vec<i64>,
    cur: usize,
    relative_base: i64
}

impl Program {
    fn new(int_code: &[i64]) -> Program {
        let mut memory = int_code.to_vec();
        memory.resize(10000, 0);
        return Program {
            memory: memory,
            cur: 0,
            relative_base: 0
        }
    }

    fn get_param_pos(&self, mode: i64, pos: usize) -> usize {
        if mode == 1 {
            return pos;
        } else if mode == 2 {
            return usize::try_from(self.relative_base + self.memory[pos]).unwrap();
        } else {
            return usize::try_from(self.memory[pos]).unwrap();
        }
    }

    fn get_param(&self, mode: i64, pos: usize) -> i64 {
        return self.memory[self.get_param_pos(mode, pos)];
    }

    fn run_code(&mut self, input: i64) -> Vec<i64> {
        let mut output = Vec::new();
        let mut param1: i64;
        let mut param2: i64;
        let mut param3: usize;
        let mut op_code;

        loop {
            op_code = self.memory[self.cur] % 100;
            if op_code == 99 {
                return output;
            }
            assert!(op_code >= 1 && op_code <= 9);
            if op_code == 1 || op_code == 2 {
                param1 = self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1);
                param2 = self.get_param((self.memory[self.cur] / 1000) % 10, self.cur + 2);
                param3 = self.get_param_pos((self.memory[self.cur] / 10000) % 10, self.cur + 3);
                if op_code == 1 {
                    self.memory[param3] = param1 + param2;
                } else {
                    self.memory[param3] = param1 * param2;
                }
                self.cur += 4;
            } else if op_code == 3 {
                param3 = self.get_param_pos((self.memory[self.cur] / 100) % 10, self.cur + 1);
                self.memory[param3] = input;
                self.cur += 2;
            } else if op_code == 4 {
                output.push(self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1));
                self.cur += 2;
            } else if op_code == 5 || op_code == 6 {
                param1 = self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1);
                param2 = self.get_param((self.memory[self.cur] / 1000) % 10, self.cur + 2);
                if (op_code == 5 && param1 != 0) || (op_code == 6 && param1 == 0) {
                    self.cur = usize::try_from(param2).unwrap();
                } else {
                    self.cur += 3;
                }
            } else if op_code == 7 || op_code == 8 {
                param1 = self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1);
                param2 = self.get_param((self.memory[self.cur] / 1000) % 10, self.cur + 2);
                param3 = self.get_param_pos((self.memory[self.cur] / 10000) % 10, self.cur + 3);
                if (op_code == 7 && param1 < param2) || (op_code == 8 && param1 == param2) {
                    self.memory[param3] = 1;
                } else {
                    self.memory[param3] = 0;
                }
                self.cur += 4;
            } else {
                self.relative_base += self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1);
                self.cur += 2;
            }
        }
    }
}

fn read_data() -> Vec<i64> {
    let stdin = io::stdin();
    return stdin.lock().lines().next().unwrap().unwrap().split(",").map(|x| x.parse::<i64>().unwrap()).collect();
}

fn create_and_run_program(int_code: &[i64], input: i64) -> i64 {
    let mut program = Program::new(int_code);
    let output = program.run_code(input);
    return output[0]
}

fn main() {
    let input = read_data();
    println!("part1: {:?}", create_and_run_program(&input, 1));
    println!("part2: {:?}", create_and_run_program(&input, 2));
}
