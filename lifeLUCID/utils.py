import textgrid as tg

NON_SPEAKING_TOKENS = ['SILP','SIL']

class LoadTextGrid:
  def __init__(self, file:str) -> None:
    self.grid = tg.TextGrid.fromFile(file)
