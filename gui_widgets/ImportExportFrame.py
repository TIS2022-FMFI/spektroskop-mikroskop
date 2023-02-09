from tkinter import *
import tkinter as tk
from gui_widgets.FrameBaseClass import FrameBaseClass
from gui_widgets.ImporExportModule import *
from idlelib.tooltip import Hovertip


class ImportExportFrame(FrameBaseClass):
    def __init__(self, plot=None, motorControllerFrame=None):
        super().__init__()

        self.plot = plot
        self.motorControllerFrame = motorControllerFrame

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Initializing widgets in frame
        self.importExportModule = ImportModule()

        # Labels
        self.importLabel = self.initializeLabel("Import", 1)
        self.importCameraSpectralImageLabel = self.initializeLabel("Camera\n spectral image:", 0)
        self.importMeasurementSeriesLabel = self.initializeLabel("Measurement\n series:", 0)
        self.exportLabel = self.initializeLabel("Export", 1)
        self.graphImageLabel = self.initializeLabel("Graph image:", 0)
        self.exportCameraSpectralImageLabel = self.initializeLabel("Camera\n spectral image:", 0)
        self.cameraImageLabel = self.initializeLabel("Camera image:", 0)
        self.calibrationChartLabel = self.initializeLabel("Calibration chart:", 0)

        # Buttons
        self.importSpectralImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH,
                                                               "Choose")
        self.importSpectralImageButton.configure(command=lambda: self.importSpectralImage())

        self.importMeasurementSeriesButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH,
                                                                   "Choose")
        self.importMeasurementSeriesButton.configure(command=lambda: self.importMeasurementSeries())

        self.graphImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Export")
        self.graphImageButton.configure(command=lambda: self.exportGraphImage())

        self.exportCameraSpectralImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH,
                                                                     "Export")
        self.exportCameraSpectralImageButton.configure(command=lambda: self.exportSpectralImage())

        self.cameraImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Export")
        self.cameraImageButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.calibrationChartButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Export")
        self.calibrationChartButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        # Tooltips
        self.importSpectrailImageTooltipMSG = "Import image from file system."
        self.importSpectrailImageTooltip = Hovertip(self.importCameraSpectralImageLabel,
                                                    self.importSpectrailImageTooltipMSG)

        self.importMeasurementSeriesTooltipMSG = "Import series of images from file system."
        self.importMeasurementSeriesTooltip = Hovertip(self.importMeasurementSeriesLabel,
                                                       self.importMeasurementSeriesTooltipMSG)

        self.graphImageTooltipMSG = "Export graph image."
        self.graphImageTooltip = Hovertip(self.graphImageLabel, self.graphImageTooltipMSG)

        self.exportCameraSpectralImageToolTipMSG = "Export image from spectrometer camera."
        self.exportCameraSpectralImageToolTip = Hovertip(self.exportCameraSpectralImageLabel,
                                                         self.exportCameraSpectralImageToolTipMSG)

        self.cameraImageTooltipMSG = "Export image from live camera."
        self.cameraImageTooltip = Hovertip(self.cameraImageLabel, self.cameraImageTooltipMSG)

        self.calibrationChartTooltipMSG = "Export calibration chart."
        self.calibrationChartTooltip = Hovertip(self.calibrationChartLabel,
                                                self.calibrationChartTooltipMSG)

        # Placing widgets into frame
        self.placeWidgets()

    def placeWidgets(self):
        self.importLabel.pack()

        self.importCameraSpectralImageLabel.pack()
        self.importSpectralImageButton.pack( pady=(5, 5))

        self.importMeasurementSeriesLabel.pack()
        self.importMeasurementSeriesButton.pack(pady=(5, 5))

        self.exportLabel.pack()

        self.graphImageLabel.pack()
        self.graphImageButton.pack( pady=(5, 5))

        self.exportCameraSpectralImageLabel.pack()
        self.exportCameraSpectralImageButton.pack( pady=(5, 5))

        self.cameraImageLabel.pack()
        self.cameraImageButton.pack( pady=(5, 5))
        self.calibrationChartLabel.pack()
        self.calibrationChartButton.pack( pady=(5, 5))


        # self.importLabel.grid(sticky=W, row=0, column=0, columnspan=2, pady=(10, 0))
        #
        # self.importCameraSpectralImageLabel.grid(row=1, column=0, sticky=W)
        # self.importSpectralImageButton.grid(row=1, column=1, padx=(0, 10), pady=(10, 10))
        #
        # self.importMeasurementSeriesLabel.grid(row=2, column=0, sticky=W)
        # self.importMeasurementSeriesButton.grid(row=2, column=1, padx=(0, 10), pady=(10, 10))
        #
        # self.exportLabel.grid(row=3, column=0, columnspan=2, sticky=W)
        #
        # self.graphImageLabel.grid(row=4, column=0, sticky=W)
        # self.graphImageButton.grid(row=4, column=1, padx=(0, 10), pady=(10, 10))
        #
        # self.exportCameraSpectralImageLabel.grid(row=5, column=0, sticky=W)
        # self.exportCameraSpectralImageButton.grid(row=5, column=1, padx=(0, 10), pady=(10, 10))
        #
        # self.cameraImageLabel.grid(row=6, column=0, sticky=W)
        # self.cameraImageButton.grid(row=6, column=1, padx=(0, 10), pady=(10, 10))
        #
        # self.calibrationChartLabel.grid(row=7, column=0, sticky=W)
        # self.calibrationChartButton.grid(row=7, column=1, padx=(0, 10), pady=(10, 10))

    def importSpectralImage(self):
        if self.plot.camera.myCanvas is None:
            self.plot.camera.initCanvas()
        self.plot.camera.setPathToImage(self.importExportModule.importCameraImage())
        self.plot.camera.setLastFrameAsImg()
        self.plot.camera.initPlot(self.plot)
        self.plot.packGraphCanvas()
        self.plot.handleStaticData()

    def exportSpectralImage(self):
        if self.plot.camera.isCapturing:
            ExportModule.exportImage(self.plot.camera.get_frame().__next__())
        else:
            ExportModule.exportImage(self.plot.camera.lastFrame)

    def exportGraphImage(self):
        ExportModule.exportImage(self.plot.saveGraph())

    def importMeasurementSeries(self):
        files = askopenfilenames(filetypes=[('Images', '*.jpg *.jpeg *.png *.bmp')])
        self.motorControllerFrame.motorController.dataContainer = []
        for file in files:
            fr = cv.imread(file)
            self.motorControllerFrame.motorController.dataContainer.append(fr)