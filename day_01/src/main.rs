use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashMap;

// The output is wrapped in a Result to allow matching on errors.
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn main() {
    let mut first_list = Vec::new();
    let mut second_list = Vec::new();

    // Parse
    if let Ok(lines) = read_lines("./input") {
        // Consumes the iterator, returns an (Optional) String
        for line in lines.flatten() {
            let linevec = Vec::from_iter(line.split_whitespace());
            println!("{linevec:?}");
            let first: i32 = linevec[0].parse().expect("not a number");
            let second: i32 = linevec[1].parse().expect("not a number");

            first_list.push(first);
            second_list.push(second);
        }
    }

    // Part 1
    let mut first_sorted = first_list.clone();
    first_sorted.sort();
    let mut second_sorted = second_list.clone();
    second_sorted.sort();

    let mut total_difference = 0;
    for (fst, snd) in first_sorted.iter().zip(second_sorted.iter()) {
        total_difference += (fst - snd).abs()
    }
    println!("first solution: {total_difference}");

    // Part 2

    let mut lookup_occurences: HashMap<i32, i32> = HashMap::new();

    for snd in second_list.iter() {
        lookup_occurences.insert(*snd, lookup_occurences.get(snd).unwrap_or(&0) + 1);
    }

    let mut total_similarity = 0;
    for fst in first_list.iter() {
        total_similarity += fst * lookup_occurences.get(fst).unwrap_or(&0);
    }

    println!("second solution: {total_similarity}");

}
