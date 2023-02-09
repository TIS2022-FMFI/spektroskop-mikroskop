from threading import Thread
from tkinter import *
from tkinter import ttk
import cv2
from idlelib.tooltip import Hovertip

from camera.Camera import Camera
from gui_widgets.FrameBaseClass import FrameBaseClass


# TODO LOGIKA PRI ZMENE CONNECTION OBRAZKA
class CameraSettingsFrame(FrameBaseClass):
    def __init__(self, plot=None, spectroCamera=None, liveCamera=None, liveCameraFrame=None):
        super().__init__()

        self.plot = plot
        self.spectroCamera : Camera = spectroCamera
        self.liveCamera = liveCamera
        self.liveCameraFrame = liveCameraFrame

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Initializing widgets in frame

        # Labels
        self.cameraSettingsLabel = self.initializeLabel("Camera\nsettings", 1)
        self.lineLabel = self.initializeLabel("Line:", 0)
        self.extraLinesLabel = self.initializeLabel("Extra lines:", 0)
        self.averageLabel = self.initializeLabel("Average:", 0)
        self.liveCameraLabel = self.initializeLabel("Live camera:", 0)
        self.spectroscopeCameraLabel = self.initializeLabel("Spectroscope\n camera:", 0)
        self.exposureTimeLabel = self.initializeLabel("Exposure time:", 0)
        self.connectionLabel = self.initializeLabel("Connection:", 0)

        # Buttons
        self.setExposureTimeButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.setExposureTimeButton.configure(command=lambda: self.spectroCamera.setExposureTime(self.getExposureTime()))

        # Entries
        self.lineEntry = self.initializeEntry(15)
        self.lineEntry.insert(0, 100)
        self.extraLinesEntry = self.initializeEntry(15)
        self.extraLinesEntry.insert(0, 0)
        self.averageEntry = self.initializeEntry(15)
        # self.exposureTimeEntry = self.initializeEntry(15)

        self.exposureTimeSlider = self.initializeScale(13)
        self.exposureTimeSlider.set(-4)
        self.exposureTimeSlider.config(command=lambda value: self.getExposureTime())

        self.lineEntry.bind("<KeyRelease>", self.setMainLine)
        self.extraLinesEntry.bind("<KeyRelease>", self.setExtraLines)

        # Comboboxes
        self.liveCameraVAR = StringVar()
        self.liveCameraComboBox = ttk.Combobox(self, width=15, state='readonly', postcommand=self.fillLiveCameraIds,
                                               textvariable=self.liveCameraVAR)
        self.liveCameraComboBox.set('1')

        self.spectroscopeCameraVAR = StringVar()
        self.spectroscopeCameraComboBox = ttk.Combobox(self, width=15, state='readonly',
                                                       postcommand=self.fillSpectroscopeCameraIds,
                                                       textvariable=self.spectroscopeCameraVAR)
        self.spectroscopeCameraComboBox.set('0')

        # Images
        self.connectionSignalImage = Label(self, image=self.OFF_IMAGE, bg=self.FRAME_COLOR)



        #Tooltips
        self.lineTooltipMSG = "Set middle line in analysed image."
        self.lineTooltip = Hovertip(self.lineLabel, self.lineTooltipMSG)

        self.extraLinesTooltipMSG = "Set number of lines above and under middle line."
        self.extraLinesTooltip = Hovertip(self.extraLinesLabel, self.extraLinesTooltipMSG)

        self.averageTooltipMSG = "avg"
        self.averageTooltip = Hovertip(self.averageLabel, self.averageTooltipMSG)

        self.liveCameraTooltipMSG = "Set camera for live sample image."
        self.liveCameraTooltip = Hovertip(self.liveCameraLabel, self.liveCameraTooltipMSG)

        self.spectroscopeCameraTooltipMSG = "Set camera for spectroscop camera image."
        self.spectroscopeCameraTooltip = Hovertip(self.spectroscopeCameraLabel, self.spectroscopeCameraTooltipMSG)

        self.exposureTimeTooltipMSG = "exposure time"
        self.exposureTimeTooltip = Hovertip(self.exposureTimeLabel, self.exposureTimeTooltipMSG)

        self.placeWidgets()

    def placeWidgets(self):
        self.cameraSettingsLabel.pack()
        self.lineLabel.pack()
        self.lineEntry.pack()
        self.extraLinesLabel.pack()
        self.extraLinesEntry.pack()
        # self.averageLabel.pack()
        # self.averageEntry.pack()
        self.liveCameraLabel.pack()
        self.liveCameraComboBox.pack()
        self.spectroscopeCameraLabel.pack()
        self.spectroscopeCameraComboBox.pack()
        self.exposureTimeLabel.pack()
        # self.exposureTimeEntry.grid(row=9, column=1, pady=(10, 0), padx=(0, 10))
        self.exposureTimeSlider.pack()
        self.setExposureTimeButton.pack(pady=(5, 5))
        # self.connectionLabel.pack()
        # self.connectionSignalImage.pack()



        # row = 0
        # self.cameraSettingsLabel.grid(sticky=W, row=row, column=0, pady=(10, 0))
        #
        # row += 1
        # self.lineLabel.grid(sticky=W, row=row, column=0, pady=(10, 0))
        # self.lineEntry.grid(row=row, column=1, pady=(10, 0), padx=(0, 10))
        #
        # row += 1
        # self.extraLinesLabel.grid(sticky=W, row=row, column=0, pady=(10, 0))
        # self.extraLinesEntry.grid(row=row, column=1, pady=(10, 0), padx=(0, 10))
        #
        # row += 1
        # self.averageLabel.grid(sticky=W, row=row, column=0, pady=(10, 0))
        # self.averageEntry.grid(row=row, column=1, pady=(10, 0), padx=(0, 10))
        #
        # row += 1
        # self.liveCameraLabel.grid(sticky=W, row=row, column=0, pady=(10, 0))
        # self.liveCameraComboBox.grid(sticky=W, row=row, column=1, pady=(10, 0), padx=(10, 10))
        #
        # row += 1
        # self.spectroscopeCameraLabel.grid(sticky=W, row=row, column=0, pady=(10, 0))
        # self.spectroscopeCameraComboBox.grid(sticky=W, row=row, column=1, pady=(10, 0), padx=(10, 10))
        #
        # row += 1
        # self.exposureTimeLabel.grid(sticky=W, row=row, column=0, pady=(10, 0))
        # # self.exposureTimeEntry.grid(row=9, column=1, pady=(10, 0), padx=(0, 10))
        #
        # row += 1
        # self.exposureTimeSlider.grid(row=row, columnspan=2, sticky=W+E, pady=(10, 10))
        #
        # row += 1
        # self.setExposureTimeButton.grid(sticky=E, row=row, column=0, pady=(10, 10))
        #
        # row += 1
        # self.connectionLabel.grid(sticky=W, row=row, column=0, pady=(10, 10))
        # self.connectionSignalImage.grid(row=row, column=0, pady=(10, 10), padx=(30, 0))

    def setMainLine(self, event):
        try:
            self.plot.setMainLine(int(event.widget.get()))
        except ValueError:
            self.plot.setMainLine(0)

    def setExtraLines(self, event):
        try:
            self.plot.setExtraLines(int(event.widget.get()))
        except ValueError:
            self.plot.setExtraLines(0)

    def getExposureTime(self):
        self.plot.setExposureTimeForCamera(self.exposureTimeSlider.get())

    def initPlot(self, plot):
        self.plot = plot

    def fillLiveCameraIds(self):
        self.liveCameraComboBox['values'] = self.getCameraIDS()
        self.liveCameraComboBox.bind("<<ComboboxSelected>>", self.setLiveCamera)

    def fillSpectroscopeCameraIds(self):
        self.spectroscopeCameraComboBox['values'] = self.getCameraIDS()
        self.spectroscopeCameraComboBox.bind("<<ComboboxSelected>>", self.setSpectroCamera)

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

    def setLiveCamera(self, *args):
        self.focus()
        idLive = self.liveCameraVAR.get()

        if idLive != "":
            if self.liveCamera is None:
                raise RuntimeError("Live camera initioalization failed")
            self.liveCamera.setCameraId(int(idLive))
            self.liveCameraFrame.start()

    def setSpectroCamera(self, *args):
        self.focus()
        idSpec = self.spectroscopeCameraVAR.get()

        if idSpec != "":
            if self.spectroCamera is None:
                raise RuntimeError("Spectro camera initioalisation failed")
            self.plot.release()
            self.spectroCamera.setCameraId(int(idSpec))
            self.spectroCamera.start()
            self.plot.show_plot()