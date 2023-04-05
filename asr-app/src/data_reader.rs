use serde::{Serialize, Deserialize};
use std::{fs::File, io::BufReader, error::Error,};

#[derive(Serialize, Deserialize, Debug)]
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

#[derive(Serialize, Deserialize, Debug)]
struct WhisperData {
    text: String,
    segments: Vec<WhisperSegments>,
    language: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct TranscriptData {
    idx: i32,
    start: f32,
    end: f32,
    transcript: String,
    whisper: WhisperData,
}

#[derive(Debug)]
pub struct TranscriptDataReader {
    filepath: String,
    data: Vec<TranscriptData>,
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

    pub fn 
}
