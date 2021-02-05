use std::fmt;
use std::ops;
use std::io::{self, BufRead};
use itertools::Itertools;
use std::collections::HashSet;

#[derive(Debug, Copy, Clone, PartialEq)]
struct ThreeDim {
    x: isize,
    y: isize,
    z: isize,
}

impl ThreeDim {
    fn new(x: isize, y: isize, z:isize) -> ThreeDim {
        return ThreeDim{x:x, y:y, z:z}
    }

    fn get_field(&self, field: &str) -> isize {
        match field {
            "x" => self.x,
            "y" => self.y,
            "z" => self.z,
            _ => panic!("unknown field")
        }
    }
}

impl ops::Add for ThreeDim {
    type Output = Self;

    fn add(self, rhs: ThreeDim) -> ThreeDim {
        let mut res = self.clone();
        res.x += rhs.x;
        res.y += rhs.y;
        res.z += rhs.z;
        return res;
    }
}

impl ops::AddAssign for ThreeDim {
    fn add_assign(&mut self, rhs: ThreeDim) {
        *self = ThreeDim {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
            z: self.z + rhs.z,
        }
    }
}

impl fmt::Display for ThreeDim {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "<x={}, y={}, z={}>", self.x, self.y, self.z)
    }
}

#[derive(Debug, Copy, Clone, PartialEq)]
struct Moon {
    id: usize,
    pos: ThreeDim,
    vel: ThreeDim
}

impl Moon {
    fn new(id: usize, initial: &str) -> Moon {
        let dim: Vec<isize> = initial.strip_prefix("<").unwrap().strip_suffix(">").unwrap().split(", ").map(|x| x.split("=").collect::<Vec<&str>>()[1].parse::<isize>().unwrap()).collect();
        return Moon{
            id: id,
            pos: ThreeDim::new(dim[0], dim[1], dim[2]),
            vel: ThreeDim::new(0, 0, 0)
        }
    }

    fn apply_velocity(&mut self) -> () {
        self.pos += self.vel;
    }

    fn get_energy(&self) -> usize {
        let pot = self.pos.x.abs() + self.pos.y.abs() + self.pos.z.abs();
        let kin = self.vel.x.abs() + self.vel.y.abs() + self.vel.z.abs();
        return (pot * kin) as usize;
    }
}

impl fmt::Display for Moon {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "id={}, pos={}, vel={}", self.id, self.pos, self.vel)
    }
}

fn read_data() -> Vec<Moon> {
    let stdin = io::stdin();
    let mut moons = Vec::new();
    for (id, line) in stdin.lock().lines().enumerate() {
        let l = line.unwrap();
        moons.push(Moon::new(id, &l));
    }
    return moons;
}

fn run_step(moons: &[Moon]) -> Vec<Moon> {
    let mut m = moons.to_vec();
    for pair in (0..m.len()).into_iter().combinations(2) {
        if m[pair[0]].pos.x < m[pair[1]].pos.x {
            m[pair[0]].vel.x += 1;
            m[pair[1]].vel.x -= 1;
        } else if m[pair[0]].pos.x > m[pair[1]].pos.x {
            m[pair[0]].vel.x -= 1;
            m[pair[1]].vel.x += 1;
        }
        if m[pair[0]].pos.y < m[pair[1]].pos.y {
            m[pair[0]].vel.y += 1;
            m[pair[1]].vel.y -= 1;
        } else if m[pair[0]].pos.y > m[pair[1]].pos.y {
            m[pair[0]].vel.y -= 1;
            m[pair[1]].vel.y += 1;
        }
        if m[pair[0]].pos.z < m[pair[1]].pos.z {
            m[pair[0]].vel.z += 1;
            m[pair[1]].vel.z -= 1;
        } else if m[pair[0]].pos.z > m[pair[1]].pos.z {
            m[pair[0]].vel.z -= 1;
            m[pair[1]].vel.z += 1;
        }
    }
    for i in 0..m.len() {
        m[i].apply_velocity();
    }
    return m;
}

fn gcd(a: usize, b: usize) -> usize {
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

fn lcm(a: usize, b: usize) -> usize {
    return a * b / gcd(a, b);
}

fn part1(moons: &[Moon]) -> usize {
    let mut m = moons.to_vec();
    for _step in 1..=1000 {
        m = run_step(&m);
    }
    let mut res = 0;
    for moon in m {
        res += moon.get_energy();
    }
    return res;
}

fn get_hash(moons: &[Moon], field: &str) -> String {
    let pos_hash:Vec<String> = moons.iter().map(|x| x.pos.get_field(field).to_string()).collect();
    let vel_hash:Vec<String> = moons.iter().map(|x| x.vel.get_field(field).to_string()).collect();
    return format!("{}|{}", pos_hash.join("|"), vel_hash.join("|"));
}

fn part2(moons: &[Moon]) -> usize {
    let mut m = moons.to_vec();
    let mut visited_x = HashSet::new();
    let mut visited_y = HashSet::new();
    let mut visited_z = HashSet::new();
    let mut x_repeat = 0;
    let mut y_repeat = 0;
    let mut z_repeat = 0;
    let mut i = 0;
    loop {
        let hash_x = get_hash(&m, "x");
        let hash_y = get_hash(&m, "y");
        let hash_z = get_hash(&m, "z");
        if x_repeat == 0 && visited_x.contains(&hash_x) {
            x_repeat = i;
        } else {
            visited_x.insert(hash_x);
        }
        if y_repeat == 0 && visited_y.contains(&hash_y) {
            y_repeat = i;
        } else {
            visited_y.insert(hash_y);
        }
        if z_repeat == 0 && visited_z.contains(&hash_z) {
            z_repeat = i;
        } else {
            visited_z.insert(hash_z);
        }
        if x_repeat != 0 && y_repeat != 0 && z_repeat != 0 {
            break;
        }
        m = run_step(&m);
        i += 1;
    }
    println!("{}", i);
    return lcm(x_repeat, lcm(y_repeat, z_repeat));
}


fn main() {
    let input = read_data();
    println!("part1: {}", part1(&input));
    println!("part2: {}", part2(&input));
}
