use std::io::{self, BufRead};
use std::convert::TryFrom;

fn read_data() -> Vec<i32> {
    let stdin = io::stdin();
    return stdin.lock().lines().next().unwrap().unwrap().split(",").map(|x| x.parse::<i32>().unwrap()).collect();
}

fn get_param(input: &[i32], mode: i32, pos: usize) -> i32 {
    if mode == 1 {
        return input[pos]
    } else {
        return input[usize::try_from(input[pos]).unwrap()]
    }
}

fn run_program(orig_input: &[i32], input_val: i32) -> Vec<i32> {
    let mut input = orig_input.to_vec();
    let mut output = Vec::new();
    let mut cur = 0;
    let mut param1: i32;
    let mut param2: i32;
    let mut param3: usize;
    let mut op_code;
    loop {
        op_code = input[cur] % 100;
        if op_code == 99 {
            break;
        }
        assert!(op_code >= 1 && op_code <= 8);
        if op_code == 1 || op_code == 2 {
            param1 = get_param(&input, (input[cur] / 100) % 10, cur + 1);
            param2 = get_param(&input, (input[cur] / 1000) % 10, cur + 2);
            param3 = usize::try_from(input[cur + 3]).unwrap();
            if op_code == 1 {
                input[param3] = param1 + param2;
            } else {
                input[param3] = param1 * param2;
            }
            cur += 4;
        } else if op_code == 3 {
            param3 = usize::try_from(input[cur + 1]).unwrap();
            input[param3] = input_val;
            cur += 2;
        } else if op_code == 4 {
            output.push(get_param(&input, (input[cur] / 100) % 10, cur + 1));
            cur += 2;
        } else if op_code == 5 || op_code == 6 {
            param1 = get_param(&input, (input[cur] / 100) % 10, cur + 1);
            param2 = get_param(&input, (input[cur] / 1000) % 10, cur + 2);
            if (op_code == 5 && param1 != 0) || (op_code == 6 && param1 == 0) {
                cur = usize::try_from(param2).unwrap();
            } else {
                cur += 3;
            }
        } else {
            param1 = get_param(&input, (input[cur] / 100) % 10, cur + 1);
            param2 = get_param(&input, (input[cur] / 1000) % 10, cur + 2);
            param3 = usize::try_from(input[cur + 3]).unwrap();
            if (op_code == 7 && param1 < param2) || (op_code == 8 && param1 == param2) {
                input[param3] = 1;
            } else {
                input[param3] = 0;
            }
            cur += 4;
        }
    }
    return output;
}

fn main() {
    let input = read_data();
    println!("part1: {:?}", run_program(&input, 1));
    println!("part2: {:?}", run_program(&input, 5));
}
