use std::io::{self, BufRead};
use std::convert::TryFrom;
use std::convert::TryInto;
use std::collections::HashMap;
use std::collections::HashSet;

struct Program {
    memory: Vec<i64>,
    cur: usize,
    relative_base: i64,
    map: HashMap<(i64, i64), u8>,
    oxygen: Option<(i64, i64)>,
    moves: usize,
}

impl Program {
    fn new(int_code: &[i64]) -> Program {
        let mut memory = int_code.to_vec();
        memory.resize(10000, 0);
        let mut map = HashMap::new();
        map.insert((0, 0), 1);
        return Program {
            memory: memory,
            cur: 0,
            relative_base: 0,
            map: map,
            oxygen: None,
            moves: 0,
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

    fn run_code(&mut self, input: i64) -> i64 {
        let mut param1: i64;
        let mut param2: i64;
        let mut param3: usize;
        let mut op_code;

        loop {
            op_code = self.memory[self.cur] % 100;
            if op_code == 99 {
                return 0;
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
                let out = self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1);
                self.cur += 2;
                return out;
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

    fn fill_map(&mut self, cur: (i64, i64), moves: usize) -> () {
        for i in 1..=4 {
            let next: (i64, i64) = match i {
                1 => (cur.0, cur.1-1),
                2 => (cur.0, cur.1+1),
                3 => (cur.0-1, cur.1),
                4 => (cur.0+1, cur.1),
                _ => panic!("invalid dir")
            };
            if !self.map.contains_key(&next) {
                let out = self.run_code(i as i64);
                self.map.insert(next, out.try_into().unwrap());
                if out == 2 {
                    self.oxygen = Some(next);
                    self.moves = moves + 1;
                }
                if out != 0 {
                    self.fill_map(next, moves + 1);
                    let back_input: i64 = match i {
                        1 => 2,
                        2 => 1,
                        3 => 4,
                        4 => 3,
                        _ => panic!("invalid back")
                    };
                    let back_out = self.run_code(back_input);
                    assert!(back_out == 1);
                }
            }
        }
    }

    fn fill_oxygen(&mut self) -> usize {
        let mut min = 0;
        loop {
            if self.map.values().filter(|&n| *n == 1).count() == 0 {
                return min;
            }
            min += 1;
            let mut new_filled = HashSet::new();
            for key in self.map.keys().cloned() {
                let val = *self.map.get(&key).unwrap();
                if val == 1 {
                    if vec![(0, -1), (0, 1), (-1, 0), (1, 0)].into_iter().map(|dir| (key.0 + dir.0, key.1 + dir.1)).any(|adj| self.map.get(&adj) == Some(&2)) {
                        new_filled.insert(key);
                    }
                }
            }
            for key in new_filled {
                self.map.insert(key, 2);
            }
        }
    }
}

fn read_data() -> Vec<i64> {
    let stdin = io::stdin();
    return stdin.lock().lines().next().unwrap().unwrap().split(",").map(|x| x.parse::<i64>().unwrap()).collect();
}

fn main() {
    let int_code = read_data();
    let mut program = Program::new(&int_code);
    program.fill_map((0, 0), 0);
    println!("part1: {:?}", program.moves);
    println!("part2: {:?}", program.fill_oxygen());
}
