#!/usr/bin/env python3
'''
General utilities for use with Whisper
'''

def fmt_time(t: float) -> str:
  '''
  Convert a given time in seconds to the format 'MM:SS'.
  
  :param float t: Time in seconds
  :return: Correctly formatted time
  :rtype: str
  '''
  
  t = int(t)
  mins = t // 60
  secs = t % 60
  if secs < 10:
    secs = f"0{secs}"
  return f"{mins}:{secs}"


def write_result(filename: str, result: dict, stamped: bool=True, inline: bool=False) -> None:
  '''
  Write the result of a Whisper transcription to a file.
  
  :param str filename: Name of file to write to
  :param dict result: Result of Whisper transcription
  :param bool stamped: Should the result be timestamped?
  :param bool inline: Should the result include linebreaks? (Ignores stamped)
  '''
  
  with open(filename, 'w') as f:
    if inline or not stamped:
      text = result['text']
      if inline:
        text = text.replace('\n', ' ')
      f.write(text)
    else:
      for s in result['segments']:
        start, end, txt = fmt_time(s['start']), fmt_time(s['end']), s['text']
        f.write(f"[{start} -> {end}] {txt}\n")

