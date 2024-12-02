use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

// The output is wrapped in a Result to allow matching on errors.
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn is_safe_first(report: &Vec<i32>) -> bool {
    if report.len() <= 1 {
        return true;
    }

    let fst = report[0];
    let snd = report[1];

    let is_counting_up = snd > fst;

    for idx in 0..(report.len() - 1) {
        if is_counting_up != (report[idx] < report[idx+1]) {
            return false; // not in same direction
        }
        let difference = (report[idx] - report[idx+1]).abs();
        if (difference < 1) || (difference > 3) {
            return false;
        }
    }
    true
}

fn is_safe_second(report: &Vec<i32>) -> bool {
    if report.len() <= 1 {
        return true;
    }
    if is_safe_first(report) {
        return true;
    }

    // report lengths are short enough that we can just try them all
    for drop_idx in 0..(report.len()) {
        let mut new_report: Vec<i32> = report.clone();
        new_report.remove(drop_idx);
        if is_safe_first(&new_report) {
            return true;
        }
    }
    false
}

fn main() {
    // Parse
    if let Ok(lines) = read_lines("./input") {

        let mut safe_first_counter = 0;
        let mut safe_second_counter = 0;
        // Consumes the iterator, returns an (Optional) String
        for line in lines.flatten() {
            let report: Vec<i32> = line.split_whitespace().map(|a| a.parse().unwrap()).collect();
            if is_safe_first(&report) {
                safe_first_counter += 1;
            }
            if is_safe_second(&report) {
                safe_second_counter += 1;
            }
        }
        println!("First solution: {safe_first_counter}");
        println!("Second solution: {safe_second_counter}");
    }
}
