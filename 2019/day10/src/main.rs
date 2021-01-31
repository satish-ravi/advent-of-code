use std::io::{self, BufRead};
use itertools::Itertools;
use std::collections::HashSet;
use std::collections::HashMap;
use std::iter::FromIterator;
use std::convert::TryFrom;
use std::cmp::Ordering;

#[derive(Debug)]
#[derive(Copy, Clone)]
struct Asteroid {
    loc: isize,
    dir: u8,
    slope: f32,
    distance: usize,
    level: usize
}

impl Asteroid {
    fn set_level(&mut self, level: usize) -> () {
        self.level = level;
    }
}

impl PartialOrd for Asteroid {
    fn partial_cmp(&self, other: &Asteroid) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Asteroid {
    fn cmp(&self, other: &Asteroid) -> Ordering {
        if self.level != other.level {
            return self.level.cmp(&other.level);
        }
        if self.dir != other.dir {
            return self.dir.cmp(&other.dir);
        }
        if self.slope != other.slope {
            if self.slope < other.slope {
                return Ordering::Less;
            } else {
                return Ordering::Greater;
            }
        }
        return self.distance.cmp(&other.distance);
    }
}

impl PartialEq for Asteroid {
    fn eq(&self, other: &Asteroid) -> bool {
        self.dir == other.dir && self.slope == other.slope && self.distance == other.distance
    }
}

impl Eq for Asteroid {
}


fn read_data() -> Vec<isize> {
    let stdin = io::stdin();
    let mut input = Vec::new();
    for (y, line) in stdin.lock().lines().enumerate() {
        for (x, ch) in line.unwrap().chars().enumerate() {
            if ch == '#' {
                input.push(isize::try_from(from_xy(x as isize, y as isize)).unwrap());
            }
        }
    }
    return input;
}

fn to_xy(num: isize) -> (isize, isize) {
    let x = num / 100;
    let y = num % 100;
    return (x, y);
}

fn from_xy(x: isize, y: isize) -> isize {
    return x * 100 + y;
}

fn gcd(a: isize, b: isize) -> isize {
    let mut x = a;
    let mut y = b;
    if b > a {
        x = b;
        y = a;
    }
    if y == 0 {
        return x;
    }
    return gcd(y, x % y);
}

fn find_station(asteroids: &[isize]) -> (isize, isize) {
    let ast_set: HashSet<isize> = HashSet::from_iter(asteroids.iter().cloned());
    let mut ast_counts: HashMap<isize, isize> = HashMap::new();
    for comb in asteroids.iter().combinations(2) {
        let (x1, y1) = to_xy(*comb[0]);
        let (x2, y2) = to_xy(*comb[1]);
        let distance = gcd((x2 - x1).abs(), (y2 - y1).abs());
        let dx = (x2 - x1) / distance;
        let dy = (y2 - y1) / distance;
        let mut visible = true;
        for i in 1..distance {
            let nx = x1 + dx * isize::try_from(i).unwrap();
            let ny = y1 + dy * isize::try_from(i).unwrap();
            if ast_set.contains(&from_xy(nx, ny)) {
                visible = false;
            }
        }
        if visible {
            *ast_counts.entry(*comb[0]).or_insert(0) += 1;
            *ast_counts.entry(*comb[1]).or_insert(0) += 1;
        }
    }
    let mut max_ast = 0;
    let mut max_loc = 0;
    for (key, val) in &ast_counts {
        if *val > max_ast {
            max_ast = *val;
            max_loc = *key;
        }
    }
    return (max_loc, max_ast);
}

fn create_asteroids(base: isize, all_asteroids: &[isize]) -> Vec<Asteroid> {
    let mut asteroids = Vec::new();
    let (bx, by) = to_xy(base);
    for ast in all_asteroids {
        if *ast == base {
            continue;
        }
        let mut dir: u8 = 0;
        let (x, y) = to_xy(*ast);
        if y < by && x >= bx {
            dir = 0;
        } else if y >= by && x > bx {
            dir = 1;
        } else if y > by && x <= bx {
            dir = 2;
        } else if y <= by && x < bx {
            dir = 3;
        }
        let slope: f32;
        if x == bx {
            slope = -f32::MAX;
        } else {
            slope = (y - by) as f32 / (x - bx) as f32;
        }
        let distance = ((x - bx).abs() + (y - by).abs()) as usize;
        asteroids.push(Asteroid{
            loc: *ast,
            dir: dir,
            slope: slope,
            distance: distance,
            level: 0
        });
    }
    asteroids.sort();
    let mut sorted = Vec::new();
    let mut level = 0;
    let mut prev = &asteroids[0];
    sorted.push(asteroids[0]);
    for asteroid in &asteroids[1..] {
        if prev.dir == asteroid.dir && prev.slope == asteroid.slope {
            level += 1;
        } else {
            level = 0;
        }
        let mut new_asteroid = *asteroid;
        new_asteroid.set_level(level);
        sorted.push(new_asteroid);
        prev = &asteroid;
    }
    sorted.sort();
    return sorted;
}

fn main() {
    let input = read_data();
    let (base, visible_ast) = find_station(&input);
    let asteroids = create_asteroids(base, &input);
    println!("part1:{}", visible_ast);
    println!("part2:{}", asteroids[199].loc);
}
