from tkinter import *
from gui_widgets.FrameBaseClass import FrameBaseClass
from idlelib.tooltip import Hovertip


# TODO FUNKCIONALITA CHECKUBUTTON/RADIOBUTTONS


class GraphFunctionFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()
        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        self.plot = None

        # Initializing widgets in frame

        # Labels
        self.measurementsLabel = self.initializeLabel("Measurement", 1)
        self.peakMinYLabel = self.initializeLabel("Peak min y:", 0)
        self.peakMinYDifLabel = self.initializeLabel("Peak min y\n difference:", 0)
        self.peakMinXDifLabel = self.initializeLabel("Peak min x\n difference:", 0)
        self.globalPeakLabel = self.initializeLabel("Global peak:", 0)
        self.referenceImageLabel = self.initializeLabel("Reference image:", 0)
        self.divideFromReferenceLabel = self.initializeLabel("Divide from\n reference image:", 0)
        self.subtractFromReferenceLabel = self.initializeLabel("Subtract from\n reference image:", 0)
        self.fromLabel = self.initializeLabel("From:", 0)
        self.toLabel = self.initializeLabel("To:", 0)
        self.scaleLabel = self.initializeLabel("Scale", 0)

        # Buttons
        self.measurementsSetButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.measurementsSetButton.configure(command=lambda: self.setMeasurements())

        self.showHidePeaksButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Show")
        self.showHidePeaksButton.configure(command=lambda: self.showHidePeaksButtonHandler())

        self.referenceImageButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.referenceImageButton.configure(command=lambda: self.getReferenceImage())

        self.divideFromReferenceButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.divideFromReferenceButton.configure(command=lambda: self.divideFromReferenceButtonHandler())

        self.subtractFromReferenceButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.subtractFromReferenceButton.configure(command=lambda: self.subtractFromReferenceButtonHandler())

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
        self.scaleVar = IntVar(value=1)

        # Pouzivam IntVar lebo automaticky sa updatuje
        # Na ziskania value pouzi  self.scaleVar.get() . Values = 1 alebo 2. 1 = px , 2 = nm

        self.radioPx = Radiobutton(self, text="px", bg=self.FRAME_COLOR, activebackground=self.FRAME_COLOR,
                                   variable=self.scaleVar, value=1, command=lambda: self.setPixelView())
        self.radioNm = Radiobutton(self, text="nm", bg=self.FRAME_COLOR, activebackground=self.FRAME_COLOR,
                                   variable=self.scaleVar, value=2, command=lambda: self.setWavelentgthView())

        self.redVar = IntVar()
        self.checkRed = Checkbutton(self, text="red", bg=self.FRAME_COLOR, activebackground=self.FRAME_COLOR,
                                    variable=self.redVar, onvalue=1, offvalue=0, command=lambda: self.setShowRedLine())
        self.greenVar = IntVar()
        self.checkGreen = Checkbutton(self, text="green", bg=self.FRAME_COLOR, activebackground=self.FRAME_COLOR,
                                      variable=self.greenVar, onvalue=1, offvalue=0,
                                      command=lambda: self.setShowGreenLine())
        self.blueVar = IntVar()
        self.checkBlue = Checkbutton(self, text="blue", bg=self.FRAME_COLOR, activebackground=self.FRAME_COLOR,
                                     variable=self.blueVar, onvalue=1, offvalue=0,
                                     command=lambda: self.setShowBlueLine())
        self.maxVar = IntVar(value=1)
        self.checkMax = Checkbutton(self, text="max", bg=self.FRAME_COLOR, activebackground=self.FRAME_COLOR,
                                    variable=self.maxVar, onvalue=1, offvalue=0, command=lambda: self.setShowMaxLine())

        self.isButtonClickedDict = {
            "showHidePeaksButton": False,
            "divideFromReferenceButton": False,
            "subtractFromReferenceButton": False
        }
        self.buttonDict = {
            "showHidePeaksButton": self.showHidePeaksButton,
            "divideFromReferenceButton": self.divideFromReferenceButton,
            "subtractFromReferenceButton": self.subtractFromReferenceButton,
        }


        #Tooltips
        self.peakMinYTooltipMSG = "..."
        self.peakMinYTooltip = Hovertip(self.peakMinYLabel, self.peakMinYTooltipMSG)

        self.peakMinYDifTooltipMSG = "Set min difference in y-axis for peak recognition."
        self.peakMinYDifTooltip = Hovertip(self.peakMinYDifLabel, self.peakMinYDifTooltipMSG)

        self.peakMinXDifTooltipMSG = "Set min difference in x-axis for peak recognition."
        self.peakMinXDifTooltip = Hovertip(self.peakMinXDifLabel, self.peakMinXDifTooltipMSG)

        self.globalPeakTooltipMSG = "..."
        self.globalPeakTooltip = Hovertip(self.globalPeakLabel,self.globalPeakTooltipMSG)

        self.referenceImageTooltipMSG = "Set actual image as reference image."
        self.referenceImageTooltip = Hovertip(self.referenceImageLabel, self.referenceImageTooltipMSG)

        self.divideFromReferenceTooltipMSG = "Set division of actual image from reference image."
        self.divideFromReferenceTooltip = Hovertip(self.divideFromReferenceLabel,
                                           self.divideFromReferenceTooltipMSG)

        self.subtractFromReferenceTooltipMSG = "Set subtraction of actual image form reference image."
        self.subtractFromReferenceTooltip = Hovertip(self.subtractFromReferenceLabel,
                                           self.subtractFromReferenceTooltipMSG)

        self.fromTooltipMSG = "..."
        self.fromTooltip = Hovertip(self.fromLabel,self.fromTooltipMSG)

        self.toTooltipMSG = "..."
        self.toTooltip = Hovertip(self.toLabel, self.toTooltipMSG)

        self.scaleTooltipMSG = "Sets x-axis view as px/nm."
        self.scaleTooltip = Hovertip(self.scaleLabel,self.scaleTooltipMSG)

        # Placing widgets into frame
        self.placeWidgets()

    def placeWidgets(self):
        self.measurementsLabel.pack()

        self.peakMinYLabel.pack()
        self.peakMinYEntry.pack()

        self.peakMinYDifLabel.pack()
        self.peakMinYDifEntry.pack()

        self.peakMinXDifLabel.pack()
        self.peakMinXDifEntry.pack()

        self.measurementsSetButton.pack(pady=(5,5))
        self.showHidePeaksButton.pack(pady=(5,5))

        self.globalPeakLabel.pack()
        self.globalPeakCheckbutton.pack()

        self.referenceImageLabel.pack()
        self.referenceImageButton.pack(pady=(5,5))

        self.divideFromReferenceLabel.pack()
        self.divideFromReferenceButton.pack(pady=(5,5))

        self.subtractFromReferenceLabel.pack()
        self.subtractFromReferenceButton.pack(pady=(5,5))

        self.fromLabel.pack()
        self.fromEntry.pack()

        self.toLabel.pack()
        self.toEntry.pack()

        self.scaleLabel.pack()
        self.radioPx.pack()
        self.radioNm.pack(padx=(5,0))

        self.checkRed.pack(padx=(2,0))
        self.checkGreen.pack(padx=(14,0))
        self.checkBlue.pack(padx=(6,0))
        self.checkMax.pack(padx=(6,0))

        # self.measurementsLabel.grid(sticky=W, row=0, column=0, pady=(10, 0), columnspan=3)
        #
        # self.peakMinYLabel.grid(sticky=W, row=1, column=0, pady=(10, 0), columnspan=2)
        # self.peakMinYEntry.grid(sticky=W, row=1, column=2, pady=(10, 0), padx=(10, 10))
        #
        # self.peakMinYDifLabel.grid(sticky=W, row=2, column=0, pady=(10, 0), columnspan=2)
        # self.peakMinYDifEntry.grid(sticky=W, row=2, column=2, pady=(10, 0), padx=(10, 10))
        #
        # self.peakMinXDifLabel.grid(sticky=W, row=3, column=0, pady=(10, 0), columnspan=2)
        # self.peakMinXDifEntry.grid(sticky=W, row=3, column=2, pady=(10, 0), padx=(10, 10))
        #
        # self.measurementsSetButton.grid(sticky=W, row=4, column=1, pady=(10, 0), padx=(15, 10), columnspan=1)
        # self.showHidePeaksButton.grid(sticky=W, row=4, column=2, pady=(10, 0), padx=(15, 10), columnspan=1)
        #
        # self.globalPeakLabel.grid(sticky=W, row=5, column=0, pady=(10, 0), columnspan=2)
        # self.globalPeakCheckbutton.grid(row=5, column=2, pady=(10, 0))
        #
        # self.referenceImageLabel.grid(sticky=W, row=6, column=0, pady=(10, 0), columnspan=2)
        # self.referenceImageButton.grid(row=6, column=2, pady=(10, 0), padx=(10, 10))
        #
        # self.divideFromReferenceLabel.grid(sticky=W, row=7, column=0, pady=(10, 0), columnspan=2)
        # self.divideFromReferenceButton.grid(row=7, column=2, pady=(10, 0), padx=(10, 10))
        #
        # self.subtractFromReferenceLabel.grid(sticky=W, row=8, column=0, pady=(10, 0), columnspan=2)
        # self.subtractFromReferenceButton.grid(row=8, column=2, pady=(10, 0), padx=(10, 10))
        #
        # self.fromLabel.grid(sticky=W, row=9, column=0, pady=(10, 0), columnspan=2)
        # self.fromEntry.grid(sticky=W, row=9, column=2, pady=(10, 0), padx=(10, 10))
        #
        # self.toLabel.grid(sticky=W, row=10, column=0, pady=(10, 0), columnspan=2)
        # self.toEntry.grid(sticky=W, row=10, column=2, pady=(10, 0), padx=(10, 10))
        #
        # self.scaleLabel.grid(sticky=W, row=11, column=0, pady=(10, 10))
        # self.radioPx.grid(row=11, column=1, pady=(10, 0))
        # self.radioNm.grid(row=11, column=2, pady=(10, 0))
        #
        # self.checkRed.grid(row=12, column=0)
        # self.checkGreen.grid(row=12, column=1)
        # self.checkBlue.grid(row=12, column=2)
        # self.checkMax.grid(row=12, column=3)

    def showHidePeaksButtonHandler(self):
        if self.isButtonClickedDict["showHidePeaksButton"] == False:
            self.setShowPeaks()
            self.buttonDict["showHidePeaksButton"].configure(text = "Hide", bg= self.BUTTON_COLOR_CLICKED, fg="black")
        else:
            self.setHidePeaks()
            self.buttonDict["showHidePeaksButton"].configure(text = "Show", bg= self.BUTTON_COLOR, fg="white")
        self.isButtonClickedDict["showHidePeaksButton"] = not self.isButtonClickedDict["showHidePeaksButton"]

    def divideFromReferenceButtonHandler(self):
        if self.isButtonClickedDict["divideFromReferenceButton"] == False:
            self.doDivision()
            self.buttonDict["divideFromReferenceButton"].configure(text = "Unset", bg= self.BUTTON_COLOR_CLICKED, fg="black")
        else:
            self.stopDivision()
            self.buttonDict["divideFromReferenceButton"].configure(text = "Set", bg= self.BUTTON_COLOR, fg="white")
        self.isButtonClickedDict["divideFromReferenceButton"] = not self.isButtonClickedDict["divideFromReferenceButton"]

    def subtractFromReferenceButtonHandler(self):
        if self.isButtonClickedDict["subtractFromReferenceButton"] == False:
            self.doSubtraction()
            self.buttonDict["subtractFromReferenceButton"].configure(text = "Unset", bg= self.BUTTON_COLOR_CLICKED, fg="black")
        else:
            self.stopSubptraction()
            self.buttonDict["subtractFromReferenceButton"].configure(text = "Set", bg= self.BUTTON_COLOR, fg="white")
        self.isButtonClickedDict["subtractFromReferenceButton"] = not self.isButtonClickedDict["subtractFromReferenceButton"]

    def initPlot(self, plot):
        self.plot = plot

    def getReferenceImage(self):
        self.plot.setReferenceData()

    def doSubtraction(self):
        self.plot.setSubstraction()

    def stopSubptraction(self):
        self.plot.unsetSubtraction()

    def doDivision(self):
        self.plot.setDivision()

    def stopDivision(self):
        self.plot.unsetDivision()

    def setPixelView(self):
        self.plot.showPixelView()

    def setWavelentgthView(self):
        self.plot.showWavelengthView()

    def setShowRedLine(self):
        self.plot.setShowRedLine(self.redVar.get())

    def setShowGreenLine(self):
        self.plot.setShowGreenLine(self.greenVar.get())

    def setShowBlueLine(self):
        self.plot.setShowBlueLine(self.blueVar.get())

    def setShowMaxLine(self):
        self.plot.setShowMaxLine(self.maxVar.get())

    def setShowPeaks(self):
        self.plot.setShowPeaks()

    def setHidePeaks(self):
        self.plot.setHidePeaks()

    def setPeakDistance(self):
        peakHeight = self.peakMinXDifEntry.get()
        if peakHeight != '':
            self.plot.setPeakDistance(int(peakHeight))

    def setPeakHeight(self):
        peakDistance = self.peakMinYDifEntry.get()
        if peakDistance != '':
            self.plot.setPeakHight(int(peakDistance))

    def setMeasurements(self):
        self.setPeakHeight()
        self.setPeakDistance()