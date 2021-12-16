use std::io::{self, BufRead};
use std::collections::HashMap;

#[derive(Debug)]
struct Resource {
    id: String,
    qty: usize
}

impl Resource {
    fn new(resource_str: &str) -> Resource {
        let mut split = resource_str.split(" ");
        let qty = split.next().unwrap().parse::<usize>().unwrap();
        return Resource {id: split.next().unwrap().to_string(), qty: qty};
    }
}

#[derive(Debug)]
struct Reaction {
    left: Vec<Resource>,
    right: Resource,
}

impl Reaction {
    fn new(reaction: &str) -> Reaction {
        let mut split = reaction.split(" => ");
        let mut left = Vec::new();
        for resource in split.next().unwrap().split(", ") {
            let r = Resource::new(resource);
            left.push(r);
        }
        return Reaction {left: left, right: Resource::new(split.next().unwrap())};
    }
}

fn read_data() -> Vec<Reaction> {
    let stdin = io::stdin();
    let mut reactions = Vec::new();
    for line in stdin.lock().lines() {
        let l = line.unwrap();
        reactions.push(Reaction::new(&l));
    }
    return reactions;
}

fn required_ores(reactions: &[Reaction], fuel: usize) -> usize {
    let mut all_reactions = HashMap::new();
    for reaction in reactions {
        all_reactions.insert(&reaction.right.id, reaction);
    }
    let mut ores = 0;
    let mut reserve = HashMap::new();
    let mut needs = HashMap::new();
    needs.insert("FUEL", fuel);
    while needs.len() > 0 {
        let cur_id = &*needs.keys().next().unwrap().to_owned();
        let mut cur_qty = needs.remove(cur_id).unwrap();
        let reaction = *all_reactions.get(&cur_id.to_owned()).unwrap();
        if reserve.contains_key(&reaction.right.id) {
            let avail = *reserve.get(&reaction.right.id).unwrap();
            if avail >= cur_qty {
                reserve.insert(&reaction.right.id, avail - cur_qty);
                continue;
            } else {
                cur_qty = cur_qty - avail;
                reserve.remove(&reaction.right.id);
            }
        }
        let mut req_reactions = cur_qty / reaction.right.qty;
        if cur_qty % reaction.right.qty != 0 {
            req_reactions += 1;
            *reserve.entry(&reaction.right.id).or_insert(0) += req_reactions * reaction.right.qty - cur_qty;
        }
        for resource in reaction.left.iter() {
            let req = req_reactions * resource.qty;
            if resource.id == "ORE" {
                ores += req;
            } else {
                *needs.entry(&resource.id).or_insert(0) += req;
            }
        }
    }
    return ores;
}

fn part1(reactions: &[Reaction]) -> usize {
    return required_ores(reactions, 1);
}

fn part2(reactions: &[Reaction]) -> usize {
    let ores = 1000000000000;
    let mut low = ores / required_ores(reactions, 1);
    let mut high = low * 2;
    while low < high {
        let mid = (low + high) / 2;
        let cur_ores = required_ores(reactions, mid);
        if cur_ores > ores {
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    for num in vec![high - 1, high, low, low + 1] {
        let cur_ores = required_ores(reactions, num);
        if cur_ores > ores {
            return num - 1;
        }
    }
    panic!("shouldn't reach");
}

fn main() {
    let input = read_data();
    println!("part1:{}", part1(&input));
    println!("part2:{}", part2(&input));
}
