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
    is_base: bool,
}

impl Reaction {
    fn new(reaction: &str) -> Reaction {
        let mut split = reaction.split(" => ");
        let mut left = Vec::new();
        let mut is_base = false;
        for resource in split.next().unwrap().split(", ") {
            let r = Resource::new(resource);
            if r.id == "ORE" {
                is_base = true;
            }
            left.push(r);
        }
        return Reaction {left: left, right: Resource::new(split.next().unwrap()), is_base: is_base};
    }
}

// struct Stoichiometry {
//     base_reactions: HashMap<String, Reaction>,
//     int_reactions: HashMap<String, Reaction>,
//     fuel: Reaction,
// }

// impl Stoichiometry {
//     fn new(reactions: &[&str]) -> Stoichiometry {
//         base_reactions = HashMap::new();
//         int_reactions = HashMap::new();
//         fuel = Vec::new();

//         for reaction in reactions {

//         }

//         return Stoichiometry{
//             base_reactions: base_reactions,
//             int_reactions: int_reactions,
//             fuel: fuel,
//         }
//     }
// }

fn read_data() -> Vec<Reaction> {
    let stdin = io::stdin();
    let mut reactions = Vec::new();
    for line in stdin.lock().lines() {
        let l = line.unwrap();
        reactions.push(Reaction::new(&l));
    }
    return reactions;
}

fn part1(reactions: &[Reaction]) -> usize {
    let mut all_reactions = HashMap::new();
    for reaction in reactions {
        all_reactions.insert(&reaction.right.id, reaction);
    }
    let mut ores = 0;
    let mut reserve = HashMap::new();
    let mut needs = HashMap::new();
    needs.insert("FUEL", 1);
    while needs.len() > 0 {
        let cur_id = &*needs.keys().next().unwrap().to_owned();
        let mut cur_qty = needs.remove(cur_id).unwrap();
        let reaction = *all_reactions.get(&cur_id.to_owned()).unwrap();
        if reserve.contains_key(&reaction.right.id) {
            let avail = *reserve.get(&reaction.right.id).unwrap();
            if avail >= cur_qty {
                cur_qty = 0;
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
        println!("{:?},{}", cur_id, req_reactions);
        println!("{:?}", reserve);
        println!("{:?}", needs);
        println!("----");
    }
    return ores;
}

fn main() {
    let input = read_data();
    println!("part1:{}", part1(&input));
}
