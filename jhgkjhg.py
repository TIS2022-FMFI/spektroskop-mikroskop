# Import Library

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create figure and subplot

figure, ax = plt.subplots(figsize=(4,3))

x = []
y = []

# Plot

plot_1, = ax.plot(x, y)
plt.axis([0, 30, -2, 2])

# Animation Function

def animate_plot (i):
    x = np.linspace(0, 30, 100)
    y = np.tan(6 * (x - 0.3 * i))
    plot_1.set_data(x, y)
    return plot_1,

# Animated Function

ani = FuncAnimation(figure,
                    animate_plot,
                    frames=3,
                    interval=100)

# Save as gif

ani.save('animation.gif', fps=10)

# Display

plt.show()