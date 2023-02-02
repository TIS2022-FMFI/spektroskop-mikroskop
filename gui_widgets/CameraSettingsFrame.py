from threading import Thread
from tkinter import *
from tkinter import ttk
import cv2

from camera.Camera import Camera
from gui_widgets.FrameBaseClass import FrameBaseClass


# TODO LOGIKA PRI ZMENE CONNECTION OBRAZKA
class CameraSettingsFrame(FrameBaseClass):
    def __init__(self, plot=None, spectroCamera=None, liveCamera=None, liveCameraFrame=None):
        super().__init__()

        self.t = None

        self.plot = plot
        self.spectroCamera = spectroCamera
        self.liveCamera = liveCamera
        self.liveCameraFrame = liveCameraFrame

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Initializing widgets in frame

        # Labels
        self.cameraSettingsLabel = self.initializeLabel("Camera settings", 1)
        self.lineLabel = self.initializeLabel("Line:", 0)
        self.extraLinesLabel = self.initializeLabel("Extra lines:", 0)
        self.averageLabel = self.initializeLabel("Average:", 0)
        self.liveCameraLabel = self.initializeLabel("Live camera:", 0)
        self.spectroscopeCameraLabel = self.initializeLabel("Spectroscope camera:", 0)
        self.exposureTimeLabel = self.initializeLabel("Exposure time:", 0)
        self.connectionLabel = self.initializeLabel("Connection:", 0)


        # Buttons
        self.setCameraLinesButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.setCameraLinesButton.configure(command=lambda: self.getLines())

        self.setCameraCamerasButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.setCameraCamerasButton.configure(command=lambda: self.setCameras())

        self.setSpectroCameraButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.setSpectroCameraButton.configure(command=lambda: self.setSpectroCamera())

        self.setExposureTimeButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.setExposureTimeButton.configure(command=lambda: self.getExposureTime())

        # Entries
        self.lineEntry = self.initializeEntry(15)
        self.extraLinesEntry = self.initializeEntry(15)
        self.averageEntry = self.initializeEntry(15)
        # self.exposureTimeEntry = self.initializeEntry(15)

        self.exposureTimeSlider = self.initializeScale(13)


        # Comboboxes
        self.liveCameraVAR = StringVar()
        self.liveCameraComboBox = ttk.Combobox(self, width=15, state='readonly', postcommand=self.fillLiveCameraIds,
                                               textvariable=self.liveCameraVAR)

        self.spectroscopeCameraVAR = StringVar()
        self.spectroscopeCameraComboBox = ttk.Combobox(self, width=15, state='readonly',
                                                       postcommand=self.fillSpectroscopeCameraIds, textvariable=self.spectroscopeCameraVAR)


        # Images
        self.connectionSignalImage = Label(self, image=self.OFF_IMAGE, bg=self.FRAME_COLOR)

        self.placeWidgets()

    def placeWidgets(self):
        self.cameraSettingsLabel.grid(sticky=W, row=0, column=0, pady=(10, 0))

        self.lineLabel.grid(sticky=W, row=1, column=0, pady=(10, 0))
        self.lineEntry.grid(row=1, column=1, pady=(10, 0), padx=(0, 10))

        self.extraLinesLabel.grid(sticky=W, row=2, column=0, pady=(10, 0))
        self.extraLinesEntry.grid(row=2, column=1, pady=(10, 0), padx=(0, 10))

        self.averageLabel.grid(sticky=W, row=3, column=0, pady=(10, 0))
        self.averageEntry.grid(row=3, column=1, pady=(10, 0), padx=(0, 10))

        self.setCameraLinesButton.grid(sticky=E, row=4, column=0, pady=(10, 0))

        self.liveCameraLabel.grid(sticky=W, row=5, column=0, pady=(10, 0))
        self.liveCameraComboBox.grid(sticky=W, row=5, column=1, pady=(10, 0), padx=(10, 10))
        self.setCameraCamerasButton.grid(sticky=E, row=6, column=0, pady=(10, 0))

        self.spectroscopeCameraLabel.grid(sticky=W, row=7, column=0, pady=(10, 0))
        self.spectroscopeCameraComboBox.grid(sticky=W, row=7, column=1, pady=(10, 0), padx=(10, 10))
        self.setSpectroCameraButton.grid(sticky=E, row=8, column=0, pady=(10, 0))

        self.exposureTimeLabel.grid(sticky=W, row=9, column=0, pady=(10, 0))
        # self.exposureTimeEntry.grid(row=9, column=1, pady=(10, 0), padx=(0, 10))
        self.exposureTimeSlider.grid(row=10, columnspan=2, sticky=W+E, pady=(10, 10))

        self.setExposureTimeButton.grid(sticky=E, row=11, column=0, pady=(10, 10))
        self.connectionLabel.grid(sticky=W, row=12, column=0, pady=(10, 10))
        self.connectionSignalImage.grid(row=12, column=0, pady=(10, 10), padx=(30, 0))

    def getMainLine(self):
        try:
            self.plot.setMainLine(int(self.lineEntry.get()))
        except ValueError:
            pass

    def getExtraLines(self):
        try:
            self.plot.setExtraLines(int(self.extraLinesEntry.get()))
        except ValueError:
            self.plot.setExtraLines(0)

    def getLines(self):
        self.getMainLine()
        self.getExtraLines()

    def getExposureTime(self):
        self.plot.setExposureTimeForCamera(self.exposureTimeSlider.get())

    def initPlot(self, plot):
        self.plot = plot

    def fillLiveCameraIds(self):
        self.liveCameraComboBox.bind("<<ComboboxSelected>>",lambda e: self.focus())
        self.liveCameraComboBox['values'] = self.getCameraIDS()

    def fillSpectroscopeCameraIds(self):
        self.spectroscopeCameraComboBox.bind("<<ComboboxSelected>>", lambda e: self.focus())
        self.spectroscopeCameraComboBox['values'] = self.getCameraIDS()

    def getCameraIDS(self):
        cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
                cap.release()
            else:
                cap.release()
                break
        return cameras

    def setCameras(self):
        idLive = self.liveCameraVAR.get()

        if idLive != "":
            if self.liveCamera is None:
                raise RuntimeError("Live camera initioalization failed")
            self.liveCamera.setCameraId(int(idLive))
            self.liveCameraFrame.start()

    def setSpectroCamera(self):
        idSpec = self.spectroscopeCameraVAR.get()

        if idSpec != "":
            if self.spectroCamera is None:
                raise RuntimeError("Spectro camera initioalisation failed")
            self.spectroCamera.setCameraId(int(idSpec))
            self.spectroCamera.start()
            self.plot.show_plot()

    def start(self):
        self.t = Thread(target=self.plot.show_plot)
        self.t.start()


