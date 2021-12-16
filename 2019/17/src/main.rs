use std::io::{self, BufRead};
use std::convert::TryFrom;
use std::collections::HashSet;

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

    fn run_code(&mut self, input: &[i64]) -> Vec<i64> {
        let mut output = Vec::new();
        let mut param1: i64;
        let mut param2: i64;
        let mut param3: usize;
        let mut op_code;
        let mut input_idx = 0;

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
                self.memory[param3] = input[input_idx];
                self.cur += 2;
                input_idx += 1;
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

fn get_map(out: &[char]) -> (HashSet<(isize, isize)>, (isize, isize), usize) {
    let mut scaffolds = HashSet::new();
    let mut i = 0;
    let mut j = 0;
    let mut pos = (0, 0);
    let mut dir = 0;
    for ch in out {
        if *ch == '#' {
            scaffolds.insert((i, j));
        } else if vec!['^', 'v', '<', '>'].iter().any(|x| x == ch) {
            pos = (i, j);
            dir = match *ch {
                '^' => 0,
                '>' => 1,
                'v' => 2,
                '<' => 3,
                _ => panic!("error")
            };
        }
        if *ch == '\n' {
            j = 0;
            i += 1;
        } else {
            j += 1;
        }
        // print!("{}", ch);
    }
    return (scaffolds, pos, dir);
}

fn part1(scaffolds: &HashSet<(isize, isize)>) -> isize {
    let mut res = 0;
    for (i, j) in scaffolds.iter() {
        if scaffolds.contains(&(*i + 1, *j)) && scaffolds.contains(&(*i - 1, *j)) && scaffolds.contains(&(*i, *j + 1)) && scaffolds.contains(&(*i, *j - 1)) {
            res += i * j;
        }
    }
    return res;
}

fn get_raw_instructions(scaffolds: HashSet<(isize, isize)>, pos: (isize, isize), init_dir: usize) -> String {
    let mut cur = pos;
    let deltas = vec![(-1, 0), (0, 1), (1, 0), (0, -1)];
    let mut cur_cnt = 0;
    let mut ins = Vec::new();
    let mut dir = init_dir;
    loop {
        let next = (cur.0 + deltas[dir].0, cur.1 + deltas[dir].1);
        let right = (cur.0 + deltas[(dir + 1) % 4].0, cur.1 + deltas[(dir + 1) % 4].1);
        let left = (cur.0 + deltas[(dir + 3) % 4].0, cur.1 + deltas[(dir + 3) % 4].1);
        // println!("dir: {}, cur: {:?}, next: {:?}, right: {:?}, left: {:?}", dir, cur, next, right, left);
        if scaffolds.contains(&next) {
            // println!("straight");
            cur = next;
            cur_cnt += 1;
        } else if scaffolds.contains(&right) {
            // println!("right");
            if cur_cnt != 0 {
                ins.push(cur_cnt.to_string());
            }
            cur_cnt = 0;
            ins.push("R".to_string());
            dir = (dir + 1) % 4;
        } else if scaffolds.contains(&left) {
            // println!("left");
            if cur_cnt != 0 {
                ins.push(cur_cnt.to_string());
            }
            cur_cnt = 0;
            ins.push("L".to_string());
            dir = (dir + 3) % 4;
        } else {
            break
        }
    }
    if cur_cnt != 0 {
        ins.push(cur_cnt.to_string());
    }
    return ins.join(",");
}

fn get_ascii(ins: &str) -> Vec<i64> {
    return ins.chars().collect::<Vec<char>>().iter().map(|&c| c as i64).collect();
}

fn part2(int_code: &[i64]) -> i64 {
    /* TODO: automate this
    A,B,A,C,A,B,A,C,B,C
    A = R,4,L,12,L,8,R,4
    B = L,8,R,10,R,10,R,6
    C = R,4,R,10,L,12
    */
    let main = "A,B,A,C,A,B,A,C,B,C\n";
    let module1 = "R,4,L,12,L,8,R,4\n";
    let module2 = "L,8,R,10,R,10,R,6\n";
    let module3 = "R,4,R,10,L,12\n";
    let mut input = Vec::new();
    input.append(&mut get_ascii(main));
    input.append(&mut get_ascii(module1));
    input.append(&mut get_ascii(module2));
    input.append(&mut get_ascii(module3));
    input.append(&mut get_ascii("n\n"));
    let mut int_code_vec = int_code.to_vec();
    int_code_vec[0] = 2;
    let mut program = Program::new(&int_code_vec);
    let output = program.run_code(&input);
    return *output.last().unwrap();
}

fn main() {
    let int_code = read_data();
    let mut program = Program::new(&int_code);
    let output = program.run_code(&[]);
    let res: Vec<char> = output.iter().map(|x| *x as u8 as char).collect();
    // let test = "..#..........\n..#..........\n#######...###\n#.#...#...#.#\n#############\n..#...#...#..\n..#####...^..\n\n".chars().collect::<Vec<char>>();
    // let test = "#######...#####\n#.....#...#...#\n#.....#...#...#\n......#...#...#\n......#...###.#\n......#.....#.#\n^########...#.#\n......#.#...#.#\n......#########\n........#...#..\n....#########..\n....#...#......\n....#...#......\n....#...#......\n....#####......\n\n".chars().collect::<Vec<char>>();
    let (scaffolds, pos, dir) = get_map(&res);
    println!("part1: {}", part1(&scaffolds));
    println!("part2: {}", part2(&int_code));
    println!("raw_instructions: {:?}", get_raw_instructions(scaffolds, pos, dir));
}
