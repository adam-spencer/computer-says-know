# Notes

---

## 15 April

I've added all the hesitation tokens (as defined in the documentation) `src/get_utterances` as extra junk tokens.
This should mean that hesitations aren't present in the reference transcripts anymore.

I could, however, make direct edits to the output of Whisper rather than doing this all over again.
The transcripts are all already done, it's just the WER calculations that need this!

TODO:
* Should edit `src/calculate_wer` to calculate other measures that `jiwer` allows:
    + Be mindful that CER will include spaces in the calculation. May be worth some kind of normalisation to remove spaces.
* Add removal of hesitation tokens to `src/normalise_text`

---
