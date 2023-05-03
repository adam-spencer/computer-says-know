## Presentation Notes

---

### Slide 1: Transcription's Trade-Off Troubles

* There is a trade-off inherent to the task of transcription
* Humans invented language and have been using it for a **LONG** time! In fact, parts of our brain have evolved just to better understand spoken words.
* We're good at understanding spoken words most of the time, but need to listen in real time and may need to listen multiple times before we're sure what's been said.
* Humans need to be paid for their work, thus human transcription is an expensive task when transcribing large quantities of data.
* Computers *can* understand what we tell them nowadays, and do it very quickly without any human oversight!
* Often make errors, especially when given 'noisy' data - i.e. background noise, high level of audio compression (e.g. standard phone lines)

---

### Slide 2: Whisper

* Whisper is a **new** automatic speech recognition model made by OpenAI
* It uses a well-respected model architecture called a *Transformer*
* What makes it stand out is:
    + Supervised training
    + Very large training set (680,000 hrs)
    + Achieves high level of accuracy across many speech corpora (labeled speech datasets)
    + Entirely open-source, meaning it could considerably reduce the cost of automatic transcription when compared to closed-source / paid services. (also I can play around with it without incurring great costs)

---

### Slide 3: Semi-Automatic Transcription

* If automatic transcription is fast but inaccurate
* And manual transcription is accurate but slow
* A solution somewhere inbetween could exploit the speed of automated transcription but use human input to ensure accuracy
* ROC Curve...
* (*show in demo*) if we could rank the ASR output reliably *or* highlight the parts which it is unsure about:
    + human transcriber is required to listen to a smaller subset of the set of audio
    + i.e. more efficient
    + ASR does the heavy lifting

\pagebreak

### Slide 4: Confident Computation

* Whisper finds the most probable sequence of words
* Outputs an average (log) probability for a given input
* If input is split into utterances, each utterance is given a score
* Caveats:
    + This score is just a measure of proximity to a decision boundary - not always indicative of accuracy
    + Due to Whisper being trained on 65% English audio, these errors are much more likely to appear in other languages less prominent in the training set

---

### Slide 5: Results and Conclusions

* Using a conversational corpus, I've found no correlation between this confidence measure and WER, although there are interesting results (TBC in demo)
* WER is flawed!:
    + Even if a word is one letter off, it is treated as a complete error
    + It's not always the case that a spoken word can be coherently matched to text (even by a human)
    + People misspeak - Whisper's language model will correct for this while a human may not - one could argue that this feature is somewhat desirable?
* Sometimes Whisper's hypothesis differs from the human-produced reference, though it **may** be more accurate in some situations? humans **ARE** fallible (i.e. non-zero error rate)
* Whisper is not quite ready to be used to aid transcription, though perhaps modifications could change this - there is literature discussing confidence measures which could be used (though requiring significant modification to the model)
