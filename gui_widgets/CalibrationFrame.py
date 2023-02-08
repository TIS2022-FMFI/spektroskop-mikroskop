from tkinter import *
from gui_widgets.FrameBaseClass import FrameBaseClass
from gui_widgets.Calibration import *
from idlelib.tooltip import Hovertip


class CalibrationFrame(FrameBaseClass):
    def __init__(self, plot):
        super().__init__()

        self.plot = plot
        self.calibrationModule = Calibration(plot=plot)
        self.calibrationModule.initPlot(plot)

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Labels
        self.calibrationLabel = self.initializeLabel("Calibration", 1)
        self.calibrationFileLabel = self.initializeLabel("Calibration file:", 0)
        self.createCalibrationFileLabel = self.initializeLabel("Create\n calibration file:", 0)
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
        self.calibrationText = Text(self, width=20, height=15)
        self.calibrationText.insert("1.0", self.calibrationModule.__str__())

        # Text value
        self.calibrationValue = self.calibrationText.get("1.0",
                                                         END)

        # Tooltips
        self.calibrationFileTooltipMSG = "Choose calibration file from folder system."
        self.calibrationFileTooltip = Hovertip(self.calibrationFileLabel, self.calibrationFileTooltipMSG)

        self.createCalibrationFileTooltipMSG = "Create calibration from values written in text box."
        self.createCalibrationFileTooltip = Hovertip(self.createCalibrationFileLabel,
                                                     self.createCalibrationFileTooltipMSG)

        self.calibrationChartTooltipMSG = "Show graph of calibration points"
        self.calibrationChartTooltip = Hovertip(self.calibrationChartLabel, self.calibrationChartTooltipMSG)

        self.placeWidgets()

    def loadFileAndChangeText(self):
        CalibrationHandler().calibrateFromFile(self.calibrationModule, 3)
        self.calibrationText.delete("1.0", END)
        self.calibrationText.insert("1.0", self.calibrationModule.__str__())

    def placeWidgets(self):
        self.calibrationLabel.pack()

        self.calibrationFileLabel.pack()
        self.calibrationFileButton.pack(pady=(5, 5))

        self.createCalibrationFileLabel.pack()

        self.calibrationText.pack()

        self.calibrationChartCreateButton.pack(pady=(5, 5))

        self.calibrationChartLabel.pack()
        self.calibrationChartShowButton.pack(pady=(5, 5))
