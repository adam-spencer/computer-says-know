#!/usr/bin/env python

__author__ = 'Adam Spencer'

import pandas as pd
from pathlib import Path
import textgrid as tg
import re
import argparse

BREAK_TOKENS = {'SILP', '<GA>'} # As described in documentation
JUNK_TOKENS = {'SIL', '<BELL>'}

def main():
  # Parse Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('in_dir', help='Name of dir to find textgrids in')
  parser.add_argument('out_dir', help='Name of dir to write JSON files to')
  parser.add_argument('--no-normalise', '-n', action='store_true',
                      help='Disable case normalisation')
  args = parser.parse_args()

  # New Path object @ specified path
  dir_path = Path(args['in_dir'])
  if not dir_path.is_dir():
    raise ValueError(f'{dir_path} is Not a directory!')

  files = [i for i in dir_path.iterdir() if 'Ac.TextGrid' in i.name]
  grids = [tg.TextGrid.fromFile(f, name=f.name.removesuffix('.TextGrid'))
           for f in files]

def segment_utterances(grid:tg.TextGrid, normalise:bool): #  -> dict[int, tuple]:
  # I need to ensure this is tracking text as well as time, overlooked that!
  segments = dict()
  start_time = float()
  seg_words = list()
  seg_counter = 0
  seg_ongoing = False

  for interval in grid[0]:
    if interval.mark in BREAK_TOKENS:
      if seg_ongoing:
        segments[seg_counter] = {'start' : start_time, 'end' : interval.minTime,
                                 'words' : ' '.join(seg_words)}
        seg_words = []
        seg_counter += 1
        seg_ongoing = False
      continue
    elif interval.mark in JUNK_TOKENS:
      continue
    elif not seg_ongoing:
      start_time = interval.minTime
      seg_ongoing = True
    if normalise:
      interval.mark = interval.mark.lower()
    seg_words.append(interval.mark)
  return segments

if __name__ == '__main__':
  # main()
  grid = tg.TextGrid.fromFile('/Users/adamspencer/Documents/University/third-year/diss/lifeLUCID/textgrids/NORM/OA01OA02FNORMF2_F2_Ac.TextGrid')
  x = segment_utterances(grid, True)
  for key, val in x.items():
    print(val, '\n')

