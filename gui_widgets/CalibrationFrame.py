from tkinter import *
from gui_widgets.FrameBaseClass import FrameBaseClass
from gui_widgets.Calibration import *


class CalibrationFrame(FrameBaseClass):
    def __init__(self, plot):
        super().__init__()

        self.calibrationModule = Calibration()
        self.plot = plot
        self.calibrationModule.initPlot(plot)

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Labels
        self.calibrationLabel = self.initializeLabel("Calibration", 1)
        self.calibrationFileLabel = self.initializeLabel("Calibration file:", 0)
        self.createCalibrationFileLabel = self.initializeLabel("Create calibration file:", 0)
        self.calibrationChartLabel = self.initializeLabel("Calibration Chart", 0)

        # Buttons
        self.calibrationFileButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Choose")
        self.calibrationFileButton.configure(command=lambda: self.FUNCTION_TODO(self.loadFileAndChangeText()))

        self.calibrationChartCreateButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH,
                                                                  "Create")
        self.calibrationChartCreateButton.configure(command=lambda: self.FUNCTION_TODO(CalibrationHandler()
                                                                                            .calibrateFromApp(
                                                                                            self.calibrationModule,
                                                                                            self.calibrationText
                                                                                            .get("1.0", END), 3)))

        self.calibrationChartShowButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Show")
        self.calibrationChartShowButton.configure(command=lambda: self.FUNCTION_TODO(CalibrationRender()
                                                                                     .render(self.calibrationModule)))

        # Text
        self.calibrationText = Text(self, width=30, height=15)

        # Text value
        self.calibrationValue = self.calibrationText.get("1.0",
                                                         END)  # to "1.0" znamena ze beriem text od 1 riadka a 0
        # znaku.. proste beries text od zaciatku po koniec"
        self.placeWidgets()

    def loadFileAndChangeText(self):
        CalibrationHandler().calibrateFromFile(self.calibrationModule, 3)
        self.calibrationText.delete("1.0", END)
        self.calibrationText.insert("1.0", self.calibrationModule.__str__())

    def placeWidgets(self):
        self.calibrationLabel.grid(sticky=W, row=0, column=0, pady=(10, 0))

        self.calibrationFileLabel.grid(sticky=W, row=1, column=0, pady=(10, 0))
        self.calibrationFileButton.grid(sticky=W, row=1, column=1, pady=(10, 0), padx=(10, 10))

        self.createCalibrationFileLabel.grid(sticky=W, row=2, column=0, pady=(10, 0))

        self.calibrationText.grid(sticky=W, row=3, column=0, pady=(10, 0), padx=(10, 0))

        self.calibrationChartCreateButton.grid(sticky=W, row=4, column=1, pady=(10, 0), padx=(10, 10))

        self.calibrationChartLabel.grid(sticky=W, row=5, column=0, pady=(10, 10))
        self.calibrationChartShowButton.grid(sticky=W, row=5, column=1, pady=(10, 10), padx=(10, 10))
