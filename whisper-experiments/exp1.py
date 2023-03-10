import whisper
import numpy as np
import matplotlib.pyplot as plt
import torch

print("Loading model...")
model = whisper.load_model("base.en")
print("DONE!")

print("Loading audio...")
audio = whisper.load_audio("./audio/ozy.wav")
audio = whisper.pad_or_trim(audio)
print("DONE!")

mel = whisper.log_mel_spectrogram(audio).to(model.device)

options = whisper.DecodingOptions(fp16=False, language="english")

print("Beginning decoding...")
result = whisper.decode(model, mel, options)

print(f"Audio features tensor : \n{result.audio_features}")
print(f"\n\nTokens : \n{result.tokens}")
print(f"\n\nText : \n{result.text}")
print(f"\n\nAvg Logprob : {result.avg_logprob}")
