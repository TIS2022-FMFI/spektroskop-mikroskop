import matplotlib.pyplot as plt

# Create multiple plots
fig1, ax1 = plt.subplots()
ax1.plot([1, 2, 3, 4], [1, 4, 9, 16], 'r-o')
ax1.set_title("First Plot")

fig2, ax2 = plt.subplots()
ax2.plot([1, 2, 3, 4], [2, 8, 18, 32], 'b-o')
ax2.set_title("Second Plot")

fig3, ax3 = plt.subplots()
ax3.plot([1, 2, 3, 4], [3, 6, 12, 24], 'g-o')
ax3.set_title("Third Plot")

# Show a specific plot
fig2.show()
