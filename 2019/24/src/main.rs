use std::io::{self, BufRead};
use std::collections::HashSet;

type Point = (isize, isize, isize);

fn read_data() -> Vec<String> {
    let stdin = io::stdin();
    let mut input = Vec::new();
    for line in stdin.lock().lines() {
        input.push(line.unwrap());
    }
    return input;
}

fn get_initial(input: &[String]) -> HashSet<Point> {
    let mut bugs = HashSet::new();
    for (r, line) in input.iter().enumerate() {
        for (c, ch) in line.chars().enumerate() {
            if ch == '#' {
                bugs.insert((r as isize, c as isize, 0));
            }
        }
    }
    return bugs;
}

fn is_bug(bugs: &HashSet<Point>, loc: Point) -> bool {
    let mut adjacent_cnt = 0;
    let mut adjacent = HashSet::new();
    for (dr, dc) in vec![(0, -1), (0, 1), (-1, 0), (1, 0)] {
        adjacent.insert((loc.0 + dr, loc.1 + dc, loc.2));
    }
    match loc.0 {
        0 => { adjacent.insert((1, 2, loc.2-1)); },
        4 => { adjacent.insert((3, 2, loc.2-1)); },
        _ => {}
    }
    match loc.1 {
        0 => { adjacent.insert((2, 1, loc.2-1)); },
        4 => { adjacent.insert((2, 3, loc.2-1)); },
        _ => {}
    }
    for n in 0..5 {
        match loc {
            (1, 2, l) => { adjacent.insert((0, n, l + 1)); },
            (3, 2, l) => { adjacent.insert((4, n, l + 1)); },
            (2, 1, l) => { adjacent.insert((n, 0, l + 1)); },
            (2, 3, l) => { adjacent.insert((n, 4, l + 1)); },
            _ => {}
        }
    }
    for adj_loc in adjacent {
        if bugs.contains(&adj_loc) {
            adjacent_cnt += 1;
        }
    }
    return match adjacent_cnt {
        1 => true,
        2 => !bugs.contains(&loc),
        _ => false
    }
}


fn get_biodiversity(bugs: &HashSet<Point>) -> isize {
    let mut biodiversity = 0;
    for bug in bugs {
        biodiversity += 2isize.pow((bug.0 * 5 + bug.1) as u32);
    }
    return biodiversity;
}


fn part1(mut bugs: HashSet<Point>) -> isize {
    let mut layouts = HashSet::new();
    layouts.insert(get_biodiversity(&bugs));
    loop {
        let mut new_bugs = HashSet::new();
        for r in 0..5 {
            for c in 0..5 {
                if is_bug(&bugs, (r, c, 0)) {
                    new_bugs.insert((r, c, 0));
                }
            }
        }
        let new_layout = get_biodiversity(&new_bugs);
        if layouts.contains(&new_layout) {
            return new_layout;
        }
        layouts.insert(new_layout);
        bugs = new_bugs;
    }
}

fn part2(mut bugs: HashSet<Point>) -> usize {
    for min in 1..=200 {
        let mut new_bugs = HashSet::new();
        for l in -min..=min {
            for r in 0..5 {
                for c in 0..5 {
                    if r == 2 && c == 2 {
                        continue;
                    }
                    if is_bug(&bugs, (r, c, l)) {
                        new_bugs.insert((r, c, l));
                    }
                }
            }
        }
        bugs = new_bugs;
    }
    return bugs.len();
}

fn main() {
    let input = read_data();
    println!("part1:{}", part1(get_initial(&input)));
    println!("part2:{}", part2(get_initial(&input)));
}
