use std::{error::Error, io, env};
mod data_reader;
use data_reader::TranscriptDataReader;
use cursive::{views::{TextView, Dialog}, Cursive};

fn main() {
    // let args: Vec<String> = env::args().collect();
    // assert!(args.len() == 2, "Usage: {} <file path>", args[0]);
    // let tdr = TranscriptDataReader::new(&args[1]);
    let mut siv = cursive::default();

    siv.add_layer(Dialog::text("This is a survery!\nPress <Next> when you're ready.")
                  .title("Important Survey")
                  .button("Next", show_next));
    siv.run();
}

fn show_next(s: &mut Cursive) {
    s.pop_layer();
    s.add_layer(Dialog::text("Did you do the thing?")
        .title("Question 1")
        .button("Yes!", |s| show_answer(s, "I knew it! Well done!"))
        .button("No!", |s| show_answer(s, "I knew you couldn't be trusted!"))
        .button("Uh?", |s| s.add_layer(Dialog::info("Try again!"))));
}

fn show_answer(s: &mut Cursive, msg: &str) {
    s.pop_layer();
    s.add_layer(Dialog::text(msg)
                .title("Results")
                .button("Finish", |s| s.quit()));
}
