from tkinter import *
from gui_widgets.FrameBaseClass import FrameBaseClass

class ImportExportFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Initializing widgets in frame

        # Labels
        self.importLabel = self.initializeLabel("Import", 1)
        self.importCameraSpectralImageLabel = self.initializeLabel("Camera spectral image:", 0)
        self.exportLabel = self.initializeLabel("Export", 1)
        self.graphImageLabel = self.initializeLabel("Graph image:", 0)
        self.exportCameraSpectralImageLabel = self.initializeLabel("Camera spectral image:", 0)
        self.cameraImageLabel = self.initializeLabel("Camera image:", 0)
        self.calibrationChartLabel = self.initializeLabel("Calibration chart:", 0)

        # Buttons
        self.importSpectralImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH,
                                                               "Choose")
        self.importSpectralImageButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.graphImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Export")
        self.graphImageButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.exportCameraSpectralImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH,
                                                                     "Export")
        self.exportCameraSpectralImageButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.cameraImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Export")
        self.cameraImageButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.calibrationChartButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Export")
        self.calibrationChartButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        # Placing widgets into frame
        self.placeWidgets()

    def placeWidgets(self):
        self.importLabel.grid(sticky=W, row=0, column=0, columnspan=2, pady=(10, 0))

        self.importCameraSpectralImageLabel.grid(row=1, column=0, sticky=W)
        self.importSpectralImageButton.grid(row=1, column=1, padx=(0, 10), pady=(10, 10))

        self.exportLabel.grid(row=2, column=0, columnspan=2, sticky=W)

        self.graphImageLabel.grid(row=3, column=0, sticky=W)
        self.graphImageButton.grid(row=3, column=1, padx=(0, 10), pady=(10, 10))

        self.exportCameraSpectralImageLabel.grid(row=4, column=0, sticky=W)
        self.exportCameraSpectralImageButton.grid(row=4, column=1, padx=(0, 10), pady=(10, 10))

        self.cameraImageLabel.grid(row=5, column=0, sticky=W)
        self.cameraImageButton.grid(row=5, column=1, padx=(0, 10), pady=(10, 10))

        self.calibrationChartLabel.grid(row=6, column=0, sticky=W)
        self.calibrationChartButton.grid(row=6, column=1, padx=(0, 10), pady=(10, 10))
