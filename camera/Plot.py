from threading import Thread
import tkinter as tk
from threading import Thread
from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from camera.Camera import Camera
from camera.FrameUtilMethods import FrameUtilMethods


class Plot:
    def __init__(self, canvas, camera=Camera(1)):
        plt.style.use('ggplot')
        self.fig, self.ax = plt.subplots()
        self.xLimValues = range(0, 1280)
        self.fig.tight_layout()

        self.camera = camera
        self.t = None
        self.t2 = None
        self.isPaused = False
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas)
        self.ani = None
        self.cameraCanvas = None
        self.label = None
        self.slider = -5

        # self.camera.initPlot(self)

        self.showWavelengt = False
        self.model = None

        '''sets defoult capturing line to be middle of comarea capture'''
        # self.mainLine = self.camera.getCameraHeight() // 2
        self.mainLine = 100
        self.lineFrom = None
        self.lineTo = None

        self.doDivison = False
        self.doSubtraction = False

        self.referenceData = None

        self.showRedLine = False
        self.showGreenLine = False
        self.showBlueLine = False
        self.showMaxLine = True

        self.frameUtils = FrameUtilMethods(lineFrom=self.lineFrom, lineTo=self.lineTo, mainLine=self.mainLine)

    # TODO extrahovat duplicity do metody?
    def updatePlot(self, frame):
        # get the red color values of the first line of the frame
        # self.startT2(frame)
        self.camera.showImage(frame)
        self.ax.clear()
        self.ax.use_sticky_edges = True
        self.ax.margins(x=0)

        self.frameUtils.setFrame(frame)

        if self.showRedLine:
            redLine = self.frameUtils.getRedLine()
            colorLine = "red"
            self.performOperations(redLine, colorLine)

            # TODO consult with Vojtek it has fuctionality for showing peaks

            # red_peaks_indices, _ = find_peaks(redLine, distance=10)
            # red_peaks_indices.astype(np.int8)
            #
            #
            # for x, y in zip(red_peaks_indices, redLine[red_peaks_indices]):
            #     # self.ax.plot(x, y, 'k', linestyle='dashed', linewidth=1, alpha=0.7)
            #     self.ax.vlines(x=x, ymin=min(redLine), ymax=y, colors='purple', linestyles='dashed')
            #     self.ax.annotate(str(y), (x, y * 1.025))

        if self.showGreenLine:
            greenLine = self.frameUtils.getGreenLine()
            colorLine = "green"
            self.performOperations(greenLine, colorLine)

        if self.showBlueLine:
            blueLine = self.frameUtils.getBlueLine()
            colorLine = "blue"
            self.performOperations(blueLine, colorLine)

        if self.showMaxLine:
            maxValue = self.frameUtils.getMaxLine()
            colorLine = "black"
            self.performOperations(maxValue, colorLine)

    def performOperations(self, line, colorLine):
        try:
            if self.doSubtraction:
                subtractedLine = self.frameUtils.subtractLines(line)
                self.ax.plot(self.xLimValues, subtractedLine, color=colorLine)
            elif self.doDivison:
                dividedLine = self.frameUtils.divdeLines(line)
                self.ax.plot(self.xLimValues, dividedLine, color=colorLine)
            else:
                self.ax.plot(self.xLimValues, line, color=colorLine)
        except ValueError:
            self.ax.plot(self.xLimValues, line, color=colorLine)

    def drawCaary(self, cary, peeky):
        for x, y in zip(peeky, cary[peeky]):
            # self.ax.plot(x, y, 'k', linestyle='dashed', linewidth=1, alpha=0.7)
            self.ax.vlines(x=x, ymin=min(cary), ymax=y, colors='purple', linestyles='dashed')
            self.ax.annotate(str(y), (x, y * 1.025))

    def show_plot(self):
        # self.startT2(self.camera.get_frame().__next__())
        self.ani = FuncAnimation(self.fig, self.updatePlot, frames=self.camera.get_frame(), interval=1)
        self.start()
        # self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

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
        self.t2 = Thread(target=self.frameUtils.getRedLine())
        self.t2.start()

    def pause(self):
        self.ani.event_source.stop()
        self.camera.pause()

    def resume(self):
        if not self.isPaused:
            self.show_plot()
            self.camera.start()
        else:
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

    def setMainLine(self, mainLine):
        self.mainLine = mainLine
        self.frameUtils.setMainLine(mainLine)

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
        self.frameUtils.setFrame(self.camera.get_frame().__next__())
        self.referenceData = self.frameUtils.getMaxLine()
        self.frameUtils.setReferenceData(self.referenceData)

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