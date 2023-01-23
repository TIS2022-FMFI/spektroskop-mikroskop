from threading import Thread
import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from camera.Camera import Camera
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class Plot:
    def __init__(self, canvas, camera=Camera(1)):
        self.fig, self.ax = plt.subplots()
        self.camera = camera
        self.t = None
        self.isPaused = False
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas)
        self.ani = None
        self.cameraCanvas = None
        self.label = None

        self.model = None

    def initModel(self, model):
        self.model = model

    def initCameraCanvas(self, cameraCanvas):
        self.cameraCanvas = cameraCanvas
        self.label = Label(self.cameraCanvas)
        self.label.pack()

    def start(self):
        self.t = Thread(target=self.canvas.draw())
        self.t.start()

    def pause(self):
        self.ani.event_source.stop()
        self.camera.pause()

    def resume(self):
        self.ani.event_source.start()
        self.camera.start()

    def update_plot(self, frame, line):
        # get the red color values of the first line of the frame
        self.camera.showImage(frame)
        if self.camera.chanel == 'r':
            # red_line = frame[250,:,2]
            if self.model:
                red_line = self.model(self.avgLines(frame, 0, 640, 2))
            else:
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
            if self.model:
                max_value = self.model(np.maximum(np.maximum(frame[250, :, 0], frame[250, :, 1]), frame[250, :, 2]))
            else:
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
        self.ax.set_xlim([0, 1280])
        self.ax.set_ylim([0, 1000])
        line, = self.ax.plot(red)
        self.ani = FuncAnimation(self.fig, self.update_plot, fargs=(line,), frames=self.camera.get_frame(), interval=10)
        self.start()

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
