use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

// The output is wrapped in a Result to allow matching on errors.
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn main() {
    let lines = read_lines("./input").unwrap();
    let mut matrix: HashMap<(i32, i32), char> = HashMap::new();
    let mut dim_x: i32 = 0;
    let mut dim_y: i32 = 0;
    for (i, line) in lines.map_while(Result::ok).enumerate() {
        dim_x = (i + 1) as i32;
        for (j, c) in line.chars().enumerate() {
            matrix.insert((i as i32, j as i32), c);
            dim_y = (j + 1) as i32;
        }
    }

    let mut xmas_found = 0;

    for x in 0..dim_x {
        for y in 0..dim_y {
            for dx in [-1, 0, 1] {
                'direction: for dy in [-1, 0, 1] {
                    if dx == 0 && dy == 0 {
                        continue;
                    }
                    for (i, c) in "XMAS".chars().enumerate() {
                        let actual = matrix.get(&(x + (i as i32) * dx, y + (i as i32) * dy));
                        if actual.is_none() || *actual.unwrap() != c {
                            continue 'direction;
                        }
                    }
                    xmas_found += 1;
                }
            }
        }
    }
    println!("First solution {xmas_found}");

    let mut global_mas_found = 0;
    for x in 0..dim_x {
        for y in 0..dim_y {
            let mut mas_found = 0;
            'direction: for (dx, dy) in [(-1, -1), (-1, 1), (1, -1), (1, 1)] {
                for (i, c) in "MAS".chars().enumerate() {
                    let step: i32 = (i as i32) - 1;
                    let actual = matrix.get(&(x + step * dx, y + step * dy));
                    if actual.is_none() || *actual.unwrap() != c {
                        continue 'direction;
                    }
                }
                mas_found += 1;
            }
            if mas_found == 2 {
                global_mas_found += 1;
            }
        }
    }
    println!("Second solution {global_mas_found}");
}
