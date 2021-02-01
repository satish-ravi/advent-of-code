use std::io::{self, BufRead};
use std::convert::TryFrom;
use std::collections::HashMap;

struct Program {
    memory: Vec<i64>,
    cur: usize,
    relative_base: i64,
    panel: HashMap<(isize, isize), usize>,
    robot_loc: (isize, isize),
    robot_dir: usize
}

impl Program {
    fn new(int_code: &[i64], start_panel_color: usize) -> Program {
        let mut memory = int_code.to_vec();
        let mut start_panel = HashMap::new();
        start_panel.insert((0, 0), start_panel_color);
        memory.resize(10000, 0);
        return Program {
            memory: memory,
            cur: 0,
            relative_base: 0,
            panel: start_panel,
            robot_loc: (0, 0),
            robot_dir: 0
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

    fn get_current_panel_color(&self) -> usize {
        match self.panel.get(&self.robot_loc) {
            Some(color) => *color,
            None => 0
        }
    }

    fn update_robot_loc(&mut self, rotation: usize) -> () {
        assert!(rotation <= 1);
        let incr = match rotation {
            0 => 3,
            1 => 1,
            _ => 0
        };
        self.robot_dir = (self.robot_dir + incr) % 4;
        assert!(self.robot_dir <= 3);
        let loc_incr: (isize, isize) = match self.robot_dir {
            0 => (-1, 0),
            1 => (0, 1),
            2 => (1, 0),
            3 => (0, -1),
            _ => (0, 0)
        };
        self.robot_loc = (self.robot_loc.0 + loc_incr.0, self.robot_loc.1 + loc_incr.1);
    }

    fn run_code(&mut self) -> Vec<i64> {
        let mut output = Vec::new();
        let mut param1: i64;
        let mut param2: i64;
        let mut param3: usize;
        let mut op_code;
        let mut output_is_color = true;

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
                self.memory[param3] = self.get_current_panel_color() as i64;
                self.cur += 2;
            } else if op_code == 4 {
                let out_val = usize::try_from(self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1)).unwrap();
                output.push(self.get_param((self.memory[self.cur] / 100) % 10, self.cur + 1));
                self.cur += 2;
                if output_is_color {
                    self.panel.insert(self.robot_loc, out_val);
                } else {
                    self.update_robot_loc(out_val);
                }
                output_is_color = !output_is_color;
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

    fn print_panel(&self) -> () {
        let mut mini = isize::MAX;
        let mut minj = isize::MAX;
        let mut maxi = isize::MIN;
        let mut maxj = isize::MIN;
        for key in self.panel.keys() {
            if key.0 < mini {
                mini = key.0;
            } else if key.0 > maxi {
                maxi = key.0;
            }
            if key.1 < minj {
                minj = key.1;
            } else if key.1 > maxj {
                maxj = key.1;
            }
        }
        for i in mini..=maxi {
            let mut row = "".to_owned();
            for j in minj..=maxj {
                match self.panel.get(&(i, j)) {
                    Some(1) => row.push_str("█"),
                    _ => row.push_str(" ")
                }
            }
            println!("{}", row);
        }
    }
}

fn read_data() -> Vec<i64> {
    let stdin = io::stdin();
    return stdin.lock().lines().next().unwrap().unwrap().split(",").map(|x| x.parse::<i64>().unwrap()).collect();
}

fn part1(int_code: &[i64]) -> usize {
    let mut program = Program::new(int_code, 0);
    program.run_code();
    return program.panel.keys().len();
}

fn part2(int_code: &[i64]) -> () {
    let mut program = Program::new(int_code, 1);
    program.run_code();
    program.print_panel();
}

fn main() {
    let input = read_data();
    println!("part1: {:?}", part1(&input));
    println!("part2:");
    part2(&input);
}
