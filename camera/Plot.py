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

        self.showWavelengt = False
        self.model = None

        '''sets defoult capturing line to be middle of comarea capture'''
        self.mainLine = self.camera.getCameraHeight() // 2
        self.lineFrom = None
        self.lineTo = None

        self.doDivison = False
        self.doSubtraction = False

        self.referenceData = None

    def update_plot(self, frame, line):
        # get the red color values of the first line of the frame
        self.camera.showImage(frame)

        if self.camera.chanel == 'r':
            '''number 2 is for second index in GBR frame'''
            redLine = self.getRedLine(frame)
            line.set_data(range(len(redLine)), redLine)
            line.set_color("red")

        if self.camera.chanel == 'g':
            '''number 0 is for zeroth index in GBR frame'''
            greenLine = self.getGreenLine(frame)
            line.set_data(range(len(greenLine)), greenLine)
            line.set_color("green")

        if self.camera.chanel == 'b':
            '''number 2 is for first index in GBR frame'''
            blueLine = self.getBlueLine(frame)
            line.set_data(range(len(blueLine)), blueLine)
            line.set_color("blue")

        if self.camera.chanel == 'a':
            '''a is for max value from GBR colours'''
            maxValue = self.getMaxLine(frame)
            if self.doSubtraction:
                subtractedLine = np.subtract(maxValue, self.referenceData).astype(np.int8)
                self.ax.set_ylim([min(subtractedLine), max(subtractedLine)])
                line.set_data(range(len(subtractedLine)), subtractedLine)
            elif self.doDivison:
                dividedLine = np.divide(maxValue, self.referenceData)
                self.ax.set_ylim([min(dividedLine), max(dividedLine)])
                line.set_data(range(len(dividedLine)), dividedLine)
            else:
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
        self.ani = FuncAnimation(self.fig, self.update_plot, fargs=(line,), frames=self.camera.get_frame(), interval=100)
        self.start()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def showPixelView(self):
        self.ax.set_xlim([0, self.camera.getCameraWidht()])

    def showWavelengthView(self):
        if self.model:
            self.ax.set_xlim(self.model([0, 1280]))

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

    def initCameraCanvas(self, cameraCanvas):
        self.cameraCanvas = cameraCanvas
        self.label = Label(self.cameraCanvas)
        self.label.pack()

    def getRedLine(self, frame):
        return self.avgLines(frame, self.lineFrom, self.lineTo, 2)

    def getGreenLine(self, frame):
        return self.avgLines(frame, self.lineFrom, self.lineTo, 0)

    def getBlueLine(self, frame):
        return self.avgLines(frame, self.lineFrom, self.lineTo, 1)

    def getMaxLine(self, frame):
        redLine = self.getRedLine(frame)
        greenLine = self.getGreenLine(frame)
        blueLine = self.getBlueLine(frame)
        return np.maximum.reduce([redLine, greenLine, blueLine])

    def setMainLine(self, mainLine):
        self.mainLine = mainLine

    def setExtraLines(self, extraLines):

        """set lines range with chack to bounds"""
        if (extraLines is None) or (extraLines == 0):
            self.lineFrom = self.lineTo = self.mainLine
        else:
            self.lineFrom = max(self.mainLine - extraLines, 0)
            self.lineTo = min(self.mainLine + extraLines, self.camera.getCameraHeight())

    def setExposureTimeForCamera(self, exposureTieme):
        self.camera.setExposureTime(exposureTieme)

    def setReferenceData(self):
        self.referenceData = self.getMaxLine(self.camera.get_frame().__next__())
        print(self.referenceData)

    def setSubstraction(self):
        self.doSubtraction = True
        self.doDivison = False

    def setDivision(self):
        self.doDivison = True
        self.doSubtraction = False

