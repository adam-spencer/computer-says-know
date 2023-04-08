import numpy as np
import sounddevice as sd
import soundfile as sf
import sys

if len(sys.argv) != 2:
  print(f'Test `sounddevice` lib. Usage: {sys.argv[0]} filename.wav')
  sys.exit(-1)

sd.play(*sf.read(sys.argv[1]))
sd.wait()
