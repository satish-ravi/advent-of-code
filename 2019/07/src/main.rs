use itertools::Itertools;
use std::io::{self, BufRead};
use std::convert::TryFrom;

struct Amplifier {
    memory: Vec<i32>,
    phase: i32,
    cur: usize,
    finished: bool,
}

impl Amplifier {
    fn new(int_code: &[i32], phase: i32) -> Amplifier {
        return Amplifier {
            memory: int_code.to_vec(),
            phase: phase,
            cur: 0,
            finished: false
        }
    }

    fn get_param(&self, mode: i32, pos: usize) -> i32 {
        if mode == 1 {
            return self.memory[pos];
        } else {
            return self.memory[usize::try_from(self.memory[pos]).unwrap()]
        }
    }

    fn run_code(&mut self, input: i32) -> i32 {
        let mut output = 0;
        let mut param1: i32;
        let mut param2: i32;
        let mut param3: usize;
        let mut op_code;
        let mut used_input = false;

        if self.finished {
            assert!(false);
        }

        loop {
            op_code = self.memory[self.cur] % 100;
            if op_code == 99 {
                self.finished = true;
                break;
            }
            assert!(op_code >= 1 && op_code <= 8);
            if op_code == 1 || op_code == 2 {
                param1 = self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1);
                param2 = self.get_param((self.memory[self.cur] / 1000) % 10, self.cur + 2);
                param3 = usize::try_from(self.memory[self.cur + 3]).unwrap();
                if op_code == 1 {
                    self.memory[param3] = param1 + param2;
                } else {
                    self.memory[param3] = param1 * param2;
                }
                self.cur += 4;
            } else if op_code == 3 {
                if used_input {
                    break;
                }
                param3 = usize::try_from(self.memory[self.cur + 1]).unwrap();
                self.memory[param3] = match self.cur {
                    0 => self.phase,
                    _ => input
                };
                if self.cur != 0 {
                    used_input = true;
                }
                self.cur += 2;
            } else if op_code == 4 {
                output = self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1);
                self.cur += 2;
            } else if op_code == 5 || op_code == 6 {
                param1 = self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1);
                param2 = self.get_param((self.memory[self.cur] / 1000) % 10, self.cur + 2);
                if (op_code == 5 && param1 != 0) || (op_code == 6 && param1 == 0) {
                    self.cur = usize::try_from(param2).unwrap();
                } else {
                    self.cur += 3;
                }
            } else {
                param1 = self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1);
                param2 = self.get_param((self.memory[self.cur] / 1000) % 10, self.cur + 2);
                param3 = usize::try_from(self.memory[self.cur + 3]).unwrap();
                if (op_code == 7 && param1 < param2) || (op_code == 8 && param1 == param2) {
                    self.memory[param3] = 1;
                } else {
                    self.memory[param3] = 0;
                }
                self.cur += 4;
            }
        }
        return output;
    }
}

fn read_data() -> Vec<i32> {
    let stdin = io::stdin();
    return stdin.lock().lines().next().unwrap().unwrap().split(",").map(|x| x.parse::<i32>().unwrap()).collect();
}

fn run_amplifiers(int_code: &[i32], phases: &[&i32]) -> i32 {
    let mut input = 0;
    let mut amplifier_a = Amplifier::new(int_code, *phases[0]);
    let mut amplifier_b = Amplifier::new(int_code, *phases[1]);
    let mut amplifier_c = Amplifier::new(int_code, *phases[2]);
    let mut amplifier_d = Amplifier::new(int_code, *phases[3]);
    let mut amplifier_e = Amplifier::new(int_code, *phases[4]);
    loop {
        input = amplifier_a.run_code(input);
        input = amplifier_b.run_code(input);
        input = amplifier_c.run_code(input);
        input = amplifier_d.run_code(input);
        input = amplifier_e.run_code(input);
        if amplifier_e.finished {
            return input;
        }
    }
}

fn find_max(program: &[i32], possible_phases: &[i32]) -> i32 {
    let mut max = -1;
    for phases in possible_phases.iter().permutations(5).unique() {
        let cur = run_amplifiers(program, &phases[..]);
        if cur > max {
            max = cur;
        }
    }
    return max;
}

fn main() {
    let input = read_data();
    println!("part1: {:?}", find_max(&input, &[0, 1, 2, 3, 4]));
    println!("part2: {:?}", find_max(&input, &[5, 6, 7, 8, 9]));
}
