use regex::Regex;
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

fn main() {
    {
        let lines = read_lines("./input").unwrap();
        let re = Regex::new(r"mul\((?P<fst>\d+)\,(?P<snd>\d+)\)").unwrap();
        let mut total = 0;
        for line in lines.flatten() {
            for (_, [fst, snd]) in re.captures_iter(&line).map(|c| c.extract()) {
                total += fst.parse::<i32>().unwrap() * snd.parse::<i32>().unwrap();
            }
        }
        println!("first solution {total}");
    }

    {
        let lines = read_lines("./input").unwrap();
        let re = Regex::new(r"((mul)\((?P<fst>\d+)\,(?P<snd>\d+)\))|((don't)(\()(\)))|((do)(\()(\)))").unwrap();
        let mut enabled = true;
        let mut total = 0;
        for line in lines.flatten() {
            for (_, [_, name, arg1, arg2]) in re.captures_iter(&line).map(|c| c.extract()) {
                
                match name {
                    "mul" => {
                        if enabled {
                            total += arg1.parse::<i32>().unwrap() * arg2.parse::<i32>().unwrap();
                        }
                    }
                    "don't" => {
                        enabled = false;
                    }
                    "do" => {
                        enabled = true;
                    }
                    def => panic!("unhandled {def}")
                }
            }
        }
        println!("second solution {total}")
    }
}
