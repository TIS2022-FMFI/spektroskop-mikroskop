from tkinter import *
from tkinter import ttk
from Calibration import *

from camera.Plot import Plot
from camera.Camera import Camera



class GUI(Tk):
    def __init__(self):
        super().__init__()
        # Initializing constants
        self.MASTER_WIDTH = 1500
        self.MASTER_HEIGHT = 750

        self.camera = Camera(0)
        # Setting master window size
        self.geometry(f"{self.MASTER_WIDTH}x{self.MASTER_HEIGHT}")

        # Initializing window for camera feed
        self.cameraFeedTopLevel = Toplevel()

        # Initializing frame objects
        self.spectroImageFrame = SpectroImageFrame()
        self.graphImageFrame = GraphImageFrame()
        self.motorControlsFrame = MotorControlFrame()

        self.cameraSettingsFrame = CameraSettingsFrame()
        self.calibrationFrame = CalibrationFrame()
        self.d32Frame = D32Frame()
        self.graphFunctionFrame = GraphFunctionFrame()
        self.d3Frame = D3Frame()
        self.importExportFrame = ImportExportFrame()

        self.navbarFrame = NavbarFrame(self.cameraSettingsFrame, self.calibrationFrame, self.d32Frame,
                                       self.graphFunctionFrame, self.d3Frame, self.importExportFrame,
                                       self.cameraFeedTopLevel)
        # Placing frame objects into the window
        self.navbarFrame.pack(side=LEFT, fill=Y)
        self.spectroImageFrame.pack(pady=(30, 0))
        self.graphImageFrame.pack(pady=(20, 0))
        self.motorControlsFrame.pack(side=BOTTOM)


        self.mainloop()


class FrameBaseClass(Frame):
    def __init__(self):
        super().__init__()
        # Initializing constants, colors, fonts and images
        self.FONT = "Arial 10 bold"
        self.FONT_H = "Arial 15 bold"

        self.NAVBAR_FRAME_COLOR = "#3E4149"
        self.FRAME_COLOR = "#b3b3b3"
        self.BUTTON_COLOR = "#9648fb"
        self.BUTTON_COLOR_CLICKED = "#e4ccfd"

        self.NAVBAR_BUTTON_SIZE = 70

        self.BUTTON_SIZE_HEIGHT = 20
        self.BUTTON_SIZE_WIDTH = 80

        self.SPECTROMETER_FRAME_WIDTH = 1280
        self.SPECTROMETER_FRAME_HEIGHT = 100

        self.GRAPH_FRAME_WIDTH = 1280
        self.GRAPH_FRAME_HEIGHT = 500

        self.IMAGE_TRICK = PhotoImage(width=1, height=1)  # Used for a trick that lets you enable button sizes by px

        self.PLAY_IMAGE = PhotoImage(file='playImage.png')
        self.STOP_IMAGE = PhotoImage(file='stopImage.png')
        self.CAMERA_IMAGE = PhotoImage(file="video-camera.png")
        self.ON_IMAGE = PhotoImage(file="circleGreen.png")
        self.OFF_IMAGE = PhotoImage(file="circleRed.png")

    def initializeButton(self, h, w, text):
        return Button(self, text=text, bg=self.BUTTON_COLOR, fg="white", font=self.FONT, borderwidth=0,
                      height=h, width=w, image=self.IMAGE_TRICK,
                      compound=CENTER)

    def initializeLabel(self, text, isHeading):
        font = self.FONT if isHeading == 0 else self.FONT_H
        return Label(self, text=text, font=font, bg=self.FRAME_COLOR)

    def initializeEntry(self, w):
        return Entry(self, width=w)

    def removeWidgetsFromFrame(self):
        for widgets in self.winfo_children():
            widgets.grid_forget()

    def FUNCTION_TODO(self, frameWidget):
        plot = Plot(frameWidget)
        plot.show_plot()
        # print(argument)


class SpectroImageFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()
        # Setting color of frame and size
        self.configure(bg="red", width=self.SPECTROMETER_FRAME_WIDTH, height=self.SPECTROMETER_FRAME_HEIGHT)
        # Setting that disables frame shrinkage to fit widgets
        self.propagate(False)

        # Initializing widgets
        self.placeWidgets()

    def placeWidgets(self):
        pass


class GraphImageFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()
        # Setting color of frame and size
        self.configure(bg="green", width=self.GRAPH_FRAME_WIDTH, height=self.GRAPH_FRAME_HEIGHT)
        # Setting that disables frame shrinkage to fit widgets
        self.propagate(False)
        self.plot = Plot(self)
        # Initializing widgets
        self.placeWidgets()

    def placeWidgets(self):
        self.plot.show_plot()
        # self.plot.camera.showImage()


# TODO SCROLLBAR ABY UPDATEOVAL LABEL
class MotorControlFrame(FrameBaseClass):

    def __init__(self):
        super().__init__()

        # Initializing widgets

        # Scrollbar
        # Radiobutton values/state
        self.scrollBarVal = DoubleVar()
        # Pouzivam DoubleVar lebo automaticky sa updatuje # Na ziskania value pouzi self.scrollBarVal.get()
        self.scrollBar = Scale(self, from_=0, to=0.3, orient=HORIZONTAL, length=500, command=self.test, resolution=0.01,font=self.FONT,variable=self.scrollBarVal)

        # Labels
        self.mmLabel = Label(self, text="mm", font=self.FONT)
        self.valueLabel = Label(self, text="Value: 0.00mm", font=self.FONT)

        # Buttons
        self.backToStartButton = self.initializeButton(30, 50, "|<")
        self.backToStartButton.configure(command=lambda: self.FUNCTION_TODO("graphFunButton"))

        self.stepBackButton = self.initializeButton(30, 50, "-")
        self.stepBackButton.configure(command=lambda: self.FUNCTION_TODO("graphFunButton"))

        self.stepForwardButton = self.initializeButton(30, 50, "+")
        self.stepForwardButton.configure(command=lambda: self.FUNCTION_TODO("graphFunButton"))

        self.forwardStepsButton = self.initializeButton(30, 50, ">|")
        self.forwardStepsButton.configure(command=lambda: self.FUNCTION_TODO("graphFunButton"))

        self.doStep = self.initializeButton(30, 50, "Start")
        self.doStep.configure(command=lambda: self.FUNCTION_TODO("graphFunButton"))

        # Entry
        self.stepEntry = self.initializeEntry(15)

        # Entry values
        self.stepValue = self.stepEntry.get()

        self.placeWidgets()

    # z nejako dovodu pri commandoch pri scale widgeti musi byt aj to "v" premenna, inak to pada idk why
    def test(self,v):
        print(self.scrollBarVal.get())

    def placeWidgets(self):
        self.backToStartButton.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
        self.stepBackButton.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
        self.mmLabel.pack(side=LEFT, padx=(10, 0), pady=(10, 10))
        self.scrollBar.pack(side=LEFT, padx=(10, 10), pady=(10, 25))
        self.stepForwardButton.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
        self.forwardStepsButton.pack(side=LEFT)
        self.doStep.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
        self.stepEntry.pack(side=LEFT, padx=(10, 10), pady=(10, 10))


# TODO ABY SA ZMENILA FARBA GOMBIKOV PLAY A STOP?
class NavbarFrame(FrameBaseClass):
    def __init__(self, cameraSettingsFrame, calibrationFrame, d32Frame, graphFunctionFrame, d3Frame, importExportFrame,
                 cameraFeedTopLevel):
        super().__init__()
        # Setting color of frame Navbar frame
        self.configure(bg=self.NAVBAR_FRAME_COLOR)

        # Setting that disables frame shrinkage to fit widgets
        self.propagate(False)

        # Popup menu frames
        self.cameraSettingsFrame = cameraSettingsFrame
        self.calibrationFrame = calibrationFrame
        self.d32Frame = d32Frame
        self.graphFunctionFrame = graphFunctionFrame
        self.d3Frame = d3Frame
        self.importExportFrame = importExportFrame
        self.cameraFeedTopLevel = cameraFeedTopLevel

        # Initializing widgets in frame

        # Navbar1
        self.settingsButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "Settings")
        self.settingsButton.configure(command=lambda: self.placeNavBar2())

        self.playButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "")
        self.playButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"), image=self.PLAY_IMAGE)

        self.pauseButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "")
        self.pauseButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"), image=self.STOP_IMAGE)

        self.graphFunButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "Graph\nfun.")
        self.graphFunButton.configure(command=lambda: self.placeRemovePopupMenu("graphFunButton"))

        self.d3Button = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "3D")
        self.d3Button.configure(command=lambda: self.placeRemovePopupMenu("d3Button"))

        self.importExportButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE,
                                                        "Import\nExport")
        self.importExportButton.configure(command=lambda: self.placeRemovePopupMenu("importExportButton"))

        # Navbar2
        self.backButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "Back")
        self.backButton.configure(command=lambda: self.placeNavBar1())

        self.cameraButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "")
        self.cameraButton.configure(command=lambda: self.placeRemovePopupMenu("cameraButton"), image=self.CAMERA_IMAGE)

        self.calibrationButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "Calibration")
        self.calibrationButton.configure(command=lambda: self.placeRemovePopupMenu("calibrationButton"))

        self.d32Button = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "3D")
        self.d32Button.configure(command=lambda: self.placeRemovePopupMenu("d32Button"))

        # List of widgets for navbar page 1 and 2
        self.navbar1Widgets = [self.settingsButton, self.playButton, self.pauseButton, self.graphFunButton,
                               self.d3Button, self.importExportButton]

        self.navbar2Widgets = [self.backButton, self.cameraButton, self.calibrationButton, self.d32Button]

        # Dictionaries used to map up buttons,frames and if they're active. Used for switching between popupmenus and
        # changing button colors
        self.buttonDict = {
            "graphFunButton": self.graphFunButton,
            "d3Button": self.d3Button,
            "importExportButton": self.importExportButton,
            "cameraButton": self.cameraButton,
            "calibrationButton": self.calibrationButton,
            "d32Button": self.d32Button
        }
        self.isButtonClickedDict = {
            "graphFunButton": False,
            "d3Button": False,
            "importExportButton": False,
            "cameraButton": False,
            "calibrationButton": False,
            "d32Button": False
        }
        self.frameDict = {
            "graphFunButton": self.graphFunctionFrame,
            "d3Button": self.d3Frame,
            "importExportButton": self.importExportFrame,
            "cameraButton": self.cameraSettingsFrame,
            "calibrationButton": self.calibrationFrame,
            "d32Button": self.d32Frame
        }

        # Placing navbar1
        self.placeNavBar1()

    def placeNavBar1(self):
        self.removeWidgetsFromFrame()
        for index, widget in enumerate(self.navbar1Widgets):
            widget.grid(row=index, column=0, padx=(10, 10), pady=(10, 10))

    def placeNavBar2(self):
        self.removeWidgetsFromFrame()
        for index, widget in enumerate(self.navbar2Widgets):
            widget.grid(row=index, column=0, padx=(10, 10), pady=(10, 10))

    # Places/forgets(hides) frame from window, changes button color and sets/unsets active frame/button.
    def placeRemovePopupMenu(self, frameButtonID):
        self.changeButtonColors(frameButtonID)
        self.forgetFrames()
        isClicked = self.isButtonClickedDict[frameButtonID]
        self.placeFrame(frameButtonID) if not isClicked else self.forgetFrame(frameButtonID)
        self.isButtonClickedDict[frameButtonID] = not self.isButtonClickedDict[frameButtonID]
        self.resetClickedButtons(frameButtonID)

    # Changes button color according to if it's active or not
    def changeButtonColors(self, buttonID):
        self.resetColorButtons()
        if self.isButtonClickedDict[buttonID] is False:
            self.buttonDict[buttonID].configure(bg=self.BUTTON_COLOR_CLICKED, fg="black")
        else:
            self.buttonDict[buttonID].configure(bg=self.BUTTON_COLOR, fg="white")

    def placeFrame(self, frameID):
        self.frameDict[frameID].place(x=94, y=0)

    def forgetFrame(self, frameID):
        self.frameDict[frameID].place_forget()

    def forgetFrames(self):
        for frame in self.frameDict.values():
            frame.place_forget()

    def resetClickedButtons(self, frameButtonID):
        for frameID in self.isButtonClickedDict:
            if frameButtonID != frameID:
                self.isButtonClickedDict[frameID] = False

    def resetColorButtons(self):
        for button in self.buttonDict.values():
            button.configure(bg=self.BUTTON_COLOR, fg="white")


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


# TODO VYBERANIE FILEU
class CalibrationFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()
        self.tkraise()
        self.calibration = Calibration()

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
        self.calibrationFileButton.configure(command=lambda: self.FUNCTION_TODO(CalibrationHandler()
                                                                            .calibrateFromFile(self.calibration, 3)))

        self.calibrationChartCreateButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH,
                                                                  "Create")
        self.calibrationChartCreateButton.configure(command=lambda: self.FUNCTION_TODO(CalibrationHandler()
                                                                .calibrateFromApp(self.calibration, self.calibrationText
                                                                                  .get("1.0", END), 3)))

        self.calibrationChartShowButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Show")
        self.calibrationChartShowButton.configure(command=lambda: self.FUNCTION_TODO(CalibrationRender().
                                                                                     render(self.calibration)))

        # Text
        self.calibrationText = Text(self, width=30, height=15)

        # Text value
        self.calibrationValue = self.calibrationText.get("1.0",
                                                         END)  # to "1.0" znamena ze beriem text od 1 riadka a 0 znaku.. proste beries text od zaciatku po kiniec"

        # ukazka jak sa insertuje do textboxu
        # self.calibrationText.insert("1.0", "10 10.4 \n11 11.4 \n12 12.4 \n13 14.4\n")

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


class D32Frame(FrameBaseClass):
    def __init__(self):
        super().__init__()
        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Initializing widgets in frame

        # Labels
        self.spectralMapLabel = self.initializeLabel("Spectral map", 1)
        self.windowDimensionsLabel = self.initializeLabel("Window dimensions:", 0)
        self.xLabel = self.initializeLabel("X:", 0)
        self.yLabel = self.initializeLabel("Y:", 0)
        self.cellSizeLabel = self.initializeLabel("Cell size:", 0)

        # Buttons
        self.spectralMapSetButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.spectralMapSetButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        # Entries
        self.xEntry = self.initializeEntry(20)
        self.yEntry = self.initializeEntry(20)
        self.cellSizeEntry = self.initializeEntry(20)

        # Entry values
        self.xValue = self.xEntry.get()
        self.yValue = self.xEntry.get()
        self.cellSizeValue = self.xEntry.get()

        self.placeWidgets()

    def placeWidgets(self):
        self.spectralMapLabel.grid(sticky=W, row=0, column=0, pady=(10, 0))

        self.windowDimensionsLabel.grid(sticky=W, row=1, column=0, pady=(10, 0))

        self.xLabel.grid(sticky=W, row=2, column=0, pady=(10, 0))
        self.xEntry.grid(sticky=W, row=2, column=1, pady=(10, 0), padx=(10, 10))

        self.yLabel.grid(sticky=W, row=3, column=0, pady=(10, 0))
        self.yEntry.grid(sticky=W, row=3, column=1, pady=(10, 0), padx=(10, 10))

        self.cellSizeLabel.grid(sticky=W, row=4, column=0, pady=(10, 0))
        self.cellSizeEntry.grid(sticky=W, row=4, column=1, pady=(10, 0), padx=(10, 10))

        self.spectralMapSetButton.grid(row=5, column=0, pady=(10, 10), columnspan=2)


# TODO FUNKCIONALITA CHECKUBUTTON/RADIOBUTTONS

class GraphFunctionFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()
        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Initializing widgets in frame

        # Labels
        self.measurementsLabel = self.initializeLabel("Measurements", 1)
        self.peakMinYLabel = self.initializeLabel("Peak min y:", 0)
        self.peakMinYDifLabel = self.initializeLabel("Peak min y difference:", 0)
        self.peakMinXDifLabel = self.initializeLabel("Peak min x difference:", 0)
        self.globalPeakLabel = self.initializeLabel("Global peak:", 0)
        self.referenceImageLabel = self.initializeLabel("Reference image:", 0)
        self.divideFromReferenceLabel = self.initializeLabel("Divide from reference image:", 0)
        self.subtractFromReferenceLabel = self.initializeLabel("Subtract from reference image:", 0)
        self.fromLabel = self.initializeLabel("From:", 0)
        self.toLabel = self.initializeLabel("To:", 0)
        self.scaleLabel = self.initializeLabel("Scale", 0)

        # Buttons
        self.measurementsSetButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.measurementsSetButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.referenceImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.referenceImageButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.divideFromReferenceButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.divideFromReferenceButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        self.subtractFromReferenceButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.subtractFromReferenceButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        # Entries
        self.peakMinYEntry = self.initializeEntry(20)
        self.peakMinYDifEntry = self.initializeEntry(20)
        self.peakMinXDifEntry = self.initializeEntry(20)
        self.fromEntry = self.initializeEntry(20)
        self.toEntry = self.initializeEntry(20)

        # Entry values
        self.peakMinYValue = self.peakMinYEntry.get()
        self.peakMinYDifValue = self.peakMinYDifEntry.get()
        self.peakMinXDifValue = self.peakMinXDifEntry.get()
        self.fromValue = self.fromEntry.get()
        self.toValue = self.toEntry.get()

        # Checkbutton value/state
        self.globalPeakVar = IntVar()

        # Pouzivam IntVar lebo automaticky sa updatuje podla toho ci je checked alebo neni
        # Na ziskania value pouzi  self.globalPeakVar.get() . Values = 0 alebo 1. 0 = neni zastiknuty, 1 = je zastiknuty

        self.globalPeakCheckbutton = Checkbutton(self, bg=self.FRAME_COLOR, activebackground=self.FRAME_COLOR,
                                                 variable=self.globalPeakVar, command=lambda: self.FUNCTION_TODO("XDD"))

        # Radiobutton values/state
        self.scaleVar = IntVar()

        # Pouzivam IntVar lebo automaticky sa updatuje
        # Na ziskania value pouzi  self.scaleVar.get() . Values = 1 alebo 2. 1 = px , 2 = nm

        self.radioPx = Radiobutton(self, text="px", bg=self.FRAME_COLOR, activebackground=self.FRAME_COLOR,
                                   variable=self.scaleVar, value=1, command=lambda: self.FUNCTION_TODO("KMS"))
        self.radioNm = Radiobutton(self, text="nm", bg=self.FRAME_COLOR, activebackground=self.FRAME_COLOR,
                                   variable=self.scaleVar, value=2, command=lambda: self.FUNCTION_TODO("XDDD"))

        # Placing widgets into frame
        self.placeWidgets()

    def placeWidgets(self):
        self.measurementsLabel.grid(sticky=W, row=0, column=0, pady=(10, 0), columnspan=3)

        self.peakMinYLabel.grid(sticky=W, row=1, column=0, pady=(10, 0), columnspan=2)
        self.peakMinYEntry.grid(sticky=W, row=1, column=2, pady=(10, 0), padx=(10, 10))

        self.peakMinYDifLabel.grid(sticky=W, row=2, column=0, pady=(10, 0), columnspan=2)
        self.peakMinYDifEntry.grid(sticky=W, row=2, column=2, pady=(10, 0), padx=(10, 10))

        self.peakMinXDifLabel.grid(sticky=W, row=3, column=0, pady=(10, 0), columnspan=2)
        self.peakMinXDifEntry.grid(sticky=W, row=3, column=2, pady=(10, 0), padx=(10, 10))

        self.measurementsSetButton.grid(sticky=W, row=4, column=1, pady=(10, 0), padx=(15, 10), columnspan=2)

        self.globalPeakLabel.grid(sticky=W, row=5, column=0, pady=(10, 0), columnspan=2)
        self.globalPeakCheckbutton.grid(row=5, column=2, pady=(10, 0))

        self.referenceImageLabel.grid(sticky=W, row=6, column=0, pady=(10, 0), columnspan=2)
        self.referenceImageButton.grid(row=6, column=2, pady=(10, 0), padx=(10, 10))

        self.divideFromReferenceLabel.grid(sticky=W, row=7, column=0, pady=(10, 0), columnspan=2)
        self.divideFromReferenceButton.grid(row=7, column=2, pady=(10, 0), padx=(10, 10))

        self.subtractFromReferenceLabel.grid(sticky=W, row=8, column=0, pady=(10, 0), columnspan=2)
        self.subtractFromReferenceButton.grid(row=8, column=2, pady=(10, 0), padx=(10, 10))

        self.fromLabel.grid(sticky=W, row=9, column=0, pady=(10, 0), columnspan=2)
        self.fromEntry.grid(sticky=W, row=9, column=2, pady=(10, 0), padx=(10, 10))

        self.toLabel.grid(sticky=W, row=10, column=0, pady=(10, 0), columnspan=2)
        self.toEntry.grid(sticky=W, row=10, column=2, pady=(10, 0), padx=(10, 10))

        self.scaleLabel.grid(sticky=W, row=11, column=0, pady=(10, 10))
        self.radioPx.grid(row=11, column=1, pady=(10, 0))
        self.radioNm.grid(row=11, column=2, pady=(10, 0))


# # TODO LOGIKA PRI ZMENE CONNECTION OBRAZKA

class D3Frame(FrameBaseClass):
    def __init__(self):
        super().__init__()

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # #Initalizing widgets in frame

        # Labels
        self.d3Label = self.initializeLabel("3D", 1)
        self.wavelengthLabel = self.initializeLabel("Wavelength:", 0)
        self.scanLabel = self.initializeLabel("Scan:", 0)

        # Buttons
        self.showButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Show")
        self.showButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        # Images
        self.scanImage = Label(self, image=self.OFF_IMAGE, bg=self.FRAME_COLOR)

        # Entries
        self.wavelengthEntry = self.initializeEntry(15)

        # Entry values
        self.wavelengthValue = self.wavelengthEntry.get()

        # Placing widgets into frame
        self.placeWidgets()

    def placeWidgets(self):
        self.d3Label.grid(sticky=W, row=0, column=0, pady=(10, 0))
        self.wavelengthLabel.grid(sticky=W, row=1, column=0, pady=(10, 0))
        self.wavelengthEntry.grid(sticky=W, row=1, column=1, padx=(0, 10), pady=(10, 0))
        self.showButton.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))
        self.scanLabel.grid(sticky=W, row=3, column=0, padx=(0, 10), pady=(10, 10))
        self.scanImage.grid(row=3, column=0, padx=(30, 10), pady=(10, 10))


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


GUI()
