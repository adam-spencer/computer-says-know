import cmd
import shutil
from pathlib import Path

from audio_data_link import AudioDataLinker
from textual.app import App, ComposeResult
from textual.coordinate import Coordinate
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
        ('u', 'sort_utt_conf', 'Sort Utterance Conf'),
        ('>', 'sort_max_conf', 'Sort Max Conf.'),
        ('<', 'sort_min_conf', 'Sort Min Conf.'),
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
        for row in rows:
            table.add_row(*row, height=ROW_HEIGHT)

    def populate_data(self, data_linker: AudioDataLinker):
        self.data_in = data_linker.data_for_table()
        self.data_linker = data_linker

    def action_play_sound(self):
        if self.selected_idx is not None:
            self.data_linker.play_audio(self.selected_idx)

    def sort_fn(self, col: str):
        rev = False
        if self.current_sort_col == col and not self.reversed_sort:
            rev = True
        self.current_sort_col = col
        self.reversed_sort = rev
        dt = self.query_one(DataTable)
        dt.sort(col, reverse=rev)

    def action_sort_id(self):
        self.sort_fn('ID')

    def action_sort_wer(self):
        self.sort_fn('WER')

    def action_sort_prob(self):
        if not self.data_linker.confidence_mode:
            self.sort_fn('Average Log Probability')

    def action_sort_utt_conf(self):
        if self.data_linker.confidence_mode:
            self.sort_fn('Utterance Confidence')

    def action_sort_max_conf(self):
        if self.data_linker.confidence_mode:
            self.sort_fn('Max Conf.')

    def action_sort_min_conf(self):
        if self.data_linker.confidence_mode:
            self.sort_fn('Min Conf.')

    def on_data_table_cell_highlighted(self, message: DataTable.CellHighlighted):
        row_num = message.coordinate.row
        idx_coord = Coordinate(row_num, 0)
        self.selected_idx = self.query_one(DataTable).get_cell_at(idx_coord)


def launcher() -> (Path, Path, bool, bool, bool):
    """
    Launcher for my ASR App!

    In order for this to work, asr_app.py must be run from the `asr-app/src`
    directory.

    It will open up a list of conversatiosn to choose from, take a user's input
    as a number corresponding to a conversation and then the app will launch.

    :returns: something...
    """
    print("Would you like to use data with confidence scores? [y/n]")
    use_confidence_inp = input("\n-> ")
    use_confidence = False
    text_highlight = False
    text_blanking = False
    if use_confidence_inp.lower() == 'y':
        use_confidence = True
        print('\nWould you like to use text blanking, highlighting, or neither?'
              + '[b/h/n]\n')
        conf_opt = input('-> ').lower()
        if conf_opt == 'b':
            text_blanking = True
        elif conf_opt == 'h':
            text_highlight = True

    data_path = Path('../data')
    if use_confidence:
        asr_data_path = data_path / 'confidence-data'
    else:
        asr_data_path = data_path / 'asr-out'
    audio_dirs_list = sorted(
        [i for i in (data_path / 'audio').iterdir() if i.is_dir()])

    # Present the conversations by code and allow the user to choose
    convos = [f'{idx:2} : {d.name} ' for idx, d in enumerate(audio_dirs_list)]
    cli = cmd.Cmd()
    print('\nChoose a conversation:\n')
    cli.columnize(convos, displaywidth=shutil.get_terminal_size().columns)
    chosen_audio = audio_dirs_list[int(input('\n-> '))]

    # Find the data file corresponding to the chosen conversation
    chosen_data = None
    for f in asr_data_path.iterdir():
        if chosen_audio.name in f.name:
            chosen_data = f
    if chosen_data:
        return (chosen_data, chosen_audio, use_confidence,
                text_blanking, text_highlight)
    raise IndexError('Can\'t find data for selected conversation')


if __name__ == "__main__":
    data_file, audio_dir, confidence_mode, text_blanking, text_highlight = launcher()
    data_linker = AudioDataLinker(
        audio_dir, data_file, confidence_mode, text_blanking, text_highlight)
    app = TranscriptionApp()
    app.populate_data(data_linker)
    app.run()
