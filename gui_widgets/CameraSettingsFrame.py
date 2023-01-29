from tkinter import *
from tkinter import ttk
import cv2

from camera.Camera import Camera
from gui_widgets.FrameBaseClass import FrameBaseClass


# TODO LOGIKA PRI ZMENE CONNECTION OBRAZKA
class CameraSettingsFrame(FrameBaseClass):
    def __init__(self, plot=None, spectroImageFrame=None, liveCameraFrame=None, spectroCamera=None, liveCamera=None):
        super().__init__()

        self.plot = plot
        self.spectroImageFrame = spectroImageFrame
        self.liveCameraFrame = liveCameraFrame
        self.spectroCamera = spectroCamera
        self.liveCamera = liveCamera

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

        self.spectroscopeCameraLabel.grid(sticky=W, row=6, column=0, pady=(10, 0))
        self.spectroscopeCameraComboBox.grid(sticky=W, row=6, column=1, pady=(10, 0), padx=(10, 10))

        self.setCameraCamerasButton.grid(sticky=E, row=7, column=0, pady=(10, 0))

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
        idSpec = self.spectroscopeCameraVAR.get()
        idLive = self.liveCameraVAR.get()
        if idSpec != "":
            if self.spectroCamera is not None:
                self.plot.release()
                spectroCamera = Camera(int(idSpec), self.plot)
                self.plot.camera = spectroCamera
                spectroCamera.initCanvas(self.spectroImageFrame)
                self.spectroCamera = spectroCamera
                self.plot.show_plot()
            else:
                spectroCamera = Camera(int(idSpec), self.plot)
                self.plot.camera = spectroCamera
                spectroCamera.initCanvas(self.spectroImageFrame)
                self.spectroCamera = spectroCamera
                self.plot.show_plot()

        if idLive != "":
            if self.liveCamera is None:
                self.liveCamera = Camera(int(idLive))
                self.liveCameraFrame.initCamera(self.liveCamera)
                self.liveCameraFrame.update_frame()
            else:
                self.liveCamera.release()
                self.liveCamera = Camera(int(idLive))
                self.liveCameraFrame.initCamera(self.liveCamera)
                self.liveCameraFrame.update_frame()


