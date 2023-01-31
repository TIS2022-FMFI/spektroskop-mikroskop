import time
from threading import Thread
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2


class Camera:
    def __init__(self, cameraId=0, plot=None, parentCanvas=None):
        self.cameraHieght = 720
        self.cameraWidth = 1200
        self.camera = None
        self.cameraId = cameraId
        self.zoom = 1.0
        self.angle = 0.0
        self.isCapturing = True
        self.rootCanvas = parentCanvas
        self.label = None
        self.scrollbar = None
        self.myCanvas = None

        self.extraLines = 0
        self.drawTopLine = self.cameraHieght // 2 - 1
        self.drawBottomLine = self.cameraHieght // 2 + 1

        self.plot = plot

        self.lastFrame = None

    def handleMauseClick(self, event):
        # print("Mouse clicked at x:", event.x, "y:", event.y)
        scroll_pos = self.scrollbar.get()
        mainLine = event.y + (scroll_pos[0] * self.cameraHieght)
        self.plot.setMainLine(int(mainLine))
        self.plot.setExtraLines(self.extraLines)
        self.setExtraLines(int(mainLine), self.extraLines)

        if not self.isCapturing:
            self.plot.updatePlot(self.lastFrame)
            self.plot.canvas.draw()

    def handleScrollEvent(self, event):
        self.myCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def initCanvas(self):
        self.myCanvas = tk.Canvas(self.rootCanvas)
        self.myCanvas.bind("<Button-1>", self.handleMauseClick)
        self.myCanvas.bind("<MouseWheel>", self.handleScrollEvent)

        self.myCanvas.pack(fill='both', expand=True)

        frame = tk.Frame(self.rootCanvas)

        self.label = Label(frame)
        # self.label.bind("<Button-1>", self.handleMauseClick)

        self.label.pack()

        self.scrollbar = tk.Scrollbar(self.myCanvas, orient=VERTICAL, command=self.myCanvas.yview)
        self.myCanvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.myCanvas.config(scrollregion=(0, 0, 0, self.cameraHieght))

    def get_frame(self):
        while self.isCapturing:
            _, frame = self.camera.read()
            yield frame
        else:
            ...
            # yield self.lastFrame

    def showImage(self, frame):
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        # Convert image to PhotoImage
        img = img.resize((self.myCanvas.winfo_width(), self.cameraHieght), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.myCanvas.create_image(0, 0, image=imgtk, anchor=NW)
        self.drawGuidengLines()

    def start(self):
        self.camera = cv2.VideoCapture(self.cameraId)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.cameraWidth)
        self.isCapturing = True
        if self.myCanvas is not None:
            self.myCanvas.destroy()
        self.initCanvas()

    def pause(self):
        self.lastFrame = self.get_frame().__next__()
        self.release()

    def release(self):
        self.isCapturing = False
        if self.camera is not None:
            self.camera.release()

    def drawGuidengLines(self):
        if self.drawTopLine:
            self.myCanvas.create_line(0, self.drawTopLine, self.myCanvas.winfo_width(), self.drawTopLine, fill="white", width=1)
        if self.drawBottomLine:
            self.myCanvas.create_line(0, self.drawBottomLine, self.myCanvas.winfo_width(), self.drawBottomLine, fill="white", width=1)

    def setExposureTime(self, exposureTime):
        self.camera.set(cv2.CAP_PROP_EXPOSURE, int(exposureTime))

    def getCameraHeight(self):
        return self.cameraHieght

    def getCameraWidht(self):
        return self.cameraWidth

    def setExtraLines(self, mainLine, extraLine=0):
        self.drawTopLine = mainLine - extraLine - 1
        self.drawBottomLine = mainLine + extraLine + 1
        self.extraLines = extraLine

        if self.drawTopLine < 0:
            self.drawTopLine = None

        if self.drawBottomLine > self.cameraHieght:
            self.drawBottomLine = None

    def initPlot(self, plot):
        self.plot = plot

    def setCameraId(self, cameraId):
        self.cameraId = cameraId

    def setRootCanvas(self, canvas):
        self.rootCanvas = canvas