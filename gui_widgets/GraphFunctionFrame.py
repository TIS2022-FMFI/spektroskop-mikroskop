from tkinter import *
from FrameBaseClass import FrameBaseClass

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
