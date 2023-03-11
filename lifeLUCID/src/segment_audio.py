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

def generate_segments(filename:Path, json:Path, channel:int,
                      verbose:bool) -> np.ndarray:
  """

  """
  pass

def save_segments(segs:np.ndarray, outpath:Path, verbose:bool) -> None:
  """

  """
  pass

def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument('in_file', help='Input audio file')
  parser.add_argument('json_file',
                      help='Input JSON file containing segment definitions')
  parser.add_argument('out_dir', help='Output directory')
  parser.add_argument('--use-channel', '-u', choices=range(0,2),
                      help='Use a specific channel, 0 = L, 1 = R, 2 = B',
                      default=0)
  parser.add_argument('--verbose', '-v', action='store_true',
                      help='Activate verbose output')
  args = parser.parse_args()

  in_file = Path(args.in_file)
  json_file = Path(args.json_file)
  out_dir = Path(args.out_dir)
  if in_file.is_dir() or json_file.is_dir() or not out_dir.is_dir():
    raise ValueError(f"Incorrect input spec!")

  segments = generate_segments(in_file, json_file, args.channel, args.verbose)
  save_segments(segments, out_dir, args.verbose)

if __name__ == '__main__':
  main()
