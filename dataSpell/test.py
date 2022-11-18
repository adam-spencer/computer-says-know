import matplotlib.pyplot as plt
import numpy as np

f = 20  # Hz
t = np.linspace(0, 0.5, num=600)
data = np.sin(2 * np.pi * f * t)

plt.plot(t, data)
plt.xlabel("Time (s)")
plt.ylabel("x(t)")
plt.title("Epic plot!!!")
