import matplotlib.pyplot as plt
from CameraUtils import CameraUtils
import matplotlib.animation as animation

class Plot:

    def __init__(self, yos=None):
        if yos is None:
            yos = list(range(0, 640))
        self.xos = []
        self.yos = yos
        self.fig = plt.figure()
        self.ax = self.fig.add_sub(1,1,1)


    def updateY(self, yos):
        self.yos = yos

    def animate(self, frame):
        self.ax.cler()
        self.yos = frame[:,:, 1][0]
        self.ax.plot(self.xos, self.yos)

    def getFig(self):
        return self.fig


if __name__ == '__main__':
    cam = CameraUtils()
    cam.start()

    plot = Plot()
    animation.FuncAnimation(plot.getFig(), plot.animate, interval=100)
    plot.animate(cam.getFrame())
    plt.show()