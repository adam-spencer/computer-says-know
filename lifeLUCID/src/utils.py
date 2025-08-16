"""
Utilities for use in other files.
"""

def vprint(verbose:bool, msg:str) -> None:
  """
  Verbose mode printing.
  
  :param verbose: Verbose mode bool.
  :param msg: Message to print.
  """
  if verbose:
    print(msg)

