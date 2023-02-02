from gui_widgets.FrameBaseClass import FrameBaseClass

# TODO ABY SA ZMENILA FARBA GOMBIKOV PLAY A STOP?


class NavbarFrame(FrameBaseClass):
    def __init__(self, cameraSettingsFrame, calibrationFrame, d32Frame, graphFunctionFrame, d3Frame, importExportFrame):
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

        self.plot = None

        # Initializing widgets in frame

        # Navbar1
        self.settingsButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "Settings")
        self.settingsButton.configure(command=lambda: self.placeNavBar2())

        self.playButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "")
        self.playButton.configure(command=lambda: self.start(), image=self.PLAY_IMAGE)

        self.pauseButton = self.initializeButton(self.NAVBAR_BUTTON_SIZE, self.NAVBAR_BUTTON_SIZE, "")
        self.pauseButton.configure(command=lambda: self.pause(), image=self.STOP_IMAGE)

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
        self.resetColorButtons()
        self.forgetFrames()
        self.resetAllClickedButtons()
        self.removeWidgetsFromFrame()
        for index, widget in enumerate(self.navbar1Widgets):
            widget.grid(row=index, column=0, padx=(10, 10), pady=(10, 10))

    def placeNavBar2(self):
        self.resetColorButtons()
        self.forgetFrames()
        self.resetAllClickedButtons()
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

    def resetAllClickedButtons(self):
        for frameID in self.isButtonClickedDict:
            self.isButtonClickedDict[frameID] = False

    def resetColorButtons(self):
        for button in self.buttonDict.values():
            button.configure(bg=self.BUTTON_COLOR, fg="white")

    def initPlot(self, plot):
        self.plot = plot

    def start(self):
        self.plot.resume()

    def pause(self):
        self.plot.pause()
