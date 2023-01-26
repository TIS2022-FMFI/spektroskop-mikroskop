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

        '''sets defoult capturing line to be middle of comarea capture'''
        self.mainLine = self.camera.getCameraHeight() // 2
        self.extraLines = None


    def update_plot(self, frame, line):
        # get the red color values of the first line of the frame
        self.camera.showImage(frame)

        '''set lines range with chack to bounds'''
        if (self.extraLines is None) or (self.extraLines == 0):
            lineFrom = lineTo = self.mainLine
        else:
            lineFrom = max(self.mainLine - self.extraLines, 0)
            lineTo = min(self.mainLine + self.extraLines, self.camera.getCameraHeight())

        if self.camera.chanel == 'r':
            '''number 2 is for second index in GBR frame'''
            redLine = self.avgLines(frame, lineFrom, lineTo, 2)
            line.set_data(range(len(redLine)), redLine)
            line.set_color("red")

        if self.camera.chanel == 'g':
            '''number 0 is for zeroth index in GBR frame'''
            greenLine = self.avgLines(frame, lineFrom, lineTo, 0)
            line.set_data(range(len(greenLine)), greenLine)
            line.set_color("green")

        if self.camera.chanel == 'b':
            '''number 2 is for first index in GBR frame'''
            blueLine = self.avgLines(frame, lineFrom, lineTo, 1)
            line.set_data(range(len(blueLine)), blueLine)
            line.set_color("blue")

        if self.camera.chanel == 'a':
            '''a is for max value from GBR colours'''
            redLine = self.avgLines(frame, lineFrom, lineTo, 2)
            greenLine = self.avgLines(frame, lineFrom, lineTo, 0)
            blueLine = self.avgLines(frame, lineFrom, lineTo, 1)

            maxValue = np.maximum.reduce([redLine, greenLine, blueLine])
            line.set_data(range(len(maxValue)), maxValue)
            line.set_color("black")

    def avgLines(self, frame, lineFrom, lineTo, color=2):
        line = []
        selectedLines = []

        if lineFrom == lineTo:
            line = frame[self.mainLine, :, color]
            return line

        for i in range(lineFrom, lineTo):
            selectedLines.append(frame[i, :, color])
        for i in range(self.camera.getCameraWidht()):
            line.append(np.mean([li[i] for li in selectedLines]))
        return line

    def show_plot(self):
        frame = self.camera.get_frame().__next__()
        red = frame[0, :, 2]

        self.ax.set_xlim([0, self.camera.getCameraWidht()])
        self.ax.set_ylim([0, 300])
        line, = self.ax.plot(red)
        self.ani = FuncAnimation(self.fig, self.update_plot, fargs=(line,), frames=self.camera.get_frame(), interval=10)
        self.start()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def start(self):
        self.t = Thread(target=self.canvas.draw())
        self.t.start()

    def pause(self):
        self.ani.event_source.stop()
        self.camera.pause()

    def resume(self):
        self.ani.event_source.start()
        self.camera.start()

    def release(self):
        self.camera.release()
        self.t.join()

    def initModel(self, model):
        self.model = model
        self.ax.set_xlim(self.model([0, 1280]))

    def initCameraCanvas(self, cameraCanvas):
        self.cameraCanvas = cameraCanvas
        self.label = Label(self.cameraCanvas)
        self.label.pack()

    def setMainLine(self, mainLine):
        self.mainLine = mainLine

    def setExtraLines(self, extraLines):
        self.extraLines = extraLines

    def setExposureTimeForCamera(self, exposureTieme):
        self.camera.setExposureTime(exposureTieme)
