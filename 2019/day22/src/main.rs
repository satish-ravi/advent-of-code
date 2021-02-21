use std::io::{self, BufRead};
use mod_exp::mod_exp;

trait Shuffler {
    fn shuffle(&self, deck: &[usize]) -> Vec<usize>;
    fn shuffle_single(&self, deck_size: usize, pos: usize) -> usize;
    fn shuffle_reverse(&self, deck_size: usize, pos: usize) -> usize;
    fn get_coefficient(&self, deck_size: i128, a: i128, b: i128) -> (i128, i128);
}

struct NewStack {}

impl Shuffler for NewStack {
    fn shuffle(&self, deck: &[usize]) -> Vec<usize> {
        let mut res = deck.to_vec();
        res.reverse();
        return res;
    }

    fn shuffle_single(&self, deck_size: usize, pos: usize) -> usize {
        return deck_size - pos - 1;
    }

    fn shuffle_reverse(&self, deck_size: usize, pos: usize) -> usize {
        return deck_size - pos - 1;
    }

    fn get_coefficient(&self, deck_size: i128, a: i128, b: i128) -> (i128, i128) {
        return (-a % deck_size, (deck_size - 1 - b) % deck_size);
    }
}

struct Cut {
    n: i32
}

impl Shuffler for Cut {
    fn shuffle(&self, deck: &[usize]) -> Vec<usize> {
        let n;
        if self.n >= 0 {
            n = self.n as usize;
        } else {
            n = (deck.len() as i32 + self.n) as usize;
        }
        let mut res = deck[n..].to_vec();
        res.extend(&deck[0..n]);
        return res;
    }

    fn shuffle_single(&self, deck_size: usize, pos: usize) -> usize {
        return (pos as i32 - self.n + deck_size as i32) as usize % deck_size;
    }

    fn shuffle_reverse(&self, deck_size: usize, pos: usize) -> usize {
        return (pos as i32 + self.n + deck_size as i32) as usize % deck_size;
    }

    fn get_coefficient(&self, deck_size: i128, a: i128, b: i128) -> (i128, i128) {
        let n = self.n as i128;
        return (a, (b - n) % deck_size);
    }
}

struct Increment {
    n: usize
}

impl Shuffler for Increment {
    fn shuffle(&self, deck: &[usize]) -> Vec<usize> {
        let mut res = vec![usize::MAX; deck.len()];
        let mut pos = 0;
        for card in deck {
            res[pos] = *card;
            pos = (pos + self.n) % deck.len();
        }
        return res;
    }

    fn shuffle_single(&self, deck_size: usize, pos: usize) -> usize {
        return (pos * self.n) % deck_size;
    }

    fn shuffle_reverse(&self, deck_size: usize, pos: usize) -> usize {
        return mod_exp(self.n, deck_size - 2, deck_size) * pos % deck_size;
    }

    fn get_coefficient(&self, deck_size: i128, a: i128, b: i128) -> (i128, i128) {
        let n = self.n as i128;
        return ((a * n) % deck_size, (b * n) % deck_size);
    }
}

fn read_data() -> Vec<Box<dyn Shuffler>> {
    let stdin = io::stdin();
    let mut shufflers: Vec<Box<dyn Shuffler>> = Vec::new();
    for line in stdin.lock().lines() {
        let l = line.unwrap();
        if l == "deal into new stack".to_string() {
            shufflers.push(Box::new(NewStack{}));
        } else if l.starts_with("deal with increment") {
            let n = l.split(" ").last().unwrap().parse::<usize>().unwrap();
            shufflers.push(Box::new(Increment{n: n}));
        } else {
            let n = l.split(" ").last().unwrap().parse::<i32>().unwrap();
            shufflers.push(Box::new(Cut{n: n}));
        }
    }
    return shufflers;
}

fn apply_shuffles(shufflers: Vec<Box<dyn Shuffler>>, deck: &[usize]) -> Vec<usize> {
    let mut res = deck.to_vec();
    for shuffler in shufflers {
        res = shuffler.shuffle(&res);
    }
    return res;
}

fn part1_v1(shufflers: Vec<Box<dyn Shuffler>>) -> usize {
    let deck: Vec<usize> = (0..10007).collect();
    let shuffled = apply_shuffles(shufflers, &deck);
    for (i, card) in shuffled.iter().enumerate() {
        if *card == 2019usize {
            return i;
        }
    }
    panic!("shouldn't reach");
}

fn part1(shufflers: &[Box<dyn Shuffler>]) -> usize {
    let mut pos = 2019;
    let deck_size = 10007;
    for shuffler in shufflers {
        pos = shuffler.shuffle_single(deck_size, pos);
    }
    return pos;
}

fn part2_v1(shufflers: &[Box<dyn Shuffler>]) -> usize {
    let mut pos = 1538;
    let deck_size = 10007;
    for shuffler in shufflers.iter().rev() {
        pos = shuffler.shuffle_reverse(deck_size, pos);
    }
    return pos;
}

fn part2(shufflers: &[Box<dyn Shuffler>]) -> i128 {
    let deck_size = 119315717514047i128;
    let num_shuffles = 101741582076661i128;
    let pos = 2020i128;
    let mut a = 1i128;
    let mut b = 0i128;
    for shuffler in shufflers {
        let res =shuffler.get_coefficient(deck_size, a, b);
        a = res.0;
        b = res.1;
    }
    // r = (b * pow(1-a, deck_size-2, deck_size)) % deck_size
// print(f"Card at #{pos}: {((pos - r) * pow(a, n*(deck_size-2), deck_size) + r) % deck_size}")
    let r = (b * mod_exp(1 - a, deck_size - 2, deck_size)) % deck_size;
    return ((pos - r) * mod_exp(a, num_shuffles * (deck_size - 2), deck_size) + r) % deck_size;
}

fn main() {
    let shufflers = read_data();
    println!("part1:{:?}", part1(&shufflers));
    println!("part2:{:?}", part2(&shufflers));
}
