import cv2
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from camera.Camera import Camera
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class Plot:
    def __init__(self, canvas, camera=Camera(1)):
        self.root = canvas
        self.camera = camera

    def update_plot(self, frame, line):
        # get the red color values of the first line of the frame
        if self.camera.chanel == 'r':
            # red_line = frame[250,:,2]
            red_line = self.avgLines(frame, 0, 640, 2)
            line.set_data(range(len(red_line)), red_line)
            line.set_color("red")
        if self.camera.chanel == 'g':
            green_line = frame[250, :, 0]
            line.set_data(range(len(green_line)), green_line)
            line.set_color("green")
        if self.camera.chanel == 'b':
            blue_line = frame[250, :, 1]
            line.set_data(range(len(blue_line)), blue_line)
            line.set_color("blue")
        if self.camera.chanel == 'a':
            # a for all (max of r, g, b)
            max_value = np.maximum(np.maximum(frame[250, :, 0], frame[250, :, 1]), frame[250, :, 2])
            line.set_data(range(len(max_value)), max_value)
            line.set_color("black")

    def avgLines(self, frame, lineFrom, lineTo, color=2):
        line = []
        selectedLines = []
        for i in range(lineFrom, lineTo):
            selectedLines.append(frame[i, :, color])
        for i in range(1280):
            line.append(np.mean([li[i] for li in selectedLines]))
        return line

    def show_plot(self):
        frame = self.camera.get_frame().__next__()
        red = frame[0, :, 2]
        fig, ax = plt.subplots()
        ax.set_xlim([0, 1280])
        ax.set_ylim([0, 256])
        # ax.autoscale(enable=True, axis='both', tight=None)
        line, = ax.plot(red)
        ani = FuncAnimation(fig, self.update_plot, fargs=(line,), frames=self.camera.get_frame(), interval=10)
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        # self.canvas = canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # plt.show()

    def pause(self):
        self.camera.pause()

    def start(self):
        self.camera.start()


# ih = Plot()
# ih.show_plot()
# ih.camera.release()
# cv2.destroyAllWindows()
