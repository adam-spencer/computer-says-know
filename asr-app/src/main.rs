use std::cmp::Ordering;
use std::{fs::File, io::BufReader, error::Error,};
use std::env;
use cursive::align::HAlign;
use cursive::traits::*;
use cursive::views::Dialog;
use cursive_table_view::{TableViewItem, TableView};
use serde::{Serialize, Deserialize};


// TODO:
//   * Restructure the JSON files themselves, having "{ filename : 000.wav, ... }'
//     etc. rather than "'0' : {...}"
//   * Fix this stuff- seems almost working strangely enough :O
//   *

#[derive(Serialize, Deserialize, Debug, Clone)]
struct WhisperSegments {
    id: i8,
    seek: i8,
    start: f32,
    end: f32,
    text: String,
    tokens: Vec<i32>,
    temperature: f32,
    avg_logprob: f64,
    compression_ratio: f64,
    no_speech_prob: f64,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct WhisperData {
    text: String,
    segments: Vec<WhisperSegments>,
    language: String,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct TranscriptData {
    idx: i32,
    start: f32,
    end: f32,
    transcript: String,
    whisper: WhisperData,
}

#[derive(Debug)]
pub struct TranscriptDataReader {
    filepath: String,
    pub data: Vec<TranscriptData>,
}

impl TranscriptDataReader {
    pub fn new(filepath: &String) -> Result<Self, Box<dyn Error>> {
        let file = File::open(filepath)?;
        let reader = BufReader::new(file);
        let tdr = Self {
            filepath : filepath.to_string(),
            data : serde_json::from_reader(reader)?,
        };

        Ok(tdr)
    }
}

#[derive(Copy, Clone, PartialEq, Eq, Hash)]
enum BasicColumn {
    ID,
    Hypothesis,
    Reference,
}

impl BasicColumn {
   fn as_str(&self) -> &str {
       match *self {
           BasicColumn::ID => "ID",
           BasicColumn::Hypothesis => "Hypothesis",
           BasicColumn::Reference => "Reference",
       }
   }
}

impl TableViewItem<BasicColumn> for TranscriptData {
    fn to_column(&self, column: BasicColumn) -> String {
        match column {
            BasicColumn::ID => format!("{}", self.idx),
            BasicColumn::Hypothesis => self.transcript.to_string(),
            BasicColumn::Reference => self.whisper.text.to_string(),
        }
    }
    fn cmp(&self, other: &Self, column: BasicColumn) -> Ordering
    where
        Self: Sized,
    {
        match column {
            BasicColumn::ID => self.idx.cmp(&other.idx),
            BasicColumn::Hypothesis => self.transcript.cmp(&other.transcript),
            BasicColumn::Reference => self.whisper.text.cmp(&other.whisper.text),
        }
    }
}

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    assert!(args.len() == 2, "Usage: {} <file path>", args[0]);
    let tdr = TranscriptDataReader::new(&args[1]).unwrap();

    let mut siv = cursive::default();
    let mut table = TableView::<TranscriptData, BasicColumn>::new()
        .column(BasicColumn::ID, "ID", |c| c.width_percent(10))
        .column(BasicColumn::Hypothesis, "Hypothesis",
                |c| c.align(HAlign::Center))
        .column(BasicColumn::Reference, "Reference",
                |c| c.align(HAlign::Right));

    table.set_items(tdr.data);

    siv.add_layer(Dialog::around(table
                                 .with_name("table")
                                 .min_size((100,100)))
                  .title("Table View"));
    siv.run();
} 

