use std::collections::HashSet;

fn is_valid_p1(num: u32) -> bool {
    let mut prev = 10;
    let mut n = num;
    let mut has_equal = false;
    while n > 0 {
        let digit = n % 10;
        if digit > prev {
            return false;
        }
        if digit == prev {
            has_equal = true;
        }
        prev = digit;
        n = n / 10;
    }
    return has_equal;
}

fn is_valid_p2(num: u32) -> bool {
    let mut prev_prev = 11;
    let mut prev = 10;
    let mut n = num;
    let mut dup_digits = HashSet::new();
    while n > 0 {
        let digit = n % 10;
        if digit > prev {
            return false;
        }
        if digit == prev {
            dup_digits.insert(digit);
        }
        if digit == prev && digit == prev_prev {
            dup_digits.remove(&digit);
        }
        prev_prev = prev;
        prev = digit;
        n = n / 10;
    }
    return dup_digits.len() > 0;
}

fn solve(start: u32, end: u32, valid_fn: fn(u32) -> bool) -> u32 {
    let mut count = 0;
    for num in start..end+1 {
        if valid_fn(num) {
            count = count + 1;
        }
    }
    return count;
}

fn main() {
    let start = 137683;
    let end = 596253;
    println!("part1: {}", solve(start, end, is_valid_p1));
    println!("part2: {}", solve(start, end, is_valid_p2));
}
