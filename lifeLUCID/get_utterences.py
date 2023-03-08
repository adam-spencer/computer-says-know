#!/usr/bin/env python

__author__ = 'Adam Spencer'

import pandas as pd
from pathlib import Path
import textgrid as tg
import re
import argparse

def main():
  # Parse Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('dirname', help='Name of dir to find textgrids in')
  args = parser.parse_args()

  # New Path object @ specified path
  dir_path = Path(args['dirname'])
  if not dir_path.is_dir():
    raise ValueError(f'{dir_path} is Not a directory!')

  files = [i for i in dir_path.iterdir() if 'Ac.TextGrid' in i.name]
  grids = [tg.TextGrid.fromFile(f) for f in files]

def segment_utterances(grid:tg.TextGrid) -> dict[str, tuple]:
  pass

def grid_to_dict(grid: tg.TextGrid) -> dict[str, tuple]:
  pass

if __name__ == '__main__':
  main()

