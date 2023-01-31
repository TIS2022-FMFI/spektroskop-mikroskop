import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

x = np.linspace(0, 10, num=100)
y = np.sin(x)
peaks, _ = find_peaks(y)

plt.plot(x, y)
plt.plot(x[peaks], y[peaks], "x")

peak_labels = [f"Peak {i}: x={x[peak]:.2f}, y={y[peak]:.2f}" for i, peak in enumerate(peaks)]
plt.text(np.repeat(x[peaks], 2), np.repeat(y[peaks], 2), peak_labels,
         ha="center", va="bottom", fontsize=9, transform=plt.gca().transData)

plt.show()
