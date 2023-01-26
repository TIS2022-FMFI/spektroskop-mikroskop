from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2

class Camera:
    def __init__(self, cameraId=0):
        self.camerHight = 640
        self.cameraWidth = 1200

        self.camera = cv2.VideoCapture(cameraId)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.cameraWidth)
        self.cameraId = cameraId
        self.zoom = 1.0
        self.angle = 0.0
        self.chanel = 'a'
        self.isCapturing = True
        self.rootCanvas = None
        self.label = None
        self.scrollbar = None
        self.myCanvas = None

    def initCanvas(self, canvas):
        self.rootCanvas = canvas

        self.myCanvas = tk.Canvas(self.rootCanvas)
        self.myCanvas.pack(fill='both', expand=True)

        frame = tk.Frame(self.rootCanvas)

        self.label = Label(frame)
        self.label.pack()

        self.scrollbar = tk.Scrollbar(self.myCanvas, orient=VERTICAL, command=self.myCanvas.yview)
        self.myCanvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.myCanvas.config(scrollregion=(0, 0, 0, self.camerHight))


    def get_frame(self):
        while self.isCapturing:
            _, frame = self.camera.read()
            yield frame

    def showImage(self, frame):
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        # Convert image to PhotoImage
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
        self.camera.set(cv2.CAP_PROP_EXPOSURE, exposureTime)

    def setColorChanel(self, chanel):
        self.chanel = chanel
    def getCameraHeight(self):
        return self.camerHight

    def getCameraWidht(self):
        return self.cameraWidth


