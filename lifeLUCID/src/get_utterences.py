#!/usr/bin/env python
"""
get_utterances.py

Given a directory of Praat TextGrid files, this program segments them all
into utterances according to the documentation provided by with the LifeLUCID
corpus (V.Hazan et al.).

The utterances are written to JSON files in a given output directory.
"""

__author__ = 'Adam Spencer'

import argparse
import json
import textgrid as tg
from pathlib import Path
from typing import Union

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
  normalise = not args['no-normalise']

  # New Path object @ specified path
  dir_path = Path(args['in_dir'])
  if not dir_path.is_dir():
    raise ValueError(f'{dir_path} is Not a directory!')

  all_utterances = dict()
  for file in dir_path.iterdir():
    if 'Ac.TextGrid' not in file.name:
      continue
    grid = tg.TextGrid.fromFile(file)
    all_utterances[file.name] = segment_utterances(grid, normalise=normalise)

def segment_utterances(grid:tg.TextGrid, /, normalise:bool) -> (
    dict[int, dict[str, Union[float, str]]]):
  """
  Segment a Praat TextGrid into utterances, with start and end times and the
  transcription as provided in the TextGrid.

  Utterance ends and beginnings are found using the `BREAK_TOKENS`, and any
  non-speaking tokens (as defined in `JUNK_TOKENS`) are removed.

  :param grid: The Praat TextGrid to segment into utterances.
  :param normalise: Enable lowercase text normalisation.
  :returns: dict of structure { segment_num -> { start_time, end_time, transcript }
  """
  segments = dict()
  start_time = float()
  seg_words = list()
  seg_counter = 0
  seg_ongoing = False

  for interval in grid[0]:
    if interval.mark in BREAK_TOKENS:
      if seg_ongoing:
        segments[seg_counter] = {'start' : start_time, 'end' : interval.minTime,
                                 'transcript' : ' '.join(seg_words)}
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
  # For testing...
  grid = tg.TextGrid.fromFile('/Users/adamspencer/Documents/University/third-year/diss/lifeLUCID/textgrids/NORM/OA01OA02FNORMF2_F2_Ac.TextGrid')
  x = segment_utterances(grid, True)
  for key, val in x.items():
    print(val, '\n')

