import textwrap
import soundfile as sf
import sounddevice as sd
import pandas as pd
import numpy as np
import json
from pathlib import Path

WRAP_WIDTH = 50

class AudioDataLinker:
  """ 
  Object to aid linking audio and transcript data
  """
  def __init__(self, audio_dir:Path, data_file:Path) -> None:
    """ 
    Create a new AudioDataLinker.

    :param audio_dir: Directory within which audio files are stored.
    :param data_file: File containing transcription data.
    """
    with open(data_file) as f:
      self.data = json.load(f)
    self.audio_dir = audio_dir

  def play_audio(self, idx:str) -> bool:
    """ 
    Play audio correlated with an utterance.

    :param idx: Index of utterance.
    :returns: True if audio file exists, false otherwise.
    """
    audio_file = self.audio_dir / f'{idx:03d}.wav'
    if not audio_file.exists():
      return False
    sd.play(*sf.read(audio_file), blocking=True)

  def data_for_table(self, height:int=2) -> list:
    """ 
    Get data in format required to be printed in DataTable object.

    :returns: List containing table rows.
    """
    table_rows = [('ID', 'Hypothesis', 'Reference')]
    for idx, utterance in self.data.items():
      ref = wrap(utterance['transcript'])
      hyp = wrap(utterance['whisper']['text'])
      table_rows.append(
          (idx, hyp, ref))
    return table_rows

def wrap(string:str) -> str:
  """
  Apply text wrapping to a string.
  """
  return '\n'.join(textwrap.wrap(string, width=WRAP_WIDTH))
