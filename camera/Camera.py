import time
from threading import Thread
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2


class Camera:
    def __init__(self, cameraId=0, plot=None, parentCanvas=None):
        self.cameraHieght = 720
        self.cameraWidth = 1280
        self.camera = None
        self.cameraId = cameraId
        self.zoom = 1.0
        self.angle = 0.0
        self.isCapturing = False
        self.rootCanvas = parentCanvas
        self.label = None
        self.scrollbar = None
        self.myCanvas = None

        self.pathToImage = None

        self.extraLines = 0
        self.drawTopLine = 100 - 1
        self.drawBottomLine = 100 + 1

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
        cv2image = cv2.resize(cv2image, (self.myCanvas.winfo_width(), self.cameraHieght))
        img = Image.fromarray(cv2image)
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.myCanvas.create_image(0, 0, image=imgtk, anchor=NW)
        self.drawGuidengLines()

    def start(self):
        self.camera = cv2.VideoCapture(self.cameraId)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.cameraWidth)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cameraHieght)
        self.isCapturing = True
        if self.myCanvas is not None:
            self.myCanvas.destroy()
        self.initCanvas()
        # self.showImage(self.get_frame().__next__())

    def pause(self):
        self.lastFrame = self.get_frame().__next__()
        self.release()

    def release(self):
        self.isCapturing = False
        if self.camera is not None:
            self.camera.release()

    def drawGuidengLines(self):
        if self.drawTopLine is None and self.drawBottomLine is None:
            self.myCanvas.create_rectangle(0, 0, self.myCanvas.winfo_width(), self.cameraHieght - 1,
                                           fill='#FFFFFF', outline='', stipple='gray12')
        elif self.drawTopLine is None:
            self.myCanvas.create_rectangle(0, 0, self.myCanvas.winfo_width(), self.drawBottomLine,
                                           fill='#FFFFFF', outline='', stipple='gray12')
        elif self.drawBottomLine is None:
            self.myCanvas.create_rectangle(0, self.drawTopLine, self.myCanvas.winfo_width(), self.myCanvas.winfo_width(),
                                           fill='#FFFFFF', outline='', stipple='gray12')
        else:
            self.myCanvas.create_rectangle(0, self.drawTopLine, self.myCanvas.winfo_width(), self.drawBottomLine,
                                           fill='#FFFFFF', outline='', stipple='gray12')

    def setExposureTime(self, exposureTime):
        self.camera.set(cv2.CAP_PROP_SETTINGS, 1)

        # cv2.namedWindow("Settings", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Settings", 640, 480)
        # cv2.createTrackbar("Brightness", "Settings", int(self.camera.get(cv2.CAP_PROP_BRIGHTNESS)), 100,
        #                    lambda value: int(self.camera.set(cv2.CAP_PROP_BRIGHTNESS, value)))
        # cv2.createTrackbar("Contrast", "Settings", int(self.camera.get(cv2.CAP_PROP_CONTRAST)), 100,
        #                    lambda value: self.camera.set(cv2.CAP_PROP_CONTRAST, value))
        # cv2.createTrackbar("Saturation", "Settings", int(self.camera.get(cv2.CAP_PROP_SATURATION)), 100,
        #                    lambda value: self.camera.set(cv2.CAP_PROP_SATURATION, value))
        # cv2.createTrackbar("Exposure Time", "Settings", int(self.camera.get(cv2.CAP_PROP_EXPOSURE) * -1), 14,
        #                    lambda value: self.camera.set(cv2.CAP_PROP_EXPOSURE, value * -1))
        # cv2.createTrackbar("Auto Exposure", "Settings", 0, 1, lambda x: x)

        # exposure_time = tk.Scale(root, from_=0, to=100, orient="horizontal", command=update_exposure_time)
        # exposure_time.pack()
        #
        # # Auto Exposure Time Checkbox
        # auto_exposure_time = tk.IntVar()
        # checkbox = tk.Checkbutton(root, text="Auto Exposure Time", variable=auto_exposure_time, onvalue=1, offvalue=0,
        #                           command=lambda: update_auto_exposure_time(auto_exposure_time.get()))
        # checkbox.pack()

    def update_exposure_time(self, value):
        self.camera.set(cv2.CAP_PROP_EXPOSURE, value)

    def update_auto_exposure_time(self, value):
        if value == 1:
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, cv2.CAP_PROP_AUTO_EXPOSURE)
        else:
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)

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

        if self.drawBottomLine > self.cameraHieght - 1:
            self.drawBottomLine = None

    def initPlot(self, plot):
        self.plot = plot

    def setCameraId(self, cameraId):
        self.cameraId = cameraId

    def setRootCanvas(self, canvas):
        self.rootCanvas = canvas

    def setPathToImage(self, path):
        self.pathToImage = path

    def setLastFrameAsImg(self):
        self.lastFrame = cv2.imread(self.pathToImage)