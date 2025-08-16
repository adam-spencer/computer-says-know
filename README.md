# Computer Says 'Know': ASR Confidence and Transcription

This was my undergraduate dissertation project as part of BSc Artificial Intelligence and Computer Science at the University of Sheffield, for which I recieved a 2.1 Hons and this project was given a mark of 69.

**This project is not meant to be run by strangers** as it misses the data I used to create transcriptions.

The objective of the project was to test the ability of an open-source automatic speech recognition (ASR) tool to improve the performance of a human transcriber.
The tool used was *OpenAI Whisper* which was brand new when my project began.

## `asr-app`

This directory contains the ASR app built as part of the project, it's pretty simple and uses the `Textual` library to make a polished-looking UI.

The app functions to allow a user to list, edit, organise, and highlight the ASR-produced transcription text.
Each token is given a confidence score which is aligned with the words in what is displayed here.

The user can change highlighting and ordering based on the confidence scores for statements, sentences, and individual words.

## `lifeLUCID/src`

This directory contains scripts used in data processing and the production of transcriptions.
The old university HPC system (Bessemer) was used to run these scripts and produce transcriptions.
