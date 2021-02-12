use std::io::{self, BufRead};
use std::convert::TryFrom;

fn read_data() -> Vec<usize> {
    let stdin = io::stdin();
    return stdin.lock().lines().next().unwrap().unwrap().chars().map(|x| usize::try_from(x.to_digit(10).unwrap()).unwrap()).collect();
}

fn apply_phase1(input: &[usize]) -> Vec<usize> {
    let mut res = Vec::new();
    let pattern = vec![0, 1, 0, -1];
    for i in 0..input.len() {
        let mut digit: i32 = 0;
        for (j, val) in input.to_vec().iter().enumerate() {
            let pattern_idx = ((j + 1) / (i + 1)) % 4;
            digit += *val as i32 * pattern[pattern_idx] as i32;
        }
        res.push(usize::try_from(digit.abs() % 10).unwrap());
    }
    return res;
}

fn apply_phases(input: &[usize], phase_fn: fn(&[usize]) -> Vec<usize>) -> String {
    let mut res = input.to_vec();
    for _ in 0..100 {
        res = phase_fn(&res);
    }
    return res[0..8].iter().map(|x| x.to_string()).collect::<Vec<String>>().join("");
}

fn part1(input: &[usize]) -> String {
    return apply_phases(input, apply_phase1);
}

fn apply_phase2(input: &[usize]) -> Vec<usize> {
    let mut res = Vec::new();
    let mut cum = 0;
    let mut reverse_input = input.to_vec();
    reverse_input.reverse();
    for num in reverse_input {
        cum += num;
        res.push(cum % 10);
    }
    res.reverse();
    return res;
}

fn part2(input: &[usize]) -> String {
    let offset = input[0..7].iter().map(|x| x.to_string()).collect::<Vec<String>>().join("").parse::<usize>().unwrap();
    assert!(offset > input.len() * 10000 / 2);
    let rem_len = input.len() * 10000 - offset;
    let mut actual_input = Vec::new();
    while actual_input.len() < rem_len {
        actual_input.append(&mut input.to_vec());
    }
    let st = actual_input.len() - rem_len;
    return apply_phases(&actual_input[st..], apply_phase2);
}

fn main() {
    let input = read_data();
    println!("part1:{}", part1(&input));
    println!("part2:{}", part2(&input));
}
