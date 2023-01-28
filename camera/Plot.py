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
        plt.style.use('ggplot')
        self.fig, self.ax = plt.subplots()
        self.xLimValues = range(0, 1280)

        self.camera = camera
        self.t = None
        self.t2 = None
        self.isPaused = False
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas)
        self.ani = None
        self.cameraCanvas = None
        self.label = None
        self.slider = -5

        self.camera.initPlot(self)

        self.showWavelengt = False
        self.model = None

        '''sets defoult capturing line to be middle of comarea capture'''
        self.mainLine = self.camera.getCameraHeight() // 2
        self.lineFrom = None
        self.lineTo = None

        self.doDivison = False
        self.doSubtraction = False

        self.referenceData = None

        self.showRedLine = False
        self.showGreenLine = False
        self.showBlueLine = False
        self.showMaxLine = True

    # TODO extrahovat duplicity do metody?
    def updatePlot(self, frame):
        # get the red color values of the first line of the frame
        # self.startT2(frame)
        self.camera.showImage(frame)
        self.ax.clear()
        self.ax.use_sticky_edges = True
        self.ax.margins(x=0)

        if self.showRedLine:
            redLine = self.getRedLine(frame)
            colorLine = "red"

            if self.doSubtraction:
                subtractedLine = self.subtractActualFromReference(redLine)
                self.ax.plot(self.xLimValues, subtractedLine, color=colorLine)
            elif self.doDivison:
                dividedLine = self.divideActualFromReference(redLine)
                self.ax.plot(self.xLimValues, dividedLine, color=colorLine)
            else:
                self.ax.plot(self.xLimValues, redLine, color=colorLine)

        if self.showGreenLine:
            greenLine = self.getGreenLine(frame)
            colorLine = "green"

            if self.doSubtraction:
                subtractedLine = self.subtractActualFromReference(greenLine)
                self.ax.plot(self.xLimValues, subtractedLine, color=colorLine)
            elif self.doDivison:
                dividedLine = self.divideActualFromReference(greenLine)
                self.ax.plot(self.xLimValues, dividedLine, color=colorLine)
            else:
                self.ax.plot(self.xLimValues, greenLine, color=colorLine)

        if self.showBlueLine:
            blueLine = self.getBlueLine(frame)
            colorLine = "blue"

            if self.doSubtraction:
                subtractedLine = self.subtractActualFromReference(blueLine)
                self.ax.plot(self.xLimValues, subtractedLine, color=colorLine)
            elif self.doDivison:
                dividedLine = self.divideActualFromReference(blueLine)
                self.ax.plot(self.xLimValues, dividedLine, color=colorLine)
            else:
                self.ax.plot(self.xLimValues, blueLine, color=colorLine)

        if self.showMaxLine:
            maxValue = self.getMaxLine(frame)
            colorLine = "black"

            if self.doSubtraction:
                subtractedLine = self.subtractActualFromReference(maxValue)
                self.ax.plot(self.xLimValues, subtractedLine, color=colorLine)
            elif self.doDivison:
                dividedLine = self.divideActualFromReference(maxValue)
                self.ax.plot(self.xLimValues, dividedLine, color=colorLine)
            else:
                self.ax.plot(self.xLimValues, maxValue, color=colorLine)

    def avgLines(self, frame, lineFrom, lineTo, color=2):
        if lineFrom == lineTo:
            line = frame[self.mainLine, :, color]
            return line

        selectedLines = frame[lineFrom:lineTo, :, color]
        line = np.mean(selectedLines, axis=0)

        return line

    def show_plot(self):
        # self.startT2(self.camera.get_frame().__next__())
        self.ani = FuncAnimation(self.fig, self.updatePlot, frames=self.camera.get_frame(), interval=100)
        self.start()
        # self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def subtractActualFromReference(self, actual):
        return np.subtract(actual, self.referenceData).astype(np.int8)

    def divideActualFromReference(self, actual):
        dividedLine = np.divide(actual, self.referenceData)
        """ replace Inf and NaN values with 1"""
        np.place(dividedLine, np.isinf(dividedLine) | np.isnan(dividedLine), 1)
        return dividedLine

    def showPixelView(self):
        self.xLimValues = range(0, 1280)
        # self.ax.set_xlim([0, self.camera.getCameraWidht()])

    def showWavelengthView(self):
        if self.model:
            self.xLimValues = self.model(self.xLimValues)

    def start(self):
        self.t = Thread(target=self.canvas.draw())
        self.t.start()

    def startT2(self, initFrame):
        self.t2 = Thread(target=self.camera.showImage(initFrame))
        self.t2.start()

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

    def initExposureTimeSlider(self, slider):
        self.slider = slider

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
            self.camera.setExtraLines(self.mainLine, 0)
        else:
            self.lineFrom = max(self.mainLine - extraLines, 0)
            self.lineTo = min(self.mainLine + extraLines, self.camera.getCameraHeight())
            self.camera.setExtraLines(self.mainLine, extraLines)

    def setExposureTimeForCamera(self, exposureTieme):
        self.camera.setExposureTime(exposureTieme)

    def setReferenceData(self):
        self.referenceData = self.getMaxLine(self.camera.get_frame().__next__())
        """change value of 0 in reference data with 1
            for reason of dividing by 0 """
        # self.referenceData = np.where(self.referenceData == 0, 1, self.referenceData)
        print(self.referenceData)

    def setSubstraction(self):
        self.doSubtraction = True
        self.doDivison = False

    def setDivision(self):
        self.doDivison = True
        self.doSubtraction = False

    def setShowRedLine(self, value):
        if value == 1:
            self.showRedLine = True
        else:
            self.showRedLine = False

    def setShowGreenLine(self, value):
        if value == 1:
            self.showGreenLine = True
        else:
            self.showGreenLine = False

    def setShowBlueLine(self, value):
        if value == 1:
            self.showBlueLine = True
        else:
            self.showBlueLine = False

    def setShowMaxLine(self, value):
        if value == 1:
            self.showMaxLine = True
        else:
            self.showMaxLine = False