import json
import sys
import textwrap
from pathlib import Path

import sounddevice as sd
import soundfile as sf
from rich.color import Color
from rich.style import Style
from rich.text import Text

WRAP_WIDTH = 40
BLOCK = '\u2588'  # Block character


class AudioDataLinker:
    """
    Object to aid linking audio and transcript data
    """

    def __init__(self, audio_dir: Path, data_file: Path, confidence_mode: bool,
                 text_blanking: bool = False, blanking_threshold: float = 0.5,
                 text_highlight: bool = False) -> None:
        """
        Create a new AudioDataLinker.

        :param audio_dir: Directory within which audio files are stored.
        :param data_file: File containing transcription data.
        :param confidence_mode: True if confidence scores are being used.
        :param text_blanking: True to enable text blanking mode.
        :param text_highlight: True to enable text highlighting based on confidence.
        """
        with open(data_file) as f:
            self.data = json.load(f)
        self.audio_dir = audio_dir
        self.confidence_mode = confidence_mode
        if text_blanking or text_highlight:
            if text_blanking and text_highlight:
                print('Error! Can\'t blank and highlight at the same time :<')
                sys.exit(1)
            self.text_blanking = text_blanking
            self.blanking_threshold = blanking_threshold
            self.text_highlight = text_highlight
        self.row_data = self.init_row_data()

    def play_audio(self, idx: int) -> bool:
        """
        Play audio correlated with an utterance.

        :param idx: Index of utterance.
        :returns: True if audio file exists, false otherwise.
        """
        audio_file = self.audio_dir / f'{idx:03d}.wav'
        if not audio_file.exists():
            return False
        sd.play(*sf.read(audio_file))

    def init_row_data(self) -> list:
        """
        Get data in format required to be printed in DataTable object.

        :returns: List containing table rows.
        """
        row_data = []
        for idx, utterance in self.data.items():
            kwgs = dict()
            kwgs['idx'] = idx
            kwgs['hyp'] = wrap_and_format(utterance['whisper']['text'])
            kwgs['ref'] = wrap_and_format(utterance['transcript'])
            kwgs['wer'] = utterance['wer']
            if self.confidence_mode:
                kwgs['conf_scoring'] = utterance['confidence_scoring']
            else:
                kwgs['avg_logprob'] = utterance['avg_logprob']
            row = TableRow(self.confidence_mode,
                           self.text_blanking, self.text_highlight,
                           self.blanking_threshold, **kwgs)
            row_data.append(row)
        return row_data

    def data_for_table(self) -> list:
        table_rows = [row.for_table() for row in self.row_data]
        table_rows.insert(0, self.row_data[0].get_header())
        return table_rows


class TableRow:
    """
    Object to represent table row.

    Using OOP simplifies text manipulation in table.
    """

    def __init__(self, confidence_mode: bool, text_blanking: bool = False,
                 text_highlight: bool = False, blanking_threshold: float = 0.5,
                 **kwargs):
        """
        Create a new TableRow.

        :param confidence_mode: True if using confidence mode.
        :param text_blanking: True to enable text blanking.
        :param text_highlight: True to enable text highlighting.
        :param blanking_threshold: Set the confidence threshold to blank text.
        :param kwargs: Data to insert into table. 
            `kwargs` allows different options based on confidence mode.
        """
        self.confidence_mode = confidence_mode
        self.highlight_mode = text_highlight
        self.idx = int(kwargs['idx'])
        self.hyp = kwargs['hyp']
        self.ref = kwargs['ref']
        self.wer = kwargs['wer']
        if confidence_mode:
            conf_scoring = kwargs['conf_scoring']
            scores = conf_scoring['confidence_scores']
            self.token_conf_pair = list(zip(
                conf_scoring['words'].split(), scores))
            if len(scores) > 0:
                self.max_conf = max(scores)
                self.min_conf = min(scores)
            else:
                self.max_conf = 0.0
                self.min_conf = 0.0
            self.utt_conf = conf_scoring['utterance_confidence']
        else:
            self.avg_logprob = kwargs['avg_logprob']

        if text_blanking:
            self.hyp_to_print = wrap_and_format(
                self.text_blanking(blanking_threshold))
        elif text_highlight:
            self.hyp_to_print = self.text_highlighting()
        else:
            self.hyp_to_print = wrap_and_format(self.hyp)

    def for_table(self):
        """Get row data in correct format for insertion into table."""
        if self.confidence_mode:
            return (int(self.idx), self.hyp_to_print, self.ref,
                    float(self.utt_conf), float(self.max_conf),
                    float(self.min_conf), float(self.wer))
        else:
            (int(self.idx), self.hyp_to_print, self.ref, float(
                self.avg_logprob), float(self.wer))

    def get_header(self):
        """Get header row for table."""
        if self.confidence_mode:
            return ['ID', 'Hypothesis', 'Reference',
                    'Utterance Confidence', 'Max Conf.', 'Min Conf.', 'WER']
        else:
            return ['ID', 'Hypothesis', 'Reference',
                    'Average Log Probability', 'WER']

    def text_highlighting(self) -> Text:
        """
        Highlight text based on confidence measure.

        :returns: Text with colour between red and green.
        """
        text_list = []
        for word, conf in self.token_conf_pair:
            text_style = compute_colour(conf)
            # Highlight text and replace underscores with space
            text_obj = Text(word.replace('_', ' '), style=text_style)
            text_list.append(text_obj)
        # Wrap text to be printed properly
        lines = Text(' ').join(text_list).wrap(None, WRAP_WIDTH)
        return Text('\n').join(lines)

    def text_blanking(self, threshold: float) -> str:
        """Blank out text based on confidence threshold."""
        text_list = []
        for word, conf in self.token_conf_pair:
            if conf < threshold:
                # Removes underscores when printing blocks
                for subword in word.split('_'):
                    text_list.append(len(subword) * BLOCK)
            else:
                text_list.append(word)
        return ' '.join(text_list)


def compute_colour(conf: float) -> Style:
    """
    Compute a colour between red and green for highlighting text.

    :param conf: Confidence score between 0 and 1.
    :returns: Style to highlight text with.
    """
    r1, g1, b1 = (255, 0, 0)  # red
    r2, g2, b2 = (0, 255, 0)  # green
    rn, gn, bn = (
        r1 + conf * (r2 - r1),
        g1 + conf * (g2 - g1),
        b1 + conf * (b2 - b1)
    )
    return Style(color=Color.from_rgb(rn, gn, bn))


def wrap_and_format(string: str) -> str:
    """Apply text wrapping to a string and remove underscores."""
    string_no_uscore = string.replace('_', ' ')
    return '\n'.join(textwrap.wrap(string_no_uscore, width=WRAP_WIDTH))
