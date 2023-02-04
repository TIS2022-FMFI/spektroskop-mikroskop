import time
from threading import Thread
import tkinter as tk
from threading import Thread
from tkinter import *

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.backends.backend_agg as agg
from scipy.signal import find_peaks

from camera.Camera import Camera
from camera.FrameUtilMethods import FrameUtilMethods


class Plot:
    def __init__(self, canvas, camera=Camera(0)):
        plt.style.use('ggplot')
        self.fig, self.ax = plt.subplots()
        self.redLine, = self.ax.step([], [], "red")
        self.greenLine, = self.ax.step([], [], "green")
        self.blueLine, = self.ax.step([], [], "blue")
        self.maxLine, = self.ax.step([], [], "black")
        self.ax.set_ylabel("INTENSITY")
        self.ax.set_xlabel("PIXELS")
        # self.fig.gca().xmargin = 0
        self.xLimValues = range(0, 1280)
        self.yMin = 255
        self.yMax = 0
        self.annList = []
        self.lines = None
        # self.ax.xmargin = 0
        self.ax.set_position([0.2, 0.1, 0.1, 0.8])

        self.fig.tight_layout()
        # self.ax.use_sticky_edges = True

        self.camera = camera
        self.t = None
        self.t2 = None
        self.isPaused = False
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas)
        self.toolbar = NavigationToolbar2Tk(self.canvas, canvas)
        self.ani = None
        self.cameraCanvas = None
        self.label = None
        self.slider = -5

        # self.camera.initPlot(self)

        self.showWavelengt = False
        self.model = None

        self.showPeaks = False
        self.peakDistance = 20
        self.peakHeight = 20

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

        self.camera.showImage(frame)  # this metod is slowing process significantly the most,
        # problem is to process image from cv2 camera to format used for canvas process

        self.frameUtils.setFrame(frame)

        if self.showRedLine:
            redLine = self.frameUtils.getRedLine()
            self.performOperations(self.redLine, redLine)

        if self.showGreenLine:
            greenLine = self.frameUtils.getGreenLine()
            self.performOperations(self.greenLine, greenLine)

        if self.showBlueLine:
            blueLine = self.frameUtils.getBlueLine()
            self.performOperations(self.blueLine, blueLine)

        if self.showMaxLine:
            maxValue = self.frameUtils.getMaxLine()
            self.performOperations(self.maxLine, maxValue)

            if self.showPeaks:
                red_peaks_indices, _ = find_peaks(maxValue, distance=self.peakDistance, height=self.peakHeight)
                red_peaks_indices.astype(np.int8)

                self.deletePeaks()

                self.lines = self.ax.vlines(x=red_peaks_indices, ymin=self.yMin, ymax=maxValue[red_peaks_indices],
                                            colors="purple", linestyles="dashed")

                for x, y in zip(red_peaks_indices, maxValue[red_peaks_indices]):
                    ann = self.ax.text(x - 2, y * 1.05, str(y))
                    self.annList.append(ann)

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

    def wofi(self, frame):
        self.t2 = Thread(target=self.camera.showImage, args=(frame, ))
        self.t2.start()

    def show_plot(self):
        """ main fuction to call for graph displaying """
        # self.startT2(self.camera.get_frame().__next__())
        self.ani = FuncAnimation(self.fig, self.updatePlot, frames=self.camera.get_frame(), interval=1)
        self.start()
        # self.canvas.draw()
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.packGraphCanvas()

    def showPixelView(self):
        """ sets pixel view """
        self.xLimValues = range(0, self.camera.getCameraWidht())
        self.ax.set_xlabel("PIXELS")
        self.handleStaticData()
        # self.ax.set_xlim([0, self.camera.getCameraWidht()])

    def showWavelengthView(self):
        """ sets wavelengt view """
        if self.model:
            self.xLimValues = self.model(self.xLimValues)
            self.ax.set_xlabel("NANOMETERS")
            self.handleStaticData()

    def start(self):
        self.t = Thread(target=self.canvas.draw())
        self.t.start()

    def pause(self):
        if self.ani is not None:
            self.ani.event_source.stop()
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
        self.camera.setExtraLines(self.mainLine, self.camera.extraLines)
        self.handleStaticData()

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
        self.handleStaticData()

    def setExposureTimeForCamera(self, exposureTieme):
        """ sets exposure time of camera """
        self.camera.setExposureTime(exposureTieme)

    def setReferenceData(self):
        """ sets reference data for subtraction and division """
        if self.camera.isCapturing:
            self.frameUtils.setFrame(self.camera.get_frame().__next__())
            self.referenceData = self.frameUtils.getMaxLine()
            self.frameUtils.setReferenceData(self.referenceData)
        else:
            self.frameUtils.setFrame(self.camera.lastFrame)
            self.referenceData = self.frameUtils.getMaxLine()
            self.frameUtils.setReferenceData(self.referenceData)

    def setSubstraction(self):
        """ sets whether to do subtraction over graph """
        self.doSubtraction = True
        self.doDivison = False
        self.handleStaticData()

    def unsetSubtraction(self):
        self.doSubtraction = False
        self.handleStaticData()

    def setDivision(self):
        """ sets whether to do division over graph """
        self.doDivison = True
        self.doSubtraction = False
        self.handleStaticData()

    def unsetDivision(self):
        self.doDivison = False
        self.handleStaticData()

    def setShowRedLine(self, value):
        """ sets whether to show redLine """
        if value == 1:
            self.showRedLine = True
        else:
            self.showRedLine = False
            self.redLine.set_data([], [])
        self.handleStaticData()

    def setShowGreenLine(self, value):
        """ sets whether to show greenLine """
        if value == 1:
            self.showGreenLine = True
        else:
            self.showGreenLine = False
            self.greenLine.set_data([], [])
        self.handleStaticData()

    def setShowBlueLine(self, value):
        """ sets whether to show blueLine """
        if value == 1:
            self.showBlueLine = True
        else:
            self.showBlueLine = False
            self.blueLine.set_data([], [])
        self.handleStaticData()

    def setShowMaxLine(self, value):
        """ sets whether to show maxLine """
        if value == 1:
            self.showMaxLine = True
        else:
            self.showMaxLine = False
            self.maxLine.set_data([], [])
            self.deletePeaks()
        self.handleStaticData()

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

    def handleStaticData(self):
        if not self.camera.isCapturing:
            self.updatePlot(self.camera.lastFrame)
            self.canvas.draw()

    def saveGraph(self):
        return np.array(self.canvas.renderer.buffer_rgba())

    def packGraphCanvas(self):
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def setShowPeaks(self):
        self.showPeaks = True
        self.handleStaticData()

    def setHidePeaks(self):
        self.showPeaks = False
        self.deletePeaks()
        self.handleStaticData()

    def setPeakDistance(self, distance):
        self.peakDistance = distance

    def setPeakHight(self, height):
        self.peakHeight = height

    def deletePeaks(self):
        for a in self.annList:
            a.remove()
        self.annList[:] = []

        if self.lines:
            try:
                self.lines.remove()
            except ValueError:
                pass