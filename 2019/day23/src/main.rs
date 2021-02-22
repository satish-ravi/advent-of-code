use std::io::{self, BufRead};
use std::convert::TryFrom;
use std::collections::VecDeque;

struct Program {
    memory: Vec<i64>,
    cur: usize,
    relative_base: i64,
    input: VecDeque<i64>,
    output: VecDeque<i64>,
    halted: bool,
    no_in_count: usize,
}

impl Program {
    fn new(int_code: &[i64]) -> Program {
        let mut memory = int_code.to_vec();
        memory.resize(10000, 0);
        return Program {
            memory: memory,
            cur: 0,
            relative_base: 0,
            input: VecDeque::new(),
            output: VecDeque::new(),
            halted: false,
            no_in_count: 0
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

    fn run_code(&mut self) -> () {
        let param1: i64;
        let param2: i64;
        let param3: usize;
        let op_code;

        if self.halted {
            panic!("program finished!");
        }

        op_code = self.memory[self.cur] % 100;
        if op_code == 99 {
            self.halted = true;
            return;
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
            let input = match self.input.pop_front() {
                Some(inp) => { self.no_in_count = 0; inp },
                None => { self.no_in_count += 1; -1 }
            };
            self.memory[param3] = input;
            self.cur += 2;
        } else if op_code == 4 {
            self.output.push_back(self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1));
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

fn read_data() -> Vec<i64> {
    let stdin = io::stdin();
    return stdin.lock().lines().next().unwrap().unwrap().split(",").map(|x| x.parse::<i64>().unwrap()).collect();
}

fn part1(int_code: &[i64]) -> i64 {
    let mut controllers = Vec::new();
    for i in 0..50 {
        let mut controller = Program::new(int_code);
        controller.input.push_back(i);
        controllers.push(controller);
    }
    loop {
        for i in 0..50 {
            controllers[i].run_code();
        }
        for i in 0..50 {
            if controllers[i].output.len() == 3 {
                let dest = controllers[i].output.pop_front().unwrap();
                let x = controllers[i].output.pop_front().unwrap();
                let y = controllers[i].output.pop_front().unwrap();
                if dest == 255 {
                    return y;
                }
                if dest >= 0 && dest < 50 {
                    controllers[dest as usize].input.push_back(x);
                    controllers[dest as usize].input.push_back(y);
                }
            }
        }
    }
}

fn part2(int_code: &[i64]) -> i64 {
    let mut controllers = Vec::new();
    let mut nat_memory: Option<(i64, i64)> = None;
    let mut last_y: Option<i64> = None;
    for i in 0..50 {
        let mut controller = Program::new(int_code);
        controller.input.push_back(i);
        controllers.push(controller);
    }
    loop {
        for i in 0..50 {
            controllers[i].run_code();
        }
        for i in 0..50 {
            if controllers[i].output.len() == 3 {
                let dest = controllers[i].output.pop_front().unwrap();
                let x = controllers[i].output.pop_front().unwrap();
                let y = controllers[i].output.pop_front().unwrap();
                if dest == 255 {
                    nat_memory = Some((x, y));
                }
                if dest >= 0 && dest < 50 {
                    controllers[dest as usize].input.push_back(x);
                    controllers[dest as usize].input.push_back(y);
                }
            }
        }
        let mut is_idle = true;
        for i in 0..50 {
            if controllers[i].no_in_count == 0 {
                is_idle = false;
                break;
            }
        }
        if is_idle && nat_memory != None {
            let (x, y) = nat_memory.unwrap();
            if last_y != None && last_y.unwrap() == y {
                return y;
            }
            last_y = Some(y);
            controllers[0].input.push_back(x);
            controllers[0].input.push_back(y);
            nat_memory = None;
        }
    }
}

fn main() {
    let input = read_data();
    println!("part1: {:?}", part1(&input));
    println!("part2: {:?}", part2(&input));
}
