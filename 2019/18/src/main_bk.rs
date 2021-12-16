use std::io::{self, BufRead};
use std::collections::HashMap;
use std::collections::HashSet;

type Point = (usize, usize);

#[derive(Debug)]
struct Tunnel {
    grid: Vec<Vec<char>>,
    src: Point,
    keys: Vec<char>,
    doors: Vec<char>,
}

type FourPoint = (Point, Point, Point, Point);

#[derive(Debug)]
struct TunnelP2 {
    grid: Vec<Vec<char>>,
    src: FourPoint,
    keys: Vec<char>,
    doors: Vec<char>,
}

fn char_to_bit(ch: char) -> usize {
    let sub = match ch {
        'A'..='Z' => 65,
        'a'..='z' => 97,
        _ => panic!("error")
    };
    return 1 << (ch as usize - sub);
}

impl Tunnel {
    fn new(grid: &[Vec<char>]) -> Tunnel {
        let mut src = (0, 0);
        let mut keys = Vec::new();
        let mut doors = Vec::new();
        for i in 1..grid.len() - 1 {
            for j in 1..grid[0].len() - 1 {
                match grid[i][j] {
                    '@' => { src = (i, j); },
                    'A'..='Z' => { doors.push(grid[i][j]); },
                    'a'..='z' => { keys.push(grid[i][j]); },
                    _ => {},
                }
            }
        }
        return Tunnel {
            grid: grid.to_vec(),
            src: src,
            keys: keys,
            doors: doors
        };
    }

    fn get_neighbors(&self, ((i, j), k): (Point, usize)) -> Vec<(Point, usize)> {
        let mut neighbors = Vec::new();
        for (di, dj) in vec![(-1, 0), (0, -1), (1, 0), (0, 1)] {
            let point = ((i as isize + di) as usize, (j as isize + dj) as usize);
            let ch = self.grid[point.0][point.1];
            match ch {
                '@' | '.' => { neighbors.push((point, k)); },
                'a'..='z' => { neighbors.push((point, k | char_to_bit(ch))); },
                'A'..='Z' => {
                    if k & char_to_bit(ch) > 0 {
                        neighbors.push((point, k));
                    }
                }
                _ => {}
            };
        }
        return neighbors;
    }

    fn find_all_keys(&mut self) -> usize {
        let mut queue = HashSet::new();
        let mut dist = HashMap::new();
        let mut visited = HashSet::new();

        queue.insert((self.src, 0));
        dist.insert((self.src, 0), 0);
        while queue.len() > 0 {
            let mut current = ((0, 0), 0);
            let mut min_dist = usize::MAX;
            for ele in &queue {
                let distance = *dist.get(&ele).unwrap();
                if distance < min_dist {
                    current = *ele;
                    min_dist = distance;
                }
            }
            if current == ((0, 0), 0) {
                panic!("no path");
            }
            if current.1 == 2usize.pow(self.keys.len() as u32) - 1 {
                // print logic
                // let mut path = Vec::new();
                // let mut cur = current;
                // while cur != self.src {
                //     cur = *prev.get(&cur).unwrap();
                //     path.push(cur);
                // }
                // path.reverse();
                // if recurse {
                //     let mut condensed_path = Vec::new();
                //     let mut cur_level = 0;
                //     let mut cur_path = Vec::new();
                //     for ele in path {
                //         if ele.2 == cur_level {
                //             cur_path.push(ele);
                //         } else {
                //             cur_level = ele.2;
                //             condensed_path.push(cur_path);
                //             cur_path = Vec::new();
                //             cur_path.push(ele);
                //         }
                //     }
                //     condensed_path.push(cur_path);
                //     for ele in condensed_path {
                //         let len = ele.len();
                //         println!("From: {:?}, To: {:?}, Level: {}, Length: {}", (ele[0].0+1, ele[0].1+1), (ele[len-1].0+1, ele[len-1].1+1), ele[0].2, ele.len());
                //     }
                // }
                return min_dist;
            }
            queue.remove(&current);
            visited.insert(current);
            for neighbor in self.get_neighbors(current) {
                if !visited.contains(&neighbor) {
                    let alt_dist = min_dist + 1;
                    queue.insert(neighbor);
                    if !dist.contains_key(&neighbor) || alt_dist < *dist.get(&neighbor).unwrap() {
                        dist.insert(neighbor, alt_dist);
                    }
                }
            }
        }
        panic!("error");
    }
}

impl TunnelP2 {
    fn new(grid: &[Vec<char>]) -> TunnelP2 {
        let mut mod_grid = grid.to_vec();
        let mut src = (0, 0);
        let mut keys = Vec::new();
        let mut doors = Vec::new();
        for i in 1..grid.len() - 1 {
            for j in 1..grid[0].len() - 1 {
                match grid[i][j] {
                    '@' => { src = (i, j); },
                    'A'..='Z' => { doors.push(grid[i][j]); },
                    'a'..='z' => { keys.push(grid[i][j]); },
                    _ => {},
                }
            }
        }

        mod_grid[src.0][src.1] = '#';
        mod_grid[src.0][src.1+1] = '#';
        mod_grid[src.0][src.1-1] = '#';
        mod_grid[src.0+1][src.1] = '#';
        mod_grid[src.0-1][src.1] = '#';
        mod_grid[src.0+1][src.1+1] = '@';
        mod_grid[src.0-1][src.1-1] = '@';
        mod_grid[src.0+1][src.1-1] = '@';
        mod_grid[src.0-1][src.1+1] = '@';

        return TunnelP2 {
            grid: mod_grid,
            src: ((src.0-1,src.1-1), (src.0-1,src.1+1), (src.0+1,src.1-1), (src.0+1,src.1+1)),
            keys: keys,
            doors: doors
        };
    }

    fn get_neighbors(&self, (robots, k): (FourPoint, usize)) -> Vec<(FourPoint, usize)> {
        let mut neighbors = Vec::new();
        let robots_vec = vec![robots.0, robots.1, robots.2, robots.3];
        for r in 0..4 {
            let i = robots_vec[r].0;
            let j = robots_vec[r].1;
            for (di, dj) in vec![(-1, 0), (0, -1), (1, 0), (0, 1)] {
                let point = ((i as isize + di) as usize, (j as isize + dj) as usize);
                let ch = self.grid[point.0][point.1];
                let mut neighbor_vec = vec![robots.0, robots.1, robots.2, robots.3];
                neighbor_vec[r] = point;
                let neighbor = (neighbor_vec[0], neighbor_vec[1], neighbor_vec[2], neighbor_vec[3]);
                match ch {
                    '@' | '.' => { neighbors.push((neighbor, k)); },
                    'a'..='z' => { neighbors.push((neighbor, k | char_to_bit(ch))); },
                    'A'..='Z' => {
                        if k & char_to_bit(ch) > 0 {
                            neighbors.push((neighbor, k));
                        }
                    }
                    _ => {}
                };
            }
        }
        return neighbors;
    }

    fn find_all_keys(&mut self) -> usize {
        let mut queue = HashSet::new();
        let mut dist = HashMap::new();
        let mut visited = HashSet::new();

        queue.insert((self.src, 0));
        dist.insert((self.src, 0), 0);
        while queue.len() > 0 {
            let mut current = (((0, 0),(0, 0),(0, 0),(0, 0)), 0);
            let mut min_dist = usize::MAX;
            for ele in &queue {
                let distance = *dist.get(&ele).unwrap();
                if distance < min_dist {
                    current = *ele;
                    min_dist = distance;
                }
            }
            if current == (((0, 0),(0, 0),(0, 0),(0, 0)), 0) {
                panic!("no path");
            }
            if current.1 == 2usize.pow(self.keys.len() as u32) - 1 {
                // print logic
                // let mut path = Vec::new();
                // let mut cur = current;
                // while cur != self.src {
                //     cur = *prev.get(&cur).unwrap();
                //     path.push(cur);
                // }
                // path.reverse();
                // if recurse {
                //     let mut condensed_path = Vec::new();
                //     let mut cur_level = 0;
                //     let mut cur_path = Vec::new();
                //     for ele in path {
                //         if ele.2 == cur_level {
                //             cur_path.push(ele);
                //         } else {
                //             cur_level = ele.2;
                //             condensed_path.push(cur_path);
                //             cur_path = Vec::new();
                //             cur_path.push(ele);
                //         }
                //     }
                //     condensed_path.push(cur_path);
                //     for ele in condensed_path {
                //         let len = ele.len();
                //         println!("From: {:?}, To: {:?}, Level: {}, Length: {}", (ele[0].0+1, ele[0].1+1), (ele[len-1].0+1, ele[len-1].1+1), ele[0].2, ele.len());
                //     }
                // }
                return min_dist;
            }
            queue.remove(&current);
            visited.insert(current);
            for neighbor in self.get_neighbors(current) {
                if !visited.contains(&neighbor) {
                    let alt_dist = min_dist + 1;
                    queue.insert(neighbor);
                    if !dist.contains_key(&neighbor) || alt_dist < *dist.get(&neighbor).unwrap() {
                        dist.insert(neighbor, alt_dist);
                    }
                }
            }
        }
        panic!("error");
    }
}

fn read_data() -> Vec<Vec<char>> {
    let stdin = io::stdin();
    let mut grid = Vec::new();
    for line in stdin.lock().lines() {
        let row: Vec<char> = line.unwrap().chars().collect();
        grid.push(row);
    }
    return grid;
}

fn part1(grid: &[Vec<char>]) -> usize {
    let mut tunnel = Tunnel::new(grid);
    return tunnel.find_all_keys();
}

fn part2(grid: &[Vec<char>]) -> usize {
    let mut tunnel = TunnelP2::new(grid);
    return tunnel.find_all_keys();
}

fn main() {
    let input = read_data();
    // println!("part1: {:?}", part1(&input));
    println!("part2: {:?}", part2(&input));
    // println!("part1: {}", maze.find_steps_to_dest(false));
    // println!("part2: {}", maze.find_steps_to_dest(true));
}
