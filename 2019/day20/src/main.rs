use std::io::{self, BufRead};
use std::collections::HashMap;
use std::cmp::Ordering;
use std::collections::BinaryHeap;

struct Maze {
    grid: Vec<Vec<char>>,
    portals: HashMap<(usize, usize), (usize, usize, char)>,
    src: (usize, usize, usize),
    dest: (usize, usize, usize)
}

#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    node: (usize, usize, usize),
}

// The priority queue depends on `Ord`.
// Explicitly implement the trait so the queue becomes a min-heap
// instead of a max-heap.
impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        // Notice that the we flip the ordering on costs.
        // In case of a tie we compare positions - this step is necessary
        // to make implementations of `PartialEq` and `Ord` consistent.
        other.cost.cmp(&self.cost)
    }
}

// `PartialOrd` needs to be implemented as well.
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Maze {
    fn new(grid: &[Vec<char>]) -> Maze {
        let mut portals = HashMap::new();
        let mut portal_tracker: HashMap<String, (usize, usize)> = HashMap::new();
        let mut src = (0, 0);
        let mut dest = (0, 0);
        for j in 2..grid[0].len() - 2 {
            for i in vec![0, grid.len() - 2] {
                if grid[i][j] != ' ' {
                    let label = format!("{}{}", grid[i][j], grid[i+1][j]);
                    let loc = match i {
                        0 => (2, j),
                        _ => (i-1, j)
                    };
                    match label.as_str() {
                        "AA" => {src = loc},
                        "ZZ" => {dest = loc},
                        _ => {portal_tracker.insert(label, loc);}
                    };
                }
            }
        }
        for i in 2..grid.len() - 2 {
            for j in vec![0, grid[0].len() - 2] {
                if grid[i][j] != ' ' {
                    let label = format!("{}{}", grid[i][j], grid[i][j+1]);
                    let loc = match j {
                        0 => (i, 2),
                        _ => (i, j-1)
                    };
                    match label.as_str() {
                        "AA" => {src = loc},
                        "ZZ" => {dest = loc},
                        _ => {portal_tracker.insert(label, loc);}
                    };
                }
            }
        }
        let mut idx = 2;
        loop {
            if grid[idx][idx] != '#' && grid[idx][idx] != '.' {
                break;
            }
            idx+=1;
        }
        for j in idx..grid[0].len() - idx {
            for i in vec![idx, grid.len() - idx - 2] {
                if grid[i][j] != ' ' && grid[i+1][j] != ' ' {
                    let label = format!("{}{}", grid[i][j], grid[i+1][j]);
                    let mut loc = (i - 1, j);
                    if i != idx {
                        loc.0 += 3;
                    }
                    if portal_tracker.contains_key(&label) {
                        let loc1 = portal_tracker.remove(&label).unwrap();
                        portals.insert(loc, (loc1.0, loc1.1, 'o'));
                        portals.insert(loc1, (loc.0, loc.1, 'i'));
                    } else {
                        panic!("error");
                    }
                }
            }
        }
        for i in idx..grid.len() - idx {
            for j in vec![idx, grid[0].len() - idx - 2] {
                if grid[i][j] != ' ' && grid[i][j+1] != ' ' {
                    let label = format!("{}{}", grid[i][j], grid[i][j+1]);
                    let mut loc = (i, j - 1);
                    if j != idx {
                        loc.1 += 3;
                    }
                    if portal_tracker.contains_key(&label) {
                        let loc1 = portal_tracker.remove(&label).unwrap();
                        portals.insert(loc, (loc1.0, loc1.1, 'o'));
                        portals.insert(loc1, (loc.0, loc.1, 'i'));
                    } else {
                        panic!("error");
                    }
                }
            }
        }
        return Maze {
            grid: grid.to_vec(),
            portals: portals,
            src: (src.0, src.1, 0),
            dest: (dest.0, dest.1, 0),
        }
    }

    fn get_neighbors(&self, (i, j, l): (usize, usize, usize), recurse: bool) -> Vec<(usize, usize, usize)> {
        let mut neighbors = Vec::new();
        for (di, dj) in vec![(-1, 0), (0, -1), (1, 0), (0, 1)] {
            let (ni, nj) = ((i as isize + di) as usize, (j as isize + dj) as usize);
            if self.grid[ni][nj] == '.' {
                neighbors.push((ni, nj, l));
            }
        }
        match self.portals.get(&(i, j)) {
            Some(&(pi, pj, dir)) => {
                if recurse {
                    match dir {
                        'o' => {
                            if l < 50 {
                                neighbors.push((pi, pj, l+1));
                            }
                        }
                        'i' => {
                            if l > 0 {
                                neighbors.push((pi, pj, l-1));
                            }
                        }
                        _ => panic!("error")
                    }
                } else {
                    neighbors.push((pi, pj, l));
                }
            },
            _ => {}
        }
        return neighbors;
    }

    fn find_steps_to_dest(&mut self, recurse: bool) -> usize {
        let mut queue = BinaryHeap::new();
        let mut dist = HashMap::new();
        let mut prev = HashMap::new();

        queue.push(State { node: self.src , cost: 0});
        dist.insert(self.src, 0);
        while let Some(State { cost, node }) = queue.pop() {
            if node == self.dest {
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
                return cost;
            }
            for neighbor in self.get_neighbors(node, recurse) {
                let alt_dist = cost + 1;
                if !dist.contains_key(&neighbor) || alt_dist < *dist.get(&neighbor).unwrap() {
                    queue.push(State {node: neighbor, cost: alt_dist});
                    dist.insert(neighbor, alt_dist);
                    prev.insert(neighbor, node);
                }
            }
        }
        panic!("no path");
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

fn main() {
    let input = read_data();
    let mut maze = Maze::new(&input);
    println!("part1: {}", maze.find_steps_to_dest(false));
    println!("part2: {}", maze.find_steps_to_dest(true));
}
