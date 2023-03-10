# Meeting Notes, March 9th

---
## Questions

* Ask for some help with the writeup:
  + What is expected of me in the literature review - what I previously produced wasn't sufficient; what is?
  + The 'Analysis' stage; how does this differ from the 'Design' and lit review chapters?
  + What are 'coding traps'?
* LifeLUCID dataset (from V.Hazan) is conversational
  + I've made a Python script to find and seperate utterances from transcript
  + Need advice - using SoX to produce utterance segments; how? in shell script?
  + To what extent is code included in the dissertation? As I writing these tools towards the project myself are they worth something? Or is the focus solely on what they produce?
* Recommendations for further conversational corpora, as were mentioned in prev meeting
* Please share code with me! If this isn't possible, perhaps point me towards useful libraries :)
* Where should I focus? Some statistical analysis was discussed, but I'm sure producing some semi-auto tool is integral to producing my own data- what does JB think?

---
## Notes

* Praat may have some interesting tools along with it
* python to cut out segments
* speaker-dependent analysis is possible using speaker metadata
* mapping from avg logprob to n errors
* learn from temp and logprob how many errors are made:
  + generalise to other speakers
  + train on half data from one speaker, test on other half
  + predict errors using ^^
* evaluate in different modes:
  + can learn on one set and predict on another set?
  + lobprob + fitting function to map to correctness (simple)
  + neural network with 2 input nodes? (more complex)
  + hidden representations from whisper
* end-to-end trained on text mapping; audio -> text tokens
* look at pre-transformed tokens, may see some more insight
* hidden representations may map to confidence

* Nothing is too trivial to include as long is it is organised
* Be as complete as possible
* Discussion about file format, how the data looks and how it is transformed
* Look at different estimators
* well-motivated, clear, good understanding, clear results
* NOT LIKE A CONCISE RESEARCH PAPER
