from tkinter import *
from tkinter import ttk
from FrameBaseClass import FrameBaseClass


# TODO LOGIKA PRI ZMENE CONNECTION OBRAZKA
class CameraSettingsFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()

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
        self.setCameraLinesButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.setCameraCamerasButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.setCameraCamerasButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.setExposureTimeButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.setExposureTimeButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        # Entries
        self.lineEntry = self.initializeEntry(15)
        self.extraLinesEntry = self.initializeEntry(15)
        self.averageEntry = self.initializeEntry(15)
        self.exposureTimeEntry = self.initializeEntry(15)

        # Comboboxes
        # test vals
        vals = ["1", "2", "3"]
        self.liveCameraComboBox = ttk.Combobox(self, values=vals, width=15)
        self.spectroscopeCameraComboBox = ttk.Combobox(self, values=vals, width=15)

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
        self.exposureTimeEntry.grid(row=9, column=1, pady=(10, 0), padx=(0, 10))

        self.setExposureTimeButton.grid(sticky=E, row=10, column=0, pady=(10, 10))
        self.connectionLabel.grid(sticky=W, row=11, column=0, pady=(10, 10))
        self.connectionSignalImage.grid(row=11, column=0, pady=(10, 10), padx=(30, 0))

