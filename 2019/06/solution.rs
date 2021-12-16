use std::io::{self, BufRead};
use std::collections::HashMap;

struct Object {
    orbits: Option<String>,
    orbited_by: Vec<String>
}

impl Object {
    fn new() -> Object {
        return Object {orbits: None, orbited_by: Vec::new() };
    }
}

fn read_data() -> HashMap<String, Object> {
    let stdin = io::stdin();
    let mut objects = HashMap::new();
    for line in stdin.lock().lines() {
        let l = line.unwrap();
        let inp: Vec<&str> = l.split(")").collect();
        let (o1, o2) = (inp[0], inp[1]);
        let object1 = objects.entry(o1.to_string()).or_insert(Object::new());
        object1.orbited_by.push(o2.to_string());
        let object2 = objects.entry(o2.to_string()).or_insert(Object::new());
        object2.orbits = Some(o1.to_string());
    }
    return objects;
}

fn count_orbits(objects: &HashMap<String, Object>, cur: &str, depth: u32) -> u32 {
    let object = objects.get(&cur.to_string()).unwrap();
    if object.orbited_by.len() == 0 {
        return depth;
    }
    let mut n_orbits = depth;
    for o in &object.orbited_by {
        n_orbits += count_orbits(objects, o.as_str(), depth + 1);
    }
    return n_orbits;
}

fn part1(objects: &HashMap<String, Object>) -> u32 {
    return count_orbits(objects, "COM", 0);
}

fn build_orbit_path(objects: &HashMap<String, Object>, obj: &str) -> Vec<String> {
    let mut path = Vec::new();
    let mut cur = obj;
    loop {
        let object = objects.get(&cur.to_string()).unwrap();
        if object.orbits == None {
            path.reverse();
            return path;
        }
        let orbits = object.orbits.as_ref().unwrap();
        path.push(orbits.to_string());
        cur = object.orbits.as_ref().unwrap().as_str();
    }
}

fn part2(objects: &HashMap<String, Object>) -> usize {
    let my_path = build_orbit_path(objects, "YOU");
    let san_path = build_orbit_path(objects, "SAN");
    let mut idx = 0;
    while my_path[idx] == san_path[idx] {
        idx += 1;
    }
    return my_path.len() + san_path.len() - 2 * idx;
}

fn main() {
    let input = read_data();
    println!("part1: {:?}", part1(&input));
    println!("part2: {:?}", part2(&input));
}
