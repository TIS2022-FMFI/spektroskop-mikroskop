import time
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
    def __init__(self, canvas, camera=Camera(0)):
        plt.style.use('ggplot')
        self.fig, self.ax = plt.subplots()
        self.redLine, = self.ax.plot([], [], "red")
        self.greenLine, = self.ax.plot([], [], "green")
        self.blueLine, = self.ax.plot([], [], "blue")
        self.maxLine, = self.ax.plot([], [], "black")
        self.xLimValues = range(0, 1280)
        self.yMin = 255
        self.yMax = 0
        # self.fig.tight_layout()
        self.ax.use_sticky_edges = True

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
        """ method for updating graph data """

        self.camera.showImage(frame)     # this metod is slowing process significantly the most,
        # problem is to process image from cv2 camera to format used for canvas process

        self.frameUtils.setFrame(frame)

        if self.showRedLine:
            redLine = self.frameUtils.getRedLine()
            self.performOperations(self.redLine, redLine)
            # colorLine = "red"
            # self.performOperations(redLine, colorLine)

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
            self.performOperations(self.greenLine, greenLine)

        if self.showBlueLine:
            blueLine = self.frameUtils.getBlueLine()
            self.performOperations(self.blueLine, blueLine)

        if self.showMaxLine:
            maxValue = self.frameUtils.getMaxLine()
            self.performOperations(self.maxLine, maxValue)

        self.selectMinMax()
        if self.yMin < 0:
            self.yMin *= 1.05
        else:
            self.yMin *= 0.95

        if self.yMax < 0:
            self.yMax *= 0.95
        else:
            self.yMax *= 1.05

        self.ax.set_ylim(self.yMin, self.yMax)
        # self.t2.join()

    def performOperations(self, desiredLine, newLine):
        """ performs operation over grpah data and updates graph lines """
        try:
            if self.doSubtraction:
                subtractedLine = self.frameUtils.subtractLines(newLine)
                self.ax.set_xlim([min(self.xLimValues), max(self.xLimValues)])
                desiredLine.set_data(self.xLimValues, subtractedLine)
            elif self.doDivison:
                dividedLine = self.frameUtils.divdeLines(newLine)
                self.ax.set_xlim([min(self.xLimValues), max(self.xLimValues)])
                desiredLine.set_data(self.xLimValues, dividedLine)
            else:
                self.ax.set_xlim([min(self.xLimValues), max(self.xLimValues)])
                desiredLine.set_data(newLine)
        except ValueError:
            desiredLine.set_data(self.xLimValues, newLine)

    def drawCaary(self, cary, peeky):
        for x, y in zip(peeky, cary[peeky]):
            # self.ax.plot(x, y, 'k', linestyle='dashed', linewidth=1, alpha=0.7)
            self.ax.vlines(x=x, ymin=min(cary), ymax=y, colors='purple', linestyles='dashed')
            self.ax.annotate(str(y), (x, y * 1.025))

    def show_plot(self):
        """ main fuction to call for graph displaying """
        # self.startT2(self.camera.get_frame().__next__())
        self.ani = FuncAnimation(self.fig, self.updatePlot, frames=self.camera.get_frame(), interval=0.1)
        self.start()
        # self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def showPixelView(self):
        """ sets pixel view """
        self.xLimValues = range(0, self.camera.getCameraWidht())
        # self.ax.set_xlim([0, self.camera.getCameraWidht()])

    def showWavelengthView(self):
        """ sets wavelengt view """
        if self.model:
            self.xLimValues = self.model(self.xLimValues)

    def start(self):
        self.t = Thread(target=self.canvas.draw())
        self.t.start()

    def startT2(self, frame):
        self.t2 = Thread(target=self.updatePlot, args=(frame, ))
        self.t2.start()

    def pause(self):
        if self.ani is not None:
            self.ani.event_source.stop()
        if self.camera is not None:
            self.camera.pause()

    def resume(self):
        if not self.isPaused:
            self.camera.start()
            self.show_plot()
        else:
            self.ani.event_source.start()
            self.camera.start()

    def release(self):
        """ stops graph animation and releases camera """
        if self.ani is not None:
            self.ani.event_source.stop()
        if self.camera is not None:
            self.camera.release()
        if self.t is not None:
            self.t.join()

    def initModel(self, model):
        """ initialise model for calculating wavelengt """
        self.model = model

    def initCameraCanvas(self, cameraCanvas):
        """ initialise canvas for camera image showing """
        self.cameraCanvas = cameraCanvas
        self.label = Label(self.cameraCanvas)
        self.label.pack()

    def initExposureTimeSlider(self, slider):
        """ initialise slider for camera showing frame """
        self.slider = slider

    def setMainLine(self, mainLine):
        """ sets the main(middle) line of frame where are data are taken from """
        self.mainLine = mainLine
        self.frameUtils.setMainLine(mainLine)

    def setExtraLines(self, extraLines):

        """set lines range with chack to bounds"""
        if (extraLines is None) or (extraLines == 0):
            self.lineFrom = self.lineTo = self.mainLine
            self.camera.setExtraLines(self.mainLine, 0)
            self.frameUtils.setLinesFromTo(self.lineFrom, self.lineTo)
        else:
            self.lineFrom = max(self.mainLine - extraLines, 0)
            self.lineTo = min(self.mainLine + extraLines, self.camera.getCameraHeight())
            self.camera.setExtraLines(self.mainLine, extraLines)
            self.frameUtils.setLinesFromTo(self.lineFrom, self.lineTo)

    def setExposureTimeForCamera(self, exposureTieme):
        """ sets exposure time of camera """
        self.camera.setExposureTime(exposureTieme)

    def setReferenceData(self):
        """ sets reference data for subtraction and division """
        self.frameUtils.setFrame(self.camera.get_frame().__next__())
        self.referenceData = self.frameUtils.getMaxLine()
        self.frameUtils.setReferenceData(self.referenceData)

    def setSubstraction(self):
        """ sets whether to do subtraction over graph """
        self.doSubtraction = True
        self.doDivison = False

    def setDivision(self):
        """ sets whether to do division over graph """
        self.doDivison = True
        self.doSubtraction = False

    def setShowRedLine(self, value):
        """ sets whether to show redLine """
        if value == 1:
            self.showRedLine = True
        else:
            self.showRedLine = False
            self.redLine.set_data([], [])

    def setShowGreenLine(self, value):
        """ sets whether to show greenLine """
        if value == 1:
            self.showGreenLine = True
        else:
            self.showGreenLine = False
            self.greenLine.set_data([], [])

    def setShowBlueLine(self, value):
        """ sets whether to show blueLine """
        if value == 1:
            self.showBlueLine = True
        else:
            self.showBlueLine = False
            self.blueLine.set_data([], [])

    def setShowMaxLine(self, value):
        """ sets whether to show maxLine """
        if value == 1:
            self.showMaxLine = True
        else:
            self.showMaxLine = False
            self.maxLine.set_data([], [])

    def selectMinMax(self):
        """ calculet the min and max borders for y-axis of graph """
        self.yMin = 255
        self.yMax = -255
        if self.showMaxLine:
            self.yMin = min(self.yMin, min(self.maxLine.get_ydata()))
            self.yMax = max(self.yMax, max(self.maxLine.get_ydata()))
        if self.showRedLine:
            self.yMin = min(self.yMin, min(self.redLine.get_ydata()))
            self.yMax = max(self.yMax, max(self.redLine.get_ydata()))
        if self.showGreenLine:
            self.yMin = min(self.yMin, min(self.greenLine.get_ydata()))
            self.yMax = max(self.yMax, max(self.greenLine.get_ydata()))
        if self.showBlueLine:
            self.yMin = min(self.yMin, min(self.blueLine.get_ydata()))
            self.yMax = max(self.yMax, max(self.blueLine.get_ydata()))

    def setCamera(self, camera):
        self.camera = camera