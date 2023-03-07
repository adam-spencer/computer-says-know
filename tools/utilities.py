import json
from typing import Union
import pandas as pd

class TableToJSON:
  def __init__(self, filename:str, index:bool, verbose:bool) -> None:
    """
    Load a table to be encoded into JSON format.

    Expected headers : [speaker, fileID, transcript]

    :param filename: name of file to load.
    :param index: if True, use column 0 as index.
    """
    self.verbose = verbose

    if self.verbose:
      print("Loading table...")
    if index:
      self.df = pd.read_csv(filename, index_col=0)
    else:
      self.df = pd.read_csv(filename)

    if self.verbose:
      print("Generating groups...")
    self.grouped = self.df.groupby('speaker')

  def encode(self, savepath:str=None) -> Union[str, None]:
    """
    Encode the loaded table into JSON file format.

    :param savepath: Path to save file to.
    :returns: JSON encoding if no save path given, otherwise nothing.
    """
    data_dict = dict()
    if self.verbose:
      print('Converting to dict...')
      counter = 0
      end = len(self.grouped.groups)
    for speaker, table in self.grouped:
      data_dict[speaker] = (table[['fileID','transcript']]
                            .set_index('fileID')
                            .to_dict()['transcript'])
      if self.verbose:
        counter+=1
        print(f"Line {counter} / {end}", end='\r')

    if self.verbose:
      print('Reformatting dict...')
    for speaker, data in data_dict.items():
      for idx, ref_transcript in data.items():
       data[idx] = dict(ref=ref_transcript, asr="") 

    if self.verbose:
      print('Encoding as JSON...')
    data_json = json.dumps(data_dict, indent=2)

    if savepath is None:
      return data_json
    else:
      if self.verbose:
        print('writing...')
      with open(savepath, 'w') as file:
        file.write(data_json)
      if self.verbose:
        print('done!')

