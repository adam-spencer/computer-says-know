import json
import textwrap
from pathlib import Path

import sounddevice as sd
import soundfile as sf

WRAP_WIDTH = 40


class AudioDataLinker:
    """
    Object to aid linking audio and transcript data
    """

    def __init__(self, audio_dir: Path, data_file: Path, confidence_mode: bool) -> None:
        """
        Create a new AudioDataLinker.

        :param audio_dir: Directory within which audio files are stored.
        :param data_file: File containing transcription data.
        """
        with open(data_file) as f:
            self.data = json.load(f)
        self.audio_dir = audio_dir
        self.confidence_mode = confidence_mode
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
            kwgs['hyp'] = wrap(utterance['whisper']['text'])
            kwgs['ref'] = wrap(utterance['transcript'])
            kwgs['wer'] = utterance['wer']
            if self.confidence_mode:
                # TODO:
                #  * Do some text highlighting thing?
                #  * Blanking out of text below threshold?
                #  * (in other file) sort on confidence measures
                kwgs['conf_scoring'] = utterance['confidence_scoring']
            else:
                kwgs['avg_logprob'] = utterance['avg_logprob']
            row = TableRow(self.confidence_mode, **kwgs)
            row_data.append(row)
        return row_data

    def data_for_table(self) -> list:
        table_rows = [row.for_table() for row in self.row_data]
        table_rows.insert(0, self.row_data[0].get_header())
        return table_rows


class TableRow:
    def __init__(self, confidence_mode: bool, **kwargs):
        self.confidence_mode = confidence_mode
        self.idx = int(kwargs['idx'])
        self.hyp = kwargs['hyp']
        self.ref = kwargs['ref']
        self.wer = kwargs['wer']
        if confidence_mode:
            conf_scoring = kwargs['conf_scoring']
            scores = conf_scoring['confidence_scores']
            self.token_conf_pair = list(zip(
                conf_scoring['words'].split(), scores))
            self.max_conf = max(scores)
            self.min_conf = min(scores)
            self.utt_conf = conf_scoring['utterance']
        else:
            self.avg_logprob = kwargs['avg_logprob']

    def for_table(self):
        if self.confidence_mode:
            return (int(self.idx), self.hyp, self.ref, float(self.utt_conf),
                    float(self.max_conf), float(self.min_conf), float(self.wer))

    def get_header(self):
        if self.confidence_mode:
            return [('ID', 'Hypothesis', 'Reference',
                           'Utterance Confidence', 'Max Conf.', 'Min Conf.', 'WER')]
        else:
            return [('ID', 'Hypothesis', 'Reference',
                           'Average Log Probability', 'WER')]


def wrap(string: str) -> str:
    """
    Apply text wrapping to a string.
    """
    return '\n'.join(textwrap.wrap(string, width=WRAP_WIDTH))
