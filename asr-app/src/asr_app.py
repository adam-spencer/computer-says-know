import sys
from pathlib import Path

from audio_data_link import AudioDataLinker
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer

ROW_HEIGHT = 4

SORT_STYLES = {'Chronological': 'ID', 'Prob': 'Posterior Prob'}


class TranscriptionApp(App):
    """
    A Textual app to demonstrate semi-automatic transcription.
    """
    BINDINGS = [
        ('p', 'play_sound', 'Play Audio'),
        ('s', 'sort_id', 'Sort ID'),
        ('w', 'sort_wer', 'Sort WER'),
        ('a', 'sort_prob', 'Sort Av. Log Prob.'),
    ]

    def compose(self) -> ComposeResult:
        """ 
        Create child widgets for the app.
        """
        yield DataTable(fixed_columns=1, zebra_stripes=True)
        yield Footer()

    def on_mount(self) -> None:
        self.current_sort_col = 'ID'
        self.reversed_sort = False
        table = self.query_one(DataTable)
        rows = iter(self.data_in)
        for col_name in next(rows):
            table.add_column(col_name, key=col_name)
        # table.add_columns(*next(rows))
        for row in rows:
            table.add_row(*row, height=ROW_HEIGHT)

    def populate_data(self, data_linker: AudioDataLinker):
        self.data_in = data_linker.data_for_table()
        self.data_linker = data_linker

    def action_play_sound(self):
        if self.selected is not None:
            self.data_linker.play_audio(self.selected)

    def sort_fn(self, col: str):
        rev = False
        if self.current_sort_col == col and not self.reversed_sort:
            rev = True
        self.current_sort_col = col
        self.reversed_sort = rev
        self.query_one(DataTable).sort(col, reverse=rev)

    def action_sort_id(self):
        self.sort_fn('ID')

    def action_sort_wer(self):
        self.sort_fn('WER')

    def action_sort_prob(self):
        self.sort_fn('Average Log Probability')

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
