use serde::{Serialize, Deserialize};
use std::path::Path;

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
struct TranscriptDataReader {
    filepath: Path,
    data: Vec<TranscriptData>,
}

impl TranscriptDataReader {
    pub fn new() -> TranscriptDataReader
