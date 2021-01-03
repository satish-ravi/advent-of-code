use std::io::{self, BufRead};

fn read_data() -> Vec<i32> {
    let stdin = io::stdin();
    let mut vec = Vec::new();
    for line in stdin.lock().lines() {
        let num = line.unwrap().parse::<i32>().unwrap();
        vec.push(num);
    }
    return vec;
}

fn get_fuel_p1(mass: i32) -> i32 {
    return mass / 3 - 2;
}

fn get_fuel_p2(mass: i32) -> i32 {
    let mut fuel = 0;
    let mut cur = mass;
    loop {
        let cur_fuel = get_fuel_p1(cur);
        if cur_fuel <= 0 {
            return fuel;
        }
        fuel += cur_fuel;
        cur = cur_fuel;
    }
}

fn get_all_fuel(input: &[i32], get_fuel_fn: fn(i32) -> i32) -> i32 {
    let mut res = 0;
    for num in input {
        res += get_fuel_fn(*num);
    }
    return res;
}

fn main() {
    let input = read_data();
    println!("part1: {}", get_all_fuel(&input, get_fuel_p1));
    println!("part2: {}", get_all_fuel(&input, get_fuel_p2));
}
