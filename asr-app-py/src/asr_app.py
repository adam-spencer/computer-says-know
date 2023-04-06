from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable
import sys
from pathlib import Path

from transcript_audio import AudioDataLinker

class TranscriptionApp(App):
  """
  A Textual app to demonstrate semi-automatic transcription.
  """
  CSS_PATH="./asr_app.css"

  def compose(self) -> ComposeResult:
    """ 
    Create child widgets for the app.
    """
    yield DataTable(fixed_columns=1)

  def on_mount(self) -> None:
    table = self.query_one(DataTable) # get col names
    rows = iter(self.data_in)
    table.add_columns(*next(rows))
    for row in rows:
      table.add_row(*row, height=2)

  def populate_data(self, data):
    self.data_in = data

  def action_toggle_ref(self) -> None:
    """
    An action to toggle reference text.
    """
    pass

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} path/to/audio/ path/to/data.json')
    sys.exit(-1)

  audio_dir = Path(sys.argv[1])
  data_file = Path(sys.argv[2])
  if audio_dir.is_dir() and data_file.exists():
    data_linker = AudioDataLinker(audio_dir, data_file)
  else:
    print('Something is wrong with your input!')
    print(f'I got {audio_dir} and {data_file}')
    sys.exit(-1)

  app = TranscriptionApp()
  app.populate_data(data_linker.data_for_table())
  app.run()
