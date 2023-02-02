import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = [1,2,3,4,5,6,7,8,9,10]
y = [2,3,4,5,1,6,2,1,7,2]
z = [1,2,6,3,2,7,3,3,7,2]

ax.scatter(x, y, z)

plt.show()