use std::io::{self, BufRead};
use std::convert::TryFrom;

fn read_data() -> Vec<u32> {
    let stdin = io::stdin();
    return stdin.lock().lines().next().unwrap().unwrap().split(",").map(|x| x.parse::<u32>().unwrap()).collect();
}

fn run_program(orig_input: &[u32], noun: u32, verb: u32) -> u32 {
    let mut input = orig_input.to_vec();
    input[1] = noun;
    input[2] = verb;
    let mut cur = 0;
    let mut pos1: usize;
    let mut pos2: usize;
    let mut respos: usize;
    loop {
        if input[cur] == 99 {
            break;
        }
        assert!(input[cur] == 1 || input[cur] == 2);
        pos1 = usize::try_from(input[cur + 1]).unwrap();
        pos2 = usize::try_from(input[cur + 2]).unwrap();
        respos = usize::try_from(input[cur + 3]).unwrap();
        if input[cur] == 1 {
            input[respos] = input[pos1] + input[pos2];
        } else {
            input[respos] = input[pos1] * input[pos2];
        }
        cur += 4;
    }
    return input[0];
}

fn part1(input: &[u32]) -> u32 {
    return run_program(input, 12, 2);
}

fn part2(input: &[u32]) -> u32 {
    for noun in 1..100 {
        for verb in 1..100 {
            let res = run_program(input, noun, verb);
            if res == 19690720 {
                return noun * 100 + verb;
            }
        }
    }
    return 0;
}

fn main() {
    let input = read_data();
    println!("part1: {}", part1(&input));
    println!("part2: {}", part2(&input));
}
