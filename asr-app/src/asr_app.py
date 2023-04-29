import sys
from pathlib import Path

from audio_data_link import AudioDataLinker
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer

ROW_HEIGHT = 3


class TranscriptionApp(App):
    """
    A Textual app to demonstrate semi-automatic transcription.
    """
    BINDINGS = [
        ('p', 'play_sound', 'Play Audio'),
    ]

    def compose(self) -> ComposeResult:
        """ 
        Create child widgets for the app.
        """
        yield DataTable(fixed_columns=1, zebra_stripes=True)
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        rows = iter(self.data_in)
        table.add_columns(*next(rows))
        for row in rows:
            table.add_row(*row, height=ROW_HEIGHT)

    def populate_data(self, data_linker: AudioDataLinker):
        self.data_in = data_linker.data_for_table()
        self.data_linker = data_linker

    def action_play_sound(self):
        if self.selected is not None:
            self.data_linker.play_audio(self.selected)

    def on_data_table_cell_highlighted(self, message: DataTable.CellHighlighted):
        self.selected = message.coordinate.row


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
    app.populate_data(data_linker)
    app.run()
