use std::io::{self, BufRead};
use std::convert::TryFrom;

fn read_data() -> Vec<u8> {
    let stdin = io::stdin();
    return stdin.lock().lines().next().unwrap().unwrap().chars().map(|x| u8::try_from(x.to_digit(10).unwrap()).unwrap()).collect();
}

fn part2(data: &[u8], width: usize, height: usize) -> () {
     let mut layers = Vec::new();
     let num_layers = data.len() / (width * height);
     for l in 0..num_layers {
        let mut rows = Vec::new();
        for h in 0..height {
            let st = l * width * height + h * width;
            rows.push(data[st..(st+width)].to_vec())
        }
        layers.push(rows);
    }
    for h in 0..height {
        let mut row = "".to_owned();
        for w in 0..width {
            for l in 0..num_layers {
                if layers[l][h][w] != 2 {
                    if layers[l][h][w] == 0 {
                        row.push_str(" ");
                    } else {
                        row.push_str("█");
                    }
                    break;
                }
            }
        }
        println!("{}", row);
    }
}

fn part1(data: &[u8], width: usize, height: usize) -> usize {
    let layer_size = width * height;
    let num_layers = data.len() / layer_size;
    let mut min_layer: &[u8] = &[];
    let mut min = layer_size + 1;
    for l in 0..num_layers {
        let layer = &data[l * layer_size..((l+1) * layer_size)];
        let num_zeroes = layer.iter().filter(|&n| *n == 0).count();
        if num_zeroes < min {
            min = num_zeroes;
            min_layer = layer;
        }
    }
    let n_1s = min_layer.iter().filter(|&n| *n == 1).count();
    let n_2s = min_layer.iter().filter(|&n| *n == 2).count();
    return n_1s * n_2s;
}

fn main() {
    let input = read_data();
    println!("part1:{}", part1(&input, 25, 6));
    println!("part2:");
    part2(&input, 25, 6)
}
