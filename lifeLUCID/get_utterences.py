#!/usr/bin/env python

__author__ = 'Adam Spencer'

import pandas as pd
from pathlib import Path
import re
import argparse

from utils import LoadTextGrid

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument('dirname', help='Name of dir to find textgrids in')
args = parser.parse_args()

# New Path object @ specified path
dir_path = Path(args['dirname'])
if not dir_path.is_dir():
  raise ValueError(f'{dir_path} is Not a directory!')


