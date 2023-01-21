from tkinter import *
from tkinter import filedialog
from FrameBaseClass import FrameBaseClass
from Calibration import Calibration


# TODO VYBERANIE FILEU
class CalibrationFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()

        self.calibrationModule = Calibration()

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Initializing widgets in frame

        # Labels
        self.calibrationLabel = self.initializeLabel("Calibration", 1)
        self.calibrationFileLabel = self.initializeLabel("Calibration file:", 0)
        self.createCalibrationFileLabel = self.initializeLabel("Create calibration file:", 0)
        self.calibrationChartLabel = self.initializeLabel("Calibration Chart", 0)

        # Buttons
        self.calibrationFileButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Choose")
        self.calibrationFileButton.configure(command=self.loadCalibrationFile)

        self.calibrationChartCreateButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH,
                                                                  "Create")
        self.calibrationChartCreateButton.configure(command= self.saveCalibrationFile)

        self.calibrationChartShowButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Show")
        self.calibrationChartShowButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        # Text
        self.calibrationText = Text(self, width=30, height=15)

        # Text value
        self.calibrationValue = self.calibrationText.get("1.0",
                                                         END)  # to "1.0" znamena ze beriem text od 1 riadka a 0 znaku.. proste beries text od zaciatku po kiniec"
        self.placeWidgets()

    def placeWidgets(self):
        self.calibrationLabel.grid(sticky=W, row=0, column=0, pady=(10, 0))

        self.calibrationFileLabel.grid(sticky=W, row=1, column=0, pady=(10, 0))
        self.calibrationFileButton.grid(sticky=W, row=1, column=1, pady=(10, 0), padx=(10, 10))

        self.createCalibrationFileLabel.grid(sticky=W, row=2, column=0, pady=(10, 0))

        self.calibrationText.grid(sticky=W, row=3, column=0, pady=(10, 0), padx=(10, 0))

        self.calibrationChartCreateButton.grid(sticky=W, row=4, column=1, pady=(10, 0), padx=(10, 10))

        self.calibrationChartLabel.grid(sticky=W, row=5, column=0, pady=(10, 10))
        self.calibrationChartShowButton.grid(sticky=W, row=5, column=1, pady=(10, 10), padx=(10, 10))

    def loadCalibrationFile(self):
        # Getting the address of the selected file
        fileAddress = filedialog.askopenfilename(filetypes=(('text files', '*.txt'),('All files', '*.*')))

        if fileAddress == "":  # fileAddress return "" if dialog closed with "cancel".
            return

        # Opening selected file and reading its content
        with open(fileAddress,'r') as file:
            text = file.read()

        # Deleting content of text widget and then inserting contents of selected file
        self.calibrationText.delete("1.0", END)
        self.calibrationText.insert("1.0", text)

    def saveCalibrationFile(self):
        # "Creating" the file
        file = filedialog.asksaveasfile(mode="w",defaultextension="*.txt",filetypes=[('Text Document', '*.txt')])
        if file is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return

        textFieldText = self.calibrationText.get("1.0")
        file.write(textFieldText)
        file.close()