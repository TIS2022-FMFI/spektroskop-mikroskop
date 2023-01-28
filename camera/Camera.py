from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2

class Camera:
    def __init__(self, cameraId=0):
        self.cameraHieght = 720
        self.cameraWidth = 1200

        self.camera = cv2.VideoCapture(cameraId)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.cameraWidth)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cameraHieght)
        self.cameraId = cameraId
        self.zoom = 1.0
        self.angle = 0.0
        self.chanel = 'a'
        self.isCapturing = True
        self.rootCanvas = None
        self.label = None
        self.scrollbar = None
        self.myCanvas = None

        self.extraLines = 1
        self.drawTopLine = self.cameraHieght // 2 - 1
        self.drawBottomLine = self.cameraHieght // 2 + 1

        self.plot = None

    def handleMauseClick(self, event):
        print("Mouse clicked at x:", event.x, "y:", event.y)
        scroll_pos = self.scrollbar.get()
        mainLine = event.y + (scroll_pos[0] * self.cameraHieght)
        self.plot.setMainLine(int(mainLine))
        self.plot.setExtraLines(self.extraLines)
        self.setExtraLines(int(mainLine), self.extraLines)

    def initCanvas(self, canvas):
        self.rootCanvas = canvas

        self.myCanvas = tk.Canvas(self.rootCanvas)
        self.myCanvas.bind("<Button-1>", self.handleMauseClick)

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

    def showImage(self, frame):
        if self.drawTopLine:
            cv2.line(frame, (0, self.drawTopLine), (frame.shape[1], self.drawTopLine), (255, 255, 255), thickness=1)
        if self.drawBottomLine:
            cv2.line(frame, (0, self.drawBottomLine), (frame.shape[1], self.drawBottomLine), (255, 255, 255), thickness=1)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        # Convert image to PhotoImage
        img = img.resize((self.myCanvas.winfo_width(), self.cameraHieght), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.myCanvas.create_image(0, 0, image=imgtk, anchor=NW)

    def start(self):
        self.camera = cv2.VideoCapture(self.cameraId)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.cameraWidth)
        self.isCapturing = True

    def pause(self):
        self.isCapturing = False
        self.release()

    def release(self):
        self.camera.release()

    def setExposureTime(self, exposureTime):
        self.camera.set(cv2.CAP_PROP_EXPOSURE, int(exposureTime))

    def setColorChanel(self, chanel):
        self.chanel = chanel

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




