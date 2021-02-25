use std::io::{self, BufRead};
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;

type Point = (usize, usize);
type Edge = (char, char, usize, usize);
type FourChar = (char, char, char, char);

#[derive(Debug)]
struct Tunnel {
    edges: HashSet<Edge>,
    keys: HashSet<char>,
    doors: HashSet<char>,
}

struct Tunnel4 {
    edges: Vec<HashSet<Edge>>,
    keys: HashSet<char>,
    doors: HashSet<char>,
}

fn char_to_bit(ch: char) -> usize {
    let sub = match ch {
        'A'..='Z' => 65,
        'a'..='z' => 97,
        _ => panic!("error")
    };
    return 1 << (ch as usize - sub);
}

fn grid_to_edges(grid: &[Vec<char>], src: Point) -> HashSet<Edge> {
    let mut queue: VecDeque<(Point, usize, usize, char)> = VecDeque::new();
    let mut visited = HashSet::new();
    let mut edges:HashSet<Edge> = HashSet::new();
    queue.push_back((src, 0, 0, '@'));
    while !queue.is_empty() {
        let cur = queue.pop_front().unwrap();
        visited.insert((cur.0, cur.3));
        for (di, dj) in vec![(-1, 0), (0, -1), (1, 0), (0, 1)] {
            let neighbor = ((cur.0.0 as isize + di) as usize, (cur.0.1 as isize + dj) as usize);
            if visited.contains(&(neighbor, cur.3)) {
                continue;
            }
            let ch = grid[neighbor.0][neighbor.1];
            match ch {
                '.' => { queue.push_back((neighbor, cur.1 + 1, cur.2, cur.3)); },
                'A'..='Z' => { queue.push_back((neighbor, cur.1 + 1, cur.2 | char_to_bit(ch), cur.3)); },
                'a'..='z' | '@' => {
                    let mut found = false;
                    for &edge in &edges {
                        if ((edge.0 == cur.3 && edge.1 == ch) || (edge.0 == ch && edge.1 == cur.3)) && edge.2 <= cur.1 + 1 {
                            found=true;
                            break;
                        }
                    }
                    if !found {
                        edges.insert((cur.3, ch, cur.1 + 1, cur.2));
                    }
                    if visited.contains(&(neighbor, ch)) {
                        continue;
                    }
                    queue.push_back((neighbor, 0, 0, ch));
                },
                _ => {}
            }
        }
    }
    return edges;
}

impl Tunnel {
    fn new(grid: &[Vec<char>]) -> Tunnel {
        let mut src = (0, 0);
        let mut keys = HashSet::new();
        let mut doors = HashSet::new();
        for i in 1..grid.len() - 1 {
            for j in 1..grid[0].len() - 1 {
                match grid[i][j] {
                    '@' => { src = (i, j); },
                    'A'..='Z' => { doors.insert(grid[i][j]); },
                    'a'..='z' => { keys.insert(grid[i][j]); },
                    _ => {},
                }
            }
        }
        return Tunnel {
            edges: grid_to_edges(grid, src),
            keys: keys,
            doors: doors
        };
    }

    fn get_neighbors(&self, (ch, k): (char, usize)) -> Vec<((char, usize), usize)> {
        let mut neighbors = Vec::new();
        for &edge in &self.edges {
            let neighbor;
            if edge.0 == ch {
                neighbor = edge.1;
            } else if edge.1 == ch {
                neighbor = edge.0;
            } else {
                continue;
            }
            if edge.3 == k & edge.3 {
                let nk = match neighbor {
                    '@' => k,
                    _ => k | char_to_bit(neighbor)
                };
                neighbors.push(((neighbor, nk), edge.2))
            }
        }
        return neighbors;
    }

    fn find_all_keys(&self) -> usize {
        let mut queue = HashSet::new();
        let mut dist = HashMap::new();
        let mut prev: HashMap<(char, usize), ((char, usize), usize)> = HashMap::new();
        let mut visited = HashSet::new();

        queue.insert(('@', 0));
        dist.insert(('@', 0), 0);
        while queue.len() > 0 {
            let mut current = ('0', 0);
            let mut min_dist = usize::MAX;
            for ele in &queue {
                let distance = *dist.get(&ele).unwrap();
                if distance < min_dist {
                    current = *ele;
                    min_dist = distance;
                }
            }
            if current == ('0', 0) {
                panic!("no path");
            }
            if current.1 == 2usize.pow(self.keys.len() as u32) - 1 {
                // print logic
                // let mut path = Vec::new();
                // let mut cur = current;
                // while cur != ('@', 0) {
                //     let cur1 = *prev.get(&cur).unwrap();
                //     path.push(cur1);
                //     cur = cur1.0;
                // }
                // path.reverse();
                // for ele in path {
                //     println!("{:?}", ele);
                // }
                return min_dist;
            }
            queue.remove(&current);
            visited.insert(current);
            for neighbor in self.get_neighbors(current) {
                if !visited.contains(&neighbor.0) {
                    let alt_dist = min_dist + neighbor.1;
                    queue.insert(neighbor.0);
                    if !dist.contains_key(&neighbor.0) || alt_dist < *dist.get(&neighbor.0).unwrap() {
                        dist.insert(neighbor.0, alt_dist);
                        prev.insert(neighbor.0, (current, alt_dist));
                    }
                }
            }
        }
        panic!("error");
    }
}

impl Tunnel4 {
    fn new(grid: &[Vec<char>]) -> Tunnel4 {
        let mut mod_grid = grid.to_vec();
        let mut src = (0, 0);
        let mut keys = HashSet::new();
        let mut doors = HashSet::new();
        for i in 1..grid.len() - 1 {
            for j in 1..grid[0].len() - 1 {
                match grid[i][j] {
                    '@' => { src = (i, j); },
                    'A'..='Z' => { doors.insert(grid[i][j]); },
                    'a'..='z' => { keys.insert(grid[i][j]); },
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

        let mut edges = Vec::new();
        // edges.push(grid_to_edges(&slice_grid(&mod_grid, (0, 0), (src.0, src.1)), (src.0 - 1, src.1 - 1)));
        // edges.push(grid_to_edges(&slice_grid(&mod_grid, (0, src.1), (src.0, grid[0].len() - 1)), (src.0 - 1, 1)));
        // edges.push(grid_to_edges(&slice_grid(&mod_grid, (src.0, 0), (grid.len() - 1, src.1)), (1, src.1 - 1)));
        // edges.push(grid_to_edges(&slice_grid(&mod_grid, (src.0, src.1), (grid.len() - 1, grid[0].len() - 1)), (1, 1)));
        edges.push(grid_to_edges(&mod_grid, (src.0 - 1, src.1 - 1)));
        edges.push(grid_to_edges(&mod_grid, (src.0 - 1, src.1 + 1)));
        edges.push(grid_to_edges(&mod_grid, (src.0 + 1, src.1 - 1)));
        edges.push(grid_to_edges(&mod_grid, (src.0 + 1, src.1 + 1)));

        return Tunnel4 {
            edges: edges,
            keys: keys,
            doors: doors
        };
    }

    fn get_neighbors(&self, (node, k): (FourChar, usize)) -> Vec<((FourChar, usize), usize)> {
        let mut neighbors = Vec::new();
        let ch = vec![node.0, node.1, node.2, node.3];
        for i in 0..self.edges.len() {
            for &edge in &self.edges[i] {
                let mut neighbor = ch.clone();
                let neighbor_ch;
                if edge.0 == ch[i] {
                    neighbor_ch = edge.1;
                } else if edge.1 == ch[i] {
                    neighbor_ch = edge.0;
                } else {
                    continue;
                }
                neighbor[i] = neighbor_ch;
                if edge.3 == k & edge.3 {
                    let nk = match neighbor_ch {
                        '@' => k,
                        _ => k | char_to_bit(neighbor_ch)
                    };
                    neighbors.push((((neighbor[0], neighbor[1], neighbor[2], neighbor[3]), nk), edge.2))
                }
            }
        }
        return neighbors;
    }

    fn find_all_keys(&self) -> usize {
        let mut queue = HashSet::new();
        let mut dist = HashMap::new();
        let mut prev: HashMap<(FourChar, usize), ((FourChar, usize), usize)> = HashMap::new();
        let mut visited = HashSet::new();

        let src = ('@', '@', '@', '@');
        queue.insert((src, 0));
        dist.insert((src, 0), 0);
        while queue.len() > 0 {
            let mut current = (('0', '0', '0', '0'), 0);
            let mut min_dist = usize::MAX;
            for ele in &queue {
                let distance = *dist.get(&ele).unwrap();
                if distance < min_dist {
                    current = *ele;
                    min_dist = distance;
                }
            }
            if current == (('0', '0', '0', '0'), 0) {
                panic!("no path");
            }
            if current.1 == 2usize.pow(self.keys.len() as u32) - 1 {
                // print logic
                // let mut path = Vec::new();
                // let mut cur = current;
                // while cur != ('@', 0) {
                //     let cur1 = *prev.get(&cur).unwrap();
                //     path.push(cur1);
                //     cur = cur1.0;
                // }
                // path.reverse();
                // for ele in path {
                //     println!("{:?}", ele);
                // }
                return min_dist;
            }
            queue.remove(&current);
            visited.insert(current);
            for neighbor in self.get_neighbors(current) {
                if !visited.contains(&neighbor.0) {
                    let alt_dist = min_dist + neighbor.1;
                    queue.insert(neighbor.0);
                    if !dist.contains_key(&neighbor.0) || alt_dist < *dist.get(&neighbor.0).unwrap() {
                        dist.insert(neighbor.0, alt_dist);
                        prev.insert(neighbor.0, (current, alt_dist));
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
    let tunnel = Tunnel::new(grid);
    return tunnel.find_all_keys();
}

fn part2(grid: &[Vec<char>]) -> usize {
    let tunnel = Tunnel4::new(grid);
    return tunnel.find_all_keys();
}

fn main() {
    let input = read_data();
    println!("part1: {:?}", part1(&input));
    println!("part2: {:?}", part2(&input));
}
