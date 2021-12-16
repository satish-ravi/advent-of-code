use std::io::{self, BufRead};
use std::collections::HashMap;

fn read_data() -> (Vec<String>, Vec<String>) {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    let wire1 = lines.next().unwrap().unwrap().split(",").map(String::from).collect();
    let wire2 = lines.next().unwrap().unwrap().split(",").map(String::from).collect();
    return (wire1, wire2);
}

fn add_wire_line(points: &mut HashMap<(i32, i32), i8>, (cx, cy, cd): (i32, i32, i32), line: &String, val: i8, points_dis: &mut HashMap<(i32, i32), i32>) -> (i32, i32, i32) {
    let dir = &line[0..1];
    let distance: i32 = line[1..].parse().unwrap();
    let (dx, dy) = match dir {
        "R" => (1, 0),
        "L" => (-1, 0),
        "U" => (0, 1),
        "D" => (0, -1),
        _ => (0, 0),
    };
    for i in 1..distance+1 {
        let x = cx + i * dx;
        let y = cy + i * dy;

        match points.get(&(x, y)) {
            Some(v) => points.insert((x, y), v | val),
            _ => points.insert((x, y), val),
        };
        if !points_dis.contains_key(&(x, y)) {
            points_dis.insert((x, y), cd + i);
        }
    }
    return (cx + distance * dx, cy + distance * dy, cd + distance);
}

fn solve(wire1: &[String], wire2: &[String]) -> (i32, i32) {
    let mut points: HashMap<(i32, i32), i8> = HashMap::new();
    let mut w1_points_dis: HashMap<(i32, i32), i32> = HashMap::new();
    let mut w2_points_dis: HashMap<(i32, i32), i32> = HashMap::new();
    let mut current = (0, 0, 0);
    for line in wire1 {
        current = add_wire_line(&mut points, current, line, 1, &mut w1_points_dis);
    }
    current = (0, 0, 0);
    for line in wire2 {
        current = add_wire_line(&mut points, current, line, 2, &mut w2_points_dis);
    }
    let mut p1 = i32::MAX;
    let mut p2 = i32::MAX;
    for (point, &value) in &points {
        if value == 3 {
            let (x, y) = point;
            let p1_distance = x.abs() + y.abs();
            if p1_distance < p1 {
                p1 = p1_distance;
            }
            let p2_distance = w1_points_dis.get(&point).unwrap() + w2_points_dis.get(&point).unwrap();
            if p2_distance < p2 {
                p2 = p2_distance;
            }
        }
    }
    return (p1, p2);
}

fn main() {
    let (wire1, wire2) = read_data();
    let (p1, p2) = solve(&wire1, &wire2);
    println!("part1: {}", p1);
    println!("part2: {}", p2);
}
