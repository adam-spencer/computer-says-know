#!/usr/bin/env python
"""
segment_audio.py

Generate audio segments using a JSON input.
"""

import soundfile as sf
import numpy as np
import json
import argparse
from pathlib import Path

def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument('in_file', help='Input audio file')
  parser.add_argument('out_dir', help='Output directory')
  parser.add_argument('--use-channel', '-u', choices=range(0,2))
  args = parser.parse_args()

  in_file = Path(args.in_file)
  out_dir = Path(args.out_dir)
  if in_file.is_dir or not out_dir.is_dir:
    raise ValueError(f"Incorrect input spec!")

  segments = generate_segments(in_file, args.channel)
  save_segments(segments, out_dir)

def generate_segments(filename:str, channel:int) -> np.ndarray:
  pass

def save_segments(segs:np.ndarray, outpath:Path):
  pass

if __name__ == '__main__':
  main()
